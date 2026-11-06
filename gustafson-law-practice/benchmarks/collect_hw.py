#!/usr/bin/env python3
"""Task 24 helper - dump CPU model, caches, RAM, NUMA info for analysis/task24_hardware_audit.md.
Works on Linux (lscpu), macOS (sysctl) and Windows (PowerShell CIM). Writes ../analysis/hardware_snapshot.txt"""
import os, platform, subprocess, sys
from pathlib import Path

def sh(cmd):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e: return f"(failed: {e})"

lines = [f"platform: {platform.platform()}", f"python: {sys.version.split()[0]}", f"os.cpu_count: {os.cpu_count()}"]
if sys.platform.startswith("linux"):
    lines += [sh("lscpu"), sh("lscpu -C=NAME,ONE-SIZE 2>/dev/null"), sh("numactl --hardware 2>/dev/null"),
              sh("grep -m1 MemTotal /proc/meminfo"), sh("sudo -n dmidecode -t memory 2>/dev/null | grep -E 'Speed|Size|Locator' | head -20")]
elif sys.platform == "darwin":
    lines += [sh("sysctl -n machdep.cpu.brand_string hw.physicalcpu hw.logicalcpu hw.memsize hw.l1dcachesize hw.l2cachesize hw.l3cachesize")]
else:
    ps = lambda q: sh(f'powershell -NoProfile -Command "{q}"')
    lines += [ps("Get-CimInstance Win32_Processor | Select Name,NumberOfCores,NumberOfLogicalProcessors,L2CacheSize,L3CacheSize,MaxClockSpeed | Format-List"),
              ps("Get-CimInstance Win32_PhysicalMemory | Select Capacity,Speed,ConfiguredClockSpeed,DeviceLocator | Format-Table"),
              ps("(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory"),
              ps("powercfg /getactivescheme")]
txt = "\n".join(lines)
Path(__file__).resolve().parent.parent.joinpath("analysis", "hardware_snapshot.txt").write_text(txt, encoding="utf-8")
print(txt)
