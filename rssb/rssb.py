import struct
import sys

code_path = "export.dmp"
code = bytearray()
executed_code = {}

def print_bytearray(ba, size, offset = 0):
	result = ""
	for i in range(0,size,0x10):
		hex_stream = " ".join(["%02X" % x for x in ba[i:i+size%0x10]])
		text_stream = "".join([chr(x) for x in ba[i:i+size%0x10]])
		for x in range(0x20):
			text_stream = text_stream.replace(chr(x), ".")
		for x in range(0x80,0x100):
			text_stream = text_stream.replace(chr(x), ".")
		result += "%08X: %s %s" % (i + offset,hex_stream,text_stream)
	return result
		
def GetWord(idx):
	global code
	# print ("idx: %04X" % idx)
	return struct.unpack("h",code[idx*2:idx*2+2])[0]
	
def SetWord(idx, data):
	global code
	code[idx*2:idx*2+2] =  struct.pack("H", data & 0xffff)

def ExecAnInstruction():
	global executed_code
	
	eip = GetWord(0)
	# Compute new value for accumulator
	if GetWord(eip) == -1:
		if eip not in executed_code.keys():
			executed_code[eip] = "variable"
		SetWord(0, eip+1)
		return
	acc = GetWord(GetWord(eip)) - GetWord(1)
	
	result = "%04X: RSSB %04X(%04X) \t acc: %04X " % (eip , GetWord(eip), GetWord(GetWord(eip)) & 0xffff , acc)
	
	# Update accumulator
	SetWord(1, acc)
	
	# Update source if it was not second word
	if GetWord(eip) != 2:
		SetWord(GetWord(eip), acc)
	
	if eip not in executed_code.keys():
		executed_code[eip] = result + print_bytearray(code,14)
	# Update eip
	eip = GetWord(0)
	if acc < 0:
		SetWord(0, eip+2)
	else:
		SetWord(0, eip+1)
	
	return result

def ChangePassword(password):
	global code
	offset = 0x10e
	i=0
	for c in password:
		SetWord(offset+i, ord(c))
		i += 1
	while i<0x40:
		SetWord(offset+i, 0)
		i += 1
	
	with open("tmp.dmp", "wb") as file:
		file.write(code)
		
def HandleOutPut():
	global code
	if GetWord(6) != 0:
		SetWord(4, 0)
		SetWord(6, 0)
def execute():
	global code
	global executed_code
	
	i = 0;
	while (GetWord(0) < 0x25b7):
		result = ExecAnInstruction()
		print("%05X: %s %s" % (i,result, print_bytearray(code,14)))
		HandleOutPut()
		i += 1
	#for k,v in executed_code.items():
	#	print("%04X: %s" % (k,v))

if __name__ == "__main__":
	with open(code_path, "rb") as file:
		code = bytearray(file.read())
	if len(sys.argv) > 1:
		ChangePassword(sys.argv[1])
	execute()

