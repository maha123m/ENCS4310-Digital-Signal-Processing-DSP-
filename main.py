#Hazar Michael  1201838
#Maha Mali      1200746
#Afaf Amwas     1203359

import os
from tkinter import *
from tkinter import filedialog , messagebox, Frame, Button, Label, Entry, StringVar, RAISED, font
import tkinter as tk
from scipy import fftpack
import scipy
from scipy.io.wavfile import write
import scipy.io as sio
import numpy as np
from matplotlib import pyplot as plot
import sounddevice
import time
from scipy import signal

duration=0.04  # Time Duration 40ms as specified in Project
sampling_freqency=8000 #Sampling Frequency must be at least 2 * highest frequency(3500)
fast_forier_transform_freq=1024 #Fast Fourier Transform sampling frequency
number_of_samples=int(duration * sampling_freqency)# Number of Samples


selected_path = ''
l = np.array([])
E1 = None
newstr = None
root = None

character_frequencies={  # Frequency table for all Alphabets

        'a': [100, 1100, 2500], 'b': [100, 1100, 3000], 'c': [100, 1100, 3500],
        'd': [100, 1300, 2500], 'e': [100, 1300, 3000], 'f': [100, 1300, 3500],
        'g': [100, 1500, 2500], 'h': [100, 1500, 3000], 'i': [100, 1500, 3500],
        'j': [300, 1100, 2500], 'k': [300, 1100, 3000], 'l': [300, 1100, 3500],
        'm': [300, 1300, 2500], 'n': [300, 1300, 3000], 'o': [300, 1300, 3500],
        'p': [300, 1500, 2500], 'q': [300, 1500, 3000], 'r': [300, 1500, 3500],
        's': [500, 1100, 2500], 't': [500, 1100, 3000], 'u': [500, 1100, 3500],
        'v': [500, 1300, 2500], 'w': [500, 1300, 3000], 'x': [500, 1300, 3500],
        'y': [500, 1500, 2500], 'z': [500, 1500, 3000], ' ': [500, 1500, 3500]
}

# Used to completely exit the program
def exitProgram():
    user_choice = messagebox.askyesno("Exit", "Do you want to exit the program?")
    if user_choice:
        root.destroy()  # Close the program if the user clicks 'Yes'


# Saving Audio File in a specified directory
def save_in_specific_directory():
    global selected_path, l
    current_path = selected_path
    selected_path = filedialog.asksaveasfilename()
    if selected_path == '':
        selected_path = current_path
    if selected_path != '':
        scipy.io.wavfile.write(selected_path, 8000, l)


# handling directories
def save_in_work_directory():
    global selected_path, l
    if selected_path == '':
        default_filename = "generated_signal.wav"
        selected_path = os.path.join(os.getcwd(), default_filename)

    try:
        scipy.io.wavfile.write(selected_path, 8000, l)
        messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {e}")


# The decoded Signal Audio File saved and uploaded
def uploaded_input_file():
    global l
    name = filedialog.askopenfilename()
    if name != '':
        samplerate, l = sio.wavfile.read(name)
        messagebox.showinfo("Success", "Audio file uploaded successfully!")


# BandPass filter to decode audio signal
def create_bandpass_filter(low_cutoff_freq, high_cutoff_freq, fs, order=5):
    nyquist_freq = 0.5 * fs           # Nyquest Rate

    # normalizing low and high frequencies
    normalized_low = low_cutoff_freq / nyquist_freq
    normalized_high = high_cutoff_freq / nyquist_freq

    b, a = signal.butter(order, [normalized_low , normalized_high], btype='band')
    return b, a

# Taking Low and High cutoff frequencies and filter order to apply bandpass filter functionality
def apply_bandpass_filter(signal_data, low_frequency_cutoff, high_frequency_cutoff, sampling_rate, filter_order=5):
    filter_coefficient_b, filter_coefficient_a = create_bandpass_filter(low_frequency_cutoff, high_frequency_cutoff, sampling_rate, order=filter_order)
    filtered_signal= signal.lfilter(filter_coefficient_b, filter_coefficient_a, signal_data)
    return filtered_signal


def phase_one_encode():
    global l, E1, is_encoded
    l = np.array([])
    stri = E1.get()

    # Validate the input: check if there are uppercase letters, numbers, or symbols
    if any(char.isupper() or char.isdigit() or (not char.isalpha() and not char.isspace()) for char in stri):
        messagebox.showerror("Invalid Input", "Please enter only lowercase letters and spaces.")
        return

    for i in stri:
        l = np.concatenate((l, [np.cos(character_frequencies[i][0] * 2 * np.pi * n / sampling_freqency) +
                                np.cos(character_frequencies[i][1] * 2 * np.pi * n / sampling_freqency) +
                                np.cos(character_frequencies[i][2] * 2 * np.pi * n / sampling_freqency)
                                for n in range(number_of_samples)]), axis=None)

    is_encoded = True
    # Show an alert message for successful encoding
    messagebox.showinfo("Success", "String encoded successfully!")


# Plotting String
def plot_string():
    global l
    fig = plot.figure()
    fig.subplots_adjust(top=0.8)

    # Time Domain Wave
    ax1 = fig.add_subplot(211)
    ax1.set_ylabel('x(t)')
    ax1.set_xlabel('t')
    ax1.set_title('Time Domain Wave')
    ax1.plot(l, color='blue', linestyle='-', linewidth=2,
             label='Original Signal')  # Set the color, linestyle, and linewidth
    ax1.grid(True, linestyle='--', alpha=0.7)  # Add grid lines

    # Frequency Domain Wave
    ax2 = fig.add_axes([0.15, 0.1, 0.7, 0.2])
    ax2.set_ylabel('X(f)')
    ax2.set_xlabel('f')
    ax2.set_title('Frequency Domain Wave')
    ax2.plot(np.abs(fftpack.fft(l)), color='green', linestyle='-', linewidth=2,
             label='FFT')  # Set the color, linestyle, and linewidth
    ax2.grid(True, linestyle='--', alpha=0.7)  # Add grid lines

    ax1.legend()  # Add legend to the time domain plot
    ax2.legend()  # Add legend to the frequency domain plot

    plot.show()


# To Listen to the sounds of AudioFiles
def play():
    global l, is_encoded
    if not is_encoded:
        messagebox.showerror("Error", "Please encode the string before playing.")
        return
    sounddevice.play(l, sampling_freqency)
    time.sleep(1)


def phaseTwo_decode():
    global l, newstr
    result_str = "FFT Result: "

    for i in range(0, len(l), number_of_samples):
        freqMag = abs(fftpack.fft(l[i:i + number_of_samples], fast_forier_transform_freq))
        maxpoints = [
            int(np.argmax(freqMag[int(100 * (fast_forier_transform_freq / sampling_freqency)):int(
                500 * (fast_forier_transform_freq / sampling_freqency))]) + 100 * (
                    fast_forier_transform_freq / sampling_freqency)) * (
                    sampling_freqency / fast_forier_transform_freq),
            int((sampling_freqency / fast_forier_transform_freq) * (np.argmax(
                freqMag[int(1100 * (fast_forier_transform_freq / sampling_freqency)):int(
                    1500 * (fast_forier_transform_freq / sampling_freqency))]) + 1100 * (
                                                                            fast_forier_transform_freq / sampling_freqency))),
            int((sampling_freqency / fast_forier_transform_freq) * (np.argmax(
                freqMag[int(2500 * (fast_forier_transform_freq / sampling_freqency)):int(
                    3500 * (fast_forier_transform_freq / sampling_freqency))]) + 2500 * (
                                                                            fast_forier_transform_freq / sampling_freqency)))
        ]
        for j in range(3):
            maxpoints[j] = int(round(maxpoints[j] / 100) * 100)
        if maxpoints in character_frequencies.values():
            for char, freqs in character_frequencies.items():
                if freqs == maxpoints:
                    result_str += char

    newstr.set(result_str)
# Show an alert message for successful decoding using FFT
    messagebox.showinfo("Decode using FFT", "String decoded successfully using Fast Fourier Transform.")

def pandBass_decode():
    global l, newstr
    result_str = "BPF Result: "

    for i in range(0, len(l), number_of_samples):
        letterfrq = [0, 0, 0]
        for j, (low, high) in enumerate([(100, 500), (1100, 1500), (2500, 3500)]):
            x = apply_bandpass_filter(l[i:i + number_of_samples], low, high, sampling_freqency, filter_order=1)
            letterfrq[j] = np.argmax(abs(fftpack.fft(x, fast_forier_transform_freq))) * (
                    sampling_freqency / fast_forier_transform_freq)
            letterfrq[j] = int(round(letterfrq[j] / 100) * 100)
        if letterfrq in character_frequencies.values():
            for char, freqs in character_frequencies.items():
                if freqs == letterfrq:
                    result_str += char

    newstr.set(result_str)
    messagebox.showinfo("Decode using Band Pass Filter", "String decoded successfully using Band Pass Filter.")



def setup_main_window(root):
    global E1, newstr
    root.title("English Character Frequency - DSP project")
    root.configure(bg='#b39ddb')

    bold_font = font.Font(weight="bold", size=12)
    welcome_font = font.Font(weight="bold", size=20)

    welcome_label = Label(root, text="Welcome To DSP Project", font=welcome_font, bg='#b39ddb')
    welcome_label.pack(side=tk.TOP, pady=(10, 20))

    left_frame = Frame(root, bg='#b39ddb')
    left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

    right_frame = Frame(root, bg='#b39ddb')
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    label = Label(left_frame, text="Enter Text:", font=bold_font, bg='#b39ddb')
    label.pack()

    E1 = Entry(left_frame, bd=4, width=25)
    E1.pack()

    B4 = Button(left_frame, text="Encode String", command=phase_one_encode, font=bold_font, width=20, bg="#d1c4e9")
    B4.pack(pady=20, padx=30)

    B1 = Button(left_frame, text="Plot Encoded String", command=plot_string, font=bold_font, width=20, bg="#d1c4e9")
    B1.pack(pady=20, padx=30)

    B2 = Button(left_frame, text="Play", command=play, font=bold_font, width=20, bg="#d1c4e9")
    B2.pack(pady=20, padx=30)

    bottom_frame = Frame(left_frame, bg='#b39ddb')
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

    save_as_button = Button(bottom_frame, text="Save as", command=save_in_specific_directory, font=bold_font, bg="#d1c4e9")
    save_as_button.pack(side=tk.LEFT, padx=10, pady=5)

    save_button = Button(bottom_frame, text="Save", command=save_in_work_directory, font=bold_font, bg="#d1c4e9")
    save_button.pack(side=tk.LEFT, padx=10, pady=5)

    exit_button = Button(bottom_frame, text="Exit", command=exitProgram, font=bold_font, bg="#d1c4e9")
    exit_button.pack(side=tk.LEFT, padx=10, pady=5)

    newstr = StringVar()

    result_title_label = Label(right_frame, text="Result of Decoding", font=bold_font, bg='#b39ddb')
    result_title_label.pack()

    L1 = Label(right_frame, textvariable=newstr, relief=tk.RAISED, bg='#b39ddb')
    L1.pack()

    B3 = Button(right_frame, text="Decode an audio signal stored in a file", command=uploaded_input_file, font=bold_font, width=30, bg="#d1c4e9")
    B3.pack(pady=20, padx=30)

    B5 = Button(right_frame, text="Decode(Fast Fourier Transform)", command=phaseTwo_decode, font=bold_font, width=30, bg="#d1c4e9")
    B5.pack(pady=20, padx=30)

    B6 = Button(right_frame, text="Decode (Band Pass Filter)", command=pandBass_decode, font=bold_font, width=30, bg="#d1c4e9")
    B6.pack(pady=20, padx=30)

    names_text = "Members:\nHazar Michael 1201838\nMaha Mali 1200746\nAfaf Amwas 1203359\n\n\n\n\n"
    names_label = Label(root, text=names_text, font=bold_font, bg='#b39ddb')
    names_label.pack(side=tk.BOTTOM, pady=(10, 0))


def main():
    global root
    root = tk.Tk()
    setup_main_window(root)

    # Set the window dimensions and position
    window_width = 900
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.mainloop()

if __name__ == "__main__":
    main()