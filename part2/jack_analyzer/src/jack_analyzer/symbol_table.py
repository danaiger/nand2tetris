from jack_analyzer.compilation_engine import IdentifierKind

class SymbolTable:

    def __init__(self):
        self.class_level_table=dict()
        self.count_table={
            IdentifierKind.field:0,
            IdentifierKind.static:0,
            IdentifierKind.arg:0,
            IdentifierKind.var:0
        }

    def start_subroutine(self):
        self.subroutine_level_table=dict()
        self.count_table[IdentifierKind.var]=0
        self.count_table[IdentifierKind.arg]=0

    def define(self,name:str,type:str,kind: IdentifierKind):
        self.class_level_table[name]=(name,type,kind,self.count_table[kind])
        self.count_table[kind]+=1
    
    def var_count(self,kind:IdentifierKind.arg|IdentifierKind.field|IdentifierKind.var|IdentifierKind.static)->int:
        return self.count_table[kind]

