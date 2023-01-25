#pragma once
#ifdef GYRO_DLL_EXPORTS
	#define MYDLL __declspec(dllexport)
#else
	#define MYDLL __declspec(dllimport)
#endif

MYDLL void open_port(unsigned long ulComNo, unsigned long ulBaudrate, int cResult);
MYDLL float* get_gValue(int ulComNo);
//MYDLL struct gVal get_gValue(int ulComNo);
