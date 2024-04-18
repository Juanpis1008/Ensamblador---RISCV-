#Ensamblador RISCV  - Juan Manuel Diaz Torres - Lina Maria Calvo 
import re
from Classes import *

def CleanFile():
    with open("output_file.asm", 'w'):
        pass
    with open("Output.hex","w"):
        pass

def OpCodeWord(Word):
    OpCode = ""
    TypeR = ["add", "sub", "xor", "or", "and", "sll", "srl", "sra", "slt", "sltu","mul", "mulh", "mulsu", "mulu", "div", "divu", "rem", "remu"]
    TypeI1 = ["addi", "xori", "ori", "andi", "slli", "srli", "srai", "slti", "sltiu"]
    TypeI2 = ["lb", "lh", "lw", "lbu", "lhu"]
    TypeI3 = ["jalr"]
    TypeI4 = ["ecall","ebreak"]
    TypeJ = ["jal"]
    TypeS = ["sb","sh","sw"]
    TypeB = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
    TypeU1 = ["lui"]
    TypeU2 = ["auipc"]


    if Word in TypeR:
        OpCode = "0110011"
    elif Word in TypeI1:
        OpCode = "0010011"
    elif Word in TypeI2:
        OpCode = "0000011"
    elif Word in TypeI3:
        OpCode = "1100111"
    elif Word in TypeI4:
        OpCode = "1110011"
    elif Word in TypeJ:
        OpCode = "1101111"
    elif Word in TypeS:
        OpCode = "0100011"
    elif Word in TypeB:
        OpCode = "1100011"
    elif Word in TypeU1:
        OpCode = "0110111"
    elif Word in TypeU2:
        OpCode = "0010111"

    return OpCode

def FindWord(line):
    words = re.findall(r'\S+', line)
    first_four = words[:4]
    if len(first_four) == 4 and re.match(r'^-?\d+$', first_four[3]):
        if first_four[3][-1] in '-':
            first_four[3] = first_four[3][:-1]
            first_four.append('-')
    first_four = [word.rstrip(',') for word in first_four]
    return first_four

def RemoveX(Word):
    WordWithoutX = re.sub(r'^x', '', Word)
    return int(WordWithoutX)

def WordEquivalence(Word):
    ABINames = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0","a1", "a2","a3","a4","a5","a6","a7","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","t3","t4","t5", "t6"]
    Register = [f'x{i}' for i in range(32)]
    if Word == "fp":
        Word == "s0"
    if Word in ABINames:
        return RemoveX(Register[ABINames.index(Word)])
    else:
        return RemoveX(Word)
    



def RemoveEmptyLines():
    with open("input.asm", 'r') as InputFile:
        with open("input2.asm", 'w') as OutputFile:
            for Line in InputFile:
                if not re.match(r'^\s*$', Line):
                    OutputFile.write(Line)


def IgnoreComments():
    Pattern = r"[#;].*?$"
    with open("input2.asm", 'r') as InputFile:
        with open("input3.asm", 'w') as OutputFile:
            for line in InputFile:
                line_without_comments = re.sub(Pattern, "", line)
                OutputFile.write(line_without_comments)

def IgnoreDirectives():
  Pattern = r"^\s*\."
  with open("input3.asm", 'r') as InputFile:
            with open("input4.asm", 'w') as OutputFile:
                for Line in InputFile:
                    if re.match(Pattern, Line):
                        continue
                    OutputFile.write(Line)

def IdentifyLabels():
    Labels = []
    Pattern = re.compile(r'^\b(\w+):\s*$')
    with open("input4.asm", 'r') as InputFile:
        for Line in InputFile:
            Line = Line.strip()
            match = Pattern.search(Line)
            if match:
                Label = match.group(1)
                Labels += [Label]
    return Labels

def Categorize(Instructions):
    InstructionsClasses = []
    for Instruction in Instructions:
        if Instruction[4] == "0110011":
            Objeto = TypeR(Instruction)
        if Instruction[4] == "0010011" or Instruction[4] == "0000011" or Instruction[4] == "1100111" or Instruction[4] == "1110011":
            Objeto = TypeI(Instruction)
        if Instruction[4] == "0100011":
            Objeto = TypeS(Instruction)
        if Instruction[4] == "1100011":
            Objeto = TypeB(Instruction)
        if Instruction[4] == "1101111":
            Objeto = TypeJ(Instruction)
        if Instruction[4] == "0110111" or Instruction[4] == "0010111":
            Objeto = TypeU(Instruction)
        InstructionsClasses += [Objeto]
    return InstructionsClasses

def IdentifyInstructions():
    Instruction = []
    Instructions = []
    InstructionsClasses = []
    MemoryAddresses = []
    MemoryAddress = 0
    OpCode = ""
    Pattern = r"([^:\s])[^\S]*$"
    with open("input4.asm", 'r') as InputFile:
        for Line in InputFile:
            match = re.search(Pattern, Line)
            if match:
                MemoryAddresses += [MemoryAddress]
                MemoryAddress += 4
                Instruction = FindWord(Line)
                Instruction[1] = WordEquivalence(Instruction[1])
                Instruction[2] = WordEquivalence(Instruction[2])
                OpCode = OpCodeWord(FindWord(Line)[0])
                if OpCode == "":
                    print("Invalid instruction")
                    break
                Instruction  += [OpCode]
                Instructions += [Instruction]
                InstructionsClasses = Categorize(Instructions)
    return InstructionsClasses, MemoryAddresses



def IsInteger(string):
    pattern = r'^-?\d+$'
    return bool(re.match(pattern, string))

def CountInstructionsLabel():
  instructions_per_label = {}
  InstructionsLabel = []
  InstructionsLabel2 = []
  i = 0
  Sum = 0
  with open("input4.asm", 'r') as file:
      current_label = None
      for line in file:
          line = line.strip()
          if line.endswith(":"):
              current_label = line[:-1]
              instructions_per_label[current_label] = 0
          elif line:
              instructions_per_label[current_label] += 1
  for Instruction in instructions_per_label.values():
    Sum += Instruction
    InstructionsLabel += [Instruction]
    InstructionsLabel2 += [i*Sum]
    i = 1

  return InstructionsLabel2


def LastWord(FourthWord,Labels,Position):
    InstructionsLabel2 = CountInstructionsLabel()
    AuxNumber = 0
    FourthWord1 = 0
    if FourthWord in Labels:
        AuxNumber = Labels.index(FourthWord)
        FourthWord1 = (InstructionsLabel2[AuxNumber]-1)*4
        FourthWord = FourthWord1 - Position * 4
    else:
        FourthWord = WordEquivalence(FourthWord)
    return FourthWord



CleanFile()
RemoveEmptyLines()
IgnoreComments()
IgnoreDirectives()
IdentifyLabels()
InstructionsClasses,MemoryAddresses = IdentifyInstructions()
Labels = IdentifyLabels()
Hexadecimal = ""
Output = []
j = 0; x = 0
for i in InstructionsClasses:
    i.Instruction[3] = LastWord(i.Instruction[3],Labels,j)
    j += 1
    i.RD()
    i.Funct3()
    i.RS1()
    i.RS2()
    i.IMM()
    if isinstance(i,TypeR):
        i.Funct7()

for i in InstructionsClasses:
    Hexadecimal = ''.join(i.Instruction[4:])
    file_name = "Output.hex"
    with open(file_name, 'a') as file:
        file.write(Hexadecimal+'\n')
