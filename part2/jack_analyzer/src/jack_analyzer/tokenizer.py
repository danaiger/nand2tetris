from typing import TextIO

KEYWORD={'class','constructor','function',
         'method','field','static','var',
         'int','char','boolean','void','true',
         'false','null','this','let','do','if',
         'else','while','return'}
SYMBOL={
    '{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','-'
}


class JackTokenizer:

    def __init__(self, file: TextIO ):
        self.current_token=None
        self.file=file

    def advance(self)->None:
       self._advance_to_begin_char() 
    
    def _ignore_if_comment(self):
        current_position=self.file.tell()
        if self.file.read(2)=='//':
            pass

    def _advance_to_begin_char(self):
        begin_char=self.file.read(1)
        while begin_char in (' ','\n'):
            begin_char=self.file.read(1)
        self._ignore_if_comment()
        
            

