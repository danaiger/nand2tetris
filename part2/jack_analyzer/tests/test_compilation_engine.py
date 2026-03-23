from jack_analyzer.compilation_engine import CompilationEngine

def test_class_without_class_var_dec_and_without_subroutine(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {}""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,output_file)
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier> SomeClass </identifier>
  <symbol> { </symbol>
  <symbol> } </symbol>
</class>"""
