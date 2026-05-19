import os
import ctypes
import psutil
import win32gui
import win32ui
import win32con
import win32process
import numpy as np
from datetime import datetime


def find_window_by_process_name(process_name):
    """
    Find the first visible window that belongs to the given process name.
    Returns HWND or None.
    """

    target_pids = []

    # Find matching processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if (
                proc.info['name']
                and proc.info['name'].lower() == process_name.lower()
            ):
                target_pids.append(proc.info['pid'])

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    if not target_pids:
        return None

    found_hwnd = None

    def enum_windows_callback(hwnd, _):
        nonlocal found_hwnd

        # Stop once found
        if found_hwnd is not None:
            return

        # Only visible windows
        if not win32gui.IsWindowVisible(hwnd):
            return

        # Get PID for this window
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        # Match process
        if pid in target_pids:
            found_hwnd = hwnd

    win32gui.EnumWindows(enum_windows_callback, None)

    return found_hwnd


def capture_window(hwnd):
    """
    Capture a screenshot of the specified window.
    Returns a PIL Image object.
    """

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    width = right - left
    height = bottom - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, width, height)

    save_dc.SelectObject(bitmap)

    result = ctypes.windll.user32.PrintWindow(
        hwnd,
        save_dc.GetSafeHdc(),
        2
    )

    if result != 1:
        print("Failed to capture window")

        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        return None

    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)

    img = np.frombuffer(
        bmpstr,
        dtype=np.uint8
    ).reshape(
        (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
    )

    # Convert BGRX -> RGB
    img = img[:, :, :3][:, :, ::-1].copy()

    # Cleanup GDI objects ASAP
    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return img


def screenshot(process_name) -> str:
    """
    Capture a screenshot from a process name.
    Returns the saved file path or None.
    """

    hwnd = find_window_by_process_name(process_name)

    if hwnd is None:
        print("Could not find process/window")
        return None

    print(f"Found window: {win32gui.GetWindowText(hwnd)}")

    # Screenshot folder
    screenshot_dir = "screenshots"

    os.makedirs(screenshot_dir, exist_ok=True)

    # Unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    clean_name = process_name.replace(".exe", "")

    filename = f"{clean_name}_{timestamp}.png"

    save_path = os.path.join(screenshot_dir, filename)

    # Capture
    capture = capture_window(hwnd)

    return capture


# Optional standalone test
#if __name__ == "__main__":
    #screenshot("likeadragon8.exe")