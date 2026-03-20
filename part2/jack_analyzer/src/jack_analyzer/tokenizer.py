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
    
    def has_more_tokens(self)->bool:
        self._advance_to_begin_char()
        next_char=self.file.read(1)
        if next_char != '':
            return True
        else:
            return False
   
    def _ignore_if_comment(self):
        self._ignore_if_inline_comment()

    def _ignore_if_inline_comment(self):
        if self.file.read(2)=='//':
            next_char=self.file.read(1)
            while next_char != '\n' and next_char != '':
                next_char=self.file.read(1)

    def _advance_to_begin_char(self)->None:
        begin_char=self.file.read(1)
        while begin_char in (' ','\n'):
            begin_char=self.file.read(1)
        self.file.seek(self.file.tell()-1)
        self._ignore_if_comment()
        
            

