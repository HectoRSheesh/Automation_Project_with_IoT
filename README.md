

```mermaid
flowchart TD
  A([Başlat])
  B{Donanim Baglantilari\nBasarili mi?}
  C[Config.py Yukle\n(esik degerler)]
  D[Web_control.py Baslat\n(HTTP & Socket)]
  E[Sensor.py Baslat\n(DHT22)]
  F[Irrigation.py Baslat\n(Role Kontrol)]
  G[10 sn Bekle]
  H[Sensor Verisi Al\n(Sicaklik, Nem)]
  I{Nem < 40% Veya\nSicaklik > 30°C?}
  J[Aktif Sulama]
  K[Pompayi 5 sn Calistir]
  L[Log Kaydi Olustur]
  M[UI'yi Guncelle]
  N[Sulama Yok]
  O[UI'ye Guncel Sensor Verisi Gonder]
  P[Web'den "Sulama Baslat" Komutu?]
  Q{Komut Geldi mi?}
  R[Manuel Pompa Aktive\n5 sn]
  S[Log Olustur\nUI Guncelle]
  U{Sensor Okuma\nHatasi?}
  V[Hata Logu\nAlert]

  A --> B
  B -- Hayir --> V --> G
  B -- Evet --> C --> D --> E --> F --> G
  G --> U
  U -- Evet --> V --> G
  U -- Hayir --> H --> P
  P -- Evet --> R --> S --> G
  P -- Hayir --> I
  I -- Evet --> J --> K --> L --> M --> G
  I -- Hayir --> N --> O --> G 
