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

class CompilationEngine:

    def __init__(self,input_file:TextIO,output_file:TextIO):
        self.input_file=input_file
        self.output_file=output_file
        self.tokenizer=JackTokenizer(input_file)
        self.indentation_spaces=0
        self.compile_class()

    def compile_atom(self):
        self.output_file.write(f"{' '*self.indentation_spaces}<{self.tokenizer.token_type().value}> {self.tokenizer.get_current_token()} </{self.tokenizer.token_type().value}>\n")

    @_xml_tag("classVarDec")
    def compile_class_var_dec(self):
        self._compile_atom_and_advance_repeatedly(3)
        while self.tokenizer.get_current_token()!=';':
            self._compile_atom_and_advance_repeatedly(2)
        self._compile_atom_and_advance_repeatedly(1)

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

    @_xml_tag("returnStatement")
    def _compile_return_statement(self):
        self._compile_atom_and_advance_repeatedly(2)

    @_xml_tag("statements")
    def _compile_statements(self):
        self._compile_return_statement()

    @_xml_tag("varDec")
    def _compile_var_dec(self):
        self._compile_atom_and_advance_repeatedly(4)

    @_xml_tag("subroutineBody")
    def _compile_subroutine_body(self):
        self._compile_atom_and_advance_repeatedly(1)
        while self.tokenizer.get_current_token()=="var":
            self._compile_var_dec()
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
            self.compile_class_var_dec()
        while self.tokenizer.get_current_token() in ["constructor","function","method"]:
            self.compile_subroutine_dec()
        self.compile_atom()