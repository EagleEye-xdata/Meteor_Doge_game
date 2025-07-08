import numpy as np
import cv2
from win32api import GetSystemMetrics
import pyautogui
import time
import os

def get_user_input():
    try:
        duration = float(input("Enter recording duration in seconds (default 10): ") or 10)
        filename = input("Enter output filename (default output.avi): ") or "output.avi"
        fps = float(input("Enter frames per second (default 30): ") or 30)
        return duration, filename, fps
    except ValueError:
        print("Invalid input. Using default values.")
        return 10, "output.avi", 30

def main():
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    dim = (width, height)

    duration, filename, fps = get_user_input()
    if not filename.lower().endswith('.avi'):
        filename += '.avi'

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, fps, dim)

    print(f"Recording {duration} seconds to {filename} at {fps} FPS...")
    start_time = time.time()
    end_time = start_time + duration

    try:
        while True:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            out.write(frame)
            elapsed = time.time() - start_time
            print(f"\rRecording... {elapsed:.2f} seconds elapsed", end="")
            if time.time() > end_time:
                break
    except KeyboardInterrupt:
        print("\nRecording interrupted by user.")
    finally:
        out.release()
        cv2.destroyAllWindows()
        print(f"\nRecording finished and saved to {filename}")

if __name__ == "__main__":
    main()
