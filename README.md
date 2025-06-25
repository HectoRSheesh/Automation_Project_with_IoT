flowchart TB
  Basla["Başla"] --> Yapilandirma["Config.py Yükle (eşik değerler ve GPIO pinleri)"]
  Yapilandirma --> Baslat["GPIO ve DHT22 Başlat"]
  Baslat --> AnaDongu["ANA DÖNGÜ(her 10 saniye)"]
  Baslat --> WebSunucu["Web Sunucusu Başlat(API)"]

  subgraph SensorDongusu["Sensör Döngüsü"]
    AnaDongu --> DhtOku["DHT22 Sensörünü Oku"]
    DhtOku --> Kontrol{" Nem<%40 VEYA Sıcaklık>30°C?"}
    Kontrol -- evet --> OtoAc["Sulamayı Başlat()(5 sn)"]
    Kontrol -- hayır --> Atla["Sulamayı Atla"]
    OtoAc --> OtoKapat["Sulamayı Durdur()"]
    OtoKapat --> KayitOto["Otomatik Olay Kaydet"]
    Atla --> Bekle["10 s Bekle"]
    KayitOto --> Bekle
    Bekle --> AnaDongu
  end

  subgraph WebKontrol["Web Kontrolü"]
    WebSunucu --> Dinle["Manuel Komutları Dinle"]
    Dinle -- manuel? --> ManAc["Sulamayı Başlat()"]
    ManAc --> ManKapat["Sulamayı Durdur()"]
    ManKapat --> KayitMan["Manuel Olay Kaydet"]
    KayitMan --> Dinle
  end
