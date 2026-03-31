from typing import TextIO
from jack_analyzer.utils import format_output
from jack_analyzer.consts import TokenType, IdentifierKind

class XMLWriter:
    def __init__(self,output_file:TextIO):
        self.output_file=output_file
        self.indentation_spaces=0

    def write_token(self,current_token:str,current_token_type:TokenType):
        output=format_output(current_token,current_token_type)
        self.output_file.write(f"{' '*self.indentation_spaces}<{current_token_type.value}> {output} </{current_token_type.value}>\n")

    def write_identifier(self,name: str,kind:IdentifierKind , is_definition:bool,occurence:int=0):
        self.write_token(name,TokenType.identifier)

    def open_compilation_unit(self,name:str):
        self.output_file.write(f"{' '*self.indentation_spaces}<{name}>\n")
        self.indentation_spaces+=2

    def close_compilation_unit(self,name:str):
        self.indentation_spaces-=2
        self.output_file.write(f"{' '*self.indentation_spaces}</{name}>\n")

class NullXMLWriter(XMLWriter):
    def __init__(self): pass
    def write_token(self, *a): pass
    def write_identifier(self, *a): pass
    def open_compilation_unit(self, *a): pass
    def close_compilation_unit(self, *a): pass

class ExtendedXMLWriter(XMLWriter):
    def write_identifier(self, name: str,kind:IdentifierKind , is_definition:bool,occurence:int=0):
        extended_info=f"{kind.value}-{'definition' if is_definition else 'use'}"
        if kind not in [IdentifierKind.class_identifier,IdentifierKind.subroutine]:
            extended_info+=f"-{occurence}"
        self.output_file.write(f"{' '*self.indentation_spaces}<{TokenType.identifier.value} {extended_info}> {name} </{TokenType.identifier.value} {extended_info}>\n")
