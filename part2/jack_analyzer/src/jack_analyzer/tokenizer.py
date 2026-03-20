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
    
    def get_current_token(self):
        return self.current_token

    def advance(self)->None:
        current_token=''
        self._advance_to_begin_char() 
        while True:
            next_char=self.file.read(1)
            if next_char == '':
                break
            else:
                current_token+=next_char
        self.current_token=current_token

    
    def has_more_tokens(self)->bool:
        place_to_return=self.file.tell()
        self._advance_to_begin_char()
        next_char=self.file.read(1)
        # print('AAAAAAAAAAAAAa')
        # print(ord(next_char))
        self.file.seek(place_to_return)
        if next_char != '':
            return True
        else:
            return False
   
    def _ignore_if_comment(self):
        self._ignore_if_inline_comment()

    def _ignore_if_inline_comment(self):
        saved_position=self.file.tell()
        if self.file.read(2)=='//':
            next_char=self.file.read(1)
            while next_char != '\n' and next_char != '':
                next_char=self.file.read(1)
        else:
            self.file.seek(saved_position)

    def _advance_to_begin_char(self)->None:
        while True:
            saved_position=self.file.tell()
            next_char=self.file.read(1)
            if next_char != ' ' and next_char!='\n':
                break
        self.file.seek(saved_position)
        # next_char=self.file.read(1)
        # print("AAAAAAAAAAAAAAAAAA")
        # print(ord(next_char))

        # begin_char=self.file.read(1)
        # while begin_char in (' ','\n'):
        #     begin_char=self.file.read(1)
        # self.file.seek(self.file.tell()-1)
        self._ignore_if_comment()
        
            

