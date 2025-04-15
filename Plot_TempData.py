import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('temperature_data.csv')
data['Time (s)'] = data['Time (s)'].astype(float)
data['Temperature (deg C)'] = data['Temperature (deg C)'].astype(float)
data['Frame Number'] = data['Frame Number'].astype(int)

data_sorted = data.sort_values(by='Time (s)')

plt.scatter(data_sorted['Time (s)'], data_sorted['Temperature (deg C)'], label='Temperature Data')
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.title('Temperature vs Time under 35 nA of 10 MeV Cu3+ Beam Heating')
plt.axvline(x=4.565, color='black', linestyle='--', label='Faraday Cup Opened')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (deg C)')
plt.legend()
plt.show()