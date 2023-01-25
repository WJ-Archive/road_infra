#include "pch.h"
using namespace std;
unsigned char ucComNo[2] = { 0,0 };
int ComNo = 0;
int cnt = 0;
char chrBuffer[2000];
unsigned short usLength = 0, usCnt = 0;


extern "C" __declspec(dllexport) void open_port(unsigned long ulComNo, unsigned long ulBaudrate, int cResult) {
	printf("Waiting to open port%d...\r\n", ulComNo);
	while (cResult != 0){
		cResult = OpenCOMDevice(ulComNo, ulBaudrate);
	}
	printf("Done\n");
	ComNo = ulComNo;
}
extern "C" __declspec(dllexport) float get_gValue(int cResult, int cnt)
{

	//float gValue[12]; 
	float gValue;
	usLength = CollectUARTData(ComNo, chrBuffer);
	if (usLength > 0)
	{
		JY901.CopeSerialData(chrBuffer, usLength);
	}
	//Sleep(100);

	if (usCnt++ >= 0)
	{
		//printf("cnt = %d ", cnt);
		usCnt = 0;
		switch (cnt) {
			case 0:
				gValue = (float)JY901.stcGyro.w[0] / 32768 * 2000;
				return gValue;
				break;
			case 1:
				gValue = (float)JY901.stcGyro.w[1] / 32768 * 2000;
				return gValue;
				break;
			case 2:
				gValue = (float)JY901.stcGyro.w[2] / 32768 * 2000;
				return gValue;
				break;
			default:
				break;
		}
		
		//printf("Acceleration : %.3f %.3f %.3f\r\n", (float)JY901.stcAcc.a[0] / 32768 * 16, (float)JY901.stcAcc.a[1] / 32768 * 16, (float)JY901.stcAcc.a[2] / 32768 * 16);
		//gValue[0] = (float)JY901.stcAcc.a[1] / 32768 * 16;
		//gValue[1] = (float)JY901.stcAcc.a[1] / 32768 * 16;
		//gValue[2] = (float)JY901.stcAcc.a[2] / 32768 * 16;

		//printf("Gyro : %.3f %.3f %.3f\r\n", (float)JY901.stcGyro.w[0] / 32768 * 2000, (float)JY901.stcGyro.w[1] / 32768 * 2000, (float)JY901.stcGyro.w[2] / 32768 * 2000);
		//gValue[3] = (float)JY901.stcGyro.w[0] / 32768 * 2000;
		//gValue[4] = (float)JY901.stcGyro.w[1] / 32768 * 2000;
		//gValue[5] = (float)JY901.stcGyro.w[2] / 32768 * 2000;

		//printf("Attitude Angle : %.3f %.3f %.3f\r\n", (float)JY901.stcAngle.Angle[0] / 32768 * 180, (float)JY901.stcAngle.Angle[1] / 32768 * 180, (float)JY901.stcAngle.Angle[2] / 32768 * 180);
		//gValue[6] = (float)JY901.stcAngle.Angle[0] / 32768 * 180;
		//gValue[7] = (float)JY901.stcAngle.Angle[1] / 32768 * 180;
		//gValue[8] = (float)JY901.stcAngle.Angle[2] / 32768 * 180;

		//printf("Magnetic field : %d %d %d\r\n", JY901.stcMag.h[0], JY901.stcMag.h[1], JY901.stcMag.h[2]);
		//gValue[9] = JY901.stcMag.h[0];
		//gValue[10] = JY901.stcMag.h[1];
		//gValue[11] = JY901.stcMag.h[2];

		//printf("========================================================================================\n");

	}
}

/*
typedef struct gVal {
	float acc[3];
	float gyro[3];
	float ang[3];
	float mag[3];
}Gval;

extern "C" __declspec(dllexport) void open_port(unsigned long ulComNo, unsigned long ulBaudrate, int cResult) {
	printf("Waiting to open port%d...\r\n", ulComNo);
	while (cResult != 0){
		cResult = OpenCOMDevice(ulComNo, ulBaudrate);
	}
	printf("Done\n");
	ComNo = ulComNo;
}

extern "C" __declspec(dllexport) Gval get_gValue(int ulComNo)
{
	Gval val;
	printf("ulcomno : %d\n",ulComNo);
	printf("comno : %d\n", ComNo);

	usLength = CollectUARTData(ComNo, chrBuffer);
	if (usLength > 0)
	{
		JY901.CopeSerialData(chrBuffer, usLength);
	}

	Sleep(100);

	if (usCnt++ >= 0)
	{
		usCnt = 0;
		printf("Acceleration : %.3f %.3f %.3f\r\n", (float)JY901.stcAcc.a[0] / 32768 * 16, (float)JY901.stcAcc.a[1] / 32768 * 16, (float)JY901.stcAcc.a[2] / 32768 * 16);
		val.acc[0] = (float)JY901.stcAcc.a[0] / 32768 * 16;
		val.acc[1] = (float)JY901.stcAcc.a[1] / 32768 * 16;
		val.acc[2] = (float)JY901.stcAcc.a[2] / 32768 * 16;

		printf("Gyro : %.3f %.3f %.3f\r\n", (float)JY901.stcGyro.w[0] / 32768 * 2000, (float)JY901.stcGyro.w[1] / 32768 * 2000, (float)JY901.stcGyro.w[2] / 32768 * 2000);
		val.gyro[0] = (float)JY901.stcGyro.w[0] / 32768 * 2000;
		val.gyro[1] = (float)JY901.stcGyro.w[1] / 32768 * 2000;
		val.gyro[2] = (float)JY901.stcGyro.w[2] / 32768 * 2000;

		printf("Attitude Angle : %.3f %.3f %.3f\r\n", (float)JY901.stcAngle.Angle[0] / 32768 * 180, (float)JY901.stcAngle.Angle[1] / 32768 * 180, (float)JY901.stcAngle.Angle[2] / 32768 * 180);
		val.ang[0] = (float)JY901.stcAngle.Angle[0] / 32768 * 180;
		val.ang[1] = (float)JY901.stcAngle.Angle[1] / 32768 * 180;
		val.ang[2] = (float)JY901.stcAngle.Angle[2] / 32768 * 180;

		printf("Magnetic field : %d %d %d\r\n", JY901.stcMag.h[0], JY901.stcMag.h[1], JY901.stcMag.h[2]);
		val.mag[0] = JY901.stcMag.h[0];
		val.mag[1] = JY901.stcMag.h[1];
		val.mag[2] = JY901.stcMag.h[2];

		printf("========================================================================================\n");

	}

	return val;
}
*/


/*
*
#include "stdafx.h"
#include "Com.h"
#include "windows.h"
#include "time.h"
#include "stdio.h"
#include "JY901.h"
unsigned char ucComNo[2] ={0,0};

class set_gyro{
	set_gyro() {
		cResult = 1;
	}
	public:
		char chrBuffer[2000];
		unsigned short usLength = 0, usCnt = 0;
		unsigned long ulBaund = 9600, ulComNo = 8;
		signed char cResult;
};

typedef struct gVal{
	double acc[3];
	double gyro[3];
	double ang[3];
	double mag[3];
};

struct gVal _stdcall get_gValue(){
	struct gVal val;
	set_gyro sg;

	while(sg.cResult!=0){
		sg.cResult = OpenCOMDevice(sg.ulComNo,sg.ulBaund);
	}

	sg.usLength = CollectUARTData(sg.ulComNo, sg.chrBuffer);

		if (sg.usLength>0){
			JY901.CopeSerialData(sg.chrBuffer, sg.usLength);
		}
		Sleep(100);

		repeat:
		if (sg.usCnt++>=0){

			sg.usCnt=0;

			printf("Acceleration : %.3f %.3f %.3f\r\n",(float)JY901.stcAcc.a[0]/32768*16,(float)JY901.stcAcc.a[1]/32768*16,(float)JY901.stcAcc.a[2]/32768*16);
			val.acc[0] = (float)JY901.stcAcc.a[0]/32768*16;
			val.acc[1] = (float)JY901.stcAcc.a[1]/32768*16;
			val.acc[2] = (float)JY901.stcAcc.a[2]/32768*16;

			printf("Gyro : %.3f %.3f %.3f\r\n",(float)JY901.stcGyro.w[0]/32768*2000,(float)JY901.stcGyro.w[1]/32768*2000,(float)JY901.stcGyro.w[2]/32768*2000);
			val.gyro[0] = (float)JY901.stcGyro.w[0]/32768*2000;
			val.gyro[1] = (float)JY901.stcGyro.w[1]/32768*2000;
			val.gyro[2] = (float)JY901.stcGyro.w[2]/32768*2000;

			printf("Attitude Angle : %.3f %.3f %.3f\r\n",(float)JY901.stcAngle.Angle[0]/32768*180,(float)JY901.stcAngle.Angle[1]/32768*180,(float)JY901.stcAngle.Angle[2]/32768*180);
			val.ang[0] = (float)JY901.stcAngle.Angle[0]/32768*180;
			val.ang[1] = (float)JY901.stcAngle.Angle[1]/32768*180;
			val.ang[2] = (float)JY901.stcAngle.Angle[2]/32768*180;

			printf("Magnetic field : %d %d %d\r\n",JY901.stcMag.h[0],JY901.stcMag.h[1],JY901.stcMag.h[2]);
			val.mag[0] = JY901.stcMag.h[0];
			val.mag[1] = JY901.stcMag.h[1];
			val.mag[2] = JY901.stcMag.h[2];
			printf("========================================================================================\n");

		}else{
			goto repeat;
		}

		return val;
}

int main() {
	while (1) {
		get_gValue();
	}


}
*/













/*
typedef struct gVal {
	float acc[3];
	float gyro[3];
	float ang[3];
	float mag[3];
}GV;

extern "C" __declspec(dllexport) void open_port(unsigned long ulComNo, unsigned long ulBaudrate, int cResult) {
	printf("Waiting to open port%d...\r\n", ulComNo);
	while (cResult != 0) {
		cResult = OpenCOMDevice(ulComNo, ulBaudrate);
	}
	printf("Done\n");
	ComNo = ulComNo;
}

extern "C" __declspec(dllexport) GV get_gValue(int ulComNo)
{
	GV val;
	printf("ulcomno : %d\n", ulComNo);
	printf("comno : %d\n", ComNo);

	usLength = CollectUARTData(ComNo, chrBuffer);
	if (usLength > 0)
	{
		JY901.CopeSerialData(chrBuffer, usLength);
	}

	Sleep(100);

	if (usCnt++ >= 0)
	{
		usCnt = 0;
		printf("Acceleration : %.3f %.3f %.3f\r\n", (float)JY901.stcAcc.a[0] / 32768 * 16, (float)JY901.stcAcc.a[1] / 32768 * 16, (float)JY901.stcAcc.a[2] / 32768 * 16);
		val.acc[0] = (float)JY901.stcAcc.a[0] / 32768 * 16;
		val.acc[1] = (float)JY901.stcAcc.a[1] / 32768 * 16;
		val.acc[2] = (float)JY901.stcAcc.a[2] / 32768 * 16;

		printf("Gyro : %.3f %.3f %.3f\r\n", (float)JY901.stcGyro.w[0] / 32768 * 2000, (float)JY901.stcGyro.w[1] / 32768 * 2000, (float)JY901.stcGyro.w[2] / 32768 * 2000);
		val.gyro[0] = (float)JY901.stcGyro.w[0] / 32768 * 2000;
		val.gyro[1] = (float)JY901.stcGyro.w[1] / 32768 * 2000;
		val.gyro[2] = (float)JY901.stcGyro.w[2] / 32768 * 2000;

		printf("Attitude Angle : %.3f %.3f %.3f\r\n", (float)JY901.stcAngle.Angle[0] / 32768 * 180, (float)JY901.stcAngle.Angle[1] / 32768 * 180, (float)JY901.stcAngle.Angle[2] / 32768 * 180);
		val.ang[0] = (float)JY901.stcAngle.Angle[0] / 32768 * 180;
		val.ang[1] = (float)JY901.stcAngle.Angle[1] / 32768 * 180;
		val.ang[2] = (float)JY901.stcAngle.Angle[2] / 32768 * 180;

		printf("Magnetic field : %d %d %d\r\n", JY901.stcMag.h[0], JY901.stcMag.h[1], JY901.stcMag.h[2]);
		val.mag[0] = JY901.stcMag.h[0];
		val.mag[1] = JY901.stcMag.h[1];
		val.mag[2] = JY901.stcMag.h[2];

		printf("========================================================================================\n");

	}

	return val;
}
*/



/*
#include "pch.h"
using namespace std;
unsigned char ucComNo[2] = { 0,0 };
int ComNo = 3;
int cnt = 0;
char chrBuffer[2000];
unsigned short usLength = 0, usCnt = 0;


extern "C" __declspec(dllexport) void open_port(unsigned long ulComNo, unsigned long ulBaudrate, int cResult) {
	printf("Waiting to open port%d...\r\n", ulComNo);
	while (cResult != 0){
		cResult = OpenCOMDevice(ulComNo, ulBaudrate);
	}
	printf("Done\n");
	ComNo = ulComNo;
}
extern "C" __declspec(dllexport) float get_gValue(int cResult, int cnt)
{

	//float gValue[12];
	float gValue;
	usLength = CollectUARTData(ComNo, chrBuffer);
	if (usLength > 0)
	{
		JY901.CopeSerialData(chrBuffer, usLength);
	}
	Sleep(100);

	if (usCnt++ >= 0)
	{
		usCnt = 0;

		printf("Acceleration : %.3f %.3f %.3f\r\n", (float)JY901.stcAcc.a[0] / 32768 * 16, (float)JY901.stcAcc.a[1] / 32768 * 16, (float)JY901.stcAcc.a[2] / 32768 * 16);
		gValue = (float)JY901.stcAcc.a[0] / 32768 * 16;
		//gValue[1] = (float)JY901.stcAcc.a[1] / 32768 * 16;
		//gValue[2] = (float)JY901.stcAcc.a[2] / 32768 * 16;

		printf("Gyro : %.3f %.3f %.3f\r\n", (float)JY901.stcGyro.w[0] / 32768 * 2000, (float)JY901.stcGyro.w[1] / 32768 * 2000, (float)JY901.stcGyro.w[2] / 32768 * 2000);
		//gValue[3] = (float)JY901.stcGyro.w[0] / 32768 * 2000;
		//gValue[4] = (float)JY901.stcGyro.w[1] / 32768 * 2000;
		//gValue[5] = (float)JY901.stcGyro.w[2] / 32768 * 2000;

		printf("Attitude Angle : %.3f %.3f %.3f\r\n", (float)JY901.stcAngle.Angle[0] / 32768 * 180, (float)JY901.stcAngle.Angle[1] / 32768 * 180, (float)JY901.stcAngle.Angle[2] / 32768 * 180);
		//gValue[6] = (float)JY901.stcAngle.Angle[0] / 32768 * 180;
		//gValue[7] = (float)JY901.stcAngle.Angle[1] / 32768 * 180;
		//gValue[8] = (float)JY901.stcAngle.Angle[2] / 32768 * 180;

		printf("Magnetic field : %d %d %d\r\n", JY901.stcMag.h[0], JY901.stcMag.h[1], JY901.stcMag.h[2]);
		//gValue[9] = JY901.stcMag.h[0];
		//gValue[10] = JY901.stcMag.h[1];
		//gValue[11] = JY901.stcMag.h[2];

		printf("========================================================================================\n");

	}

	return gValue;
}


*/