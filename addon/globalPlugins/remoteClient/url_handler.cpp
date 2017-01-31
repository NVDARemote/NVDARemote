#define UNICODE
#include <string>
#include <windows.h>

std::wstring GetNVDAPath ();
LONG GetStringRegKey(HKEY hKey, const std::wstring &strValueName, std::wstring &strValue, const std::wstring &strDefaultValue);

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPWSTR     lpCmdLine, int       nCmdShow)
{
	if (__argc < 2) {
		return 0;
	}
	std::wstring args;
	std::wstring NVDAPath;
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
	if (hwnd == 0) {
		NVDAPath = GetNVDAPath();
			ShellExecute(0, NULL, NVDAPath.c_str(), NULL, NULL, 0);
	};
	for (int tries = 0; tries < 300; tries++) {
		Sleep(100);
		hwnd = FindWindow(L"NVDARemoteURLHandler", NULL);
		if (hwnd > 0) {
			Sleep(100); /* Needed to ensure the window is fully created */
			SendMessage(hwnd, WM_COPYDATA, 0, (LPARAM)&cds);
			return 0;
		};
}
	return 1;
}

/* Get the path to the NVDA executable if installed
Return an empty string if the path cannot be found. */

std::wstring GetNVDAPath () {
	HKEY hKey;
	LONG lRes = RegOpenKeyExW(HKEY_LOCAL_MACHINE, L"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\NVDA", 0, KEY_READ, &hKey);
	if (lRes != ERROR_SUCCESS) {
		return L"";
	}
	std::wstring result;
	std::wstring BadValue;
	GetStringRegKey(hKey, L"InstallDir", result, L"bad");
	if (result == L"bad") {
		return L"";
	}
	result += L"\\NVDA.exe";
	return result;
}

LONG GetStringRegKey(HKEY hKey, const std::wstring &strValueName, std::wstring &strValue, const std::wstring &strDefaultValue)
{
	strValue = strDefaultValue;
	WCHAR szBuffer[512];
	DWORD dwBufferSize = sizeof(szBuffer);
	ULONG nError;
	nError = RegQueryValueExW(hKey, strValueName.c_str(), 0, NULL, (LPBYTE)szBuffer, &dwBufferSize);
	if (ERROR_SUCCESS == nError)
	{
		strValue = szBuffer;
	}
	return nError;
}