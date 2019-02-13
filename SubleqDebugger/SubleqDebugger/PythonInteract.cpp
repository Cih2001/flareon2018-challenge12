#include "PythonInteract.h"
#include "Emulator.h"


#define emu pyInteract->_emulator

PyObject* PythonInteract::emulator_start_emulation(PyObject *self, PyObject *args)
{
	bool debug = false;
	if (!PyArg_ParseTuple(args, "b",  &debug))
		return NULL;

	emu->StartEmulation(debug);
	return PyLong_FromLong(1);
}

PyObject * PythonInteract::emulator_trace_block(PyObject * self, PyObject * args)
{
	bool debug = false;
	if (!PyArg_ParseTuple(args, "|b", &debug))
		return NULL;

	emu->TraceBlock(debug);
	
	return PyLong_FromLong(1);
}

PyObject * PythonInteract::emulator_reload(PyObject * self, PyObject * args)
{
	auto input_file_name = emu->GetInputFileName();
	auto output_file_name = emu->GetOutputFileName();

	delete emu;

	emu = new Emulator(
		input_file_name,
		output_file_name
	);
	
	return PyLong_FromLong(1);
}

PyObject * PythonInteract::emulator_read_memory(PyObject * self, PyObject * args)
{
	auto Buffer = PyBytes_FromStringAndSize((char *)emu->GetMemory(), 0x2dad * 2);
	if (Buffer == NULL) {
		PyErr_Print();
		throw std::exception("FATAL ERROR");
	}

	return Buffer;
}

PyObject * PythonInteract::emulator_read_eip(PyObject * self, PyObject * args)
{
	return PyLong_FromLong(emu->GetEip());
}

PyObject * PythonInteract::emulator_read_last_eip(PyObject * self, PyObject * args)
{
	return PyLong_FromLong(emu->GetLastEip());
}

PyObject * PythonInteract::emulator_run_to(PyObject * self, PyObject * args)
{
	int eip = 5;
	bool debug = false;
	if (!PyArg_ParseTuple(args, "i|b", &eip, &debug))
		return NULL;

	emu->RunTo(eip, debug);

	return PyLong_FromLong(1);
}


PythonInteract::PythonInteract(Emulator* emulator, std::string ModuleName) :
	_ModuleName(ModuleName),
	_emulator(emulator)
{
	PyImport_AppendInittab("emulator", &PyInit_emb);

	Py_Initialize();
	pName = PyUnicode_DecodeFSDefault(ModuleName.c_str());

	/* Error checking of pName left out */

	pModule = PyImport_Import(pName);
	Py_DECREF(pName);

	if (pModule == NULL) {
		PyErr_Print();
		printf("Failed to load \"%s\"\n", ModuleName.c_str());
		throw std::exception("Error loading python file.");
	}

	_initialized = true;
}

PythonInteract::~PythonInteract()
{
	Py_DECREF(pModule);
}

void PythonInteract::RunMainFunction(Emulator* emulator)
{
	
	pyInteract = new PythonInteract(emulator, std::string("debugger"));
	PyObject *pFunc, *pValue;

	pFunc = PyObject_GetAttrString(pyInteract->pModule, "main");
	/* pFunc is a new reference */

	if (pFunc && PyCallable_Check(pFunc)) {
		pValue = PyObject_CallObject(pFunc, nullptr);
		Py_DECREF(pValue);
		Py_DECREF(pFunc);
	}
}

int PythonInteract::RunYesNoCancelInput(unsigned int eip)
{
	int result = 1;
	PyObject *pFunc, *pArgs, *pValue;

	pFunc = PyObject_GetAttrString(pyInteract->pModule, "input_yes_no_cancel");
	/* pFunc is a new reference */

	pArgs = PyTuple_New(1);
	pValue = PyLong_FromLong(eip);
	if (!pValue) {
		throw std::exception("Cannot convert argument.");
	}
	PyTuple_SetItem(pArgs, 0, pValue);

	if (pFunc && PyCallable_Check(pFunc)) {
		pValue = PyObject_CallObject(pFunc, pArgs);

		if (pValue != NULL) {
			result = PyLong_AsLong(pValue);
		}
		else {
			PyErr_Print();
			throw std::exception("Call failed.\n");
		}
		
	}
	Py_DECREF(pValue);
	Py_DECREF(pFunc);
	return result;
}
