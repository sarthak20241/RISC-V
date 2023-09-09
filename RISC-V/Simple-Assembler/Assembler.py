import re
import sys
opcodes = {
    "add" : ("00000","A",['r','r','r']),
    "sub" : ("00001","A",['r','r','r']),
    "mov" : (("00010","B",['r','i']),("00011","C",['r','r'])),
    "ld"  : ("00100","D",['r','v']),
    "st"  : ("00101","D",['r','v']),
    "mul" : ("00110","A",['r','r','r']),
    "div" : ("00111","C",['r','r']),
    "rs"  : ("01000","B",['r','i']),
    "ls"  : ("01001","B",['r','i']),
    "xor" : ("01010","A",['r','r','r']),     
    "or"  : ("01011","A",['r','r','r']),
    "and" : ("01100","A",['r','r','r']),
    "not" : ("01101","C",['r','r']),
    "cmp" : ("01110","C",['r','r']),
    "jmp" : ("01111","E",['v']),
    "jlt" : ("10000","E",['v']),
    "jgt" : ("10001","E",['v']),
    "je"  : ("10010","E",['v']),
    "hlt" : ("10011","F",[])
}

register = {
  "R0" : ["000",0],
  "R1" : ["001",0],
  "R2" : ["010",0],
  "R3" : ["011",0],
  "R4" : ["100",0],
  "R5" : ["101",0],
  "R6" : ["110",0],
  "FLAGS" : ["111",0,0,0,0] }

label = {}
labels=[]
label_c={}
variable={}
variables=[]
counter=0
output=[]
regis=["R0","R1","R2","R3","R4","R5","R6"]
FLAGS_r = "000000000"

global emp   #count no. of empty line 

# This Counts the Number of Variables In the program 
def variablecount(code):
  vc=0
  f=0
  e=0
  for k in range(len(code)):
    a=code[k].strip()
    b=a.split()
    if(b):
      break
  
  for j in range(len(code[k])-2):
    if(code[k][j:j+3]=='var' and code[k][j+3]==' '):
      f=1
  ev=k  #no. of lines empty before variable at line i+1
  for i in range(k,len(code)):
    if(f==1):
      oldvc=vc 
      a=code[i].strip()
      b=a.split()
      if(not b):
        e=1
        ev=ev+1 
      for l in range(len(code[i])-2):
        if(code[i][l:l+3]=='var' and code[i][l+3]==' '):
          vc=vc+1
        
      if(e==0 and oldvc==vc):
        f=0
      e=0
  
    #error handling
  
  for i in range(vc+ev,len(code)):
    for j in range(len(code[i])-2):
      if(code[i][j:j+3]=='var' and code[i][j+3]==' '):
        print("Variables not declared at the beginning--> error at line ", i+1 )
        exit(0)
  return vc

#Initialize Label Table 
#pass 1 collecting labels into label table
def label_table(code,vc): 
  k=0 #line number
  e=0 #no. of empty lines before label
  for i in range(len(code)):
    label_count=0 #counting number of labels on same line
    line=code[i]
    for j in range(len(line)):
      # Counting no. of empty lines before label
      l=code[i].strip()
      l=l.split()
      if(not line):
        e=e+1  
      if(line[j:j+1]==':' ):
        #error check
        if(line[j-1:j]==' '):
          print("General Syntax Error(Space Between Label Name and Colon) at line number" + k+1 )
          exit(0)
        else:
          for a in range(j):
            if (line[a]!=' '):
              label_count=label_count+1
              break
        if(label_count==1):
          s=line[a:j]
          if(s+':' not in labels):
            label[s] = k+1-vc-e-1 #assigning true line number removing var
            label_c[s+':']=0
            labels.append(s+':')

        elif(label_count>1):
          print("Two labels on same line-->Error at line ",k+1)
          exit(0)
    k=k+1

#Count No Of Empty Lines 
def count_empty(code):
  emp=0
  for i in range(len(code)):
    code[i]=code[i].strip()
    line=code[i].split()
    if(not line):
      emp=emp+1  
  return emp

#Initialize Variable Table 
def variable_table(code,vc,emp):
  n=len(code)-vc+1
  s=""
  for i in range(vc):
    for j in range(len(code[i])):
      if(code[i][j:j+3]=='var'):
        for k in range(j+4,len(code[i])):      
          #error handling of var for eg var x y<--error
          if(code[i][k]==' '):
            print("Wrong syntax of var-->error at line ",i+1)
            exit(0)
          #finding the variable name and writing in dictionary in next steps
          if(k==len(code[i])-1):
            s=code[i][j+4:k+1]
    #error handling variable name not alphanumeric or _
    if(not(allowed(s))):
      print("invalid variable name at line ",i+1)
      exit(0)     
    variable[s]=n-emp-1
    n=n+1

# error handling
def single_line_error(a,l):
  b=a.strip()  #removes indentation in the start of the code 

  tokens = re.findall('\s+', b)             # checks if there is typo in spacing of terms
  for i in range(0, len(tokens)):
    if len(tokens[i]) !=1:
      print("Line ",l,": typo in spacing of terms.")
      exit(0)

  c=b.split()                            # calling functions according to their first term
  A=["add","sub","mul","xor","or","and"]
  B=["mov","rs","ls"]
  C=["mov","div","not","cmp"]
  D=["ld","st"]
  E=["jmp","jlt","jgt","je"]
  
  
  if(not c):  #Handling Empty lines
    pass
  elif c[0] in A:
    type_A_error(c,l)
  elif c[0] in B and c[2][0]=="$":
    type_B_error(c,l)
  elif c[0] in C:
    type_C_error(c,l) 
  elif c[0] in D:
    type_D_error(c,l)
  elif c[0] in E:
    type_E_error(c,l)
  elif c[0]=="var":
    if(len(c)==1):
      print("No arguments passed in var at line no.",l)
      exit(0)
    elif c[1] not in variables:
        variables.append(c[1])
    else:
      print("Line ",l,": variable already defined")
      exit(0)
  elif(labels and c[0] in labels):
    pass
  elif c[0]=='hlt':
    pass

  else:
    print("Instruction Mistyped at line", l)
    exit(0)
def general_errors(code): #Handling major errors
  l=0
  for a in code:
    l+=1
    single_line_error(a,l)
    
    
def type_A_error(line,l):
  if len(line)!=4:
    print("Line ",l,": General syntax error :- Required No. of arguments were not passed ")
    exit(0)
  # checks if 2nd, 3rd and 4th terms are registers or not
  elif((line[1] not in regis) or (line[2] not in regis) or (line[3] not in regis)):
    print("Line ",l,": syntax error")
    exit(0)

def type_B_error(line,l):
  if (line[1] not in regis): 
    print("Line ",l,": syntax error:- second term is not a register")
    exit(0)
  if line[2][0]!="$":
    print("Line ",l,": syntax error:- third term not a immediate value")
    exit(0)

  #error handling if immediate is float or a string not a whole number
  #is numeric-->float--->'.'is there so it rejects it
  #-->negative-->'-' is there so it rejects it too

  if(not line[2][1:].isnumeric()):
    print("Immediate value entered is not valid at line ",l)
    exit(0)
    
  if int(line[2][1:])<0 or int(line[2][1:])>255:
    print("Line ",l,": Illegal Immediate values (less than 0 or more than 255)")
    exit(0)
  

def type_C_error(line,l):
  if line[1] not in regis and (line[2] not in regis or line[2]!="FLAGS"):      # checks if 2nd and 3rd terms are registers or not
    print("Line ",l,": syntax error")
    exit(0)

def type_D_error(line,l):
  if (line[1] not in regis): 
    print("Line ",l,": syntax error:- second term is not a register")
    exit(0)
  if line[2] not in variables:
    if line[2] in label.keys():
      print("Line ",l,": misuse of labels as a variable")
      exit(0)
    else:
      print("Line ",l,": third term is not a variable")
      exit(0)

def type_E_error(line,l):
  if(len(line)==1):
    print("No arguments passed in line",l)
    exit(0)
  if (not(line[1]+':' in labels)):
    if line[1][:-1] in variables:
      print("Line ",l,": misuse of variables as a label")
      exit(0)
    else:
      print("Line ",l,": use of undefined labels")
      exit(0)
  if (line[1]=="FLAGS"):
    print("Line ",l,": Illegal use of flag register")
    exit(0)
#Call All The Function 
def convert(code,vc):
  instr=""
  s=""
  for i in range(len(code)):
    code[i]=code[i].strip()
    line=code[i].split()
    #Handling empty line
    if(line):
      instr=line[0]
      #Handling Labels
      if(instr in labels):
        if(label_c[instr]==0):
          label_c[instr]=label_c[instr]+1
          line.pop(0)
          label_line=" ".join(line)
          
          single_line_error(label_line,i+1)
          if(line):
            instr=line[0]
          else:
            print("Error: No instruction inside label at line",i+1)
            exit(0)
        else:
          print("Error: Same Label Used More Than Once : in line ",i+1)
          exit(0)

    if(not line):
      continue

    elif(instr=='var'):
      continue  
    elif(instr == 'add'):
      add(line[1],line[2],line[3]) 
         
    elif(instr == 'sub'):
      sub(line[1],line[2],line[3])
      
    elif(instr == 'mov'):
      s= "mov " +(" ".join([line[1],line[2]]))
      mov(s)
      
    elif(instr == 'ld'):
      ld(line[1],line[2])

    elif(instr == 'st'):
      str(line[1],line[2])

    elif(instr == 'mul'):
      mul(line[1],line[2],line[3])

    elif(instr == 'div'):
      divide(line[1],line[2])

    elif(instr == 'rs'):
      s="rs "+(" ".join([line[1],line[2]]))
      rs(s)

    elif(instr == 'ls'):
      s="ls "+(" ".join([line[1],line[2]]))
      ls(s)

    elif(instr == 'xor'):
      XOR(line[1],line[2],line[3])

    elif(instr == 'or'):
      Or(line[1],line[2],line[3])
      
    elif(instr == 'and'):
      And(line[1],line[2],line[3])
      
    elif(instr == 'not'):
      s="not "+(" ".join([line[1],line[2]]))
      invert(s)
      
    elif(instr == 'cmp'):
      s="cmp "+(" ".join([line[1],line[2]]))
      compare(s)

    elif(instr == 'jmp'):
      jmp(line[1])
    
    elif(instr == 'jlt'):
      jlt(line[1])
      
    elif(instr == 'jgt'):
      jgt(line[1])
      
    elif(instr == 'je'):
      je(line[1])
      
    elif(instr == 'hlt'):
      hlt()

def add(X1,X2,X3):
  output.append(opcodes["add"][0] +"00" +  register[X1][0] + register[X2][0]+ register[X3][0])

def sub(X1,X2,X3):
  output.append(opcodes["sub"][0] +"00"+ register[X1][0] + register[X2][0]+ register[X3][0])

def mov(line):
  b=line.strip()
  c=b.split(" ")
  if c[2][0]=="$":
    output.append(opcodes["mov"][0][0]+register[c[1]][0] +binaryvalueto_eight_bit(int(c[2][1:])))
    register[c[1]][1]=c[2][1:]
  else:
    output.append(opcodes["mov"][1][0]+"00000"+register[c[1]][0]+register[c[2]][0])
    register[c[1]][1]=register[c[1]][1]

def ld(X1,var):
  output.append(opcodes["ld"][0] + register[X1][0] + binaryvalueto_eight_bit(variable[var]))

def str(X1,var):
  output.append(opcodes["st"][0] + register[X1][0] + binaryvalueto_eight_bit(variable[var]))

def mul(X1,X2,X3):
  output.append(opcodes["mul"][0] +"00"+ register[X1][0] + register[X2][0]+ register[X3][0])

def divide(X1,X2):
  output.append(opcodes["div"][0] +"00000"+ register[X1][0] + register[X2][0])

def rs(line):
  b=line.strip()
  c=b.split(" ")
  imm=c[2][1:]
  
  output.append(opcodes["rs"][0]+register[c[1]][0] +binaryvalueto_eight_bit(imm))

def ls(line):
  b=line.strip()
  c=b.split(" ")
  imm=int(c[2][1:])
  output.append(opcodes["ls"][0]+register[c[1]][0] +binaryvalueto_eight_bit(imm))


def XOR(X1,X2,X3):
  output.append(opcodes["xor"][0] +"00"+ register[X1][0] + register[X2][0]+ register[X3][0])
  
def Or(X1,X2,X3):
  output.append(opcodes["or"][0] +"00"+ register[X1][0] + register[X2][0]+ register[X3][0])

def And(X1,X2,X3):
  output.append(opcodes["and"][0] +"00"+ register[X1][0] + register[X2][0]+ register[X3][0])

def invert(line):
  b=line.strip()
  c=b.split(" ")
  output.append(opcodes["not"][0] +"00000"+register[c[1]][0]+register[c[2]][0])

def compare(line):
  register["FLAGS"]=("111",0,0,0,0)
  b=line.strip()
  c=b.split(" ")
  if register[c[1]][1]==register[c[2]][1]:
    register["FLAGS"]=("111",0,0,0,1)
  if int(register[c[1]][1])>int(register[c[2]][1]):
    register["FLAGS"]=("111",0,0,1,0)
  if int(register[c[1]][1])<int(register[c[2]][1]):
    register["FLAGS"]=("111",0,1,0,0)
  output.append(opcodes["cmp"][0] +"00000"+register[c[1]][0]+register[c[2]][0])

def jmp(a):
  output.append(opcodes["jmp"][0] + "000" + binaryvalueto_eight_bit(label[a]))

def jlt(a): 
  output.append(opcodes["jlt"][0] + "000" + binaryvalueto_eight_bit(label[a])) 

def jgt(a):
  output.append(opcodes["jgt"][0] + "000" + binaryvalueto_eight_bit(label[a]))

def je(a):
    output.append(opcodes["je"][0] + "000" + binaryvalueto_eight_bit(label[a]))

def hlt():
  output.append(opcodes["hlt"][0] + "00000000000")

# Checking Is AlNum 
def allowed(s):
    a=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','0','_']
    for k in s:
        if k not in a:
            return False
    return True    
  
# Convert Binary Value Into 16 Bit 
def binaryvalue(number):
  number = int(number)
  a=bin(number).replace("0b", "")
  if(len(a)<=16):
    d="0"*(16-len(a))+a
  else:
    d=a[-16:]
  return d

# Convert Binary Value Into 8 Bit 
def binaryvalueto_eight_bit(number):
  number = int(number)
  a=bin(number).replace("0b", "")
  if(len(a)<=8):
    d="0"*(8-len(a))+a
  else:
    d=a[-8:]
  return d

# Main function 
def main():
  code = []
  for i in sys.stdin:
    code.append(i)
  vc=variablecount(code); #variable count
  halt_flag=0;  #halt flag
  n=len(code) #no. of lines of code
  label_table(code,vc)  #assigning labels in dictionary

  for i in range(len(code)):
    code_ws=code[i].strip()
    line=code_ws.split()
    if("hlt" in line):
      if(len(line)==1 and line[0]=='hlt'):
        halt_flag=halt_flag+1
      elif(line[0] in labels):
        halt_flag=halt_flag+1

  if("hlt" not in code[n-1]):
    a=code[n-1].strip()
    b=a.split()
    lflag=0  #last line is empty before hlt(flag)
    if(not b):
      l=n-1
      for h in range(l,0,-1):
        a=code[h].strip()
        b=a.split()
        if(not b):
          pass
        elif('hlt' in b):
            lflag=1
            break
    if(lflag==0 and halt_flag>0):
      print("Halt not at last line")
      exit(0)
    elif(halt_flag==0):
      print("Missing Halt Instruction")
      exit(0)

  if(halt_flag > 1):
    print("More Than One Halt Instruction")
    
  if(halt_flag == 1):
    label_table(code,vc)  #assigning labels in dictionary(label table)
    emp=count_empty(code)
    variable_table(code,vc,emp) #assigning variables in dictionary
    general_errors(code)
    convert(code,vc)
    print("\n".join(output))
main()
