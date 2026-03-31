from jack_analyzer.compilation_engine import CompilationEngine,ExtendedXMLWriter,NullVMWriter

def test_class_without_class_var_dec_and_without_subroutine(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {}""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
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
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier field-definition-0> size </identifier field-definition-0>
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
   static int x; 
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier field-definition-0> size </identifier field-definition-0>
    <symbol> ; </symbol>
  </classVarDec>
  <classVarDec>
    <keyword> static </keyword>
    <keyword> int </keyword>
    <identifier static-definition-0> x </identifier static-definition-0>
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
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier field-definition-0> size </identifier field-definition-0>
    <symbol> , </symbol>
    <identifier field-definition-1> anothersize </identifier field-definition-1>
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
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
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
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
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
    <identifier subroutine-definition> dispose </identifier subroutine-definition>
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
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
      <keyword> int </keyword>
      <identifier arg-definition-0> Ax </identifier arg-definition-0>
      <symbol> , </symbol>
      <keyword> int </keyword>
      <identifier arg-definition-1> Ay </identifier arg-definition-1>
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
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <keyword> char </keyword>
        <identifier var-definition-0> key </identifier var-definition-0>
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
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <keyword> char </keyword>
        <identifier var-definition-0> key </identifier var-definition-0>
        <symbol> ; </symbol>
      </varDec>
      <varDec>
        <keyword> var </keyword>
        <keyword> boolean </keyword>
        <identifier var-definition-1> exit </identifier var-definition-1>
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

def test_multiple_subroutines_with_var_declaration(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {
        var char key;
        return;
                    }
    method void erase() {
        var char key;
        return;
                    }
    }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <keyword> char </keyword>
        <identifier var-definition-0> key </identifier var-definition-0>
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
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> erase </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <keyword> char </keyword>
        <identifier var-definition-0> key </identifier var-definition-0>
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

def test_subroutine_with_var_declaration_which_its_type_is_other_class(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {
        var SquareGame game;
        return;
                    }
    }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <identifier class-use> SquareGame </identifier class-use>
        <identifier var-definition-0> game </identifier var-definition-0>
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

def test_subroutine_declaration_that_returns_custom_type(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method SquareGame draw() {
        var SquareGame game;                  
        return game;
      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <identifier class-use> SquareGame </identifier class-use>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <identifier class-use> SquareGame </identifier class-use>
        <identifier var-definition-0> game </identifier var-definition-0>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <returnStatement>
          <keyword> return </keyword>
          <expression>
            <term>
              <identifier var-use-0> game </identifier var-use-0>
            </term>
          </expression>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>
"""

def test_do_statement(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {
        do erase();
        return;}
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <doStatement>
          <keyword> do </keyword>
          <identifier subroutine-use> erase </identifier subroutine-use>
          <symbol> ( </symbol>
          <expressionList>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
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

def test_do_statement_using_method_on_var(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {
        var Square square;
        do square.dec_size();
        return;}
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <identifier class-use> Square </identifier class-use>
        <identifier var-definition-0> square </identifier var-definition-0>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <doStatement>
          <keyword> do </keyword>
          <identifier var-use-0> square </identifier var-use-0>
          <symbol> . </symbol>
          <identifier subroutine-use> dec_size </identifier subroutine-use>
          <symbol> ( </symbol>
          <expressionList>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
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


def test_do_statement_using_class_function(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {
        do Something.doSomething();
        return;}
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <doStatement>
          <keyword> do </keyword>
          <identifier class-use> Something </identifier class-use>
          <symbol> . </symbol>
          <identifier subroutine-use> doSomething </identifier subroutine-use>
          <symbol> ( </symbol>
          <expressionList>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
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

def test_subroutine_call_term(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
    method void draw() {
        var SquareGame game;
        let game = SquareGame.new();
        return;}
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,NullVMWriter(),ExtendedXMLWriter(output_file))
    assert output_path.read_text()== """<class>
  <keyword> class </keyword>
  <identifier class-definition> SomeClass </identifier class-definition>
  <symbol> { </symbol>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier subroutine-definition> draw </identifier subroutine-definition>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <identifier class-use> SquareGame </identifier class-use>
        <identifier var-definition-0> game </identifier var-definition-0>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <letStatement>
          <keyword> let </keyword>
          <identifier var-use-0> game </identifier var-use-0>
          <symbol> = </symbol>
          <expression>
            <term>
              <identifier class-use> SquareGame </identifier class-use>
              <symbol> . </symbol>
              <identifier subroutine-use> new </identifier subroutine-use>
              <symbol> ( </symbol>
              <expressionList>
              </expressionList>
              <symbol> ) </symbol>
            </term>
          </expression>
          <symbol> ; </symbol>
        </letStatement>
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
