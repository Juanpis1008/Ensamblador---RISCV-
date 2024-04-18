import re

def DecimalToBinary(DecimalNumber):
    if DecimalNumber == 0:
        return '0'
    
    bits = []
    absolute_number = abs(DecimalNumber)
    while absolute_number > 0:
        remainder = absolute_number % 2
        bits.append(str(remainder))
        absolute_number //= 2
    
    bits.reverse()
    binary_representation = ''.join(bits)
    if DecimalNumber < 0:
        binary_representation = binary_representation.zfill(32)
        binary_representation = ''.join(['1' if bit == '0' else '0' for bit in binary_representation])
        binary_representation = binary_representation.lstrip('0')
        binary_representation = '1' + binary_representation 
        binary_representation = bin(int(binary_representation, 2) + 1)[2:]
    
    return binary_representation or '0' 

def IsNegative(string):
    pattern = r'^-\d+(\.\d+)?$'
    return bool(re.match(pattern, string))

def TwosComplement(Word):
    print(Word)
    Word = Word.zfill(12)
    print(Word)
    for i in range(len(Word)):
        if Word[i] == "1":
            Word[i] == "0"
        else:
            Word[i] == "1"
    return(int(Word))

class Types:
    def __init__(self, Instruction):
        self.Instruction = Instruction
    
    def RD(self):
        if isinstance(self,TypeS) or isinstance(self,TypeB):
            pass
        else:
            rd = (DecimalToBinary(int(self.Instruction[1]))).zfill(5)
            self.Instruction.insert(4,rd)
        return self.Instruction
    
    def RS1(self):
        if isinstance(self,TypeJ) or isinstance(self,TypeU):
            pass
        elif isinstance(self,TypeB):
            rs1 = (DecimalToBinary(int(self.Instruction[1]))).zfill(5)
            self.Instruction.insert(4,rs1)
        else:
            rs1 = (DecimalToBinary(int(self.Instruction[2]))).zfill(5)
            self.Instruction.insert(4,rs1)
        return self.Instruction
    
    def RS2(self):
        if  isinstance(self,TypeR) or isinstance(self,TypeS):
            rs2 = DecimalToBinary(int(self.Instruction[3])).zfill(5)
            self.Instruction.insert(4,rs2)
        elif isinstance(self,TypeB):
            rs2 = DecimalToBinary(int(self.Instruction[2])).zfill(5)
            self.Instruction.insert(4,rs2)
        else:
            pass
        return self.Instruction
    
    def Funct7(self):
        if self.Instruction[0] == "sub" or self.Instruction[0] == "sra":
            funct7 = "0100000"
        else:
            funct7 = "0000000"
        return self.Instruction.insert(4,funct7)

    def Funct3(self):
        OpCode = self.Instruction[4]
        if isinstance(self,TypeJ) or isinstance(self,TypeU):
            pass
        else:
            Word = self.Instruction[0]
            WordsX1 = ["sll","slli","lh","sh","bne","mulh"]
            WordsX2 = ["slt","slti","lw","sw","mulsu"]
            WordsX3 = ["sltu","sltiu","mulu"]
            WordsX4 = ["xor","xori","lbu","blt","div"]
            WordsX5 = ["srl","sra","srli","srai","lhu","bge","divu"]
            WordsX6 = ["or","ori","vltu","rem"]
            WordsX7 = ["and","andi","bgeu","remu"]
            if Word in WordsX1:
                funct3 = "001"
            elif Word in WordsX2:
                funct3 = "010"
            elif Word in WordsX3:
                funct3 = "011"
            elif Word in WordsX4:
                funct3 = "100"
            elif Word in WordsX5:
                funct3 = "101"
            elif Word in WordsX6:
                funct3 = "110"
            elif Word in WordsX7:
                funct3 = "111"
            else:
                funct3 = "000"
            self.Instruction.insert(4,funct3)
        return self.Instruction

    def IMM(self):
        imm = ""
        if isinstance(self,TypeR):    
            pass
        else:
            if isinstance(self, TypeI):
                imm = DecimalToBinary(int(self.Instruction[3]))[-12:].zfill(12) 
            elif isinstance(self, TypeS):
                imm = DecimalToBinary(int(self.Instruction[3]))[-5:].zfill(5) 
                self.Instruction.insert(-1, imm)
                imm = DecimalToBinary(int(self.Instruction[3]))[-12:-5].zfill(7) 
            elif isinstance(self, TypeB):
                imm = (DecimalToBinary(int(self.Instruction[3]))[-4:]+DecimalToBinary(int(self.Instruction[3]))[-12:-11]).zfill(5) 
                self.Instruction.insert(-1, imm)
                imm = (DecimalToBinary(int(self.Instruction[3]))[-13:-12] + DecimalToBinary(int(self.Instruction[3]))[-11:-5]).zfill(7)
            elif isinstance(self, TypeU):
                imm = DecimalToBinary(int(self.Instruction[3]))[-32:-12].zfill(20) 
            elif isinstance(self, TypeJ):
                imm = DecimalToBinary(int(self.Instruction[3]))[-21:-20] + DecimalToBinary(int(self.Instruction[3]))[-11:-1] + DecimalToBinary(int(self.Instruction[3]))[-12:-11] + DecimalToBinary(int(self.Instruction[3]))[-20:-12] 
            self.Instruction.insert(4, imm)
        
        return self.Instruction


class TypeR(Types):
    def __init__(self, Instruction):
        super().__init__(Instruction)
        

class TypeI(Types):
    def __init__(self, Instruction):
        super().__init__(Instruction)


class TypeS(Types):
    def __init__(self, Instruction):
        super().__init__(Instruction)

class TypeB(Types):
    def __init__(self, Instruction):
        super().__init__(Instruction)

class TypeJ(Types):
    def __init__(self, Instruction):
        super().__init__(Instruction)

class TypeU(Types):
    def __init__(self, Instruction):
        super().__init__(Instruction)
