from tkinter import *  # Tkinter kütüphanesinden her şeyi içe aktar

from PIL import ImageTk, Image  # PIL kütüphanesinden ImageTk ve Image sınıflarını içe aktar

import requests  # requests kütüphanesini içe aktar

url = "http://api.openweathermap.org/data/2.5/weather"  # Hava durumu verilerini çekeceğimiz URL

api_key = "48fa1272d9f1a6912367ba9b34ede792"  # OpenWeatherMap API anahtarı

iconUrl = "http://openweathermap.org/img/wn/{}@2x.png"  # Hava durumu ikonlarının bulunduğu URL

def getWeather(city):
    # Belirtilen şehrin hava durumu verilerini almak için API'yi kullan
    params = {'q':city,'appid':api_key,'lang':'tr'}  # API isteği için gerekli parametreler
    data = requests.get(url,params=params).json()  # API'ye istek gönder ve JSON verisini al
    if data:  # Veri başarıyla alındıysa
        city = data['name'].capitalize()  # Şehir adını büyük harfle başlatarak al
        country = data['sys']['country']  # Ülke kodunu al
        temp = int(data['main']['temp'] - 273.15)  # Sıcaklık birimi Kelvin olduğundan Celcius'a çevir
        icon = data['weather'][0]['icon']  # Hava durumu ikonunu al
        condition = data['weather'][0]['description']  # Hava durumu durumunu al
        return (city,country,temp,icon,condition)  # Verileri tuple olarak döndür

def main():
    city = entryCity.get()  # Kullanıcının girdiği şehir adını al
    weather = getWeather(city)  # Şehir için hava durumu verilerini al
    if weather:  # Veriler başarıyla alındıysa
        locaitonLabel['text'] = '{},{}'.format(weather[0],weather[1])  # Şehir ve ülke kodunu gösteren etiketi güncelle
        tempLabel['text'] = '{}°C'.format(weather[2])  # Sıcaklık değerini gösteren etiketi güncelle
        conditionLabel['text'] = weather[4]  # Hava durumu durumunu gösteren etiketi güncelle
        icon = ImageTk.PhotoImage(Image.open(requests.get(iconUrl.format(weather[3]),stream=True).raw))  # Hava durumu ikonunu al ve göster
        iconLabel.configure(image=icon)  # İkon görüntüsünü güncelle
        iconLabel.image = icon  # İkon görüntüsünü sakla

app = Tk()  # Tkinter uygulaması oluştur
app.geometry("300x450")  # Uygulama penceresinin boyutunu ayarla
app.title("Hava Durumu")  # Uygulama penceresinin başlığını ayarla
app.configure(bg="Orange")  # Arka plan rengini ayarla

entryCity = Entry(app, justify='center', width=20, font=("Arial", 14))  # Metin giriş kutusunu oluştur ve özelliklerini ayarla
#entryCity.insert(0, "Şehir Adı")  # Metin giriş kutusuna varsayılan metni ekle
entryCity.pack(fill = BOTH, ipady=10, padx=18, pady=5)  # Metin giriş kutusunu uygulamaya ekle

searchButton = Button(app, text="Arama", font=("Arial",16), command=main, bg="#004D63", fg="Orange", width=20)  # Arama butonunu oluştur ve özelliklerini ayarla
searchButton.pack(fill=BOTH, ipady=10, padx=20)  # Arama butonunu uygulamaya ekle

iconLabel = Label(app, bg="Orange")  # İkon görüntüsü için etiket oluştur
iconLabel.pack()  # İkon etiketini uygulamaya ekle

locaitonLabel = Label(app, font=("Arial",30), bg="Orange")  # Lokasyon etiketini oluştur ve özelliklerini ayarla
locaitonLabel.pack()  # Lokasyon etiketini uygulamaya ekle

tempLabel = Label(app, font=("Arial",30,"bold"), bg="Orange")  # Sıcaklık etiketini oluştur ve özelliklerini ayarla
tempLabel.pack()  # Sıcaklık etiketini uygulamaya ekle

conditionLabel = Label(app, font=("Arial",25), bg="Orange")  # Hava durumu durumu etiketini oluştur ve özelliklerini ayarla
conditionLabel.pack()  # Hava durumu durumu etiketini uygulamaya ekle

app.mainloop()  # Uygulamayı çalıştır

