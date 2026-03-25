from typing import TextIO
from jack_analyzer.consts import TokenType,JACK_KEYWORDS,JACK_SYMBOLS


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
            next_char=self._peek()
            if not next_char.isdigit():
                break
            else:
                current_token+=self.file.read(1)
        return current_token
    
    def _tokenize_symbol(self):
        return self.file.read(1)

        

    def advance(self)->None:
        self._advance_to_begin_char() 
        next_char=self._peek()
        if next_char=='"':
            current_token=self._tokenize_str()
        elif next_char.isdigit():
            current_token=self._tokenize_int_const()
        elif next_char in JACK_SYMBOLS:
            current_token=self._tokenize_symbol()
        else:
            current_token=''
            while True:
                next_char=self._peek()
                if next_char in ['','\n',' ','"'] or next_char in JACK_SYMBOLS:
                    break
                else:
                    current_token+=self.file.read(1)
        self.current_token=current_token

    def token_type(self)->TokenType:
        if self.current_token.startswith('"'):
            return TokenType.string_const
        elif self.current_token in JACK_SYMBOLS:
            return TokenType.symbol
        elif self.current_token[0].isdigit():
            return TokenType.int_const
        elif self.current_token in JACK_KEYWORDS:
            return TokenType.keyword
        else:
            return TokenType.identifier

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
        self._ignore_if_multiline_comment()

    def _ignore_if_multiline_comment(self):
        saved_position=self.file.tell()
        if self.file.read(2)=='/*':
            while self._peek(2)!='*/':
                self.file.read(1)
            self.file.read(2)
        else:
            self.file.seek(saved_position)

    def _ignore_if_inline_comment(self):
        saved_position=self.file.tell()
        if self.file.read(2)=='//':
            next_char=self.file.read(1)
            while next_char != '\n' and next_char != '':
                next_char=self.file.read(1)
        else:
            self.file.seek(saved_position)

    def _peek(self,number_of_chars=1)->str:
        saved_position=self.file.tell()
        next_chars=self.file.read(number_of_chars)
        self.file.seek(saved_position)
        return next_chars

    def _is_comment(self)->bool:
        if self._peek(2)=='//' or self._peek(2)=='/*':
            return True
        else: 
            return False

    def _advance_to_begin_char(self)->None:
        self._skip_empty_chars()
        self._ignore_if_comment()

        next_char=self._peek()
        if next_char=='/' and not self._is_comment():
            return
        if next_char in [' ','\n','/']:
            self._advance_to_begin_char()
        
    def _skip_empty_chars(self)->None:
        while True:
            next_char=self._peek()
            if next_char != ' ' and next_char!='\n' and next_char!='\t':
                break
            self.file.read(1)
            

