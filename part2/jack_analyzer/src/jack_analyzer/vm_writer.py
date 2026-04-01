import io
from typing import TextIO, Literal
from enum import Enum

class VMSegment(Enum):
    const= "constant"
    arg = "arg"
    local= "local"
    static = "static"
    this = "this"
    that = "that"
    pointer = "pointer"
    temp = "temp"

PopSegment = Literal[
    VMSegment.arg, VMSegment.local, VMSegment.static,
    VMSegment.this, VMSegment.that, VMSegment.pointer, VMSegment.temp
]

ArithmeticOpToVMCommand={
    "+":"add",
    "-":"sub",
    "&":"and",
    "|":"or",
    "<":"lt",
    ">":"gt",
    "=":"eq",
    "~":"not"
}

class VMWriter:
    def __init__(self, output_file: TextIO):
        self.output_file = output_file
    
    def write_function(self,name:str,n_locals:int):
        self.output_file.write(f"function {name} {n_locals}\n")

    def write_arithmetic(self,command:str):
        if command in ArithmeticOpToVMCommand:
            self.output_file.write(f"{ArithmeticOpToVMCommand[command]}\n")
        else:
            self.output_file.write(f"{command}\n")

    def write_push(self,segment: VMSegment, index: int):
        self.output_file.write(f"push {segment.value} {index}\n")

    def write_pop(self,segment: PopSegment, index: int):
        self.output_file.write(f"pop {segment.value} {index}\n")
    
    def write_call(self,name: str, n_args:int):
        self.output_file.write(f"call {name} {n_args}\n")
    
    def write_if(self,label:str):            
        self.output_file.write(f"if-goto {label}\n")
    
    def write_goto(self,label:str):            
        self.output_file.write(f"goto {label}\n")

    def write_label(self,label:str):            
        self.output_file.write(f"Label {label}\n")

    def write_return(self):
        self.output_file.write("return\n")


class NullVMWriter(VMWriter):
    def __init__(self):
        super().__init__(io.StringIO())
