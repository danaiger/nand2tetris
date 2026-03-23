from typing import TextIO
from jack_analyzer.tokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self,input_file:TextIO,output_file:TextIO):
        self.input_file=input_file
        self.output_file=output_file
        self.tokenizer=JackTokenizer(input_file)
        self.compile_class()

    def compile_atom(self):
        self.output_file.write(f"  <{self.tokenizer.token_type().value}> {self.tokenizer.get_current_token()} </{self.tokenizer.token_type().value}>\n")
    
    def compile_class_var_dec(self):
        pass
    def compile_subroutine_dec(self):
        pass

    def compile_class(self):
        self.output_file.write("<class>\n")
        self.tokenizer.advance()
        self.compile_atom() #class keyword
        self.tokenizer.advance()
        self.compile_atom() #className
        self.tokenizer.advance()
        self.compile_atom() #{
        self.tokenizer.advance()
        while self.tokenizer.get_current_token() in ["field","static"]:
            self.compile_class_var_dec()
            self.tokenizer.advance()
        while self.tokenizer.get_current_token() in ["constructor","function","method"]:
            self.compile_subroutine_dec()
            self.tokenizer.advance()
        self.compile_atom()
        self.output_file.write("</class>")