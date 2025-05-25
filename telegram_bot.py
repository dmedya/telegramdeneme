import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import zipfile
import datetime
import json
import re
from PIL import Image
import io
import sqlite3
import base64
from config import TOKEN

async def analyze_browser_data(content):
    browser_data = {
        'passwords': [],
        'history': [],
        'cookies': [],
        'autofill': []
    }
    
    # Browser veri formatlarını kontrol et
    try:
        # SQLite formatında browser verileri
        if b'SQLite format 3' in content[:16]:
            temp_db = 'temp_browser.db'
            with open(temp_db, 'wb') as f:
                f.write(content)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Login verilerini kontrol et
            try:
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                browser_data['passwords'] = ["URL: {}, Kullanıcı: {}".format(row[0], row[1]) 
                                          for row in cursor.fetchall()]
            except: pass
            
            # Geçmişi kontrol et
            try:
                cursor.execute("SELECT url, title, visit_count FROM urls")
                browser_data['history'] = ["Site: {}, Başlık: {}, Ziyaret: {}".format(row[0], row[1], row[2]) 
                                         for row in cursor.fetchall()]
            except: pass
            
            conn.close()
            os.remove(temp_db)
            
        # JSON formatında browser verileri
        elif content.startswith(b'{'):
            try:
                json_data = json.loads(content)
                if 'cookies' in json_data:
                    browser_data['cookies'] = [f"Domain: {c.get('domain', 'N/A')}" for c in json_data['cookies']]
                if 'passwords' in json_data:
                    browser_data['passwords'] = [f"Site: {p.get('url', 'N/A')}" for p in json_data['passwords']]
            except: pass
            
    except Exception as e:
        return f"Browser veri analizi hatası: {str(e)}"
    
    return browser_data

async def analyze_screenshot(image_data):
    try:
        # Screenshot'ı aç ve analiz et
        img = Image.open(io.BytesIO(image_data))
        width, height = img.size
        format_type = img.format
        
        return f"Screenshot bulundu:\n" \
               f"- Boyut: {width}x{height}\n" \
               f"- Format: {format_type}"
    except:
        return "Geçersiz screenshot formatı"

async def analyze_file_content(file_path, file_name):
    analysis_result = ""
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Şüpheli dosyaları kontrol et
            suspicious_files = {
                'passwords.txt': ['password', 'username', 'login'],
                'browsers.log': ['chrome', 'firefox', 'edge', 'cookie'],
                'cookies.txt': ['cookie', 'session'],
                'wallets.json': ['wallet', 'bitcoin', 'ethereum'],
                'telegram_desktop': ['tdata', 'telegram'],
                'discord_token.txt': ['token', 'discord'],
                'system_info.txt': ['windows', 'os', 'cpu', 'ram']
            }
            
            found_files = []
            screenshot_count = 0
            browser_data_found = False
            
            for file_info in zip_ref.filelist:
                file_lower = file_info.filename.lower()
                
                # Screenshot kontrolü
                if file_lower.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    with zip_ref.open(file_info.filename) as f:
                        screenshot_analysis = await analyze_screenshot(f.read())
                        found_files.append({
                            'name': file_info.filename,
                            'size': file_info.file_size,
                            'analysis': screenshot_analysis
                        })
                        screenshot_count += 1
                
                # Browser veri kontrolü
                elif any(ext in file_lower for ext in ['.sqlite', '.db', '.json']):
                    with zip_ref.open(file_info.filename) as f:
                        browser_analysis = await analyze_browser_data(f.read())
                        if any(browser_analysis.values()):
                            browser_data_found = True
                            found_files.append({
                                'name': file_info.filename,
                                'size': file_info.file_size,
                                'analysis': 'Browser verisi bulundu',
                                'details': browser_analysis
                            })
                
                # Diğer şüpheli dosyalar
                else:
                    for susp_file, keywords in suspicious_files.items():
                        if any(keyword in file_lower for keyword in keywords):
                            with zip_ref.open(file_info.filename) as f:
                                try:
                                    content = f.read().decode('utf-8')
                                    sensitive_data = analyze_sensitive_data(content)
                                    found_files.append({
                                        'name': file_info.filename,
                                        'size': file_info.file_size,
                                        'analysis': sensitive_data
                                    })
                                except:
                                    found_files.append({
                                        'name': file_info.filename,
                                        'size': file_info.file_size,
                                        'analysis': 'Binary/encrypted içerik'
                                    })
            
            # Analiz sonuçlarını formatla
            if found_files:
                analysis_result += "\n🔍 Detaylı Analiz:\n"
                
                if screenshot_count > 0:
                    analysis_result += f"\n📸 Screenshot Sayısı: {screenshot_count}\n"
                
                if browser_data_found:
                    analysis_result += "\n🌐 Browser Verileri Tespit Edildi\n"
                
                for file in found_files:
                    analysis_result += f"\n📄 Dosya: {file['name']}"
                    analysis_result += f"\n📊 Boyut: {file['size']} bytes"
                    analysis_result += f"\n⚠️ Analiz: {file['analysis']}"
                    
                    if 'details' in file and isinstance(file['details'], dict):
                        for key, value in file['details'].items():
                            if value:
                                analysis_result += f"\n- {key.capitalize()}: {len(value)} adet bulundu"
                    
                    analysis_result += "\n"
            else:
                analysis_result += "\n✅ Şüpheli içerik bulunamadı."
                
    except Exception as e:
        analysis_result += f"\n❌ Analiz hatası: {str(e)}"
    
    return analysis_result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! Ben log analiz botuyum. "
        "Gruba .zip veya .rar dosyası gönderebilirsiniz."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Kullanım:\n"
        "1. Gruba bir .zip veya .rar dosyası gönderin\n"
        "2. Ben içeriğini analiz edip rapor edeceğim\n"
        "3. /start - Botu başlat\n"
        "4. /help - Yardım menüsü"
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Dosyayı al
        file = await update.message.document.get_file()
        file_name = update.message.document.file_name
        file_size = update.message.document.file_size
        user = update.effective_user

        if file_name.endswith(('.zip', '.rar')):
            await update.message.reply_text("🔍 Dosya alındı, analiz ediliyor...")
            
            # Dosyayı geçici olarak kaydet
            await file.download_to_drive("temp_analysis.zip")
            
            # Analiz zamanı
            analysis_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Detaylı analiz yap
            detailed_analysis = await analyze_file_content("temp_analysis.zip", file_name)
            
            # Rapor oluştur
            analysis_result = f"""
📁 Stealer Log Analizi:
📌 Dosya Adı: {file_name}
📊 Boyut: {file_size} bytes
⏰ Analiz Zamanı: {analysis_time}
👤 Gönderen: {user.first_name} (@{user.username})

{detailed_analysis}
"""
            # Geçici dosyayı sil
            os.remove("temp_analysis.zip")
            
            await update.message.reply_text(analysis_result)
        else:
            await update.message.reply_text("⚠️ Lütfen sadece .zip veya .rar dosyası gönderin.")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Hata oluştu: {str(e)}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("Bot başlatıldı...")
    application.run_polling()

if __name__ == '__main__':
    main()
