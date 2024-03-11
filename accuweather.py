import calendar
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_monthly_weather(driver, month, year):
    # Bangun URL untuk bulan dan tahun yang spesifik
    base_url = "https://www.accuweather.com/en/id/jakarta/208971/"
    month_name = calendar.month_name[month].lower()
    url = f"{base_url}{month_name}-weather/208971?year={year}"

    driver.get(url)
    time.sleep(5)  # Biarkan waktu untuk halaman untuk memuat sepenuhnya

    # Mendapatkan data tanggal, suhu tinggi, dan suhu rendah
    dates = driver.find_elements(By.CSS_SELECTOR, ".date")
    highs = driver.find_elements(By.CSS_SELECTOR, ".high")
    lows = driver.find_elements(By.CSS_SELECTOR, ".low")

    # Menyusun data
    monthly_weather_data = {}
    for date, high, low in zip(dates, highs, lows):
        date_text = date.text
        high_temp = high.text
        low_temp = low.text
        monthly_weather_data[date_text] = {'High Temp': high_temp, 'Low Temp': low_temp}

    return monthly_weather_data

# Menyimpan data ke excel
def save_to_excel(data, month, year):
    df = pd.DataFrame.from_dict(data, orient='index')

    file_name = f"data_{calendar.month_name[month].lower()}_{year}.xlsx"
    df.to_excel(file_name)
    print(f"Data telah disimpan dalam file: {file_name}")

driver = webdriver.Chrome()  

# Rentang tahun yang diinginkan
start_year = 2023
end_year = 2024

for year in range(start_year, end_year + 1):
    # Bulan Januari - Desember (1-12)
    for month in range(1, 13): 
        monthly_weather_data = scrape_monthly_weather(driver, month, year)
        save_to_excel(monthly_weather_data, month, year)

driver.quit()

