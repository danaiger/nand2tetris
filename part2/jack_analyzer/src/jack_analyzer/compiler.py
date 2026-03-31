from pathlib import Path
from jack_analyzer.tokenizer import JackTokenizer
from jack_analyzer.compilation_engine import CompilationEngine
from jack_analyzer.xml_writer import XMLWriter
from jack_analyzer.vm_writer import VMWriter

class JackCompiler:
    def __init__(self,path:Path):
        self.path=path
   
    def _compile_file(self, path, output_dir=None):
        out_dir = output_dir if output_dir is not None else path.parent
        out_path = out_dir / path.with_suffix(".vm").name
        with open(path) as input_file:
            with open(out_path, 'w') as vm_file:
                CompilationEngine(input_file, VMWriter(vm_file))

    def compile(self, output_dir=None):
        if self.path.is_file():
            self._compile_file(self.path, output_dir)
        elif self.path.is_dir():
            for file in self.path.glob("*.jack"):
                self._compile_file(file, output_dir)


if __name__ == "__main__":
    import sys
    JackCompiler(Path(sys.argv[1])).compile()
