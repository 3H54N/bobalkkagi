from unicorn import *
from unicorn.x86_const import *
from loader import EndOfString
<<<<<<< HEAD
from config import DLL_SETTING, HEAP_HANDLE, GlobalVar
from util import *

from logger import PrintFunction
=======
from config import DLL_SETTING, HEAP_HANDLE

import logging
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
import struct
import os, sys

 

def hook_LoadLibraryA(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    rbx = uc.reg_read(UC_X86_REG_RBX)
    rsi = uc.reg_read(UC_X86_REG_RSI)
    
    d_address = 0
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]

    dllName = EndOfString(bytes(uc.mem_read(rcx, 0x20))) #byte string
    
    if dllName in DLL_SETTING.LOADED_DLL:
        d_address = DLL_SETTING.LOADED_DLL[dllName]
    else:
        print(f"{dllName} is not Loaded!")
    
    if d_address:
        uc.reg_write(UC_X86_REG_RAX,d_address)

    uc.mem_write(rsp+0x8,struct.pack('<Q',rbx))
    uc.mem_write(rsp+0x10,struct.pack('<Q',rsi))
<<<<<<< HEAD
=======
    log.info(f"API Call : LoadLibraryA, {dllName}: {hex(d_address)}")
    #log.debug("DEBUGING")
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)
    

def hook_GetProcAddress(ip, rsp, uc, log):
    
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    rdx = uc.reg_read(UC_X86_REG_RDX)
    rbx = uc.reg_read(UC_X86_REG_RBX)
    rbp = uc.reg_read(UC_X86_REG_RBP)
    rsi = uc.reg_read(UC_X86_REG_RSI)
  
    f_address = 0
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]
    
    #func_nameByte = bytes(uc.mem_read(rdx, 0x20))
    
    
    functionName=EndOfString(bytes(uc.mem_read(rdx, 0x20)))
    functionName = DLL_SETTING.INV_LOADED_DLL[rcx]+"_" + functionName
    f_address = DLL_SETTING.DLL_FUNCTIONS[functionName]

    uc.mem_write(rsp+0x8,struct.pack('<Q',rbx))
    uc.mem_write(rsp+0x18,struct.pack('<Q',rbp))
    uc.mem_write(rsp+0x20,struct.pack('<Q',rsi))
    uc.mem_write(rsp+0x10,struct.pack('<Q',f_address))
    if f_address:
        uc.reg_write(UC_X86_REG_RAX,f_address)
    log.info(f"API Call : GetProcAddress, {functionName}: {hex(f_address)}")
    #log.debug("DEBUGING")
    

    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_GetModuleHandleA(ip, rsp, uc, log):
    
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    d_address = 0
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]
    

    handle = EndOfString(bytes(uc.mem_read(rcx, 0xd)))
<<<<<<< HEAD

=======
    log.info(f"API Call : GetModuleHandleA, RCX : {handle}")    
    #log.debug("DEBUGING")
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
    if handle in DLL_SETTING.LOADED_DLL:
        d_address = DLL_SETTING.LOADED_DLL[handle]

    if d_address:
        uc.reg_write(UC_X86_REG_RAX, d_address)

    uc.reg_write(UC_X86_REG_RIP, tmp)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)

def hook_RtlInitializeCriticalSection(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    rbx = uc.reg_read(UC_X86_REG_RBX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]
    uc.mem_write(rsp+0x10,struct.pack('<Q',rbx))
<<<<<<< HEAD
=======
    log.info(f"API Call : RtlInitializeCriticalSection, RCX : {hex(rcx)}")
    #log.debug("DEBUGING")
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
    uc.reg_write(UC_X86_REG_RAX,0x0)
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)
    

def hook_GetUserDefaultUILanguage(ip,rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]
    
    
    uc.mem_write(rsp+0x8,struct.pack('<Q',0x409))
<<<<<<< HEAD

=======
    log.info(f"API Call : GetUserDefaultUILanguage, RCX : {hex(rcx)}")
    #log.debug("DEBUGING")
    
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
    uc.reg_write(UC_X86_REG_RAX,0x409)
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)
    

def hook_GetProcessHeap(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]
    
    rax =uc.mem_read(0xff20000000000000+0x30,8)
    rax =struct.unpack('<Q',rax)[0]
<<<<<<< HEAD

=======
    
    log.info(f"API Call : GetProcessHeap, RAX : {hex(rcx)}")
    #log.debug("DEBUGING")
    
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
    uc.reg_write(UC_X86_REG_RAX,rax)
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)
    

def hook_RtlAllocateHeap(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    rbx = uc.reg_read(UC_X86_REG_RBX)
    r8 = uc.reg_read(UC_X86_REG_R8)

    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]

    HEAP_HANDLE.heap_handle.append(HEAP_HANDLE.heap_handle[HEAP_HANDLE.heap_handle_size-1]+(r8*8))
    HEAP_HANDLE.heap_handle_size+=1

    uc.reg_write(UC_X86_REG_RAX,HEAP_HANDLE.heap_handle[HEAP_HANDLE.heap_handle_size-1])
   
    uc.mem_write(rsp+0x8,struct.pack('<Q',0x3))
    uc.mem_write(rsp+0x10,struct.pack('<Q',rbx))

<<<<<<< HEAD
=======
    log.info(f"API Call : RtlAllocateHeap, RAX : {hex(HEAP_HANDLE.heap_handle[HEAP_HANDLE.heap_handle_size-1])}")
    #log.debug("DEBUGING")
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)
    

def hook_RtlTryEnterCriticalSection(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]

    uc.reg_write(UC_X86_REG_RAX,0x0)
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)
   

def hook_RtlEnterCriticalSection(ip, rsp, uc, log):
    
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
  
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]
    
    
    uc.reg_write(UC_X86_REG_RAX,0x0)
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)
    
def hook_RtlLeaveCriticalSection(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
   
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]
    
    uc.reg_write(UC_X86_REG_RAX,0x0)
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)
   

def hook_GetCurrentDirectoryW(ip, rsp, uc, log):
    
    rdx = uc.reg_read(UC_X86_REG_RDX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]

    cwd = os.getcwd()
<<<<<<< HEAD

=======
    cwd_len = len(cwd)
    #log.debug("DEBUGING")
    log.info(f"API Call : GetCurrentDirectoryW, path : {cwd}, len : {hex(cwd_len)}")
    
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
    uc.mem_write(rdx,cwd.encode('utf-8'))
    uc.reg_write(UC_X86_REG_RAX,len(cwd))
    uc.reg_write(UC_X86_REG_RCX,rdx)
    uc.reg_write(UC_X86_REG_R11,rdx)
    #log.debug("DEBUGING")
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_SetCurrentDirectoryW(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
<<<<<<< HEAD
    tmp = struct.unpack('<Q',tmp)[0]

=======
    tmp=struct.unpack('<Q',tmp)[0]


    #log.debug("DEBUGING")
    log.info(f"API Call : SetCurrentDirectoryW")
    
    #log.debug("DEBUGING")
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
    uc.reg_write(UC_X86_REG_RAX,0x1)
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_GetModuleFileNameW(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    rdx = uc.reg_read(UC_X86_REG_RDX)
    rbx = uc.reg_read(UC_X86_REG_RBX)
    rbp = uc.reg_read(UC_X86_REG_RBP)
    rsi = uc.reg_read(UC_X86_REG_RSI)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]

    if not rcx:
        path = GlobalVar['ProgPath']
    else:
        try:
            module_name = DLL_SETTING.LOADED_DLL[rcx]
        except KeyError:
            module_name = "somefakename.dll"
        path = f"C:/Windows/System32/{module_name}"
    
<<<<<<< HEAD
    uc.reg_write(UC_X86_REG_R11,rdx)
    
    uc.mem_write(rsp+0x8,struct.pack('<Q', rbx))
    uc.mem_write(rsp+0x10,struct.pack('<Q', rbp))
    uc.mem_write(rsp+0x18,struct.pack('<Q', rsi))
    uc.mem_write(rdx,path.encode("utf-16"))
    uc.reg_write(UC_X86_REG_RAX, len(path))
    uc.reg_write(UC_X86_REG_RDX, 0x0)
    uc.reg_write(UC_X86_REG_R8, 0x0)
=======
    #log.debug("DEBUGING")
    uc.reg_write(UC_X86_REG_R11,rdx)
    
    #print(path.encode("utf-8"))
    #print(hex(len(path)))
    log.info(f"API Call : GetModuleFileNameW, path : {path}")
    uc.mem_write(rsp+0x8,struct.pack('<Q',rbx))
    uc.mem_write(rsp+0x10,struct.pack('<Q',rbp))
    uc.mem_write(rsp+0x18,struct.pack('<Q',rsi))
    uc.mem_write(rdx,path.encode("utf-16"))
    uc.reg_write(UC_X86_REG_RAX,len(path))
    uc.reg_write(UC_X86_REG_RDX,0x0)
    uc.reg_write(UC_X86_REG_R8,0x0)
    #log.debug("DEBUGING")
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_GetCurrentThreadId(ip, rsp, uc, log):
    
    log.info(f"API Call : GetCurrentThreadId")
    
   

   

def hook_OpenThread(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]


    #log.debug("DEBUGING")
    log.info(f"API Call : OpenThread")
    
    #log.debug("DEBUGING")

    uc.reg_write(UC_X86_REG_RAX,0xcc) # 임시 스레드 핸들
    uc.mem_write(rsp+0x20,struct.pack('<Q',0xcc))
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_GetVersion(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]


    #log.debug("DEBUGING")
    log.info(f"API Call : GetVersion, Returning 6.2 (Windows 8 or Windows 10)")
    
    #log.debug("DEBUGING")

    uc.reg_write(UC_X86_REG_RAX,0x206) 
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_RtlAddVectoredExceptionHandler(ip, rsp, uc, log):
    
    
    rbx = uc.reg_read(UC_X86_REG_RBX)
    rbp = uc.reg_read(UC_X86_REG_RBP)
    rsi = uc.reg_read(UC_X86_REG_RSI)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]

    
    #log.debug("DEBUGING")
  
    
    #print(path.encode("utf-8"))
    #print(hex(len(path)))
    log.info(f"API Call : RtlAddVectoredExceptionHandler")
    uc.mem_write(rsp+0x8,struct.pack('<Q',rbx))
    uc.mem_write(rsp+0x10,struct.pack('<Q',rbp))
    uc.mem_write(rsp+0x18,struct.pack('<Q',rsi))
   
    uc.reg_write(UC_X86_REG_RAX,0x000001E9E3860000) #임시 핸들
    #log.debug("DEBUGING")
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_GetCommandLineA(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]


    #log.debug("DEBUGING")
    log.info(f"API Call : GetCommandLineA")
    
    #log.debug("DEBUGING")
    uc.reg_write(UC_X86_REG_RAX,0x000001E9E3860000+0x3480) #임시포인터
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_GetCurrentProcess(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]


    #log.debug("DEBUGING")
    log.info(f"API Call : GetCurrentProcess")
    
    #log.debug("DEBUGING")
    uc.reg_write(UC_X86_REG_RAX,0xffffffffffffffff)
>>>>>>> 83b1aec4f56d0b52a4dbeffc2f32c1a652965bc3
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_GetCurrentThreadId(ip, rsp, uc, log):
    pass
    
   
def hook_OpenThread(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp, 8)
    tmp=struct.unpack('<Q', tmp)[0]

    uc.reg_write(UC_X86_REG_RAX, 0xcc) # 임시 스레드 핸들
    uc.mem_write(rsp+0x20,struct.pack('<Q', 0xcc))
    uc.reg_write(UC_X86_REG_RIP, tmp)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)

def hook_GetVersion(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp, 8)
    tmp=struct.unpack('<Q', tmp)[0]

    uc.reg_write(UC_X86_REG_RAX, 0x206) 
    uc.reg_write(UC_X86_REG_RIP, tmp)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)

def hook_RtlAddVectoredExceptionHandler(ip, rsp, uc, log):
    
    
    rbx = uc.reg_read(UC_X86_REG_RBX)
    rbp = uc.reg_read(UC_X86_REG_RBP)
    rsi = uc.reg_read(UC_X86_REG_RSI)
    
    tmp = uc.mem_read(rsp, 8)
    tmp=struct.unpack('<Q', tmp)[0]

    uc.mem_write(rsp+0x8, struct.pack('<Q', rbx))
    uc.mem_write(rsp+0x10, struct.pack('<Q', rbp))
    uc.mem_write(rsp+0x18, struct.pack('<Q', rsi))
    uc.reg_write(UC_X86_REG_RAX, 0x000001E9E3860000) #임시 핸들
    uc.reg_write(UC_X86_REG_RIP, tmp)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)

def hook_GetCommandLineA(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]

    uc.reg_write(UC_X86_REG_RAX, 0x000001E9E3860000 + 0x3480) #임시포인터
    uc.reg_write(UC_X86_REG_RIP, tmp)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)

def hook_GetCurrentProcess(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    
    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]

    uc.reg_write(UC_X86_REG_RAX, 0xffffffffffffffff)
    uc.reg_write(UC_X86_REG_RIP, tmp)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)

def hook_GetCurrentThread(ip, rsp, uc, log):

    uc.reg_write(UC_X86_REG_RAX, 0xfffffffffffffffe)
    
    ret = uc.mem_read(rsp,8)
    ret = struct.unpack('<Q',ret)[0]
    uc.reg_write(UC_X86_REG_RIP, ret)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)

def hook_OpenThreadToken(ip, rsp, uc, log):

    rcx = uc.reg_read(UC_X86_REG_RCX)
    rbx = uc.reg_read(UC_X86_REG_RBX)
    rsi = uc.reg_read(UC_X86_REG_RSI)

    tmp = uc.mem_read(rsp,8)
    tmp=struct.unpack('<Q',tmp)[0]

    uc.reg_write(UC_X86_REG_RAX,0x0)
    uc.reg_write(UC_X86_REG_RIP,tmp)
    uc.reg_write(UC_X86_REG_RSP,rsp+8)

def hook_OpenProcessToken(ip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    rdx = uc.reg_read(UC_X86_REG_RBX)
    r8 = uc.reg_read(UC_X86_REG_R8)
    r9 = uc.reg_read(UC_X86_REG_R9)


    ret = uc.mem_read(rsp,8)
    ret = struct.unpack('<Q',ret)[0]

    uc.reg_write(UC_X86_REG_RAX, 0x1)
    uc.reg_write(UC_X86_REG_RIP, ret)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)
    
    #PrintFunction(log, uc)


def hook_GetTokenInformation(rip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX)
    rdx = uc.reg_read(UC_X86_REG_RBX)
    r8 = uc.reg_read(UC_X86_REG_R8)
    r9 = uc.reg_read(UC_X86_REG_R9)
    #r10 = uc.mem_read(rsp+0x60,0x8)
    #print(rcx,rdx,r8,r9,r10)

    ret = uc.mem_read(rsp,8)
    ret = struct.unpack('<Q',ret)[0]

    uc.reg_write(UC_X86_REG_RAX, 0x1)
    uc.reg_write(UC_X86_REG_RIP, ret)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)
    

def hook_VirtualAlloc(rip, rsp, uc, log):
    
    rcx = uc.reg_read(UC_X86_REG_RCX) #address
    rdx = uc.reg_read(UC_X86_REG_RBX) #size
    r8 = uc.reg_read(UC_X86_REG_R8) # t
    r9 = uc.reg_read(UC_X86_REG_R9) # protection

    if rcx == 0:
        offset = None
    else:
        offset = rcx

    print(rcx,rdx,r8,r9)

    aligned_address = alloc(uc, rdx, log, offset)
    print(aligned_address)
    PrintFunction(log,uc)
    ret = uc.mem_read(rsp,8)
    ret = struct.unpack('<Q',ret)[0]

    uc.reg_write(UC_X86_REG_RAX, aligned_address)
    uc.reg_write(UC_X86_REG_RIP, ret)
    uc.reg_write(UC_X86_REG_RSP, rsp+8)
    
    
#def hook_VirtualProtect(rip, rsp, uc, log):

MB = 2**20

def alloc(uc, size, log, offset = None):
    log.info("ALLOC!")
    page_size = 4 * 1024
    aligned_size = align(size, page_size)
    if offset is None:
        for chunk_start, chunk_end in GlobalVar['allocated_chunks']:
            if chunk_start <= GlobalVar['DynamicMemOffset'] <= chunk_end:
                GlobalVar['DynamicMemOffset'] = chunk_end + 1
        offset = GlobalVar['DynamicMemOffset']
        GlobalVar['DynamicMemOffset'] += aligned_size
    #new_offset_memory = offset % page_size
    aligned_address = offset

    if aligned_address % page_size != 0:
        aligned_address = align(offset)
    log.info(f"{hex(aligned_address)} : {hex(aligned_size)}")
    mapped_partial = False
    for chunk_start, chunk_end in GlobalVar['allocated_chunks']:
        if chunk_start <= aligned_address < chunk_end:
            log.info("Already fully mapped")
        else:
            log.info(f"Mapping missing piece 0x{chunk_end + 1:02x} to 0x{aligned_address + aligned_size:02x}")
            uc.mem_map(chunk_end, aligned_address + aligned_size - chunk_end)
        mapped_partial = True
        break

    if not mapped_partial:
        uc.mem_map(aligned_address, aligned_size)

    log.info(f"\tfrom 0x{aligned_address:02x} to 0x{(aligned_address + aligned_size):02x}")
    GlobalVar['allocated_chunks'] = list( merge(GlobalVar['allocated_chunks'] + [(aligned_address, aligned_address + aligned_size)]))
    GlobalVar['alloc_sizes'][aligned_address] = aligned_size

    return aligned_address