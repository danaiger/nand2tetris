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

def test_basic_class_var_dec(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
   field int size; 
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,output_file)
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier> SomeClass </identifier>
  <symbol> { </symbol>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier> size </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <symbol> } </symbol>
</class>"""

def test_multiple_basic_class_var_dec(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
   field int size; 
   field int x; 
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,output_file)
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier> SomeClass </identifier>
  <symbol> { </symbol>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier> size </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier> x </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <symbol> } </symbol>
</class>"""