from jack_analyzer.compilation_engine import IdentifierKind

class SymbolTable:

    def __init__(self):
        self.class_level_table=dict()


    def start_subroutine(self):
        self.subroutine_level_table=dict()

    def define(self,name:str,type:str,kind: IdentifierKind):
        if kind in [IdentifierKind.arg,IdentifierKind.var]: 
            self.subroutine_level_table[name]=(name,type,kind,self.var_count(kind))
        else:
            self.class_level_table[name]=(name,type,kind,self.var_count(kind))

    
    def var_count(self,kind:IdentifierKind.arg|IdentifierKind.field|IdentifierKind.var|IdentifierKind.static)->int:
        counter=0
        if kind in [IdentifierKind.arg,IdentifierKind.var]: 
            for entry in self.subroutine_level_table.values():
                if entry[2]==kind:
                    counter+=1
        else:
            for entry in self.class_level_table.values():
                if entry[2]==kind:
                    counter+=1
        return counter

    def index_of(self,name:str):
        if hasattr(self,"subroutine_level_table") and name in self.subroutine_level_table:
            return self.subroutine_level_table[name][3]
        else:
            return self.class_level_table[name][3]