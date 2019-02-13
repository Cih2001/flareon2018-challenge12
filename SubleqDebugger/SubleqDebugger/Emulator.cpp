#include "Emulator.h"
#include "PythonInteract.h"


void sprint_hexstream(std::ostringstream& str, unsigned char * offset, unsigned int size) {
	char line[0x40];
	for (unsigned int index = 0; index < size; index++)
	{
		sprintf_s(line, 0x40, "%02X ", offset[index]);
		str << line;
	}

}

unsigned int Emulator::execute_instruction(unsigned short eip, bool debug, bool auto_eip, bool write_back, bool& jmp_found)
{
	jmp_found = false;

	char line[0x100];
	int str_idx = 0;

	unsigned int result = 0;

	auto idx1 = *(data + eip + 0);
	auto idx2 = *(data + eip + 1);
	auto next_eip = *(data + eip + 2);

	auto tmp1 = *(data + idx1);
	auto tmp2 = *(data + idx2);

	short sub = *(data + idx2) - *(data + idx1);
	if (write_back)
		*(data + idx2) = sub;

	/* Printing debug information */
	if (debug) {
		sprintf_s(line, "%04X(%04X): ", eip, eip * 2);
		_StringStream << line;

		sprint_hexstream(_StringStream, (unsigned char *)(data + eip), 0x6);

		sprintf_s(line, "subleq [%04X(%04X)], [%04X(%04X)] jmp %04X ", idx2, idx2 * 2, idx1, idx1 * 2, next_eip);
		_StringStream << line;

		sprintf_s(line, "%4X - %4X = %4X ", tmp2 & 0xffff, tmp1 & 0xffff, sub & 0xffff);
		_StringStream << line;
		sprintf_s(line, "Regs: ");

		_StringStream << line;
		sprint_hexstream(_StringStream, (unsigned char *)(data), 0xA);

		sprintf_s(line, "\n");
		_StringStream << line;
	}

	if (auto_eip) {
		if (next_eip == 0)
			result = eip + 3;
		else
		{
			jmp_found = true;
			if (sub > 0)
				result = eip + 3;
			else
				result = next_eip;
		}
	}
	else {
		throw std::exception("NOT IMPLEMENTED");
		if (next_eip != 0)
		{
			jmp_found = true;
			flush_output_stream();
			auto user_choice = PythonInteract::RunYesNoCancelInput(eip);
			if (user_choice == 1)
			{
				result = next_eip;
			}
			else if (user_choice == -1)
			{
				result = 0xffffffff;
			}
			else result = eip + 3;
		} else result = eip + 3;
	}
	


	return result;
}

void Emulator::flush_output_stream()
{
	if (_StringStream.str().length() == 0)
		return;
	std::ofstream _OutputFileStream;
	_OutputFileStream.open(_OutputFileName, std::ios_base::app);
	_OutputFileStream << _StringStream.str();
	_StringStream.str(std::string());
	_StringStream.clear();
	_OutputFileStream.close();
}

void Emulator::clean_vm_registers(bool output)
{
	auto p = (unsigned char *)data;
	if (*(p + 0x8) != 0)
	{
		if (output)
			printf("%c", *(p + 0x4));
		*(data + 2) = 0;
		*(data + 4) = 0;
	}
}

Emulator::Emulator(std::string InputFileName, std::string OutputFileName) :
	_InputFileName(InputFileName) ,
	_OutputFileName(OutputFileName)
{
	std::ifstream in(_InputFileName, std::ifstream::ate | std::ifstream::binary);
	data_size = (int) in.tellg();
	in.close();
	if (data_size < 0)
		throw std::exception("Error opening vm file");

	auto buffer = new char[data_size];
	std::ifstream infile;
	infile.open(_InputFileName, std::ios::binary | std::ios::in);
	infile.read(buffer, data_size);
	infile.close();

	data = (short *)buffer;
	_initialized = true;
	return;
}

unsigned int Emulator::ExecInstruction(unsigned short eip, bool debug, bool& jmp_found) {
	return this->execute_instruction(eip, debug, true, true, jmp_found);
}

unsigned int Emulator::TraceInstruction(unsigned short eip, bool debug, bool& jmp_found)
{
	return this->execute_instruction(eip, debug, false, true, jmp_found);
}

void Emulator::StartEmulation(bool debug)
{
	int i = 0;
	while (_eip != 0xffffffff) {
		_last_eip = _eip;
		bool jmp_found = false;
		_eip = ExecInstruction(_eip, debug, jmp_found);
		clean_vm_registers(true);
		flush_output_stream();
	}
	
}

void Emulator::TraceBlock(bool debug)
{
	int i = 0;
	bool jmp_found = false;
	while (_eip != 0xffffffff && !jmp_found) {
		_last_eip = _eip;
		_eip = ExecInstruction(_eip, debug, jmp_found);
		clean_vm_registers(true);
		flush_output_stream();
	}
}

void Emulator::RunTo(int eip, bool debug)
{
	int i = 0;
	bool jmp_found = false;
	do {
		_last_eip = _eip;
		_eip = ExecInstruction(_eip, debug, jmp_found);
		clean_vm_registers(true);
		flush_output_stream();
	} while (_eip != eip);
}

Emulator::~Emulator()
{
	delete[] data;
}
