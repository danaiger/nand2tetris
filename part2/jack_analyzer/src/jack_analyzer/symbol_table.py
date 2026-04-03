from jack_analyzer.consts import IdentifierKind, VarKind

class SymbolTable:

    def __init__(self):
        self.class_level_table=dict()


    def start_subroutine(self):
        self.subroutine_level_table=dict()

    def define(self,name:str,type:str,kind: VarKind):
        if kind in [IdentifierKind.arg,IdentifierKind.var]: 
            self.subroutine_level_table[name]=(name,type,kind,self.var_count(kind))
        else:
            self.class_level_table[name]=(name,type,kind,self.var_count(kind))

    
    def var_count(self, kind: VarKind) -> int:
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

    def index_of(self,name:str)->int:
        if hasattr(self,"subroutine_level_table") and name in self.subroutine_level_table:
            return self.subroutine_level_table[name][3]
        else:
            return self.class_level_table[name][3]

    def type_of(self,name:str)->str:
        if hasattr(self,"subroutine_level_table") and name in self.subroutine_level_table:
            return self.subroutine_level_table[name][1]
        else:
            return self.class_level_table[name][1]
        
    def kind_of(self,name:str)->VarKind | None:
        if hasattr(self,"subroutine_level_table") and name in self.subroutine_level_table:
            return self.subroutine_level_table[name][2]
        elif name in self.class_level_table:
            return self.class_level_table[name][2]
        else:
            return None
