# ULTIMATE-ANDROID-CRASHER
a standard for testing or crashing devices.
# ⚠️ THE ULTIMATE ANDROID CRASHER (Flagship Max-Saturate Edition)

A high-intensity hardware and OS benchmark script designed to stress-test modern flagship Android devices (Snapdragon 8 Gen series, MediaTek Dimensity, Google Tensor). It operates as a dual-vector attack: flooding the device via a high-thread PC automation pipe while simultaneously triggering native internal loops to force the phone into a localized self-DDoS state.

## 🚀 Architectural Attack Vectors

Unlike basic loop scripts, this framework simultaneously attacks multiple deep subsystem bottlenecks:

*   **Zygote & Memory Thrashing (18 PC Threads):** Rapidly forks process generation by spamming `monkey` multi-launches across random packages in the background (`&`), bypassing traditional RAM caching and forcing constant heap reallocations.
*   **SurfaceFlinger & GPU Vector Stress (Internal Local Loop):** Spams hidden status bar expansion commands (`cmd statusbar expansion-drag`) alongside window composition requests, forcing intensive GPU blur calculations that instantly buckle high-refresh-rate layouts (120Hz/144Hz).
*   **UFS 4.0 Storage Saturation (18 PC Threads + Internal Loops):** Stacks 4 parallel uncompressed `screencap` pipelines from the PC while concurrently running local phone-side `dd` raw streams over `/dev/urandom`. This completely chokes the storage controller's high-speed write bandwidth.
*   **Binder IPC & Input Subsystem Lockout (12 PC Threads + Internal Loops):** Floods the Inter-Process Communication layer with massive text memory dumps via intent broadcasts, while spamming physical touch and hardware key handlers to lock up the main user interface thread.

## 🛠️ Prerequisites

Before executing the stress test, ensure your environment is fully configured:

1.  **Python 3.x** installed on your host PC.
2.  **Android SDK Platform-Tools (ADB)** installed and added to your system's PATH variables.
3.  **scrcpy** installed on your PC and verified via command line (`scrcpy --version`).
4.  **USB Debugging** enabled under *Settings > Developer Options* on the target device.
5.  A high-quality **USB 3.0+ Data Cable** connected directly to a high-speed PC port (avoid loose USB hubs).

## 📦 Installation

Install the required Python ADB client library using pip:

```bash
pip install pure-python-adb
```

## 🎮 Usage

1. Initialize the ADB server on your PC:
   ```bash
   adb start-server
   ```
2. Verify your device connection (ensure it says `device` and not `unauthorized`):
   ```bash
   adb devices
   ```
3. Run the script:
   ```bash
   python ultimate_android_crasher.py
   ```
4. A black, hacker-style Tkinter GUI will load. Once the green progress bar tracks the initial payload transfer to 100%, the 48-thread flood will trigger and launch a `scrcpy` viewport automatically.

## 🧹 Post-Test Reset & Cleanup

Because this script generates uncompressed screenshot blocks to saturate storage, run this cleanup command from your PC terminal immediately after a testing session to free up your phone's disk space:

```bash
adb shell "rm -f /sdcard/Pictures/Screenshots/st_*.png /sdcard/Pictures/Screenshots/swap*.bin"
```

*Note: Due to severe kernel log and RAM cache saturation, a manual device reboot is highly recommended after running this test to restore baseline device performance.*

## 🚨 Thermal & Structural Warning

This script intentionally disables safety pauses and targets extreme multi-core execution. The target device will generate significant heat rapidly. Do not run this test continuously for prolonged periods to avoid triggering the phone's native emergency thermal shutdown or risking storage overflow bootloops.
