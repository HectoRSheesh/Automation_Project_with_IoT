# main.py
import time
# sensor modülünden sensör verilerini okumak için tanımlı fonksiyonu içe aktarır.
from sensor import get_sensor_data
# irrigation modülünden sulama başlatma ve temizlik işlemleri için tanımlı fonksiyonları içe aktarır.
from irrigation import start_irrigation, cleanup
# config modülünden sensör okuma aralığı ve eşik değerleri (sıcaklık & nem) içe aktarılır.
from config import SENSOR_READ_INTERVAL, TEMPERATURE_THRESHOLD, HUMIDITY_THRESHOLD
def main():
    # Program başlatıldığını kullanıcıya bildirir.
    print("Otomatik sulama sistemi başlatıldı.")
    try:
        # Sonsuz döngü sayesinde sürekli olarak sensör verileri okunur.
        while True:
            # Sensör verilerini alır (sıcaklık ve nem).
            temperature, humidity = get_sensor_data()
            # Eğer sensörden alınan veri None (geçersiz) ise, hata mesajı yazdırılır.
            if temperature is None or humidity is None:
                print("Sensör verileri okunamadı, yeniden deneniyor...")
            else:
                # Alınan geçerli sıcaklık ve nem değerleri ekrana yazdırılır.
                print("Sıcaklık: {:.2f} °C, Nem: {:.2f} %".format(temperature, humidity))
                # Belirlenen eşik değerlerin kontrolü:
                # Eğer nem değeri HUMIDITY_THRESHOLD değerinin altındaysa veya sıcaklık değeri
                # TEMPERATURE_THRESHOLD değerinin üstündeyse, sulama işlemini başlatır.
                if humidity < HUMIDITY_THRESHOLD or temperature > TEMPERATURE_THRESHOLD:
                    print("Koşullar uygun, otomatik sulama başlatılıyor...")
                    start_irrigation()
                else:
                    # Eşik değerler sağlanmadıysa, sulamanın yapılmaması gerektiğini bildirir.
                    print("Şu anda sulamaya gerek yok.")
            # Sensör verilerinin okunması arasında belirli bir süre bekler.
            time.sleep(SENSOR_READ_INTERVAL)
    except KeyboardInterrupt:
        # Kullanıcı Ctrl+C gibi bir kesme komutu gönderdiğinde, düzgün çıkış yapıldığını bildirir.
        print("\nProgram kullanıcı tarafından sonlandırıldı.")
    finally:
        # Program sonlanmadan önce, sulama sistemine ait kaynaklar temizlenir.
        cleanup()
if __name__ == "__main__":
    # Dosya doğrudan çalıştırıldığında main fonksiyonunu çağırır.
    main()