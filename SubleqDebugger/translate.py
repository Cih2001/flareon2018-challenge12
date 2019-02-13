import struct

def DecodeInstruction(ba):
	result = ""

	reg1 = struct.unpack("H",ba[0:2])[0]
	reg2 = struct.unpack("H",ba[2:4])[0]
	jmp = struct.unpack("H",ba[4:6])[0]

	result = "subleq [%04X], [%04X], [%04X]" % (reg2,reg1, jmp)
	return result

def DecodeInstructionFull(ba, eip):
	
	result = "%04X: " % eip
	result += " ".join(["%02X" % x for x in ba[eip*2: eip*2+6]])
	result += " "
	result += DecodeInstruction(ba[eip*2: eip*2+6])

	return result