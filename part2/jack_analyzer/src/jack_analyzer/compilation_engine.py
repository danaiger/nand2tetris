from typing import TextIO
from jack_analyzer.utils import format_output
from jack_analyzer.tokenizer import JackTokenizer
from jack_analyzer.consts import JACK_OPERATIONS,UNARY_OPERATIONS,TokenType

def _compilation_unit(name:str):
    def decorator(func):
        def wrapper(self:CompilationEngine):
            self.writer.open_compilation_unit(name)
            func(self)
            self.writer.close_compilation_unit(name)
        return wrapper
    return decorator

class XMLWriter:
    def __init__(self,output_file:TextIO):
        self.output_file=output_file
        self.indentation_spaces=0
    
    def write_token(self,current_token:str,current_token_type:TokenType):
        output=format_output(current_token,current_token_type)
        self.output_file.write(f"{' '*self.indentation_spaces}<{current_token_type.value}> {output} </{current_token_type.value}>\n")

    
    def open_compilation_unit(self,name:str):
        self.output_file.write(f"{' '*self.indentation_spaces}<{name}>\n")
        self.indentation_spaces+=2

    def close_compilation_unit(self,name:str):
        self.indentation_spaces-=2
        self.output_file.write(f"{' '*self.indentation_spaces}</{name}>\n")

class CompilationEngine:

    def __init__(self,input_file:TextIO,writer:XMLWriter):
        self.input_file=input_file
        self.tokenizer=JackTokenizer(input_file)
        self.writer=writer
        self.compile_class()

    def compile_atom(self):
        current_token_type=self.tokenizer.token_type()
        current_token=self.tokenizer.get_current_token()
        self.writer.write_token(current_token,current_token_type)
    
    def _compile_var_dec(self):
        self._compile_atom_and_advance_repeatedly(3)
        while self.tokenizer.get_current_token()!=';':
            self._compile_atom_and_advance_repeatedly(2)
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
        self._compile_atom_and_advance_repeatedly(2)
        while self.tokenizer.get_current_token()==',':
            self._compile_atom_and_advance_repeatedly(3)

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
            self._compile_atom_and_advance_repeatedly(1)
            if self.tokenizer.get_current_token()=='[':
                self._compile_atom_and_advance_repeatedly(1)
                self._compile_expression()
                self._compile_atom_and_advance_repeatedly(1)
            elif self.tokenizer.get_current_token() in ['(','.']:
                self._compile_subroutine_call_from_end_of_identifier()

    @_compilation_unit("expression")
    def _compile_expression(self):
        self._compile_term()
        while self.tokenizer.get_current_token() in JACK_OPERATIONS:
            self._compile_atom_and_advance_repeatedly(1)
            self._compile_term()
        

    @_compilation_unit("letStatement")
    def _compile_let_statement(self):
        self._compile_atom_and_advance_repeatedly(2)
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
            self._compile_atom_and_advance_repeatedly(3)
        elif self.tokenizer.get_current_token()=='(':
            self._compile_atom_and_advance_repeatedly(1)
        else:
            raise ValueError("wrong syntax")
        self._compile_expression_list()
        self._compile_atom_and_advance_repeatedly(1)


    @_compilation_unit("doStatement")
    def _compile_do_statement(self):
        self._compile_atom_and_advance_repeatedly(2)
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
        self._compile_atom_and_advance_repeatedly(4)
        self._compile_parameter_list()
        self._compile_atom_and_advance_repeatedly(1)
        self._compile_subroutine_body()

    @_compilation_unit("class")
    def compile_class(self):
        self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(3)
        while self.tokenizer.get_current_token() in ["field","static"]:
            self._compile_class_var_dec()
        while self.tokenizer.get_current_token() in ["constructor","function","method"]:
            self.compile_subroutine_dec()
        self.compile_atom()