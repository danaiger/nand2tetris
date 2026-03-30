from enum import Enum

class TokenType(str, Enum):
    keyword = "keyword"
    symbol = "symbol"
    string_const = "stringConstant"
    int_const = "integerConstant"
    identifier = "identifier"

class IdentifierKind(str, Enum):
    class_identifier= "class"
    subroutine= "subroutine"
    field= "field"
    static= "static"
    var= "var"
    arg= "arg"


JACK_KEYWORDS={'class','constructor','function',
         'method','field','static','var',
         'int','char','boolean','void','true',
         'false','null','this','let','do','if',
         'else','while','return'}
JACK_SYMBOLS={
    '{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','-','~'
}

JACK_OPERATIONS={'+','-','*','/','&','|','<','>','='}

UNARY_OPERATIONS={'-','~'}