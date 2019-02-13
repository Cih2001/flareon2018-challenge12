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


if __name__ == "__main__":
	with open(code_path, "rb") as file:
		code = bytearray(file.read())
	if len(sys.argv) > 1:
		print ("%04X" % GetWord(int(sys.argv[1],16)))

