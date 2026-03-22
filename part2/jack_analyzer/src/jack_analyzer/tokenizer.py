from typing import TextIO

JACK_KEYWORDS={'class','constructor','function',
         'method','field','static','var',
         'int','char','boolean','void','true',
         'false','null','this','let','do','if',
         'else','while','return'}
JACK_SYMBOLS={
    '{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','-'
}


class JackTokenizer:

    def __init__(self, file: TextIO ):
        self.current_token=None
        self.file=file
    
    def get_current_token(self):
        return self.current_token
    
    def _tokenize_str(self)->str:
        current_token=self.file.read(1)

        while True:
            next_char=self.file.read(1)
            if next_char in ['"']:
                break
            else:
                current_token+=next_char
        return current_token+'"'

    def _tokenize_int_const(self)->int:
        current_token=self.file.read(1)

        while True:
            next_char=self.file.read(1)
            if not next_char.isdigit():
                break
            else:
                current_token+=next_char
        return current_token

        

    def advance(self)->None:
        self._advance_to_begin_char() 
        next_char=self._peek()
        if next_char=='"':
            current_token=self._tokenize_str()
        elif next_char.isdigit():
            current_token=self._tokenize_int_const()
        else:
            current_token=''
            while True:
                next_char=self.file.read(1)
                if next_char in ['','\n',' ']:
                    break
                else:
                    current_token+=next_char
        self.current_token=current_token

    def token_type(self)->str:
        if self.current_token.startswith('"'):
            return "STRING_CONST"
        elif self.current_token in JACK_SYMBOLS:
            return "SYMBOL"
        elif self.current_token[0].isdigit():
            return "INT_CONST"
        elif self.current_token in JACK_KEYWORDS:
            return "KEYWORD"
        else:
            return "IDENTIFIER"

    def has_more_tokens(self)->bool:
        place_to_return=self.file.tell()
        self._advance_to_begin_char()
        next_char=self.file.read(1)
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

    def _peek(self,number_of_chars=0)->str:
        saved_position=self.file.tell()
        next_chars=self.file.read(number_of_chars+1)
        self.file.seek(saved_position)
        return next_chars

    def _is_comment(self)->bool:
        if self._peek(2)=='//':
            return True
        else: 
            return False

    def _advance_to_begin_char(self)->None:
        self._skip_white_spaces_and_newlines()
        self._ignore_if_comment()

        next_char=self._peek()
        if next_char=='/' and not self._is_comment():
            return
        if next_char in [' ','\n']:
            self._advance_to_begin_char()
        
    def _skip_white_spaces_and_newlines(self)->None:
        while True:
            next_char=self._peek()
            if next_char != ' ' and next_char!='\n':
                break
            self.file.read(1)
            

