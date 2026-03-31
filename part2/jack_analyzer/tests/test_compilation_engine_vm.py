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
