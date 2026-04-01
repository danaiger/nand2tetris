from typing import TextIO
from jack_analyzer.tokenizer import JackTokenizer
from jack_analyzer.consts import JACK_OPERATIONS,UNARY_OPERATIONS,TokenType,IdentifierKind
from jack_analyzer.symbol_table import SymbolTable
from jack_analyzer.vm_writer import ArithmeticOpToVMCommand, VMSegment, VMWriter
from jack_analyzer.xml_writer import XMLWriter,NullXMLWriter

IdentifierKindToVMSegment={
    IdentifierKind.var:VMSegment.local,
    IdentifierKind.field:VMSegment.this,
    IdentifierKind.static:VMSegment.static,
    IdentifierKind.arg:VMSegment.arg
}

def _compilation_unit(name:str):
    def decorator(func):
        def wrapper(self:CompilationEngine):
            self.xml_writer.open_compilation_unit(name)
            value=func(self)
            self.xml_writer.close_compilation_unit(name)
            return value
        return wrapper
    return decorator

class CompilationEngine:

    def __init__(self,input_file:TextIO,vm_writer:VMWriter,writer:XMLWriter=None):
        self.input_file=input_file
        self.tokenizer=JackTokenizer(input_file)
        self.vm_writer=vm_writer
        self.xml_writer=writer or NullXMLWriter()
        self.symbol_table=SymbolTable()
        self._labels=set()
        self.compile_class()

    def compile_atom(self):
        current_token_type=self.tokenizer.token_type()
        current_token=self.tokenizer.get_current_token()
        self.xml_writer.write_token(current_token,current_token_type)
    
    def _compile_var_dec(self):
        current_token=self.tokenizer.get_current_token()
        if current_token=="static":
            kind=IdentifierKind.static
        elif current_token=="field":
            kind=IdentifierKind.field
        else:
            kind=IdentifierKind.var
        self._compile_atom_and_advance_repeatedly(1)
        current_type=self.tokenizer.get_current_token()
        if current_type in ['char','int','boolean']:
            self._compile_atom_and_advance_repeatedly(1)
        else:
            self.xml_writer.write_identifier(current_type,kind.class_identifier,False)
            self.tokenizer.advance()
        name=self.tokenizer.get_current_token()
        self.symbol_table.define(name,current_type,kind)
        self.xml_writer.write_identifier(name,kind,True,self.symbol_table.index_of(name))
        self.tokenizer.advance()
        while self.tokenizer.get_current_token()!=';':
            self._compile_atom_and_advance_repeatedly(1)
            name=self.tokenizer.get_current_token()
            self.symbol_table.define(name,current_type,kind)
            self.xml_writer.write_identifier(name,kind,True,self.symbol_table.index_of(name))
            self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(1)


    @_compilation_unit("classVarDec")
    def _compile_class_var_dec(self):
        self._compile_var_dec()

    def _compile_atom_and_advance_repeatedly(self,times:int)->None:
        for _ in range(times):
            self.compile_atom() 
            self.tokenizer.advance()

    @_compilation_unit("parameterList")
    def _compile_parameter_list(self):
        if self.tokenizer.get_current_token()==')':
            return
        current_type=self.tokenizer.get_current_token()
        self._compile_atom_and_advance_repeatedly(1)
        name=self.tokenizer.get_current_token()
        self.tokenizer.advance()
        self.symbol_table.define(name,current_type,IdentifierKind.arg)
        self.xml_writer.write_identifier(name,IdentifierKind.arg,True,self.symbol_table.index_of(name))
        while self.tokenizer.get_current_token()==',':
            self._compile_atom_and_advance_repeatedly(1)
            current_type=self.tokenizer.get_current_token()
            self._compile_atom_and_advance_repeatedly(1)
            name=self.tokenizer.get_current_token()
            self.tokenizer.advance()
            self.symbol_table.define(name,current_type,IdentifierKind.arg)
            self.xml_writer.write_identifier(name,IdentifierKind.arg,True,self.symbol_table.index_of(name))

    @_compilation_unit("term")
    def _compile_term(self):
        if self.tokenizer.get_current_token()=='(':
            self._compile_atom_and_advance_repeatedly(1)
            self._compile_expression()
            self._compile_atom_and_advance_repeatedly(1)
        elif self.tokenizer.get_current_token() in UNARY_OPERATIONS:
            self._compile_atom_and_advance_repeatedly(1)
            self._compile_term()
        else:
            if self.tokenizer.token_type() in [TokenType.string_const,TokenType.keyword]:
                self._compile_atom_and_advance_repeatedly(1)
            elif self.tokenizer.token_type() in [TokenType.int_const]:
                number=self.tokenizer.get_current_token()
                self.vm_writer.write_push(VMSegment.const,number)
                self._compile_atom_and_advance_repeatedly(1)
            else:
                name=self.tokenizer.get_current_token()
                kind=self.symbol_table.kind_of(name)
                self.tokenizer.advance()
                if self.tokenizer.get_current_token()=='[':
                    occurence=self.symbol_table.index_of(name)
                    self.xml_writer.write_identifier(name,kind,False,occurence)
                    self._compile_atom_and_advance_repeatedly(1)
                    self._compile_expression()
                    self._compile_atom_and_advance_repeatedly(1)
                elif self.tokenizer.get_current_token() in ['(','.']:
                    self._compile_subroutine_call_from_end_of_identifier(name)
                else:
                    occurence=self.symbol_table.index_of(name)
                    self.xml_writer.write_identifier(name,kind,False,occurence)
                    self.vm_writer.write_push(IdentifierKindToVMSegment[kind], occurence)

    @_compilation_unit("expression")
    def _compile_expression(self):
        self._compile_term()
        while self.tokenizer.get_current_token() in JACK_OPERATIONS:
            op=self.tokenizer.get_current_token()
            self._compile_atom_and_advance_repeatedly(1)
            self._compile_term()
            if op in ArithmeticOpToVMCommand.keys():
                self.vm_writer.write_arithmetic(op)
            elif op == "*":
                self.vm_writer.write_call("Math.multiply",2)
            elif op == "/":
                self.vm_writer.write_call("Math.divide",2)
        

    @_compilation_unit("letStatement")
    def _compile_let_statement(self):
        self._compile_atom_and_advance_repeatedly(1)
        name=self.tokenizer.get_current_token()
        kind=self.symbol_table.kind_of(name)
        occurence=self.symbol_table.index_of(name)
        self.xml_writer.write_identifier(name,kind,False,occurence)
        self.tokenizer.advance()
        if self.tokenizer.get_current_token()=="[":
            self._compile_atom_and_advance_repeatedly(1)
            self._compile_expression()
            self._compile_atom_and_advance_repeatedly(1)
        self._compile_atom_and_advance_repeatedly(1)
        self._compile_expression()
        self.vm_writer.write_pop(IdentifierKindToVMSegment[kind],occurence)
        self._compile_atom_and_advance_repeatedly(1)

    @_compilation_unit("returnStatement")
    def _compile_return_statement(self):
        self._compile_atom_and_advance_repeatedly(1)
        if self.tokenizer.get_current_token()!=';':
            self._compile_expression()
        else:
            self.vm_writer.write_push(VMSegment.const,0)
        self.vm_writer.write_return()
        self._compile_atom_and_advance_repeatedly(1)
    
    def _generate_unique_label(self,name:str="L")->str:
        added_label=f"{name}{len(self._labels)+1}"
        self._labels.add(added_label)
        return added_label


    @_compilation_unit("ifStatement")
    def _compile_if_statement(self):
        else_label=self._generate_unique_label()
        continue_label=self._generate_unique_label()
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_expression()
        self.vm_writer.write_arithmetic("~")
        self.vm_writer.write_if(else_label)
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_statements()
        self.vm_writer.write_goto(continue_label)
        self._compile_atom_and_advance_repeatedly(1)
        self.vm_writer.write_label(else_label)
        if self.tokenizer.get_current_token()=="else":
            self._compile_atom_and_advance_repeatedly(2)
            self._compile_statements()
            self._compile_atom_and_advance_repeatedly(1)
        self.vm_writer.write_label(continue_label)

    @_compilation_unit("whileStatement")
    def _compile_while_statement(self):
        loop_label=self._generate_unique_label()
        self.vm_writer.write_label(loop_label)
        continue_label=self._generate_unique_label()
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_expression()
        self.vm_writer.write_arithmetic("~")
        self.vm_writer.write_if(continue_label)
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_statements()
        self._compile_atom_and_advance_repeatedly(1)
        self.vm_writer.write_goto(loop_label)
        self.vm_writer.write_label(continue_label)

    
    @_compilation_unit("expressionList")
    def _compile_expression_list(self)->int:
        number_of_expressions=0
        while self.tokenizer.get_current_token()!=')':
            self._compile_expression()
            number_of_expressions+=1
            if self.tokenizer.get_current_token()==',':
                self._compile_atom_and_advance_repeatedly(1)
        return number_of_expressions
            
    def _compile_subroutine_call_from_end_of_identifier(self,start_of_subroutine):
        subroutine_to_call=start_of_subroutine
        if self.tokenizer.get_current_token()=='.':
            kind=self.symbol_table.kind_of(start_of_subroutine)
            if kind:
                self.xml_writer.write_identifier(start_of_subroutine,kind,False,self.symbol_table.index_of(start_of_subroutine))
            else:
                self.xml_writer.write_identifier(start_of_subroutine,IdentifierKind.class_identifier,False)
            self._compile_atom_and_advance_repeatedly(1)
            name=self.tokenizer.get_current_token()
            subroutine_to_call+=f".{name}"
            self.xml_writer.write_identifier(name,IdentifierKind.subroutine,False)
            self.tokenizer.advance()
            self._compile_atom_and_advance_repeatedly(1)
        elif self.tokenizer.get_current_token()=='(':
            self.xml_writer.write_identifier(start_of_subroutine,IdentifierKind.subroutine,False)
            self._compile_atom_and_advance_repeatedly(1)
        else:
            raise ValueError("wrong syntax")
        parameters_number=self._compile_expression_list()
        self.vm_writer.write_call(subroutine_to_call,parameters_number)
        self._compile_atom_and_advance_repeatedly(1)


    @_compilation_unit("doStatement")
    def _compile_do_statement(self):
        self._compile_atom_and_advance_repeatedly(1)
        name=self.tokenizer.get_current_token()
        self.tokenizer.advance()
        self._compile_subroutine_call_from_end_of_identifier(name)
        self.vm_writer.write_pop(VMSegment.temp,0)
        self._compile_atom_and_advance_repeatedly(1)
        

    @_compilation_unit("statements")
    def _compile_statements(self):
        while self.tokenizer.get_current_token() in ["let","if","return","while","do"]:
            if self.tokenizer.get_current_token()=="let":
                self._compile_let_statement()
            elif self.tokenizer.get_current_token()=="if":
                self._compile_if_statement()
            elif self.tokenizer.get_current_token()=="return":
                self._compile_return_statement()
            elif self.tokenizer.get_current_token()=="while":
                self._compile_while_statement()
            elif self.tokenizer.get_current_token()=="do":
                self._compile_do_statement()

    @_compilation_unit("varDec")
    def _compile_subroutine_var_dec(self):
        self._compile_var_dec()

    @_compilation_unit("subroutineBody")
    def _compile_subroutine_body(self):
        self._compile_atom_and_advance_repeatedly(1)
        while self.tokenizer.get_current_token()=="var":
            self._compile_subroutine_var_dec()
        self._compile_statements()
        self._compile_atom_and_advance_repeatedly(1)

    @_compilation_unit("subroutineDec")
    def compile_subroutine_dec(self):
        self.symbol_table.start_subroutine()
        self._compile_atom_and_advance_repeatedly(1)
        current_type=self.tokenizer.get_current_token()
        if current_type in ['char','int','boolean','void']:
            self._compile_atom_and_advance_repeatedly(1)
        else:
            self.xml_writer.write_identifier(current_type,IdentifierKind.class_identifier,False)
            self.tokenizer.advance()
        subroutine_name=self.tokenizer.get_current_token()
        self.xml_writer.write_identifier(subroutine_name,IdentifierKind.subroutine,True)
        self.vm_writer.write_function(f"{self._current_class_name}.{subroutine_name}",0)
        self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(1)
        self._compile_parameter_list()
        self._compile_atom_and_advance_repeatedly(1)
        self._compile_subroutine_body()

    @_compilation_unit("class")
    def compile_class(self):
        self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(1)
        self._current_class_name=self.tokenizer.get_current_token()
        self.xml_writer.write_identifier(self._current_class_name,IdentifierKind.class_identifier,True)
        self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(1)
        while self.tokenizer.get_current_token() in ["field","static"]:
            self._compile_class_var_dec()
        while self.tokenizer.get_current_token() in ["constructor","function","method"]:
            self.compile_subroutine_dec()
        self.compile_atom()