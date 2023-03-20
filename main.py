import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert

plt.rcParams['figure.figsize'] = [12, 8]

with open('file.asc') as file:
    for i in range(4):
        next(file)
    data = [list(map(float, line.split())) for line in file]

y = [row[1] for row in data]

time_step = 80/len(data)*1000
time_data = [i*time_step for i in range(len(data))]

analytical_signal = hilbert(y)

amplitude_envelope = np.abs(np.real(analytical_signal))

# построение графиков
plt.plot(time_data, y, label='ЭМГ', color='red')
plt.plot(time_data, amplitude_envelope, label='Преобразование Гильберта', color='green')

plt.xlabel('Время (мс)')
plt.ylabel('Амплитуда')
plt.suptitle('ЭМГ и преобразование Гильберта с фильтрацией')

plt.legend()
plt.show()
