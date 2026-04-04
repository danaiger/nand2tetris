from jack_analyzer.compilation_engine import CompilationEngine,VMWriter

def test_compile_class_with_void_function_no_parameters(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
                return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 0
push constant 0
return
"""

def test_function_call_with_simple_expression(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
          do Output.printInt(1);
                return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 0
push constant 1
call Output.printInt 1
pop temp 0
push constant 0
return
"""

def test_function_call_with_more_than_one_parameter_as_simple_expressions(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
          do NotRealClass.twoParams(1,2);
                return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 0
push constant 1
push constant 2
call NotRealClass.twoParams 2
pop temp 0
push constant 0
return
"""

def test_function_call_with_expression_including_operation(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
          do Output.printInt(1+2);
                return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 0
push constant 1
push constant 2
add
call Output.printInt 1
pop temp 0
push constant 0
return
"""


def test_expressions_in_paranthesis_are_compiled_in_right_order(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
          do Output.printInt(1+(2*3));
                return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 0
push constant 1
push constant 2
push constant 3
call Math.multiply 2
add
call Output.printInt 1
pop temp 0
push constant 0
return
"""


def test_let(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
            var int something;
            let something=7;
                return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 1
push constant 7
pop local 0
push constant 0
return
"""

def test_if(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
    	    if (3 > 0) {
    	        do Output.printInt(1);
       	    }
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 0
push constant 3
push constant 0
gt
not
if-goto L1
push constant 1
call Output.printInt 1
pop temp 0
goto L2
label L1
label L2
push constant 0
return
"""


def test_if_else(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
    	    if (3 > 0) {
    	        do Output.printInt(1);
       	    }
            else {
                do Output.printInt(2);
            }
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 0
push constant 3
push constant 0
gt
not
if-goto L1
push constant 1
call Output.printInt 1
pop temp 0
goto L2
label L1
push constant 2
call Output.printInt 1
pop temp 0
label L2
push constant 0
return
"""

def test_expression_with_var(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
        var int count;

    	let count = 0;
        let count = count + 1; 
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 1
push constant 0
pop local 0
push local 0
push constant 1
add
pop local 0
push constant 0
return
"""

def test_while(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
        var int count;

    	let count = 0;
    	while (count<2) {
    	    do Output.printInt(count);
            let count= count+1;
    	}
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 1
push constant 0
pop local 0
label L1
push local 0
push constant 2
lt
not
if-goto L2
push local 0
call Output.printInt 1
pop temp 0
push local 0
push constant 1
add
pop local 0
goto L1
label L2
push constant 0
return
"""

def test_boolean(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
            var boolean test;
            let test= true;
            let test= false;
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 1
push constant 1
neg
pop local 0
push constant 0
pop local 0
push constant 0
return
"""

def test_unary_op(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
            var int test;
            let test= -3;
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 1
push constant 3
neg
pop local 0
push constant 0
return
"""

def test_function_definition_includes_right_number_of_locals(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Main {
        function void main(){
            var int test;
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Main.main 1
push constant 0
return
"""

def test_construction_definition(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Point {
        field int x,y;
        
        constructor Point new(int ax, int ay){
            let x = ax;
            let y = ay;
            return this;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Point.new 0
push constant 2
call Memory.alloc 1
pop pointer 0
push argument 0
pop this 0
push argument 1
pop this 1
push pointer 0
return
"""


def test_method_definition(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Point {
        field int x,y;
        
        method int someMethod(){
            var int somevar;
            let somevar = x;
            return somevar;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Point.someMethod 1
push argument 0
pop pointer 0
push this 0
pop local 0
push local 0
return
"""

def test_method_definition_arguments(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class Point {
        field int x,y;
        
        method int someMethod(int par){
            var int somevar;
            let somevar = x + par;
            return somevar;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function Point.someMethod 1
push argument 0
pop pointer 0
push this 0
push argument 1
add
pop local 0
push local 0
return
"""



def test_method_call(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
        
        function void someFunc(){
            var Point p1;
            let p1 = Point.new();
            do p1.nothing();
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function SomeClass.someFunc 1
call Point.new 0
pop local 0
push local 0
call Point.nothing 1
pop temp 0
push constant 0
return
"""


def test_function_call_without_class_name_is_compiled_as_method(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
        
        function void someFunc(){
            do nothing();
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function SomeClass.someFunc 0
push pointer 0
call SomeClass.nothing 1
pop temp 0
push constant 0
return
"""


def test_simple_array_assignment(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
        
        function void someFunc(){
            var Array a;
            let a = Array.new(3);
            let a[1]=2;
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function SomeClass.someFunc 1
push constant 3
call Array.new 1
pop local 0
push local 0
push constant 1
add
push constant 2
pop temp 0
pop pointer 1
push temp 0
pop that 0
push constant 0
return
"""


def test_simple_array_assignment(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
        
        function void someFunc(){
            var Array a;
            let a = Array.new(3);
            let a[1]=2;
            let a[2]=a[1];
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()=="""function SomeClass.someFunc 1
push constant 3
call Array.new 1
pop local 0
push local 0
push constant 1
add
push constant 2
pop temp 0
pop pointer 1
push temp 0
pop that 0
push local 0
push constant 2
add
push local 0
push constant 1
add
pop temp 0
pop pointer 1
push temp 0
pop that 0
push constant 0
return
"""

def test_string_of_one_char_assignment(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
        
        function void someFunc(){
            var String a;
            let a = "A";
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()==f"""function SomeClass.someFunc 1
push constant 1
call String.new 1
push constant {ord("A")}
call String.appendChar 2
pop local 0
push constant 0
return
"""

def test_string_of_multiple_char_assignments(tmp_path):
    input_path = tmp_path /"input_file"
    output_path = tmp_path /"output_file"
    input_path.write_text("""class SomeClass {
        
        function void someFunc(){
            var String a;
            let a = "AD";
            return;
                      }
                          }""")
    with open(input_path) as input_file:
        with open(output_path,"w") as output_file:
            CompilationEngine(input_file,VMWriter(output_file))
    assert output_path.read_text()==f"""function SomeClass.someFunc 1
push constant 2
call String.new 1
push constant {ord("A")}
call String.appendChar 2
push constant {ord("D")}
call String.appendChar 2
pop local 0
push constant 0
return
"""