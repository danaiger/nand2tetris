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
</class>
"""

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
</class>
"""

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
</class>
"""

def test_multiple_inline_class_var_dec(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
   field int size, anothersize; 
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
    <symbol> , </symbol>
    <identifier> anothersize </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <symbol> } </symbol>
</class>
"""

def test_basic_subroutine_declaration(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {return;}
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,output_file)
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier> SomeClass </identifier>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> draw </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>
"""

def test_multiple_basic_subroutine_declarations(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {return;}
    method void dispose() {return;}
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,output_file)
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier> SomeClass </identifier>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> draw </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> dispose </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>
"""

def test_subroutine_with_parameters_list(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw(int Ax, int Ay) {return;}
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,output_file)
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier> SomeClass </identifier>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> draw </identifier>
    <symbol> ( </symbol>
    <parameterList>
      <keyword> int </keyword>
      <identifier> Ax </identifier>
      <symbol> , </symbol>
      <keyword> int </keyword>
      <identifier> Ay </identifier>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>
"""
def test_subroutine_with_var_declaration(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {
        var char key;
        return;
                    }
    }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,output_file)
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier> SomeClass </identifier>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> draw </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <keyword> char </keyword>
        <identifier> key </identifier>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>
"""

def test_subroutine_with_multiple_var_declarations(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {
        var char key;
        var boolean exit;
        return;
                    }
    }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,output_file)
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier> SomeClass </identifier>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> draw </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <keyword> char </keyword>
        <identifier> key </identifier>
        <symbol> ; </symbol>
      </varDec>
      <varDec>
        <keyword> var </keyword>
        <keyword> boolean </keyword>
        <identifier> exit </identifier>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>
"""

def test_subroutine_with_multiple_inline_var_declarations(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {
        var char key, anotherkey;
        return;
                    }
    }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,output_file)
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier> SomeClass </identifier>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> draw </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <keyword> char </keyword>
        <identifier> key </identifier>
        <symbol> , </symbol>
        <identifier> anotherkey </identifier>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>
"""