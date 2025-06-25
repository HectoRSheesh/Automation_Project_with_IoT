# sensor.py, config modülünden simülasyon modu, sensör tipi ve DHT pini değerlerini içe aktarır.
from config import SIMULATION, SENSOR_TYPE, DHT_PIN
# Eğer simülasyon modu kapalıysa, gerçek sensör verilerini okumak için Adafruit_DHT kütüphanesini içe aktarır.
if not SIMULATION:
    import Adafruit_DHT
def get_sensor_data():
    """Gerçek sensör verilerini (sıcaklık, nem) okur.
    SIMULATION kapalı ise, Adafruit_DHT kullanılarak sensör verisinin okunmasını sağlar."""
    if SIMULATION:
        # Simülasyon modundayken rastgele veri üretilir.
        import random
        # Sıcaklık değeri 20 ile 40 °C arasında rastgele belirlenir.
        temperature = random.uniform(20, 40)
        # Nem değeri 20 ile 80 % arasında rastgele belirlenir.
        humidity = random.uniform(20, 80)
    else:
        # Gerçek sensör verilerini okumak için:
        # SENSOR_TYPE kontrol edilerek kullanılacak sensör tipi belirlenir:
        # Eğer SENSOR_TYPE "DHT22" ise Adafruit_DHT.DHT22, değilse Adafruit_DHT.DHT11 kullanılır.
        sensor_type = Adafruit_DHT.DHT22 if SENSOR_TYPE == "DHT22" else Adafruit_DHT.DHT11
        # Belirtilen sensör tipi ve DHT_PIN değeriyle sensör verisi okunmaya çalışılır.
        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, DHT_PIN)
        # Eğer sensör verisi başarılı şekilde okunamadıysa hata mesajı yazdırılır.
        if humidity is None or temperature is None:
            print("Sensör verisi okunamadı.")
    # Okunan veya simüle edilmiş sıcaklık ve nem değerlerini döndürür.
    return temperature, humidity
# Eğer dosya doğrudan çalıştırılırsa (yani başka bir modül tarafından içe aktarılmamışsa):
if __name__ == "__main__":
    # get_sensor_data fonksiyonunu çağırarak sıcaklık ve nem verilerini elde eder.
    temp, hum = get_sensor_data()
    # Elde edilen verileri formatlanmış şekilde ekrana yazdırır.
    print("Sıcaklık: {:.2f} °C, Nem: {:.2f} %".format(temp, hum))