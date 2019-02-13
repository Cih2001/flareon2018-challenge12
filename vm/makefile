
PE := vm
DIR_BUILD := .

all:
	nasm -fwin32 -F cv8 -o $(DIR_BUILD)\$(PE).obj $(PE).asm
	link /subsystem:console,5.1 /entry:main /section:.text,RWE /section:.data,RWE /SAFESEH:NO /version:5.1 /out:$(DIR_BUILD)\$(PE).exe $(DIR_BUILD)\$(PE).obj kernel32.lib
	