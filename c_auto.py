"""
@brief : c언어 파일 자동 input 입력기
@author : https://github.com/karinysis
"""

import subprocess
import os
import time

def compile(filename):
    exe_filename="tmp.exe"
    compile_error=False
    compile_process=subprocess.run(["gcc",filename,"-o",exe_filename])
    if compile_process.returncode!=0:
        compile_error=True
    return exe_filename, compile_error

def run_c_file(filename,testcase,max_timeout=3):
    exe_filename,compile_error=compile(filename)
    outputs=[]
    frame="==============================\n"
    if compile_error: #컴파일 에러시 실행해볼 필요가 없음
        output=frame+"Compile Error\n"+frame
        outputs.append(output)
        return outputs
    num_exec=0
    for input_data in testcase:
        num_exec+=1
        input_str=input_data
        if not input_data:
            input_data="<!--void--!>"
        output=frame+f"#{num_exec}\n\n"
        output+=f"입력값\n{input_data}\n\n출력값\n"
        try:
            start=time.time()
            result=subprocess.run([exe_filename],input=input_str,stdout=subprocess.PIPE,text=True,universal_newlines=True,timeout=max_timeout,encoding="utf-8")
            end=time.time()
            if result.returncode!=0:
                output+=(f"Error with return code {result.returncode}")
            else:
                if not result.stdout:
                    output+="<!--void--!>"
                else:
                    output+=result.stdout
            output+="\n\n"
            output+=f"실행시간 : [{(end-start)*1000:.2f} ms]\n"+frame

        except subprocess.TimeoutExpired:
            output+=f"<!--Timeout--!>\n\n실행시간 : [Timeover {max_timeout*1000} ms]\n"+frame

        finally:
            outputs.append(output)

    os.remove(exe_filename)
    return outputs   
    
if __name__=="__main__":
    filename="__test__.c"
    testcase=['','1','2']
    with open("log.txt",'w',encoding="utf-8") as f:
        for output in run_c_file(filename,testcase):
            print(output)
            f.write(output)