# 🔍 Stealer Log Analiz Botu

Bu bot, Telegram üzerinden paylaşılan stealer loglarını (.zip veya .rar) analiz eder ve içeriğinde şüpheli dosyaların varlığını kontrol eder.

## 🌟 Özellikler

### 📸 Screenshot Analizi
- PNG, JPG, JPEG, BMP formatlarını destekler
- Resim boyutları ve formatı hakkında bilgi verir
- Bulunan screenshot sayısını raporlar

### 🌐 Browser Veri Analizi
- Chrome, Firefox, Opera, Edge verilerini analiz eder
- Login bilgileri
- Tarama geçmişi
- Çerezler ve oturum bilgileri
- Otomatik doldurma verileri

### 🔐 Hassas Dosya Analizi
- passwords.txt
- browsers.log
- cookies.txt
- wallets.json (kripto cüzdan bilgileri)
- telegram_desktop
- discord_token.txt
- system_info.txt

### 🔍 Veri Tespiti
- Email adresleri
- Kripto cüzdan adresleri
- Discord tokenları
- Sistem bilgileri
- Clipboard içeriği

### 📊 Detaylı Raporlama
- Dosya adı ve boyutu
- Analiz zamanı
- Gönderen kişi bilgisi
- Bulunan şüpheli dosyalar
- İçerik önizlemeleri

## 🚀 Test Grubu

Bot şu anda test aşamasındadır. Test grubuna katılmak için: [Stealer Log Analiz Test Grubu](https://t.me/denemegrubuu)

## 💻 Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/dmedya/telegramdeneme.git
```

2. Sanal ortam oluşturun:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

4. config.py dosyası oluşturun:
```python
TOKEN = "YOUR_BOT_TOKEN"  # BotFather'dan aldığınız token'ı buraya yazın
```

5. Botu çalıştırın:
```bash
python telegram_bot.py
```

## 🛡️ Güvenlik Önlemleri

- Token'ınızı asla GitHub'a push etmeyin
- config.py dosyası .gitignore'da olmalı
- Hassas bilgileri paylaşmayın
- Geçici dosyalar otomatik silinir
- Sadece .zip ve .rar dosyaları kabul edilir

## ⚠️ Uyarı

Bu bot sadece eğitim amaçlıdır. Kötüye kullanım yasaktır.

## 📝 Örnek Kullanım

1. Botu gruba ekleyin
2. /start komutu ile botu başlatın
3. Analiz edilecek .zip/.rar dosyasını gönderin
4. Bot otomatik olarak analiz edip detaylı rapor verecektir

## 🤝 Katkıda Bulunma

1. Bu repo'yu fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun
