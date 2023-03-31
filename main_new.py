import tkinter.filedialog
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fft as fft
import tkinter as tk


def get_filename():
    tk.Tk().withdraw()
    return tkinter.filedialog.askopenfile(filetypes=[('ASCII file', '.asc')])


def fix(data_filtered):
    for i in range(len(data_filtered)):
        if data_filtered[i] > 50:
            data_filtered[i] = 50
        if data_filtered[i] < -50:
            data_filtered[i] = -50
    return data_filtered


k = 1
fs = 200
alpha = fs // k


def main():
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 8)
    filename = get_filename()
    data = np.loadtxt(filename, skiprows=4, usecols=1)

    data_corrected = data - np.mean(data)
    high = 20 / (1000 / 2)
    low = 450 / (1000 / 2)
    b, a = signal.butter(4, [high, low], btype='bandpass')
    data_filtered = signal.filtfilt(b, a, data_corrected)
    start = 0
    x_axis = []
    for i in range(len(data_filtered)):
        x_axis.append(start)
        start += 1 / fs
    x_axis = np.array(x_axis)
    plt.subplot(2, 1, 1)
    plt.grid()
    plt.plot(x_axis, data_filtered)
    # plt.plot(x_axis, np.zeros_like(data_filtered) + 30, color='red', label='Desync')

    analytics = []
    for j in range(0, len(data_filtered) - alpha, alpha):
        peaks, _ = signal.find_peaks(data_filtered[j:j + alpha], height=30)
        # plt.plot(peaks, data_filtered[peaks], '.')
        stat = data_filtered[peaks]
        print(stat)
        analytics.append(len(stat))
    start = 0
    x_axis = []
    for i in range(len(analytics)):
        x_axis.append(start)
        start += 1 / (fs / alpha)
    x_axis = np.array(x_axis)
    plt.subplot(2, 1, 2)
    plt.plot(x_axis, analytics)
    # plt.subplot(3, 1, 3)
    # plt.plot(np.diff(analytics))
    # plt.plot(np.zeros_like(analytics), color='red', label='desync')
    # plt.show()

    start = 0
    x_axis = []
    for i in range(len(data_filtered)):
        x_axis.append(start)
        start += 1 / fs
    x_axis = np.array(x_axis)

    plt.subplot(2, 1, 1)
    plt.grid()
    plt.plot(x_axis, data_filtered)
    # plt.plot(x_axis, np.zeros_like(analytics) + 30, color='red', label='Desync')
    plt.xlabel('Time, sec')
    plt.ylabel('Amplitude')
    plt.subplots_adjust(hspace=0.5)
    analytics = []
    for j in range(0, len(data_filtered) - alpha, alpha):
        s = np.average(np.abs(data_filtered[j:j + alpha]))
        analytics.append(s)

    start = 0
    x_axis = []
    for i in range(len(analytics)):
        x_axis.append(start)
        start += 1 / (fs / alpha)
    x_axis = np.array(x_axis)

    # plt.subplot(3, 1, 2)
    # plt.grid()
    # plt.plot(x_axis, analytics)
    # plt.xlabel('Time, sec')
    #
    # plt.subplot(3, 1, 3)
    # plt.title('Diff')
    # plt.grid()
    # plt.plot(np.diff(analytics))
    # plt.plot(np.zeros_like(analytics) - 2.5, color='red', label='Desync')
    # plt.legend()
    # plt.xlabel('Time, sec')
    plt.show()


root = tk.Tk()
root.title('EMG Analyzer')

button = tk.Button(root, text='Загрузить файл', command=main)
button.pack()

root.mainloop()
