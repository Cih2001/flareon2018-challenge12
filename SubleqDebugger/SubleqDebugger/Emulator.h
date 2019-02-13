#pragma once

#include <fstream>
#include <sstream>
#include <string>

class Emulator
{
	std::string _InputFileName;
	std::string _OutputFileName;

	bool _initialized = false;
	short* data = nullptr;
	int data_size = 0;
	std::ostringstream _StringStream;

	unsigned int execute_instruction(unsigned short eip, bool debug, bool auto_eip, bool write_back, bool& jmp_found);
	void flush_output_stream();
	void clean_vm_registers(bool output = false);

	int _eip = 5;
	int _last_eip = 0;

public:

	Emulator(std::string InputFileName, std::string OutputFileName);
	~Emulator();

	std::string GetInputFileName() { return _InputFileName; }
	std::string GetOutputFileName() { return _OutputFileName; }

	unsigned int ExecInstruction(unsigned short eip, bool debug , bool& jmp_found);
	unsigned int TraceInstruction(unsigned short eip, bool debug, bool& jmp_found);

	void StartEmulation(bool debug = false);
	void TraceBlock(bool debug = false);
	void RunTo(int eip, bool debug = false);

	unsigned char * GetMemory() { return (unsigned char *)data; }
	int GetEip() { return _eip; }
	int GetLastEip() { return _last_eip; }
};

