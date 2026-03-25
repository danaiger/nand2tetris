from typing import TextIO
from jack_analyzer.tokenizer import JackTokenizer

def _xml_tag(name:str):
    def decorator(func):
        def wrapper(self):
            self.output_file.write(f"{' '*self.indentation_spaces}<{name}>\n")
            self.indentation_spaces+=2
            func(self)
            self.indentation_spaces-=2
            self.output_file.write(f"{' '*self.indentation_spaces}</{name}>\n")
        return wrapper
    return decorator

JACK_OPERATIONS={'+','-','*','/','&','|','<','>','='}
UNARY_OPERATIONS={'-','~'}

class CompilationEngine:

    def __init__(self,input_file:TextIO,output_file:TextIO):
        self.input_file=input_file
        self.output_file=output_file
        self.tokenizer=JackTokenizer(input_file)
        self.indentation_spaces=0
        self.compile_class()

    def compile_atom(self):
        self.output_file.write(f"{' '*self.indentation_spaces}<{self.tokenizer.token_type().value}> {self.tokenizer.get_current_token()} </{self.tokenizer.token_type().value}>\n")
    
    def _compile_var_dec(self):
        self._compile_atom_and_advance_repeatedly(3)
        while self.tokenizer.get_current_token()!=';':
            self._compile_atom_and_advance_repeatedly(2)
        self._compile_atom_and_advance_repeatedly(1)


    @_xml_tag("classVarDec")
    def _compile_class_var_dec(self):
        self._compile_var_dec()

    def _compile_atom_and_advance_repeatedly(self,times:int)->None:
        for _ in range(times):
            self.compile_atom() 
            self.tokenizer.advance()

    @_xml_tag("parameterList")
    def _compile_parameter_list(self):
        if self.tokenizer.get_current_token()==')':
            return
        self._compile_atom_and_advance_repeatedly(2)
        while self.tokenizer.get_current_token()==',':
            self._compile_atom_and_advance_repeatedly(3)

    @_xml_tag("term")
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

    @_xml_tag("expression")
    def _compile_expression(self):
        self._compile_term()
        while self.tokenizer.get_current_token() in JACK_OPERATIONS:
            self._compile_atom_and_advance_repeatedly(1)
            self._compile_term()
        

    @_xml_tag("letStatement")
    def _compile_let_statement(self):
        self._compile_atom_and_advance_repeatedly(3)
        self._compile_expression()
        self._compile_atom_and_advance_repeatedly(1)

    @_xml_tag("returnStatement")
    def _compile_return_statement(self):
        self._compile_atom_and_advance_repeatedly(1)
        if self.tokenizer.get_current_token()!=';':
            self._compile_expression()
        self._compile_atom_and_advance_repeatedly(1)
    
    @_xml_tag("ifStatement")
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

    @_xml_tag("whileStatement")
    def _compile_while_statement(self):
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_expression()
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_statements()
        self._compile_atom_and_advance_repeatedly(1)
    
    @_xml_tag("expressionList")
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


    @_xml_tag("doStatement")
    def _compile_do_statement(self):
        self._compile_atom_and_advance_repeatedly(2)
        self._compile_subroutine_call_from_end_of_identifier()
        self._compile_atom_and_advance_repeatedly(1)
        

    @_xml_tag("statements")
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

    @_xml_tag("varDec")
    def _compile_subroutine_var_dec(self):
        self._compile_var_dec()

    @_xml_tag("subroutineBody")
    def _compile_subroutine_body(self):
        self._compile_atom_and_advance_repeatedly(1)
        while self.tokenizer.get_current_token()=="var":
            self._compile_subroutine_var_dec()
        self._compile_statements()
        self._compile_atom_and_advance_repeatedly(1)

    @_xml_tag("subroutineDec")
    def compile_subroutine_dec(self):
        self._compile_atom_and_advance_repeatedly(4)
        self._compile_parameter_list()
        self._compile_atom_and_advance_repeatedly(1)
        self._compile_subroutine_body()

    @_xml_tag("class")
    def compile_class(self):
        self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(3)
        while self.tokenizer.get_current_token() in ["field","static"]:
            self._compile_class_var_dec()
        while self.tokenizer.get_current_token() in ["constructor","function","method"]:
            self.compile_subroutine_dec()
        self.compile_atom()