#include <iostream>
#include <string>
#include "PythonInteract.h"
#include "main.h"
#include "Emulator.h"
#include "Generals.h"




int main(int argc, char *argv[])
{
	if (argc < 2) {
		printf("Usage: Emulator.exe <vmcode> <outputfile>");
		return 0;
	}
	
	auto emulator = new Emulator(std::string(argv[1]), std::string(argv[2]));
	// emulator->StartEmulation(5);

	pyInteract->RunMainFunction(emulator);
	
	system("pause");
	return 0;
}