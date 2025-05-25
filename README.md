# 🔍 Stealer Log Analiz Botu

Bu bot, Telegram üzerinden paylaşılan stealer loglarını (.zip veya .rar) analiz eder ve içeriğinde şüpheli dosyaların varlığını kontrol eder.

## 🚀 Test Grubu

Bot şu anda test aşamasındadır. Test grubuna katılmak için: [Stealer Log Analiz Test Grubu](https://t.me/denemegrubuu)

## 💻 Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/dmedya/telegramdeneme.git
```

2. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

3. config.py dosyası oluşturun:
```python
TOKEN = "YOUR_BOT_TOKEN"  # BotFather'dan aldığınız token'ı buraya yazın
```

4. Botu çalıştırın:
```bash
python telegram_bot.py
```

## 🔍 Bot Ne Yapar?

- Zip/Rar dosyalarını analiz eder
- Şüpheli dosyaları tespit eder:
  * passwords.txt
  * browsers.log
  * cookies.txt
  * wallets.json
  * telegram_desktop
  * discord_token.txt
  * system_info.txt
- Dosya bilgilerini raporlar
- Gönderen kişi bilgisini gösterir

## ⚠️ Güvenlik

- Token'ınızı asla GitHub'a push etmeyin
- config.py dosyası .gitignore'da olmalı
- Hassas bilgileri paylaşmayın

## ⚠️ Uyarı

Bu bot sadece eğitim amaçlıdır. Kötüye kullanım yasaktır.
