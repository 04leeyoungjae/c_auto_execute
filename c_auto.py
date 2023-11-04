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

def read_log(file='log.txt'):
    with open(file,'r',encoding="utf-8") as f:
        print(f.read())

def execution(filename,testcase,option):
    with open("log.txt",'w',encoding="utf-8") as f:
        for output in run_c_file(filename,testcase):
            f.write(output)
    if option:
        read_log()

def file_in_path(path):
    files=os.listdir(path)
    result=[]
    for file in files:
        if file[-2:]==".c":
            result.append(file)
    return result

def folder_in_path(path):
    files=os.listdir(path)
    result=[]
    parent_folder = os.path.abspath(os.path.join(path,os.pardir))
    result.append(parent_folder)
    for file in files:
        full_path=os.path.join(path,file)
        if os.path.isdir(full_path):
            result.append(full_path.replace("\\\\","\\"))
    return result

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

def clear():
    os.system('cls')
    return

def main(path="C:\\",filename=""):
    testcase=['1','2','3']
    auto_read_option=False
    frame_char='#'
    frame_const=60
    frame=frame_char*frame_const
    clear()
    while True:
        c_file=path+filename
        print(frame)
        print(f"#{formatting('MENU',frame_const-2)}#")
        print(f"#{formatting('0.Exit',frame_const-2)}#")
        print(f"#{formatting('1.Execute File',frame_const-2)}#")
        print(f"#{formatting('2.Edit Path or Filename',frame_const-2)}#")
        print(f"#{formatting('3.Edit Testcase',frame_const-2)}#")
        print(f"#{formatting(f'4.Toggle Auto-read logs (Now:{auto_read_option})',frame_const-2)}#")
        print(f"#{formatting('5.Read logs',frame_const-2)}#")
        print(frame)
        print(f"#{formatting(f'File : {c_file}',frame_const-2)}#")
        print(frame)
        print(f"Testcase : {testcase}")
        select=input(">>> ")
        
        if select=='0':
            quit()
        elif select=='1':
            clear()
            if filename=="":
                print("You should select file before execution")
            else:
                execution(c_file,testcase,auto_read_option)
        elif select=='2':
            clear()
            print("1.Change Path")
            print("2.Change Filename")
            select=input(">>> ")
            if select=='1':
                while True:
                    clear()
                    print("Now path :",path[:-1])
                    lst_print(folder_in_path(path))
                    print("Please enter the index to be change folder '0' to save and return menu")
                    select=input(">>> ")
                    try:
                        select=int(select)
                        if select<0:
                            clear()
                            print("Wrong Input!!!")
                            break
                        elif select==0:
                            clear()
                            print("The path has been successfully changed")
                            break
                        else:
                            path=folder_in_path(path)[select-1]+'\\'
                    except:
                        clear()
                        print("Wrong Input!!!")

            elif select=="2":
                clear()
                while True:
                    if file_in_path(path):
                        lst_print(file_in_path(path))
                        print("Please enter the index to change filename. '0' to return menu")
                        select=input(">>> ")
                        try:
                            select=int(select)
                            if select<0:
                                clear()
                                print("Wrong Input!!!")
                            elif select==0:
                                break
                            else:
                                filename=file_in_path(path)[select-1]
                                clear()
                                print("The filename has been successfully changed")
                                break
                        except:
                            clear()
                            print("Wrong Input!!!")
                    else:
                        clear()
                        print("No file in current path")
                        break
            else:
                clear()
                    
        elif select=='3':
            clear()
            while True:
                lst_print(testcase)
                print()
                print("0.Return to the menu")
                print("1.Add Testcase")
                print("2.Remove Testcase")
                select=input()
                if select=='0':
                    clear()
                    break
                elif select=='1':
                    clear()
                    lst_print(testcase)
                    print()
                    print("Please enter additional testcase")
                    select=input()
                    testcase.append(select.replace("\\n","\n").replace("\\t","\t"))
                    clear()
                elif select=='2':
                    if testcase:
                        clear()
                        lst_print(testcase)
                        print()
                        print("Please enter the testcase want to remove, \'reset\' to remove all")
                        select=input()
                        clear()
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
                        clear()
                        print("Already Empty!!!")
        elif select=='4':
            clear()
            auto_read_option=not(auto_read_option)
        elif select=='5':
            clear()
            read_log()
        else:
            clear()
            print("Wrong Input!!!")
    
if __name__=="__main__":
    main()
