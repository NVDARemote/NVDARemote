#define UNICODE
#include <string>
#include <windows.h>

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPWSTR     lpCmdLine, int       nCmdShow)
{
	if (__argc < 2) {
		return 0;
	}
	std::wstring args;
	for (int i=1; i <= __argc - 1;i++) {
		args += __wargv[i];
		if (i != __argc - 1) {
			args += L" ";
		}
	}
	COPYDATASTRUCT cds;
	const wchar_t *data = args.c_str();
	cds.lpData = (char *)data;
	cds.cbData = (args.length()*2)+2;
	HWND hwnd;
	hwnd = FindWindow(L"NVDARemoteURLHandler", NULL);
	if (hwnd > 0) {
		SendMessage(hwnd, WM_COPYDATA, 0, (LPARAM)&cds);
	}
	return 0;
}
