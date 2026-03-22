from pathlib import Path
from jack_analyzer.tokenizer import JackTokenizer,TokenType

class JackAnalyzer:
    def __init__(self,path:Path):
        self.path=path

    def tokenize(self):
        name=self.path.stem+'T'
        path_for_artifact=self.path.parent.absolute()/(name+'.xml')
        with open(path_for_artifact,'w') as artifact:
            with open(self.path) as file_to_tokenize:
                tokenizer=JackTokenizer(file_to_tokenize)
                artifact.write("<tokens>\n")
                while tokenizer.has_more_tokens():
                    tokenizer.advance()
                    current_token_type=tokenizer.token_type()
                    current_token=tokenizer.get_current_token()
                    if current_token_type==TokenType.string_const:
                        output_representation=(current_token[1:-1])
                    elif current_token_type==TokenType.symbol and current_token in ['<','>','"','&']:
                        if current_token == '<':
                            output_representation='&lt;'
                        elif current_token == '>':
                            output_representation='&gt;'
                        elif current_token == '"':
                            output_representation='&quot;'
                        elif current_token == '&':
                            output_representation='&amp;'
                    else:
                        output_representation=current_token
                    artifact.write(f"<{tokenizer.token_type().value}> ")
                    artifact.write(output_representation)
                    artifact.write(f" </{tokenizer.token_type().value}>\n")
                artifact.write("</tokens>\n")