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

def read_log(file:str='log.txt')->None:
    with open(file,'r',encoding="utf-8") as f:
        print(f.read())
    print("Press enter key to continue")
    input() #로그 읽을 동안 메뉴가 안뜨게 설정
    return

def execution(filename:str,testcase:list,option:bool,timeout:int)->None:
    with open("log.txt",'w',encoding="utf-8") as f:
        for output in run_c_file(filename,testcase,timeout):
            f.write(output)
    if option:
        read_log()

def file_in_path(path:str)->list:
    files=os.listdir(path)
    result=[]
    for file in files:
        if file[-2:]==".c":
            result.append(file)
    return result

def folder_in_path(path:str)->list:
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

def formatting(string:str,padding:int)->str:
    return f"{string:^{padding}}"

def clear()->None:
    os.system('cls')
    return

def random_int(minimum:int=0,maximum:int=100)->int:
    return __import__('random').randint(minimum,maximum)

def random_pseudo()->bool:
    return random_int(0,1)

def random_alphabet(uppercase:bool=0)->str:
    if uppercase:
        return chr(random_int(ord('A'),ord('Z')))
    return chr(random_int(ord('a'),ord('z')))

def random_word(length:int,uppercase:int=0)->str: #case=0 소문자단어 case=1 대문자단어 case2 첫글자만대문자
    result=''
    if uppercase==2: #첫글자만 대문자로
        result+=random_alphabet(1)
        length-=1
        uppercase-=2
    for i in range(length):
        result+=random_alphabet(uppercase)
    return result

def random_list_int(length:int,minimum:int=0,maximum:int=100)->str:
    result=''
    for i in range(length):
        result+=f"{random_int(minimum,maximum)} "
    return result

def random_matrix_int(row:int,col:int,minimum:int=0,maximum:int=100,view_row:bool=0,view_col:bool=0)->str:
    result=''
    if view_row:
        result+=f"{row}"
        if view_col:
            result+=f" {col}\n"
        else:
            result+='\n'
    elif view_col:
        result+=f"{col}\n"
    for i in range(row):
        result+=f"{random_list_int(col,minimum,maximum)}\n"
    return result

def main(path="C:\\",filename=""):
    testcase=[]
    auto_read_option=False
    frame_char='#'
    frame_const=60
    format_frame=frame_const-2
    timeout=3
    frame=frame_char*frame_const
    clear()
    while True:
        c_file=path+filename
        print(frame)
        print(f"#{formatting('MENU',format_frame)}#")
        print(f"#{formatting('0.Exit',format_frame)}#")
        print(f"#{formatting('1.Execute File',format_frame)}#")
        print(f"#{formatting('2.Edit Path or Filename',format_frame)}#")
        print(f"#{formatting('3.Edit Testcase',format_frame)}#")
        print(f"#{formatting(f'4.Toggle Auto-read logs (Current:{auto_read_option})',format_frame)}#")
        print(f"#{formatting(f'5.Change Timeout (Current:{timeout})',format_frame)}#")
        print(f"#{formatting('6.Read logs',format_frame)}#")
        print(frame)
        print(f"#{formatting(f'File : {c_file}',format_frame)}#")
        print(frame)
        print(f"Testcase : {testcase}")
        select=input(">>> ")
        
        if select=='0': #0.Exit
            quit()
        elif select=='1': #1.Execute File
            clear()
            if filename=="":
                print("You should select file before execution")
            else:
                execution(c_file,testcase,auto_read_option,timeout)
        elif select=='2': #2.Edit Path or Filename
            clear()
            print("1.Change Path")
            print("2.Change Filename")
            select=input(">>> ")
            if select=='1':
                while True:
                    clear()
                    print("[0] Current path :",path[:-1])
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
                    
        elif select=='3': #3.Edit Testcase
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
                    print("Please enter additional testcase, 'random' to add random testcase")
                    select=input()
                    if select.lower()!="random":
                        testcase.append(select.replace("\\n","\n").replace("\\t","\t"))
                        clear()
                        print("Successfully changed")
                    else:
                        clear()
                        return_edit_testcase=False
                        while True:
                            if return_edit_testcase:
                                break
                            print("Enter number of testcase you want to add '0' to return Edit testcase")
                            select=input()
                            clear()
                            if select=='0':                                
                                break
                            else:
                                try:
                                    num_random_testcase=int(select)
                                    while True:
                                        print("0.Return Edit testcase")
                                        print("1.Random int Matrix")
                                        select=input()
                                        clear()
                                        if select=='0':
                                            break
                                        elif select=='1':
                                            while True: #num_row
                                                print("Enter num_row, 'random minimum maxinum' to random")
                                                print("ex. '5', 'random 2 10'")
                                                select=input().split()
                                                clear()
                                                if len(select)==1:
                                                    try:
                                                        random_row_min=int(select[0])
                                                        random_row_max=int(select[0])
                                                        break
                                                    except:
                                                        print("Wrong Input!!!")
                                                elif len(select)==3:
                                                    if select[0].lower()!="random":
                                                        print("Wrong Input!!!")
                                                    else:
                                                        try:
                                                            random_row_min=int(select[1])
                                                            random_row_max=int(select[2])
                                                            break
                                                        except:
                                                            print("Wrong Input!!!")
                                            while True: #num_col
                                                print("Enter num_col, 'random minimum maxinum' to random")
                                                print("ex. '5', 'random 2 10'")
                                                select=input().split()
                                                clear()
                                                if len(select)==1:
                                                    try:
                                                        random_col_min=int(select[0])
                                                        random_col_max=int(select[0])
                                                        break
                                                    except:
                                                        print("Wrong Input!!!")
                                                elif len(select)==3:
                                                    if select[0].lower()!="random":
                                                        print("Wrong Input!!!")
                                                    else:
                                                        try:
                                                            random_col_min=int(select[1])
                                                            random_col_max=int(select[2])
                                                            break
                                                        except:
                                                            print("Wrong Input!!!")
                                            while True: #min_matrix_element
                                                print("Enter minimum of matrix element")
                                                select=input()
                                                clear()
                                                try:
                                                    min_matrix_element=int(select)
                                                    break
                                                except:
                                                    print("Wrong Input!!!")
                                            while True: #max_matrix_element
                                                print("Enter maximum of matrix element")
                                                select=input()
                                                clear()
                                                try:
                                                    max_matrix_element=int(select)
                                                    break
                                                except:
                                                    print("Wrong Input!!!")
                                            while True: #view_row
                                                print("Include the number of rows?")
                                                print("1 to include, 0 to not")
                                                select=input()
                                                clear()
                                                try:
                                                    view_row=int(select)
                                                    if view_row!=1 and view_row!=0:
                                                        print("Wrong Input!!!")
                                                    else:
                                                        break
                                                except:
                                                    print("Wrong Input!!!")
                                            while True: #view col
                                                print("Include the number of cols?")
                                                print("1 to include, 0 to not")
                                                select=input()
                                                clear()
                                                try:
                                                    view_col=int(select)
                                                    if view_col!=1 and view_col!=0:
                                                        print("Wrong Input!!!")
                                                    else:
                                                        break
                                                except:
                                                    print("Wrong Input!!!")
                                            for i in range(num_random_testcase): #append matrix input
                                                testcase.append(random_matrix_int(random_int(random_row_min,random_row_max),random_int(random_col_min,random_col_max),min_matrix_element,max_matrix_element,view_row,view_col))
                                            print("Successfully changed")
                                            return_edit_testcase=True
                                            break


                                except:
                                    print("Wrong Input!!!")
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
        elif select=='4': #4.Toggle Auto-read logs
            clear()
            auto_read_option=not(auto_read_option)
        elif select=='5': #5.Change Timeout
            clear()
            print("Enter the timeout per single execution (Seconds)")
            while True:
                try:
                    select=int(input())
                    clear()
                    if(select<=0):
                        print("Please input more than 0 second")
                    else:
                        timeout=select
                        print("Successfully changed")
                        break
                except:
                    clear()
                    print("Wrong Input!!!")
        elif select=='6':
            clear()
            read_log()
        else:
            clear()
            print("Wrong Input!!!")
    
if __name__=="__main__":
    main()
