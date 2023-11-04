"""
@brief : c언어 파일 자동 input 입력기
@author : https://github.com/karinysis
"""

import subprocess
import os
import time

def visual_whitespace(string:str)->str:
    return string.replace("\n","\\n").replace("\t","\\t").replace(" ","<space>")

def compile(filename:str)->tuple:
    exe_filename="tmp.exe"
    compile_error=False
    compile_process=subprocess.run(["gcc",filename,"-o",exe_filename])
    if compile_process.returncode!=0:
        compile_error=True
    return exe_filename, compile_error

def run_c_file(filename:str,testcase:list=None,max_timeout:int=3)->list:
    if not testcase:
        testcase=['']
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
        input_str=str(input_data)
        if not input_data:
            input_data="<!--void--!>"
        output=frame+f"#{num_exec}\n\n"
        output+=f"입력값\n{input_data}\n\n출력값\n"
        try:
            start_time=time.time()
            result=subprocess.run([exe_filename],input=input_str,stdout=subprocess.PIPE,text=True,universal_newlines=True,timeout=max_timeout,encoding="utf-8")
            end_time=time.time()
            if result.returncode!=0:
                output+=(f"Error with return code {result.returncode}")
            else:
                if not result.stdout:
                    output+="<!--void--!>"
                elif not result.stdout.strip():
                    output+=visual_whitespace(result.stdout)
                else:
                    output+=result.stdout
            output+="\n\n"
            output+=f"실행시간 : [{(end_time-start_time)*1000:.2f} ms]\n"+frame

        except subprocess.TimeoutExpired:
            output+=f"<!--Timeout--!>\n\n실행시간 : [Timeover {max_timeout*1000} ms]\n"+frame

        finally:
            outputs.append(output)

    os.remove(exe_filename)
    return outputs   

def execution(filename,testcase):
    with open("log.txt",'w',encoding="utf-8") as f:
        for output in run_c_file(filename,testcase):
            print(output)
            f.write(output)

def lst_print(lst:list,new_line=1)->None:
    ending="\n"
    if not new_line:
        ending=" "
    if not lst:
        print("[Void]",end=ending)
    for i in range(len(lst)):
        print(f"[{i+1}]","".join(str(lst[i].replace("\n","\\n").replace("\t","\\t"))),end=ending)
    return

def formatting(string,padding):
    return f"{string:^{padding}}"

def main(path="./",filename="__test__.c"):
    testcase=['1','2','3']
    frame_char='#'
    frame_const=60
    frame=frame_char*frame_const
    while True:
        c_file=path+filename
        print(frame)
        print(f"#{formatting('MENU',frame_const-2)}#")
        print(f"#{formatting('0.Exit',frame_const-2)}#")
        print(f"#{formatting('1.Execute File',frame_const-2)}#")
        print(f"#{formatting('2.Edit Path or Filename',frame_const-2)}#")
        print(f"#{formatting('3.Edit Testcase',frame_const-2)}#")
        print(frame)
        print(f"#{formatting(f'File : {c_file}',frame_const-2)}#")
        print(frame)
        print(f"Testcase : {testcase}")
        select=input(">>> ")
        if select=='0':
            quit()
        if select=='1':
            execution(c_file,testcase)
        if select=='2':
            print("1.Change Path")
            print("2.Change Filename")
            select=input(">>> ")
            if select=='1':
                print("Please enter the path to be changed")
                select=input(">>> ")
                path=select+'\\'
                print("The path has been successfully changed")
            if select=="2":
                print("Please enter the filename to be changed")
                select=input(">>> ")
                filename=select
                print("The filename has been successfully changed")
        if select=='3':
            while True:
                print("0.Return to the menu")
                print("1.Add Testcase")
                print("2.Remove Testcase")
                select=input()
                if select=='0':
                    break
                if select=='1':
                    print("Please enter additional testcase")
                    select=input()
                    testcase.append(select.replace("\\n","\n").replace("\\t","\t"))
                if select=='2':
                    if testcase:
                        print("Current Input")
                        lst_print(testcase)
                        print("Please enter the testcase want to remove, \'reset\' to remove all")
                        select=input()
                        if select.lower()=='reset':
                            testcase=[]
                        else:
                            try:
                                select=int(select)
                                if select<=0:
                                    print("Wrong Input!!!")
                                else:
                                    testcase.remove(testcase[select-1])
                            except:
                                print("Wrong Input!!!")
                    else:
                        print("Already Empty!!!")

    
if __name__=="__main__":
    main()
