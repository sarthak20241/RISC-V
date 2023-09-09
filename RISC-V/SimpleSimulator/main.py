import sys
import matplotlib.pyplot as plt
register = {
    "000": 0,
    "001": 0,
    "010": 0,
    "011": 0,
    "100": 0,
    "101": 0,
    "110": 0,
    "111": [0, 0, 0, 0]}

def memory(code):
    mem = []
    n = len(code)
    memlen = 256 - n
    for line in code:
        mem.append(line[0:16])
    for i in range(memlen):
        mem.append("0000000000000000")
    return mem

# Convert Binary Value Into 16 Bit
def binaryvalue(number):
    a = bin(number).replace("0b", "")
    if (len(a) <= 16):
        d = "0" * (16 - len(a)) + a
    else:
        d = a[-16:]
    return d

def binaryToDecimal(n):
    return int(n, 2)

def memoryupdate(mem, val, location):
    bval = binaryvalue(val)
    mem[location] = bval
    return mem

flags = "0000000000000000"
ans = []
prc = "00000000"  #Program Counter-->8 bits-->initialy pointing to 0 address

def output(pc, line, mem,flags):  #identifies the instruction and calls the appropriate function
    address="10"
    instr = line[0:5]
    line = line[5:16]
    halt = 0
    oldpc = pc

    if (instr == "00000"):  #add
        flags = "0000000000000000"
        X1 = line[2:5]
        X2 = line[5:8]
        X3 = line[8:11]

        if (register[X2] + register[X3] > 65535):
            flags = "0000000000001000"
            x = register[X2] + register[X3]
            xbinary = binaryvalue(x)
            register[X1] = binaryToDecimal(xbinary)
        else:
            register[X1] = register[X2] + register[X3]
    elif (instr == "00001"):  #Subtraction
        flags = "0000000000000000"
        X1 = line[2:5]
        X2 = line[5:8]
        X3 = line[8:11]
        if (register[X3] > register[X2]):
            register[X1] = 0
            flags = "0000000000001000"
        else:
            register[X1] = register[X2] - register[X3]

    elif (instr == "00010"):  #mov reg1 $Imm
        flags = "0000000000000000"
        X1 = line[0:3]
        Imm = line[3:]
        register[X1] = binaryToDecimal(Imm)

    elif (instr == "00011"):  #mov reg1 reg2
        X1 = line[5:8]
        X2 = line[8:]
        if(X2=="111"):
          m= binaryToDecimal(flags)
          register[X1]=m
        else:  
          register[X1] = register[X2]
        flags = "0000000000000000"
    elif (instr == "00100"):  #Load  ld reg1 memaddr
        flags = "0000000000000000"
        X1 = line[0:3]
        memadr = line[3:11]
        address=line[3:11]
        memad = binaryToDecimal(memadr)
        bval = mem[memad]
        val = binaryToDecimal(bval)
        for i in register:
            if (i == X1):
                register[i] = val

    elif (instr == "00101"):  #Store    st reg1 memaddr
        flags = "0000000000000000"
        X1 = line[0:3]
        val = 0
        memadr = line[3:]
        address=line[3:11]
        location = binaryToDecimal(memadr)
        for i in register:
            if (i == X1):
                val = register[i]
        mem = memoryupdate(mem, val, location)

    elif (instr == "00110"):  #Multiply
        flags = "0000000000000000"
        X1 = line[2:5]
        X2 = line[5:8]
        X3 = line[8:11]
        if (register[X2] * register[X3] > 65535):
            flags = "0000000000001000"
            x = register[X2] * register[X3]
            xbinary = binaryvalue(x)
            register[X1] = binaryToDecimal(xbinary)
        else:
            register[X1] = register[X2] * register[X3]

    elif (instr == "00111"):  #Divide
        flags = "0000000000000000"
        X1 = line[5:8]
        X2 = line[8:11]
        register["000"] = register[X1] // register[X2]
        register["001"] = register[X1] % register[X2]

    elif (instr == "01000"):  #Right Shift     rs reg1 $imm
        flags = "0000000000000000"
        X1 = line[0:3]
        imm = int(line[3:11])
        register[X1] = register[X1] << imm

    elif (instr == "01001"):  #Left Shift      ls reg1 $imm
        flags = "0000000000000000"
        X1 = line[0:3]
        imm = int(line[3:11])
        register[X1] = register[X1] >> imm

    elif (instr == "01010"):  #Exclusive OR
        flags = "0000000000000000"
        X1 = line[2:5]
        X2 = line[5:8]
        X3 = line[8:11]
        x=binaryvalue(register[X2]) 
        y=binaryvalue(register[X3])
        z=''
        for i in range(16):
          a=str(int(x[i]))^str(int(y[i]))
          z+=a
        register[X1] = binaryToDecimal(z)

    elif (instr == "01011"):  #Or
        flags = "0000000000000000"
        X1 = line[2:5]
        X2 = line[5:8]
        X3 = line[8:11]
        x=binaryvalue(register[X2]) 
        y=binaryvalue(register[X3])
        z=''
        for i in range(16):
          a=str(int(x[i]))|str(int(y[i]))
          z+=a
        register[X1] = binaryToDecimal(z)

    elif (instr == "01100"):  #And
        flags = "0000000000000000"
        X1 = line[2:5]
        X2 = line[5:8]
        X3 = line[8:11]
        x=binaryvalue(register[X2]) 
        y=binaryvalue(register[X3])
        z=''
        for i in range(16):
          a=str(int(x[i]))&str(int(y[i]))
          z+=a
        register[X1] = binaryToDecimal(z)

    elif (instr == "01101"):  #Invert
        flags = "0000000000000000"
        X1 = line[5:8]
        X2 = line[8:11]
        register[X1] = ~register[X2]

    elif (instr == "01110"):  #Compare
        flags = "0000000000000000"
        X1 = line[5:8]
        X2 = line[8:11]
        if register[X1] == register[X2]:
            flags = "0000000000000001"
        if int(register[X2]) > int(register[X2]):
            flags = "0000000000000010"
        if int(register[X1]) < int(register[X2]):
            flags = "0000000000000100"

    elif (instr == "01111"):  #UnconditionalJump
        memad = line[3:11]
        memval = binaryToDecimal(memad)
        pc = memval - 1  #-1 is done as in last lines we are doing pc=pc+1
        flags = "0000000000000000"

    elif (instr == "10000"):  #Jump If Less Than
        if flags[
                15] == "1":  
            memad = line[3:]
            memval = binaryToDecimal(memad)
            pc = memval - 1  #-1 is done as in last lines we are doing pc=pc+1
        flags = "0000000000000000"
        #yaha pe jump

    elif (instr == "10001"):  #Jump If Greater Than
        if flags[14] == "1":
            memad = line[3:]
            memval = binaryToDecimal(memad)
            pc = memval - 1  #-1 is done as in last lines we are doing pc=pc+1
        flags = "0000000000000000"

    elif (instr == "10010"):  #Jump If Equal
        if flags[13] == "1":
            memad = line[3:]
            memval = binaryToDecimal(memad)
            pc = memval - 1  #-1 is done as in last lines we are doing pc=pc+1
        flags = "0000000000000000"
    elif (instr == "10011"):  #Halt
        flags = "0000000000000000"
        halt = 1
    pc = pc + 1  #updation of program counter after fetching instruction
    #appending output

    prc = binaryvalue(oldpc)[8:16]  #updating program counter(string)
    r0 = binaryvalue(register["000"])
    r1 = binaryvalue(register["001"])
    r2 = binaryvalue(register["010"])
    r3 = binaryvalue(register["011"])
    r4 = binaryvalue(register["100"])
    r5 = binaryvalue(register["101"])
    r6 = binaryvalue(register["110"])
    klist = [prc, r0, r1, r2, r3, r4, r5, r6, flags]
    print(" ".join(klist))

    prc = binaryvalue(pc)[8:16]  #updating program counter(string)
    return halt, pc, mem, flags,address

def main():
  pc = 0
  code = []
  for i in sys.stdin:
    code.append(i)
  
  flags = "0000000000000000"
  halt = 0
  i = 0
  cycle = 0
  x=[]
  y=[]
  address="10"
  mem = memory(code)
  while (halt == 0):
    i = pc
    line = code[i]
    x.append(cycle)
    y.append(pc)
    halt, pc, mem, flags, address = output(pc, line, mem, flags)
    if address!="10":
      x.append(cycle)
      ad=binaryToDecimal(address)
      y.append(ad)
    cycle = cycle + 1 
  for line in mem:  #memory dump
    print(line)
  plt.scatter(x, y)
  plt.show()
main()