from pathlib import Path

class JackAnalyzer:
    def __init__(self,path:Path):
        self.path=path

    def tokenize(self):
        name=self.path.stem+'T'
        path_for_artifact=self.path.parent/(name+'.xml')
        with open(path_for_artifact,'w') as artifact:
            artifact.write("""<tokens>
</tokens>""")