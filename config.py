# config.py
# Bu dosya, gerçek donanım kullanımı için yapılandırma ayarlarını içerir.
# Ayarlar; sensör okuma, sulama sistemi kontrolü ve
# donanım bağlantıları için gerekli parametreleri tanımlar.

# SIMULATION modunu kapatın:
# Gerçek donanımın kullanılmasını sağlayın.
# Eğer bu değeri True yaparsanız, simülasyon ortamı veya test modu kullanılır.
SIMULATION = True
# Eşik değerler:
# Aşağıdaki sıcaklık ve nem değerleri, sulamanın devreye girme koşullarını belirler.
# Örneğin, sıcaklık 30°C'nin üzerinde veya nem %40'ın altında ise sulama sistemi çalıştırılabilir.
TEMPERATURE_THRESHOLD = 30.0  # Sulama için üst sıcaklık eşiği (°C)
HUMIDITY_THRESHOLD = 40.0     # Sulama için alt nem eşiği (%)

# Sulama süresi:
# Su pompasının kaç saniye çalıştırılacağını belirler; bu örnekte 10 saniye.
WATERING_DURATION = 10  # Su pompası 10 saniye boyunca çalıştırılır.

# Sensör okuma aralığı:
# Sensörlerden veri alma sıklığını saniye cinsinden belirler.
SENSOR_READ_INTERVAL = 5  # Her 5 saniyede bir sensör verileri okunur.

# Gerçek donanımda kullanılacak DHT sensörünün tipi ve
# bu sensörün veri pinine bağlı olduğu GPIO pini:
# Örneğin, DHT22 sensörü kullanılıyorsa SENSOR_TYPE "DHT22" olarak ayarlanır.
SENSOR_TYPE = "DHT22"  # Kullanılacak sensör tipi; "DHT22" veya "DHT11" olabilir.
DHT_PIN = 4            # DHT sensörünün bağlı olduğu GPIO pini (örneğin, Raspberry Pi üzerinde 4 numaralı pin).

# Röle kontrolü için kullanılacak GPIO pini:
# Bu pin, su pompasını kontrol eden rölenin bağlı olduğu pindir.
RELAY_PIN = 17  # Rölenin kontrol edildiği GPIO pini (örneğin, 17 numaralı pin).