import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

api_key = "48fa1272d9f1a6912367ba9b34ede792"  
url = "http://api.openweathermap.org/data/2.5/weather"

def get_city_data(city_name):
    try:
       
        cities_df = pd.read_csv('data/cities.csv')
       
        city_rows = cities_df[cities_df['city_name'].str.lower() == city_name.lower()]
        
        if city_rows.empty:
            return None, f"{city_name} does not exist in our database. Please enter a different city."

        
        station_id = city_rows.iloc[0]['station_id']
        coordinates = city_rows.iloc[0][['latitude', 'longitude']]
        
        weather_df = pd.read_parquet('data/daily_weather.parquet')
        city_weather = weather_df[weather_df['station_id'] == station_id]
        return city_weather, coordinates, None
    except FileNotFoundError as e:
        return None, None, str(e)

def getWeather(city, api_key, url):
    params = {'q': city, 'appid': api_key, 'lang': 'tr'}
    data = requests.get(url, params=params).json()
    if data:
        city = data['name'].capitalize()
        country = data['sys']['country']
        temp = int(data['main']['temp'] - 273.15)
        icon = data['weather'][0]['icon']
        condition = data['weather'][0]['description']
        return (city, country, temp, icon, condition)

def main():
    st.set_page_config(layout="wide")
    st.title("Hava Durumu Uygulaması")

    with st.sidebar:
        st.header("Tarihi Hava Durumu Verileri")
        city_name = st.text_input("Enter a city name:", value="Ankara")
        city_data, coordinates, error = get_city_data(city_name)

    if error:
        st.error(error)
        return

    if city_data is not None:
        city_data['year'] = city_data['date'].dt.year
        years = city_data['year'].drop_duplicates().sort_values()
        with st.sidebar:
            year = st.selectbox("Choose a year:", years)

        year_data = city_data[city_data['year'] == year]
        daily_avg_temp = year_data.groupby(year_data['date'].dt.dayofyear)['avg_temp_c'].mean()

       
        max_temp = year_data['max_temp_c'].max()
        min_temp = year_data['min_temp_c'].min()

        months = {1: 'Jan', 32: 'Feb', 60: 'Mar', 91: 'Apr', 121: 'May', 152: 'Jun',
                  182: 'Jul', 213: 'Aug', 244: 'Sep', 274: 'Oct', 305: 'Nov', 335: 'Dec'}

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_avg_temp.index, daily_avg_temp.values)
        ax.set_xticks(list(months.keys()))
        ax.set_xticklabels(list(months.values()))
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Temperature (°C)')
        ax.set_title(f'{year} yılında {city_name.title()} için Aya Göre Günlük Ortalama Sıcaklık')

        col1, col2 = st.columns([1,2])
        with col1:
            avg_temp = daily_avg_temp.mean()
            weather_data = getWeather(city_name, api_key, url)
            city, country, temp, icon, condition = weather_data

            st.write(f"""
            * The average temperature in {city_name.title()} for {year} was {avg_temp:.2f} °C.
            * The maximum temperature in {city_name.title()} for {year} was {max_temp:.2f} °C.
            * The minimum temperature in {city_name.title()} for {year} was {min_temp:.2f} °C.
            * The average temperature in {city_name.title()} for Now was {temp:.2f} °C.     
            """)
        
        with col2:
            if coordinates is not None:
               
                map_data = pd.DataFrame({'lat': [coordinates['latitude']], 'lon': [coordinates['longitude']]})
                st.map(map_data)
            st.pyplot(fig)


    with st.sidebar:
        st.header("Canlı hava durumu sorgula")
        weather_city = st.text_input("Şehir adı girin:")
        get_weather = st.button("Hava Durumunu Sorgula")

        weather_data = getWeather(weather_city, api_key, url)
        city, country, temp, icon, condition = weather_data
        
        if get_weather and weather_city:
            if weather_data:
                st.text(f"Şehir: {city}, Ülke: {country}")
                st.text(f"Sıcaklık: {temp}°C")
                st.text(f"Hava Durumu: {condition}")
                st.image(f"http://openweathermap.org/img/w/{icon}.png")
            else:
                st.error("Hava durumu verisi alınamadı.")
    

if __name__ == "__main__":
    main()
