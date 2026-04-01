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
    assert output_path.read_text()=="""function Main.main 0
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
Label L1
Label L2
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
Label L1
push constant 2
call Output.printInt 1
pop temp 0
Label L2
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
    assert output_path.read_text()=="""function Main.main 0
push constant 0
pop local 0
push local 0
push constant 1
add
pop local 0
push constant 0
return
"""

# def test_while(tmp_path):
#     input_path = tmp_path /"input_file"
#     output_path = tmp_path /"output_file"
#     input_path.write_text("""class Main {
#         function void main(){
#         var int count;

#     	let count = 0;
#     	while (count<2) {
#     	    do Output.printInt(count);
#             let count= count+1;
#     	}
#             return;
#                       }
#                           }""")
#     with open(input_path) as input_file:
#         with open(output_path,"w") as output_file:
#             CompilationEngine(input_file,VMWriter(output_file))
#     assert output_path.read_text()=="""function Main.main 0
# push constant 0
# pop local 0
# Label L1
# push local 0
# push constant 2
# lt
# not
# if-goto L2
# push local 0
# call Output.printInt 1
# pop temp 0
# goto L2
# push local 0
# push constant 1
# add
# pop local 0
# goto L1
# Label L2
# push constant 0
# return
# """

