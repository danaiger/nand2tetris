from jack_analyzer.compilation_engine import CompilationEngine,ExtendedXMLWriter

def test_class_without_class_var_dec_and_without_subroutine(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {}""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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
            CompilationEngine(input_file,ExtendedXMLWriter(output_file))
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

# def test_return_with_degenerate_expression(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         return x;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <returnStatement>
#           <keyword> return </keyword>
#           <expression>
#             <term>
#               <identifier> x </identifier>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """


# def test_subroutine_with_multiple_inline_var_declarations(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         var char key, anotherkey;
#         return;
#                     }
#     }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <varDec>
#         <keyword> var </keyword>
#         <keyword> char </keyword>
#         <identifier> key </identifier>
#         <symbol> , </symbol>
#         <identifier> anotherkey </identifier>
#         <symbol> ; </symbol>
#       </varDec>
#       <statements>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """

# def test_let_statement_degenerate_expression(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         let game = game;
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <letStatement>
#           <keyword> let </keyword>
#           <identifier> game </identifier>
#           <symbol> = </symbol>
#           <expression>
#             <term>
#               <identifier> game </identifier>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </letStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """

# def test_let_statement_when_assigning_to_array_degenerate_expression(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         let a[1] = somevar;
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <letStatement>
#           <keyword> let </keyword>
#           <identifier> a </identifier>
#           <symbol> [ </symbol>
#           <expression>
#             <term>
#               <integerConstant> 1 </integerConstant>
#             </term>
#           </expression>
#           <symbol> ] </symbol>
#           <symbol> = </symbol>
#           <expression>
#             <term>
#               <identifier> somevar </identifier>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </letStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """


# def test_multiple_let_statement_degenerate_expression(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         let game = game;
#         let x = x;
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <letStatement>
#           <keyword> let </keyword>
#           <identifier> game </identifier>
#           <symbol> = </symbol>
#           <expression>
#             <term>
#               <identifier> game </identifier>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </letStatement>
#         <letStatement>
#           <keyword> let </keyword>
#           <identifier> x </identifier>
#           <symbol> = </symbol>
#           <expression>
#             <term>
#               <identifier> x </identifier>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </letStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """

# def test_if_statement_degenerate_expression_no_else(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         if (x) {
#         let size = size;
#       }
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <ifStatement>
#           <keyword> if </keyword>
#           <symbol> ( </symbol>
#           <expression>
#             <term>
#               <identifier> x </identifier>
#             </term>
#           </expression>
#           <symbol> ) </symbol>
#           <symbol> { </symbol>
#           <statements>
#             <letStatement>
#               <keyword> let </keyword>
#               <identifier> size </identifier>
#               <symbol> = </symbol>
#               <expression>
#                 <term>
#                   <identifier> size </identifier>
#                 </term>
#               </expression>
#               <symbol> ; </symbol>
#             </letStatement>
#           </statements>
#           <symbol> } </symbol>
#         </ifStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """

# def test_if_statement_degenerate_expression(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         if (b) {
#         }
#         else { 
#         }
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <ifStatement>
#           <keyword> if </keyword>
#           <symbol> ( </symbol>
#           <expression>
#             <term>
#               <identifier> b </identifier>
#             </term>
#           </expression>
#           <symbol> ) </symbol>
#           <symbol> { </symbol>
#           <statements>
#           </statements>
#           <symbol> } </symbol>
#           <keyword> else </keyword>
#           <symbol> { </symbol>
#           <statements>
#           </statements>
#           <symbol> } </symbol>
#         </ifStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """


# def test_while_statement_degenerate_expression(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         while (key) {
#             let key = key;
#          }
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <whileStatement>
#           <keyword> while </keyword>
#           <symbol> ( </symbol>
#           <expression>
#             <term>
#               <identifier> key </identifier>
#             </term>
#           </expression>
#           <symbol> ) </symbol>
#           <symbol> { </symbol>
#           <statements>
#             <letStatement>
#               <keyword> let </keyword>
#               <identifier> key </identifier>
#               <symbol> = </symbol>
#               <expression>
#                 <term>
#                   <identifier> key </identifier>
#                 </term>
#               </expression>
#               <symbol> ; </symbol>
#             </letStatement>
#           </statements>
#           <symbol> } </symbol>
#         </whileStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """

# def test_do_statement_for_functions_degenerate_expression(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         do erase();
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <doStatement>
#           <keyword> do </keyword>
#           <identifier> erase </identifier>
#           <symbol> ( </symbol>
#           <expressionList>
#           </expressionList>
#           <symbol> ) </symbol>
#           <symbol> ; </symbol>
#         </doStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """

# def test_do_statement_for_methods_degenerate_expression(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         do game.run();
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <doStatement>
#           <keyword> do </keyword>
#           <identifier> game </identifier>
#           <symbol> . </symbol>
#           <identifier> run </identifier>
#           <symbol> ( </symbol>
#           <expressionList>
#           </expressionList>
#           <symbol> ) </symbol>
#           <symbol> ; </symbol>
#         </doStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """


# def test_do_statement_for_subroutine_with_single_degenerate_expression(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         do Screen.setColor(x);
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <doStatement>
#           <keyword> do </keyword>
#           <identifier> Screen </identifier>
#           <symbol> . </symbol>
#           <identifier> setColor </identifier>
#           <symbol> ( </symbol>
#           <expressionList>
#             <expression>
#               <term>
#                 <identifier> x </identifier>
#               </term>
#             </expression>
#           </expressionList>
#           <symbol> ) </symbol>
#           <symbol> ; </symbol>
#         </doStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """


# def test_do_statement_for_subroutine_with_multiple_degenerate_expressions(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         do Screen.drawRectangle(x, y, x, y);
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <doStatement>
#           <keyword> do </keyword>
#           <identifier> Screen </identifier>
#           <symbol> . </symbol>
#           <identifier> drawRectangle </identifier>
#           <symbol> ( </symbol>
#           <expressionList>
#             <expression>
#               <term>
#                 <identifier> x </identifier>
#               </term>
#             </expression>
#             <symbol> , </symbol>
#             <expression>
#               <term>
#                 <identifier> y </identifier>
#               </term>
#             </expression>
#             <symbol> , </symbol>
#             <expression>
#               <term>
#                 <identifier> x </identifier>
#               </term>
#             </expression>
#             <symbol> , </symbol>
#             <expression>
#               <term>
#                 <identifier> y </identifier>
#               </term>
#             </expression>
#           </expressionList>
#           <symbol> ) </symbol>
#           <symbol> ; </symbol>
#         </doStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """

# def test_expression_with_multiple_terms(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         let size = size + 2;
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <letStatement>
#           <keyword> let </keyword>
#           <identifier> size </identifier>
#           <symbol> = </symbol>
#           <expression>
#             <term>
#               <identifier> size </identifier>
#             </term>
#             <symbol> + </symbol>
#             <term>
#               <integerConstant> 2 </integerConstant>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </letStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """

# def test_term_with_parantheses(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         let i = i * (j);
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <letStatement>
#           <keyword> let </keyword>
#           <identifier> i </identifier>
#           <symbol> = </symbol>
#           <expression>
#             <term>
#               <identifier> i </identifier>
#             </term>
#             <symbol> * </symbol>
#             <term>
#               <symbol> ( </symbol>
#               <expression>
#                 <term>
#                   <identifier> j </identifier>
#                 </term>
#               </expression>
#               <symbol> ) </symbol>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </letStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """

# def test_unary_op_term(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         let i = i * (-j);
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <letStatement>
#           <keyword> let </keyword>
#           <identifier> i </identifier>
#           <symbol> = </symbol>
#           <expression>
#             <term>
#               <identifier> i </identifier>
#             </term>
#             <symbol> * </symbol>
#             <term>
#               <symbol> ( </symbol>
#               <expression>
#                 <term>
#                   <symbol> - </symbol>
#                   <term>
#                     <identifier> j </identifier>
#                   </term>
#                 </term>
#               </expression>
#               <symbol> ) </symbol>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </letStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """


# def test_access_array_term(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         let somevar = a[2];
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <statements>
#         <letStatement>
#           <keyword> let </keyword>
#           <identifier> somevar </identifier>
#           <symbol> = </symbol>
#           <expression>
#             <term>
#               <identifier> a </identifier>
#               <symbol> [ </symbol>
#               <expression>
#                 <term>
#                   <integerConstant> 2 </integerConstant>
#                 </term>
#               </expression>
#               <symbol> ] </symbol>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </letStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """








# def test_subroutine_call_term(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {
#     method void draw() {
#         var SquareGame game;
#         let game = SquareGame.new();
#         return;}
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,ExtendedXMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <subroutineDec>
#     <keyword> method </keyword>
#     <keyword> void </keyword>
#     <identifier> draw </identifier>
#     <symbol> ( </symbol>
#     <parameterList>
#     </parameterList>
#     <symbol> ) </symbol>
#     <subroutineBody>
#       <symbol> { </symbol>
#       <varDec>
#         <keyword> var </keyword>
#         <identifier class-use> SquareGame </identifier class-use>
#         <identifier var-definition-0> game </identifier var-definition-0>
#         <symbol> ; </symbol>
#       </varDec>
#       <statements>
#         <letStatement>
#           <keyword> let </keyword>
#           <identifier var-use-0> game </identifier var-use-0>
#           <symbol> = </symbol>
#           <expression>
#             <term>
#               <identifier class-use> SquareGame </identifier class-use>
#               <symbol> . </symbol>
#               <identifier subroutine-use> new </identifier subroutine-use>
#               <symbol> ( </symbol>
#               <expressionList>
#               </expressionList>
#               <symbol> ) </symbol>
#             </term>
#           </expression>
#           <symbol> ; </symbol>
#         </letStatement>
#         <returnStatement>
#           <keyword> return </keyword>
#           <symbol> ; </symbol>
#         </returnStatement>
#       </statements>
#       <symbol> } </symbol>
#     </subroutineBody>
#   </subroutineDec>
#   <symbol> } </symbol>
# </class>
# """


# def test_class_(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class SomeClass {}""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,XMLWriter(output_file))
#     assert output_path.read_text()== """<class>
#   <keyword> class </keyword>
#   <identifier> SomeClass </identifier>
#   <symbol> { </symbol>
#   <symbol> } </symbol>
# </class>
# """