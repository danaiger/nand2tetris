from jack_analyzer.tokenizer import TokenType

def format_output(token:str,token_type:TokenType)->str:
    if token_type==TokenType.string_const:
        output_representation=(token[1:-1])
    elif token_type==TokenType.symbol and token in ['<','>','"','&']:
        if token == '<':
            output_representation='&lt;'
        elif token == '>':
            output_representation='&gt;'
        elif token == '"':
            output_representation='&quot;'
        elif token == '&':
            output_representation='&amp;'
    else:
        output_representation=token
    return output_representation

