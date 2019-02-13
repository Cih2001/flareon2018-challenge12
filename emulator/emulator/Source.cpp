#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

unsigned short * data = nullptr;

std::ofstream* ofile = new std::ofstream;

unsigned short * open_file(const char * filename, const char * ofilename = nullptr) {
	std::ifstream in(filename, std::ifstream::ate | std::ifstream::binary);
	auto size = in.tellg();
	in.close();
	if (size < 0) return nullptr;

	auto buffer = new char[size];
	std::ifstream infile;
	infile.open(filename, std::ios::binary | std::ios::in);
	infile.read(buffer, size);

	infile.close();

	if (ofilename != nullptr) {
		ofile->open(ofilename, std::ios_base::app);
	}
	else {
		delete[] ofile;
		ofile = nullptr;
	}
	return (unsigned short*)buffer;
}


void sprint_hexstream(std::ostringstream& str, unsigned char * offset, unsigned int size) {
	char line[0x40];
	for (unsigned int index = 0; index < size; index++)
	{
		sprintf_s(line, 0x40, "%02X ", offset[index]);
		str << line;
	}
	
}

unsigned int ExecIntruction(int iteration, unsigned short eip, bool debug = false) {
	std::ostringstream stringStream;
	char line[0x100];


	int str_idx = 0;

	bool jmp = false;
	unsigned int result = 0;

	auto idx1 = *(data + eip + 0);
	auto idx2 = *(data + eip + 1);
	auto next_eip = *(data + eip + 2);

	auto tmp1 = *(data + idx1);
	auto tmp2 = *(data + idx2);

	short sub = *(data + idx2) - *(data + idx1);
	*(data + idx2) = sub;

	if (next_eip == 0 || sub > 0)
		result = eip + 3;
	else
	{
		jmp = true;
		result = next_eip;
	}

	
	/* Printing debug information */
	if (debug) {
		sprintf_s(line, "%08X: ", iteration);
		stringStream << line;

		sprintf_s(line, "%04X(%04X): ", eip, eip*2);
		stringStream << line;
		
		sprint_hexstream(stringStream, (unsigned char *)(data + eip), 0x6);
		
		if (jmp)
			sprintf_s(line, "subleq [%04X], [%04X] jmp %04X ", idx2, idx1, next_eip);
		else
			sprintf_s(line, "subleq [%04X], [%04X]          ", idx2, idx1);
		stringStream << line;
		
		sprintf_s(line, "%4X - %4X = %4X ", tmp2 , tmp1, sub & 0xffff);
		stringStream << line;
		sprintf_s(line, "Regs: ");
		
		stringStream << line;
		sprint_hexstream(stringStream, (unsigned char *)(data), 0xA);
		
		sprintf_s(line, "\n");
		stringStream << line;
		
		// std::cout << stringStream.str();
		
		if (ofile != nullptr)
			*(ofile) << stringStream.str();
	}
	
	
	return result;
}

void Emulate(unsigned int eip) {
	bool debug = true;
	int i = 0, iter = 0;
	while (eip != 0xffff) {
		eip = ExecIntruction(iter, eip, debug);
		
		auto p = (unsigned char *)data;
		if (*(p + 0x8) != 0)
		{
			i++;
			printf("%c", *(p + 0x4));
			*(data + 2) = 0;
			*(data + 4) = 0;
			//if (i == 145) debug = true;
			//else debug = false;

		}
		iter++;
		//if (i == 0x100) break;
	}
}


unsigned int TranslateIntruction(int iteration, unsigned short eip, bool debug = false, bool writeback = false) {
	std::ostringstream stringStream;
	char line[0x100];
	int str_idx = 0;

	bool jmp = false;
	unsigned int result = 0;

	auto idx1 = *(data + eip + 0);
	auto idx2 = *(data + eip + 1);
	auto next_eip = *(data + eip + 2);

	auto tmp1 = *(data + idx1);
	auto tmp2 = *(data + idx2);

	short sub = *(data + idx2) - *(data + idx1);

	if (writeback)
		*(data + idx2) = sub;


	/* Printing debug information */
	if (debug) {
		sprintf_s(line, "%08X: ", iteration);
		stringStream << line;

		sprintf_s(line, "%04X(%04X): ", eip, eip * 2);
		stringStream << line;

		sprint_hexstream(stringStream, (unsigned char *)(data + eip), 0x6);

		sprintf_s(line, "subleq [%04X(%04X)], [%04X(%04X)] jmp %04X ", idx2, idx2*2, idx1, idx1*2, next_eip);
		stringStream << line;

		sprintf_s(line, "%4X - %4X = %4X ", tmp2, tmp1, sub & 0xffff);
		stringStream << line;
		sprintf_s(line, "Regs: ");

		stringStream << line;
		sprint_hexstream(stringStream, (unsigned char *)(data), 0xA);

		sprintf_s(line, "\n");
		stringStream << line;

		std::cout << stringStream.str();

		if (ofile != nullptr)
			*(ofile) << stringStream.str();
	}

	if (next_eip == 0)
		result = eip + 3;
	else
	{
		if (!debug) std::cout << stringStream.str();

		printf("Do you want to jump? (Y/n):");

		char responce;
		std::cin >> responce;
		
		if (responce == 'n' || responce == 'N')
			result = eip + 3;
		else if (responce == 'c' || responce == 'C')
			result = -1;
		else
			result = next_eip;
	}

	return result;
}

void Translate(unsigned int start_eip) {
	bool debug = true;
	bool writeback = true;

	int i = 0;
	while (start_eip >= 0) {
		start_eip = TranslateIntruction(i, start_eip, debug, writeback);
		i++;
	}
}

int main(int argc, char** argv) {
	if (argc <= 2) {
		printf("Usage: Emulator.exe <cmd> <vmcode> <outputfile>");
		return 0;
	}
	data = open_file(argv[2], argv[3]);
	if (data == nullptr) {
		printf("Error opening file...");
		return 0;
	}

	if (argv[1][0] == '1')
		Emulate(5);
	else if (argv[1][0] == '2')
		Translate(5);

	system("pause");
	return 0;
}