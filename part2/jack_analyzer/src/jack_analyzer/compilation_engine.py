from typing import TextIO
from jack_analyzer.tokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self,input_file:TextIO,output_file:TextIO):
        self.input_file=input_file
        self.output_file=output_file
        self.tokenizer=JackTokenizer(input_file)
        self.indentation_spaces=0
        self.compile_class()

    def compile_atom(self):
        self.output_file.write(f"{' '*self.indentation_spaces}<{self.tokenizer.token_type().value}> {self.tokenizer.get_current_token()} </{self.tokenizer.token_type().value}>\n")
    
    def compile_class_var_dec(self):
        self.output_file.write(f"{' '*self.indentation_spaces}<classVarDec>\n")
        self.indentation_spaces+=2
        self._compile_atom_and_advance_repeatedly(4)
        self.indentation_spaces-=2
        self.output_file.write(f"{' '*self.indentation_spaces}</classVarDec>\n")

    def _compile_atom_and_advance_repeatedly(self,times:int)->None:
        for _ in range(times):
            self.compile_atom() 
            self.tokenizer.advance()
        

    def compile_subroutine_dec(self):
        pass

    def compile_class(self):
        self.output_file.write("<class>\n")
        self.indentation_spaces+=2
        self.tokenizer.advance()
        self._compile_atom_and_advance_repeatedly(3)
        while self.tokenizer.get_current_token() in ["field","static"]:
            self.compile_class_var_dec()
        while self.tokenizer.get_current_token() in ["constructor","function","method"]:
            self.compile_subroutine_dec()
            self.tokenizer.advance()
        self.compile_atom()
        self.indentation_spaces-=2
        self.output_file.write("</class>")