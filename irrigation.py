# irrigation.py
import time
from config import WATERING_DURATION, SIMULATION, RELAY_PIN
# Eğer simülasyon modu kapalıysa yani gerçek donanım kullanılıyorsa,
# RPi.GPIO kütüphanesini içe aktarır, GPIO ayarlarını yapar ve röleyi başlangıçta kapalı konuma getirir.
if not SIMULATION:
    import RPi.GPIO as GPIO
    # GPIO pinlerini Broadcom SOC kanal numaraları ile kullanmak için ayarlanır.
    GPIO.setmode(GPIO.BCM)
    # Belirtilen röle pini çıkış olarak yapılandırılır.
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    # Röle, genellikle HIGH durumunda kapalı, LOW durumunda aktif olduğundan,
    # başlangıçta röleyi kapalı (HIGH) konuma alır.
    GPIO.output(RELAY_PIN, GPIO.HIGH)
def start_irrigation():
    """Gerçek donanımda sulama işlemini başlatır; röle aktif hale getirilir.
    Simülasyon modunda ise sulama işlemi simüle edilir."""
    if SIMULATION:
        # Simülasyon modunda sulama başladığını terminale basar.
        print("Sulama başlatıldı... (Simülasyon)")
    else:
        import RPi.GPIO as GPIO
        # Gerçek modda röleyi aktif hale getirir; LOW duruma alarak sulamayı başlatır.
        GPIO.output(RELAY_PIN, GPIO.LOW)
        print("Gerçek donanımda sulama başladı.")
    # Sulama işlemi için belirlenmiş süre kadar bekler.
    time.sleep(WATERING_DURATION)
    # Belirtilen süre sonunda sulamayı durdurmak için stop_irrigation() fonksiyonunu çağırır.
    stop_irrigation()
def stop_irrigation():
    """Gerçek donanımda sulama işlemini durdurur; röle pasif konuma getirilir.
    Simülasyon modunda ise sulama işleminin durduğunu simüle eder."""
    if SIMULATION:
        # Simülasyon modunda sulama durdurulduğunu terminale basar.
        print("Sulama durduruldu... (Simülasyon)")
    else:
        import RPi.GPIO as GPIO
        # Gerçek modda röleyi pasif hale getirir; HIGH durumuna getirerek sulamayı sonlandırır.
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Gerçek donanımda sulama durduruldu.")
def cleanup():
    """Eğer gerçek modda kullanılmaktaysa, GPIO pin yapılandırmasını temizler.
    Bu, program sonlanırken düzgün kaynak yönetimi için önemlidir."""
    if not SIMULATION:
        import RPi.GPIO as GPIO
        GPIO.cleanup()
if __name__ == "__main__":
    # Dosya doğrudan çalıştırıldığında, start_irrigation() fonksiyonunu çağırarak sulama işlemini test eder.
    start_irrigation()