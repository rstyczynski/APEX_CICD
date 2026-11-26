"""Read aggregate host resource counters every five seconds; no process arguments."""
import time
from pathlib import Path
print('unix_seconds,mem_available_kib,cpu_counters,disk_free_bytes',flush=True)
while True:
 mem=dict(line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())
 import shutil
 cpu=Path('/proc/stat').read_text().splitlines()[0].split()[1:]
 print(f"{time.time()},{mem['MemAvailable'].split()[0]},{':'.join(cpu)},{shutil.disk_usage('/').free}",flush=True)
 time.sleep(5)
