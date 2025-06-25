from flask import Flask, render_template, request, jsonify, send_from_directory, \
    send_file  # Flask ve ilgili modüllerin import edilmesi
import threading  # Çoklu iş parçacığı (thread) yönetimi için
import time  # Zamanlayıcı işlemleri için
from sensor import get_sensor_data  # Sensör verilerini okumak için fonksiyon
from irrigation import start_irrigation, stop_irrigation, cleanup  # Sulama işlemlerini kontrol eden fonksiyonlar
from config import SENSOR_READ_INTERVAL, TEMPERATURE_THRESHOLD, \
    HUMIDITY_THRESHOLD  # Konfigürasyon parametreleri (okuma aralığı ve eşik değerleri)
import zipfile  # Dosya arşivleme işlemleri için
import os  # İşletim sistemiyle ilgili işlemler için
app = Flask(__name__)  # Flask uygulama nesnesi oluşturulur

# Global sensör verilerini saklamak için başlangıç değerleri tanımlanır.
sensor_data = {"temperature": 0.0, "humidity": 0.0}

# Otomatik sulama kontrolünün aktif olup olmadığını belirleyen bayrak (True -> otomatik sulama aktif)
automation_enabled = True
def sensor_loop():
    """
    Arka planda sürekli çalışarak sensör verilerini güncelleyen ve
    otomatik sulama koşullarını kontrol eden döngüyü tanımlar.
    """
    global sensor_data
    while True:
        # Sensör verilerini al (sıcaklık ve nem)
        temperature, humidity = get_sensor_data()
        # Eğer değer None gelirse, 0.0 değeri kullanılarak global sözlük güncellenir.
        sensor_data["temperature"] = temperature if temperature is not None else 0.0
        sensor_data["humidity"] = humidity if humidity is not None else 0.0

        # Güncellenen sensör verileri terminale yazdırılır.
        print("Sıcaklık: {:.2f} °C, Nem: {:.2f} %".format(sensor_data["temperature"], sensor_data["humidity"]))

        # Eğer otomatik sulama aktifse ve:
        # - Nem eşik değerinin altındaysa veya
        # - Sıcaklık eşik değerinin üstündeyse,
        # o zaman sulama işlemi başlatılır.
        if automation_enabled and (
                sensor_data["humidity"] < HUMIDITY_THRESHOLD or sensor_data["temperature"] > TEMPERATURE_THRESHOLD):
            print("Koşullar uygun, otomatik sulama başlatılıyor...")
            start_irrigation()

        # Sensör okuma işlemleri arasında belirlenmiş süre kadar beklenir.
        time.sleep(SENSOR_READ_INTERVAL)
@app.route("/")
def index():
    """Ana sayfa route'u: index.html şablonunu render ederek,
    güncel sensör verilerini ve otomatik sulama durumunu kullanıcıya iletir."""
    return render_template("index.html", sensor=sensor_data, automation=automation_enabled)
@app.route("/sensor", methods=["GET"])
def sensor():
    """Sensör verilerinin JSON formatında döndürüldüğü route.
    Bu sayede, istemciler (web tarayıcısı vb.) güncel verilere erişebilir."""
    return jsonify(sensor_data)
@app.route("/irrigation/start", methods=["POST"])
def irrigation_start():
    """POST isteği alındığında, ayrı bir iş parçacığı üzerinden sulama işlemini başlatır.
    Bu, ana uygulamayı bloklamadan sulamanın yapılabilmesini sağlar."""
    threading.Thread(target=start_irrigation).start()
    return jsonify({"status": "Sulama başlatıldı."})
@app.route("/irrigation/stop", methods=["POST"])
def irrigation_stop():
    """POST isteği alındığında, sulama işlemini durduran fonksiyonu çağırır."""
    stop_irrigation()
    return jsonify({"status": "Sulama durduruldu."})
@app.route("/automation/enable", methods=["POST"])
def enable_automation():
    """Otomatik sulamayı etkinleştiren route.
    Bu route çağrıldığında 'automation_enabled' bayrağı True olarak ayarlanır."""
    global automation_enabled
    automation_enabled = True
    return jsonify({"status": "Otomatik sulama etkinleştirildi."})
@app.route("/automation/disable", methods=["POST"])
def disable_automation():
    """Otomatik sulamayı devre dışı bırakan route.
    Bu route çağrıldığında 'automation_enabled' bayrağı False olarak ayarlanır."""
    global automation_enabled
    automation_enabled = False
    return jsonify({"status": "Otomatik sulama devre dışı bırakıldı."})
@app.route('/download-index', methods=['GET'])
def download_index():
    """'index.html' dosyasının indirilebilmesi için oluşturulan route.
    Kullanıcı, bu route aracılığıyla HTML dosyasını indirebilir."""
    return send_from_directory(directory='templates', filename='index.html', as_attachment=True)
@app.route('/download-zip', methods=['GET'])
def download_zip():
    """Tüm proje dosyalarını bir ZIP arşivine ekleyip,
    kullanıcıya indirilmek üzere sunan route."""
    zip_filename = 'proje_dosyalar.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Belirli dosyalar arşive eklenir (şablon, konfigürasyon ve diğer modüller)
        zipf.write('templates/index.html', arcname='index.html')
        zipf.write('config.py')
        zipf.write('sensor.py')
        zipf.write('irrigation.py')
        zipf.write('main.py')
        zipf.write('web_control.py')
    # Oluşturulan ZIP dosyası dosya gönderim fonksiyonu ile kullanıcıya sunulur.
    response = send_file(zip_filename, as_attachment=True)
    # İstenirse; dosyanın gönderim sonrası silinmesi için:
    # os.remove(zip_filename)
    return response
if __name__ == "__main__":
    # Arka planda sensör verilerini sürekli güncellemek için 'sensor_loop' fonksiyonu bir iş parçacığında çalıştırılır.
    # daemon=True sayesinde ana uygulamayla birlikte sonlandırılır.
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()

    # Flask web sunucusu belirtilen host ve portta başlatılır.
    app.run(host="0.0.0.0", port=5002)
