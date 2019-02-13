#pragma once
#include <string>
#include <Python.h>
#include "Generals.h"

class Emulator;

class PythonInteract
{
private:
	std::string _ModuleName;
	PyObject *pName = nullptr;
	PyObject *pModule = nullptr;

	bool _initialized = false;
	
public:
	Emulator * _emulator = nullptr;

	PythonInteract(Emulator* emulator, std::string ModuleName);
	~PythonInteract();

	static void RunMainFunction(Emulator* emulator);
	static int RunYesNoCancelInput(unsigned int eip);

	static PyObject* emulator_start_emulation(PyObject *self, PyObject *args);
	static PyObject* emulator_trace_block(PyObject *self, PyObject *args);
	static PyObject* emulator_reload(PyObject *self, PyObject *args);
	static PyObject* emulator_read_memory(PyObject *self, PyObject *args);
	static PyObject* emulator_read_eip(PyObject *self, PyObject *args);
	static PyObject* emulator_read_last_eip(PyObject *self, PyObject *args);
	static PyObject* emulator_run_to(PyObject *self, PyObject *args);
};


static PyMethodDef EmbMethods[] = {
	{ "StartEmulation", PythonInteract::emulator_start_emulation, METH_VARARGS, "Starts the emulation" },
	{ "ReloadEmulator", PythonInteract::emulator_reload, METH_VARARGS, "reloads the emulator" },
	{ "TraceBlock", PythonInteract::emulator_trace_block, METH_VARARGS, "traces a block" },
	{ "ReadMemory", PythonInteract::emulator_read_memory, METH_VARARGS, "starts the translation process" },
	{ "ReadEip", PythonInteract::emulator_read_eip, METH_VARARGS, "Gets the current eip" },
	{ "ReadLastEip", PythonInteract::emulator_read_last_eip, METH_VARARGS, "Gets the previous eip" },
	{ "RunTo", PythonInteract::emulator_run_to, METH_VARARGS, "Run vm to reach a eip" },
	{ NULL, NULL, 0, NULL }
};

static PyModuleDef EmbModule = {
	PyModuleDef_HEAD_INIT, "emulator", NULL, -1, EmbMethods, NULL, NULL, NULL, NULL
};

static PyObject* PyInit_emb(void)
{
	return PyModule_Create(&EmbModule);
}



