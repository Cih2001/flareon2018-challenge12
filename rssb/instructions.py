import re
import struct
import operator

class InstructionUnknown:
	pattern = "^(....)"
	num_words = 1
	priority = -1

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s" % (hex_stream[0])
		return "Unknown %s" % (arg1)

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionUnknown.pattern, text)
		if m == None:
			return 0
		return InstructionUnknown.num_words*5

class InstructionCLR:
	pattern = "^0001"
	num_words = 1
	priority = 0

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		return ""

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionCLR.pattern, text)
		if m == None:
			return 0
		return InstructionCLR.num_words*5
		
class InstructionDefVar:
	pattern = "^0001 (....) 0002 0002 0000 0002 (....)"
	num_words = 7
	priority = 1

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		hex_stream = self.data.split(" ")
		
		arg1 = int(hex_stream[1],16) + 1
		arg2 = hex_stream[6]
		return "VAR %04X = %s" % (arg1, arg2)

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionDefVar.pattern, text)
		if m == None:
			return 0
		return InstructionDefVar.num_words*5

class InstructionNegIfPositive:
	pattern = "^0001 (....) 0002 0002 0002 (....) 0001 0001"
	num_words = 7
	priority = 1

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = hex_stream[1]
		return "MOV %s, -%s IF (%s) > 0 ELSE 0" % (arg1, arg1, arg1)

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionNegIfPositive.pattern, text)
		if m == None:
			return 0
		if m.group(1) != m.group(2):
			return 0
		return InstructionNegIfPositive.num_words*5
		
class InstructionSUB:
	pattern = "^0001 (....) FFFF 0002 FFFF 0002 FFFF (....) FFFF"
	num_words = 9
	priority = 3

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s" % (hex_stream[1])
		arg2 = "%s" % (hex_stream[7])
		return "SUB %s, %s" % (arg2, arg1)

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionSUB.pattern, text)
		if m == None:
			return 0
		return InstructionSUB.num_words*5

class InstructionMOV:
	pattern = "^0001 (....) FFFF 0002 FFFF 0002 FFFF (....) FFFF 0001 (....) 0002 0002 (....) 0001"
	num_words = 14
	priority = 4

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s" % (hex_stream[1])
		arg2 = "%s" % (hex_stream[10])
		return "MOV %s, %s" % (arg1, arg2)

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionMOV.pattern, text)
		if m == None:
			return 0
		if m.group(1) != m.group(2) or m.group(1) != m.group(4):
			return 0
		return InstructionMOV.num_words*5

class InstructionINDDESMOV:
	pattern = "^0001 (....) FFFF 0002 FFFF 0002 FFFF (....) FFFF 0001 (....) 0002 0002 (....) 0001 0001 (....) 0002 0002 (....) 0001"
	
	num_words = 20
	priority = 5

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s" % (hex_stream[10])
		arg2 = "%s" % (hex_stream[16])
		return "IMOV [%s], %s" % (arg1, arg2)

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionINDDESMOV.pattern, text)
		if m == None:
			return 0
		if m.group(1) != m.group(2) or m.group(1) != m.group(4):
			return 0
		# print ("%04X --- %04X\n" % (int(m.group(1),16), offset + 19))
		if int(m.group(1),16) != offset + 19:
			return 0
		return InstructionINDDESMOV.num_words*5

class InstructionINDSRCMOV:
	pattern = "^0001 (....) FFFF 0002 FFFF 0002 FFFF (....) FFFF 0001 (....) 0002 0002 (....) 0001 0001 (....) 0002 0002 (....) 0001"
	#attern = "^0001 (0CF5) FFFF 0002 FFFF 0002 FFFF (0CF5) FFFF 0001 (0B5C) 0002 0002 (0CF5) 0001 0001 (0B5C) 0002 0002 (0B39)"
	num_words = 20
	priority = 5

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s" % (hex_stream[10])
		arg2 = "%s" % (hex_stream[19])
		return "IMOV %s, [%s]" % (arg2, arg1)

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionINDSRCMOV.pattern, text)
		if m == None:
			return 0
		if m.group(1) != m.group(2) or m.group(1) != m.group(4):
			return 0
		if m.group(3) != m.group(5):
			return 0
		# print ("%04X --- %04X\n" % (int(m.group(1),16), offset + 19))
		if int(m.group(1),16) != offset + 16:
			return 0
		return InstructionINDSRCMOV.num_words*5
		
class InstructionADD:
	pattern = "^0001 (....) 0002 0002 (....) 0001"
	num_words = 5
	priority = 2

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		hex_stream = self.data.split(" ")
		src = hex_stream[1]
		des = hex_stream[4]
		result = "ADD %s, %s" % (des, src)
		if des == "0000":
			result = "ADD eip, %s" % (src)
		return result

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionADD.pattern, text)
		if m == None:
			return 0
		if m.group(1) == m.group(2):
			return 0
		return InstructionADD.num_words*5

class InstructionJMP:
	pattern = "^(....) 0002 0002 0000 (....)"
	num_words = 5
	priority = 1

	def __init__(self, _data, num_dw, offset):
		self.offset = offset
		self.num_words = num_dw
		self.data = _data
	def Text(self):
		hex_stream = self.data.split(" ")
		src = hex_stream[1]
		des = hex_stream[4]
		return "JMP eip + %s" % (des)

	@staticmethod
	def Match(text, offset = 0):
		m = re.match(InstructionJMP.pattern, text)
		if m == None:
			return 0
		if m.group(1) == m.group(2):
			return 0
		return InstructionJMP.num_words*5	
		
classes = dict([(cls, cls.priority) for name, cls in globals().items() if name.startswith("Instruction")])

def FindInstruction(inst_text):
	global classes

	inst_list = []
	offset = 0x15b
	while (len(inst_text) >= 5):
		match = False
		for cls, priority in sorted(classes.items(), key=lambda kv: kv[1],reverse=True):
			num_bytes = cls.Match(inst_text, offset)
			if num_bytes > 0:
				new_class = cls(inst_text[:num_bytes],cls.num_words, offset)
				inst_list.append(new_class)
				inst_text = inst_text[num_bytes:]
				match = True
				offset += new_class.num_words
				break
		if not match :
			# should not happen
			inst_text = inst_text[5:]

	return inst_list

def DecodeInstructions(ba):
	result = ""
	inst_text = ""
	for i in range(len(ba)>>1): 
		inst_text += "%04X " % struct.unpack("H",ba[i*2:i*2+2])[0]
	inst_text += " " # it is needed.

	inst_list = FindInstruction(inst_text)
	for ins in inst_list:
		result += "%04X: " % ins.offset
		result += "%-40s" % ins.Text()
		result += " %s\n" % ins.data
	result += "\n"

	return result

	

if __name__ == "__main__":
	code_path = "export.dmp"
	code = bytearray()
	with open(code_path, "rb") as file:
		code = bytearray(file.read())
		print (DecodeInstructions(code[0x15b*2:]))