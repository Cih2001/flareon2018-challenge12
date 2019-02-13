import emulator
import translate
import instructions
import struct
import os
import time

# Extended functions in emulator module:
# 
# emulator.StartEmulation(eip, debug)
#
#
debug = True  
logfile = "C:/hamid/log.txt"
inc_file = "C:/hamid/vm/include/2dad.inc"
dump_path = "C:/hamid/"
last_eip = 5

def print_bytearray(ba, size, offset = 0):
	for i in range(0,size,0x10):
		hex_stream = " ".join(["%02X" % x for x in ba[i:i+0x10]])
		text_stream = "".join([chr(x) for x in ba[i:i+0x10]])
		for x in range(0x20):
			text_stream = text_stream.replace(chr(x), ".")
		for x in range(0x80,0xff):
			text_stream = text_stream.replace(chr(x), ".")
		print ("%08X: %s %s" % (i + offset,hex_stream,text_stream))


# this function is called from SubleqDebugger.
def input_yes_no_cancel(eip):
	global debug
	global logfile
	global last_eip

	result = 1

	mem = emulator.ReadMemory()
	ba = bytearray(mem)

	if debug:
		with open(logfile, "a+") as file:
			file.write("\n")
			region = ba[last_eip*2: (eip+3)*2]
			file.write(instructions.DecodeInstructions(region))

	reg1 = struct.unpack("H",ba[eip*2: eip*2+2])[0]
	reg2 = struct.unpack("H",ba[eip*2+2: eip*2+4])[0]

	if reg1 == 0 and reg2 == 0:
		# unconditional jump
		result = 1
	else:
		decided = False;
		while not decided:
			print (translate.DecodeInstructionFull(ba,eip))
			print ("Do you want to jump: [Y/n/c]: ", end="")
	
			cmd = input().upper()
			if cmd == "N":
				result = 0
				decided = True
			elif cmd == "C":
				result = -1
				decided = True
			elif cmd.startswith("M"):
				offset = int(cmd.split(" ")[1],16)
				print_bytearray(ba[offset*2:offset*2+0x20], 0x20, offset*2)
			else:
				result = 1
				decided = True

	last_eip = eip + 3 if result == 0 else struct.unpack("H",ba[eip*2 + 4: eip*2+6])[0]
	return result


def TraceBlock(debug, conditional_stop):
	global logfile
	global last_eip
	while (True):
		emulator.TraceBlock(debug)

		mem = emulator.ReadMemory()
		ba = bytearray(mem)
		eip = emulator.ReadEip();
		emulator_last_eip = emulator.ReadLastEip();

		if debug:
			with open(logfile, "a+") as file:
				file.write("\n")
				# file.write("current eip: [%04X]\n" % eip)
				# file.write("last eip: [%04X]\n" % last_eip)
				# file.write("emulator last eip: [%04X]\n\n" % emulator_last_eip)
				region = ba[last_eip*2: (emulator_last_eip+3)*2]
				file.write(instructions.DecodeInstructions(region))

		last_eip = eip

		if not conditional_stop:
			break

		reg1 = struct.unpack("H",ba[emulator_last_eip*2: emulator_last_eip*2+2])[0]
		reg2 = struct.unpack("H",ba[emulator_last_eip*2+2: emulator_last_eip*2+4])[0]
		if reg1 != 0 or reg2 != 0:
			break

def Export2DAD():
	global inc_file
	if os.path.exists(inc_file):
		os.remove(inc_file)

	mem = emulator.ReadMemory()
	ba = bytearray(mem)

	with open(inc_file, "a+") as file:
		file.write("%ifndef __2DAD_INC__\n")
		file.write("%define __2DAD_INC__\n\n")
		file.write("%macro  TODAD 0\n")
		for i in range(0,len(ba),0x10):
			hex_stream = " ,".join(["0x%02X" % x for x in ba[i:i+0x10]])
			file.write("\t db %s\n" % hex_stream)
		file.write("%endmacro\n\n")
		file.write("%endif\n")
		
# this function is called from SubleqDebugger.
# it's the entry point of the program.
def main():  
	global debug
	global logfile
	global last_eip
	global dump_path

	menu = """Command list:
[0] Exit
[1] Reload Emulator
[2] Start Simulation
[3] Trace Block (Trace till next unconditional jump)
[4] Trace Block Cond.(Trace till next conditional jump)
[5] Run To <eip>

[D] Toggle Debug mode
[M] Read Memory
[C] Clean Log File
[T] Translate memory (T <offset> [<size>]
[E] Export 2DAD include file"""
	print (menu)
	cmd_list = []
	while (True):
		if len(cmd_list) == 0:
			print (":", end="")
			cmd_list = input().upper().split(";")
		cmd = cmd_list[0].strip()
		cmd_list = cmd_list[1:]
		if cmd == "0":
			return
		elif cmd == "1":
			emulator.ReloadEmulator()
			last_eip = 5
		elif cmd == "2":
			emulator.StartEmulation(debug)
		elif cmd == "3":
			TraceBlock(debug, False);
		elif cmd == "4":
			TraceBlock(debug, True);
		elif cmd == "E":
			Export2DAD()
		elif cmd.startswith("5"):
			offset = int(cmd.split(" ")[1],16)
			last_eip = offset;
			emulator.RunTo(offset, False);
		elif cmd == "C":
			if os.path.exists(logfile):
				os.remove(logfile)
		elif cmd == "D":
			debug = not debug
			print("Debug mode is: ", debug)
		elif cmd.startswith("M"):
			mem = emulator.ReadMemory()
			ba = bytearray(mem)
			if cmd == "MD":
				timestr = time.strftime("%Y%m%d-%H%M%S")
				with open(dump_path + timestr + ".dmp", "wb") as file:
					file.write(ba)
			elif " " in cmd:
				offset = int(cmd.split(" ")[1],16)
				if len(cmd.split(" ")) == 2:
					print_bytearray(ba[offset*2:offset*2+0x20], 0x20, offset*2)
				elif len(cmd.split(" ")) == 3:
					size = int(cmd.split(" ")[2],16)
					print_bytearray(ba[offset*2:offset*2+size], size, offset*2)
		elif cmd.startswith("T"):
			mem = emulator.ReadMemory()
			ba = bytearray(mem)
			if " " in cmd:
				offset = int(cmd.split(" ")[1],16)
				size = len(ba[offset:])
				if len(cmd.split(" ")) == 3:
					size = int(cmd.split(" ")[2],16)
				with open(logfile, "a+") as file:
					file.write("Translation of %X to %X:\n" %(offset, offset+size))
					region = ba[offset:offset+size]
					file.write(instructions.TranslateRegion(region))