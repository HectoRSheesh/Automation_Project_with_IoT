# IoT Destekli Otomatik Sulama Sistemi

```mermaid
flowchart TD
  A([Başlat]) --> B{Donanim Baglantilari\nBasarili mi?}
  B -- Hayir --> V[Hata Logu\nAlert] --> G[10 sn Bekle]
  B -- Evet --> C[Config.py Yukle\n(esik degerler)]
  C --> D[Web_control.py Baslat\n(HTTP & Socket)]
  D --> E[Sensor.py Baslat\n(DHT22)]
  E --> F[Irrigation.py Baslat\n(Role Kontrol)]
  F --> G

  G --> U{Sensor Okuma\nHatasi?}
  U -- Evet --> V
  V --> G
  U -- Hayir --> H[Sensor Verisi Al\n(Sicaklik, Nem)]

  H --> P[Web'den "Sulama Baslat" Komutu?]
  P -- Evet --> R[Manuel Pompa Aktive\n5 sn]
  R --> S[Log Olustur\nUI Guncelle]
  S --> G
  P -- Hayir --> I{Nem < 40% Veya\nSicaklik > 30°C?}

  I -- Evet --> J[Aktif Sulama]
  J --> K[Pompayi 5 sn Calistir]
  K --> L[Log Kaydi Olustur]
  L --> M[UI'yi Guncelle]
  M --> G

  I -- Hayir --> N[Sulama Yok]
  N --> O[UI'ye Guncel Sensor Verisi Gonder]
  O --> G
