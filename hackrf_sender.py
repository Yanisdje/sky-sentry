#This file contains code for only jamming a drone on a RF set by the user. 
import tkinter as tk
from tkinter import messagebox
from hackrf import HackRF
import numpy as np


def send_signal():
    try:
        frequency = int(entry.get())

        if frequency < 1e6 or frequency > 6e9:  # HackRF frequency range
            raise ValueError("Frequency must be between 1 MHz and 6 GHz.")

        hackrf.set_freq(frequency)  # Set the frequency

        # Create a simple signal 
        sample_rate = 10e6  # 10 MHz sample rate
        duration = 5  # duration in seconds
        num_samples = int(sample_rate * duration)

        t = np.linspace(0, duration, num_samples, endpoint=False)
        signal = (np.sin(2 * np.pi * 1e6 * t) * 127).astype(np.int8)  # 1 MHz sine wave

        hackrf.start_tx_mode()  # Start transmission
        hackrf.tx(signal.tobytes(), len(signal))  # Transmit the signal

        messagebox.showinfo("Success", f"Signal sent at {frequency / 1e6} MHz")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_close():
    hackrf.stop_tx_mode()  # Stop transmission when closing
    hackrf.close()
    root.destroy()


# Initialize HackRF
hackrf = HackRF()

# Create the main window
root = tk.Tk()
root.title("HackRF Signal Sender")

# Create and place the frequency input label and entry
label = tk.Label(root, text="Enter Frequency (Hz):")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

# Create and place the send signal button
send_button = tk.Button(root, text="Send Signal", command=send_signal)
send_button.pack(pady=10)

# Handle window close
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the Tkinter main loop
root.mainloop()
