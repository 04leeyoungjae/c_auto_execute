"""
@brief : c언어 파일 자동 input 입력기
@author : https://github.com/karinysis
"""

import subprocess
import os

def compile(filename):
    exe_filename="tmp.exe"
    compile_error=False
    compile_process=subprocess.run(["gcc",filename,"-o",exe_filename])
    if compile_process.returncode!=0:
        compile_error=True
    return exe_filename, compile_error

def run_c_file(filename,testcase):
    exe_filename,compile_error=compile(filename)
    outputs=[]
    frame="==============================\n"
    if compile_error: #컴파일 에러시 실행해볼 필요가 없음
        output=frame+"Compile Error\n"+frame
        outputs.append(output)
        return outputs
    for input_data in testcase:
        output=frame
        output+=f"입력값 : {input_data}\n출력값 : "
        result=subprocess.run([exe_filename],input=input_data,stdout=subprocess.PIPE,text=True,universal_newlines=True)
        if result.returncode!=0:
            output+=(f"Error with return code {result.returncode}")
        else:
            output+=(result.stdout)
        output+="\n"+frame
        outputs.append(output)
    os.remove(exe_filename)
    return outputs   
    

filename="__test__.c"
testcase=['','1','2']
for output in run_c_file(filename,testcase):
    print(output)