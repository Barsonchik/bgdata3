import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from hdfs import InsecureClient

# Загрузка данных из файла JSON
with open('weather_data_november.json', 'r', encoding='utf-8') as file:
    weather_data = json.load(file)

# Создание DataFrame для хранения данных о температуре
temperature_data = []
for city, data in weather_data.items():
    for date, temperature in data.items():
        temperature_data.append((city, date, temperature))

df = pd.DataFrame(temperature_data, columns=['City', 'Date', 'Temperature'])

# Преобразование столбца 'Date' в формат даты с добавлением года
df['Date'] = pd.to_datetime(df['Date'] + ' 2024')

# Построение графиков изменения температуры в разных городах
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='Date', y='Temperature', hue='City', marker='o')
plt.title('Temperature Change in Different Cities (November)')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('temperature_change.png')
plt.show()

# Построение графика распределения температуры
plt.figure(figsize=(8, 6))
sns.histplot(df['Temperature'], bins=10, kde=True)
plt.title('Распределение температуры в ноябре')
plt.xlabel('Температура (°C)')
plt.ylabel('Частота')
plt.grid(True)
plt.tight_layout()
plt.savefig('temperature_distribution.png')
plt.show()

# Сохранение результатов в HDFS
client = InsecureClient('http://localhost:9870')
with client.write('/home/hloop/dfsdata/datanode/temperature_change.png', encoding='utf-8') as stream:
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Date', y='Temperature', hue='City', marker='o')
    plt.title('Temperature Change in Different Cities (November)')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(stream)

with client.write('/home/hloop/dfsdata/datanode/temperature_distribution.png', encoding='utf-8') as stream:
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Temperature'], bins=10, kde=True)
    plt.title('Распределение температуры в ноябре')
    plt.xlabel('Температура (°C)')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(stream)

# Выгрузка результатов из HDFS на локальный компьютер
client.download('/user/weather/temperature_change.png', 'temperature_change_hdfs.png', overwrite=True)
client.download('/user/weather/temperature_distribution.png', 'temperature_distribution_hdfs.png', overwrite=True)

print('Графики успешно сохранены в HDFS и загружены на локальный компьютер.')