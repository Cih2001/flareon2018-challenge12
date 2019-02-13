import re
import struct
import operator

class InstructionUnknown:
	num_bytes = 6
	priority = -1

	def __init__(self, _data):
		self.data = _data
		self.num_bytes = InstructionUnknown.num_bytes
	def Text(self):
		return "Unknown %s\n" % (self.data)
	def AsmText(self):
		return "dw %s\n" % (self.data)

	@staticmethod
	def Match(text):
		return True

class InstructionClear:
	pattern = "^(.. ..) (.. ..) 00 00"
	num_bytes = 6
	priority = 0

	def __init__(self, _data):
		self.data = _data
		self.num_bytes = InstructionClear.num_bytes
	def Text(self):
		hex_stream = self.data.strip().replace(" ","")
		arg = "%s%s" % (hex_stream[2:4], hex_stream[0:2])
		return "xor %s, %s\n" % (arg,arg)
	def AsmText(self):
		hex_stream = self.data.strip().replace(" ","")
		arg = "%s%s" % (hex_stream[2:4], hex_stream[0:2])
		return "XOR lbl_%s, lbl_%s\n" % (arg,arg)

	@staticmethod
	def Match(text):
		m = re.match(InstructionClear.pattern, text)
		if m == None:
			return False
		if m.group(1) != m.group(2):
			return False
		return True

class InstructionMightAdd:
	pattern = "^(.. ..) 00 00 00 00 00 00 (.. ..) 00 00"
	num_bytes = 6 * 2
	priority = 1

	def __init__(self, _data):
		self.data = _data
		self.num_bytes = InstructionMightAdd.num_bytes
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[1], hex_stream[0])
		arg2 = "%s%s" % (hex_stream[9], hex_stream[8])
		return "madd %s, %s\n" % (arg2,arg1)
	def AsmText(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[1], hex_stream[0])
		arg2 = "%s%s" % (hex_stream[9], hex_stream[8])
		return "MADD lbl_%s, lbl_%s\n" % (arg2,arg1)

	@staticmethod
	def Match(text):
		m = re.match(InstructionMightAdd.pattern, text)
		if m == None:
			return False
		if m.group(1) == m.group(2):
			return False
		return True

class InstructionMov:
	pattern = "^00 00 00 00 00 00 (.. ..) (.. ..) 00 00 (.. ..) 00 00 00 00 00 00 (.. ..) 00 00"
	num_bytes = 6 * 4
	priority = 3

	def __init__(self, _data):
		self.data = _data
		self.num_bytes = InstructionMov.num_bytes
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[7], hex_stream[6])
		arg2 = "%s%s" % (hex_stream[13], hex_stream[12])
		return "mov %s, %s\n" % (arg1,arg2)
	def AsmText(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[7], hex_stream[6])
		arg2 = "%s%s" % (hex_stream[13], hex_stream[12])
		return "MOV lbl_%s, lbl_%s\n" % (arg1,arg2)

	@staticmethod
	def Match(text):
		m = re.match(InstructionMov.pattern, text)
		if m == None:
			return False
		if m.group(1) != m.group(2) or m.group(1) != m.group(4):
			return False
		return True

class InstructionMightMov:
	pattern = "^(.. ..) (.. ..) 00 00 (.. ..) 00 00 00 00 00 00 (.. ..) 00 00"
	num_bytes = 6 * 3
	priority = 2
	def __init__(self, _data):
		self.data = _data
		self.num_bytes = InstructionMightMov.num_bytes
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[1], hex_stream[0])
		arg2 = "%s%s" % (hex_stream[7], hex_stream[6])
		return "mmov %s, %s\n" % (arg1,arg2)
	def AsmText(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[1], hex_stream[0])
		arg2 = "%s%s" % (hex_stream[7], hex_stream[6])
		return "MMOV lbl_%s, lbl_%s\n" % (arg1,arg2)

	@staticmethod
	def Match(text):
		m = re.match(InstructionMightMov.pattern, text)
		if m == None:
			return False
		if m.group(1) != m.group(2) or m.group(1) != m.group(4):
			return False
		return True

class InstructionAdd2:
	pattern = "^(.. ..) (.. ..) 00 00 " +  "(.. ..) 00 00 00 00 " + "00 00 (.. ..) 00 00 " + "00 00 00 00 00 00 " + "(.. ..) 00 00 00 00 " + "00 00 (.. ..) 00 00"

	num_bytes = 6 * 6
	priority = 3
	def __init__(self, _data):
		self.data = _data
		self.num_bytes = InstructionAdd2.num_bytes
	def Text(self):
		hex_stream = self.data.split(" ")
		res = "%s%s" % (hex_stream[1], hex_stream[0])
		arg1 = "%s%s" % (hex_stream[25], hex_stream[24])
		arg2 = "%s%s" % (hex_stream[7], hex_stream[6])
		return "add %s, %s + %s\n" % (res, arg1, arg2)
	def AsmText(self):
		hex_stream = self.data.split(" ")
		res = "%s%s" % (hex_stream[1], hex_stream[0])
		arg1 = "%s%s" % (hex_stream[25], hex_stream[24])
		arg2 = "%s%s" % (hex_stream[7], hex_stream[6])
		return "ADD lbl_%s, lbl_%s + lbl_%s\n" % (res, arg1, arg2)

	@staticmethod
	def Match(text):
		m = re.match(InstructionAdd2.pattern, text)
		if m == None:
			return False
		if m.group(1) != m.group(2) or m.group(1) != m.group(4) or m.group(1) != m.group(6):
			return False
		return True

class InstructionJmp:
	pattern = "^00 00 00 00 (.. ..)"
	num_bytes = 6
	priority = 3
	def __init__(self, _data):
		self.data = _data
		self.num_bytes = InstructionJmp.num_bytes
	def Text(self):
		hex_stream = self.data.strip().replace(" ","")
		return "jmp %s%s\n" % (hex_stream[10:12], hex_stream[8:10])
	def AsmText(self):
		hex_stream = self.data.strip().replace(" ","")
		return "JMP lbl_%s%s\n" % (hex_stream[10:12], hex_stream[8:10])

	@staticmethod
	def Match(text):
		m = re.match(InstructionJmp.pattern, text)
		if m == None:
			return False
		if m.group(1) == "00 00":
			return False
		return True

class InstructionCmpZJz:
	pattern = "^00 00 00 00 00 00 00 00 (.. ..) (.. ..)"
	num_bytes = 6 * 2
	priority = 3
	def __init__(self, _data):
		self.data = _data
		self.num_bytes = InstructionCmpZJz.num_bytes
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[9], hex_stream[8])
		des = "%s%s" % (hex_stream[11], hex_stream[10])
		return "cmp %s, 0; jz %s\n" % (arg1,des)
	def AsmText(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[9], hex_stream[8])
		des = "%s%s" % (hex_stream[11], hex_stream[10])
		return "CMP lbl_%s, 0; JZ lbl_%s\n" % (arg1,des)

	@staticmethod
	def Match(text):
		m = re.match(InstructionCmpZJz.pattern, text)
		if m == None:
			return False
		if m.group(1) == "00 00" or m.group(2) == "00 00":
			return False
		return True

class InstructionSubJA:
	pattern = "^00 00 00 00 00 00 (.. ..) (.. ..) 00 00 (.. ..) 00 00 (.. ..)"
	num_bytes = 6 * 3
	priority = 3
	def __init__(self, _data):
		self.data = _data
		self.num_bytes = InstructionSubJA.num_bytes
	def Text(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[7], hex_stream[6])
		arg2 = "%s%s" % (hex_stream[9], hex_stream[8])
		des = "%s%s" % (hex_stream[17], hex_stream[16])
		return "sub %s, %s; ja %s\n" % (arg2,arg1,des)
	def AsmText(self):
		hex_stream = self.data.split(" ")
		arg1 = "%s%s" % (hex_stream[7], hex_stream[6])
		arg2 = "%s%s" % (hex_stream[9], hex_stream[8])
		des = "%s%s" % (hex_stream[17], hex_stream[16])
		return "SUB lbl_%s, lbl_%s; JA lbl_%s\n" % (arg2,arg1,des)

	@staticmethod
	def Match(text):
		m = re.match(InstructionSubJA.pattern, text)
		if m == None:
			return False
		if m.group(4) == "00 00":
			return False
		if m.group(2) != m.group(3):
			return False
		return True

# defined_instructions = {}
# for key, value in classes.items():
# 	defined_instructions[key[-2:]] = value()

class NotInstruction:
	num_bytes = 2
	def __init__(self, _data):
		self.data = _data
		self.num_bytes = NotInstruction.num_bytes
	def Text(self):
		return "Unknown %s\n" % (self.data)
	def AsmText(self):
		byts = self.data.split(" ")
		return "db %s, %s\n" % (byts[0], byts[1])



all_inst_classes = dict([(cls, cls.priority) for name, cls in globals().items() if name.startswith("Instruction")])
known_inst_classes = dict([(cls, cls.priority) for name, cls in globals().items() if (name.startswith("Instruction") and name != "InstructionUnknown")])

def FindInstructions(inst_text, skip_size = 18):
	global all_inst_classes
	global known_inst_classes
	classes = all_inst_classes
	if (skip_size != 18):
		classes = known_inst_classes

	inst_list = []
	while (len(inst_text) >= skip_size):
		match = False
		for cls, priority in sorted(classes.items(), key=lambda kv: kv[1],reverse=True):
			if cls.Match(inst_text):
				inst_list.append(cls(inst_text[:cls.num_bytes*3]))
				inst_text = inst_text[cls.num_bytes*3:]
				match = True
				break
		if not match :
			if (skip_size != 18):
				inst_list.append(NotInstruction(inst_text[:NotInstruction.num_bytes*3]))
			inst_text = inst_text[skip_size:]

	return inst_list

def DecodeInstructions(ba):
	result = ""
	inst_text = " ".join(["%02X" % x for x in ba])
	inst_text += " " # it is needed.

	inst_list = FindInstructions(inst_text)
	for ins in inst_list:
		result += ins.Text()
	result += "\n"

	return result

def TranslateRegion(ba, offset = 0xa):
	result = ""
	inst_text = " ".join(["%02X" % x for x in ba])
	inst_text += " " # it is needed.

	inst_list = FindInstructions(inst_text,6)
	for ins in inst_list:
		result += "lbl_%04X-" % (offset >> 1)
		offset += ins.num_bytes
		result += "%04X: " % (offset >> 1)
		result += ins.AsmText()
		
	result += "\n"

	return result