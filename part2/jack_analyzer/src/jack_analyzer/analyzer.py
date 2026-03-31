from pathlib import Path
from jack_analyzer.tokenizer import JackTokenizer
from jack_analyzer.compilation_engine import CompilationEngine
from jack_analyzer.xml_writer import XMLWriter
from jack_analyzer.vm_writer import NullVMWriter
from jack_analyzer.utils import format_output

class JackAnalyzer:
    def __init__(self,path:Path):
        self.path=path

    def _tokenize_file(self,path:Path):
        name=path.stem+'T'
        path_for_artifact=path.parent.absolute()/(name+'.xml')
        with open(path_for_artifact,'w') as artifact:
            with open(path) as file_to_tokenize:
                tokenizer=JackTokenizer(file_to_tokenize)
                artifact.write("<tokens>\n")
                while tokenizer.has_more_tokens():
                    tokenizer.advance()
                    current_token_type=tokenizer.token_type()
                    current_token=tokenizer.get_current_token()
                    output_representation=format_output(current_token,current_token_type)
                    artifact.write(f"<{tokenizer.token_type().value}> ")
                    artifact.write(output_representation)
                    artifact.write(f" </{tokenizer.token_type().value}>\n")
                artifact.write("</tokens>\n")
        
    def tokenize(self):
        if self.path.is_file():
            self._tokenize_file(self.path)
        elif self.path.is_dir():
            for file in self.path.glob("*.jack"):
                self._tokenize_file(file)
    
    def _analyze_file(self,path):
        with open(path) as input_file:
            with open(path.with_suffix(".xml"),'w') as xml_file:
                CompilationEngine(input_file,NullVMWriter(),XMLWriter(xml_file))

    
    def analyze(self):
        if self.path.is_file():
            self._analyze_file(self.path)
        elif self.path.is_dir():
            for file in self.path.glob("*.jack"):
                self._analyze_file(file)
