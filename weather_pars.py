import requests
from bs4 import BeautifulSoup
import json

# Функция для получения температуры с указанной страницы
def get_temperature(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        temperature_element = soup.find('td', class_='weather-temperature')
        
        if temperature_element:
            temperature = temperature_element.find('span').text.strip()
            return temperature
        else:
            print(f"Не удалось найти элемент с температурой на странице: {url}")
            return None
    else:
        print(f"Ошибка при запросе страницы: {response.status_code} для URL: {url}")
        return None

# Функция для получения температуры за месяц для указанного города
def get_monthly_weather(city_name, base_url, days_in_month=30):
    weather_data = {}
    
    for day in range(1, days_in_month + 1):
        url = f"{base_url}/{day:02d}-november/"
        temperature = get_temperature(url)
        
        if temperature:
            weather_data[f"{day:02d} november"] = temperature
    
    return weather_data

# Основной код
if __name__ == "__main__":
    # Получаем данные для Москвы
    moscow_base_url = "https://world-weather.ru/pogoda/russia/moscow"
    moscow_weather = get_monthly_weather("Moscow", moscow_base_url)
    
    # Получаем данные для Ханоя
    hanoi_base_url = "https://world-weather.ru/pogoda/vietnam/ha_noi"
    hanoi_weather = get_monthly_weather("Hanoi", hanoi_base_url)
    
    # Получаем данные для Гаваны
    havana_base_url = "https://world-weather.ru/pogoda/cuba/havana"
    havana_weather = get_monthly_weather("Havana", havana_base_url)

    # Сохраняем данные в формате JSON
    all_weather_data = {
        "Moscow": moscow_weather,
        "Hanoi": hanoi_weather,
        "Havana": havana_weather
    }

    with open('weather_data_november.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_weather_data, json_file, ensure_ascii=False, indent=4)

    print("Данные о температуре за ноябрь сохранены в файл weather_data_november.json.")