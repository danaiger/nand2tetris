from typing import TextIO
from jack_analyzer.utils import format_output
from jack_analyzer.tokenizer import JackTokenizer
from jack_analyzer.consts import JACK_OPERATIONS,UNARY_OPERATIONS,TokenType,IdentifierKind
from jack_analyzer.symbol_table import SymbolTable

class VMWriter:
    def __init__(self, output_file: TextIO):
        self.output_file = output_file

class NullVMWriter(VMWriter):
    def __init__(self): pass

def _compilation_unit(name:str):
    def decorator(func):
        def wrapper(self:CompilationEngine):
            self.xml_writer.open_compilation_unit(name)
            func(self)
            self.xml_writer.close_compilation_unit(name)
        return wrapper
    return decorator

class XMLWriter:
    def __init__(self,output_file:TextIO):
        self.output_file=output_file
        self.indentation_spaces=0
    
    def write_token(self,current_token:str,current_token_type:TokenType):
        output=format_output(current_token,current_token_type)
        self.output_file.write(f"{' '*self.indentation_spaces}<{current_token_type.value}> {output} </{current_token_type.value}>\n")

    def write_identifier(self,name: str,kind:IdentifierKind , is_definition:bool,occurence:int=0):
        self.write_token(name,TokenType.identifier)
    
    def open_compilation_unit(self,name:str):
        self.output_file.write(f"{' '*self.indentation_spaces}<{name}>\n")
        self.indentation_spaces+=2

    def close_compilation_unit(self,name:str):
        self.indentation_spaces-=2
        self.output_file.write(f"{' '*self.indentation_spaces}</{name}>\n")
    
class NullXMLWriter(XMLWriter):
    def __init__(self): pass
    def write_token(self, *a): pass
    def write_identifier(self, *a): pass
    def open_compilation_unit(self, *a): pass
    def close_compilation_unit(self, *a): pass

class ExtendedXMLWriter(XMLWriter):
    def write_identifier(self, name: str,kind:IdentifierKind , is_definition:bool,occurence:int=0):
        extended_info=f"{kind.value}-{'definition' if is_definition else 'use'}"
        if kind not in [IdentifierKind.class_identifier,IdentifierKind.subroutine]:
            extended_info+=f"-{occurence}"
        self.output_file.write(f"{' '*self.indentation_spaces}<{TokenType.identifier.value} {extended_info}> {name} </{TokenType.identifier.value} {extended_info}>\n")

class CompilationEngine:

    def __init__(self,input_file:TextIO,vm_writer:VMWriter,writer:XMLWriter=None):
        self.input_file=input_file
        self.tokenizer=JackTokenizer(input_file)
        self.vm_writer=vm_writer
        self.xml_writer=writer or NullXMLWriter()
        self.symbol_table=SymbolTable()
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
            if self.tokenizer.token_type() in [TokenType.string_const,TokenType.keyword,TokenType.int_const]:
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
                    if self.tokenizer.get_current_token()=='(':
                        self.xml_writer.write_identifier(name,IdentifierKind.subroutine,False)
                    else:
                        self.xml_writer.write_identifier(name,IdentifierKind.class_identifier,False)
                    self._compile_subroutine_call_from_end_of_identifier()
                else:
                    occurence=self.symbol_table.index_of(name)
                    self.xml_writer.write_identifier(name,kind,False,occurence)

    @_compilation_unit("expression")
    def _compile_expression(self):
        self._compile_term()
        while self.tokenizer.get_current_token() in JACK_OPERATIONS:
            self._compile_atom_and_advance_repeatedly(1)
            self._compile_term()
        

    @_compilation_unit("letStatement")
    def _compile_let_statement(self):
        self._compile_atom_and_advance_repeatedly(1)
        name=self.tokenizer.get_current_token()
        self.xml_writer.write_identifier(name,self.symbol_table.kind_of(name),False,self.symbol_table.index_of(name))
        self.tokenizer.advance()
        if self.tokenizer.get_current_token()=="[":
            self._compile_atom_and_advance_repeatedly(1)
            self._compile_expression()
            self._compile_atom_and_advance_repeatedly(1)
        self._compile_atom_and_advance_repeatedly(1)
        self._compile_expression()
        self._compile_atom_and_advance_repeatedly(1)

    @_compilation_unit("returnStatement")
    def _compile_return_statement(self):
        self._compile_atom_and_advance_repeatedly(1)
        if self.tokenizer.get_current_token()!=';':
            self._compile_expression()
        self._compile_atom_and_advance_repeatedly(1)
    
    @_compilation_unit("ifStatement")
    def _compile_if_statement(self):
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_expression()
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_statements()
        self._compile_atom_and_advance_repeatedly(1)
        if self.tokenizer.get_current_token()=="else":
            self._compile_atom_and_advance_repeatedly(2)
            self._compile_statements()
            self._compile_atom_and_advance_repeatedly(1)

    @_compilation_unit("whileStatement")
    def _compile_while_statement(self):
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_expression()
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_statements()
        self._compile_atom_and_advance_repeatedly(1)
    
    @_compilation_unit("expressionList")
    def _compile_expression_list(self):
        while self.tokenizer.get_current_token()!=')':
            self._compile_expression()
            if self.tokenizer.get_current_token()==',':
                self._compile_atom_and_advance_repeatedly(1)
            
    def _compile_subroutine_call_from_end_of_identifier(self):
        if self.tokenizer.get_current_token()=='.':
            self._compile_atom_and_advance_repeatedly(1)
            name=self.tokenizer.get_current_token()
            self.xml_writer.write_identifier(name,IdentifierKind.subroutine,False)
            self.tokenizer.advance()
            self._compile_atom_and_advance_repeatedly(1)
        elif self.tokenizer.get_current_token()=='(':
            self._compile_atom_and_advance_repeatedly(1)
        else:
            raise ValueError("wrong syntax")
        self._compile_expression_list()
        self._compile_atom_and_advance_repeatedly(1)


    @_compilation_unit("doStatement")
    def _compile_do_statement(self):
        self._compile_atom_and_advance_repeatedly(1)
        name=self.tokenizer.get_current_token()
        self.tokenizer.advance()
        if self.tokenizer.get_current_token()=='.':
            kind=self.symbol_table.kind_of(name)
            if kind:
                self.xml_writer.write_identifier(name,kind,False,self.symbol_table.index_of(name))
            else:
                self.xml_writer.write_identifier(name,IdentifierKind.class_identifier,False)
        else:
            self.xml_writer.write_identifier(name,IdentifierKind.subroutine,False)
        self._compile_subroutine_call_from_end_of_identifier()
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
        self.xml_writer.write_identifier(self.tokenizer.get_current_token(),IdentifierKind.subroutine,True)
        self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(1)
        self._compile_parameter_list()
        self._compile_atom_and_advance_repeatedly(1)
        self._compile_subroutine_body()

    @_compilation_unit("class")
    def compile_class(self):
        self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(1)
        self.xml_writer.write_identifier(self.tokenizer.get_current_token(),IdentifierKind.class_identifier,True)
        self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(1)
        while self.tokenizer.get_current_token() in ["field","static"]:
            self._compile_class_var_dec()
        while self.tokenizer.get_current_token() in ["constructor","function","method"]:
            self.compile_subroutine_dec()
        self.compile_atom()