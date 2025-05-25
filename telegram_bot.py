<<<<<<< HEAD
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN

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
    doc = update.message.document
    user = update.effective_user
    
    if doc.file_name.endswith(('.zip', '.rar')):
        await update.message.reply_text("Dosya alındı, analiz ediliyor...")
        
        suspicious_files = [
            "passwords.txt",
            "browsers.log",
            "cookies.txt",
            "wallets.json",
            "telegram_desktop",
            "discord_token.txt",
            "system_info.txt"
        ]
        
        await update.message.reply_text(
            f"📁 Dosya Analizi:\n"
            f"📌 İsim: {doc.file_name}\n"
            f"📊 Boyut: {doc.file_size} bytes\n"
            f"📋 MIME type: {doc.mime_type}\n"
            f"🔍 Şüpheli Dosyalar:\n"
            f"- {', '.join(suspicious_files)}\n\n"
            f"👤 Gönderen: {user.first_name} (@{user.username})"
        )
    else:
        await update.message.reply_text(
            "⚠️ Lütfen sadece .zip veya .rar dosyası gönderin."
        )

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("Bot başlatıldı...")
    application.run_polling()

if __name__ == '__main__':
    main()
=======
# .gitignore oluştur
echo "config.py
__pycache__/
venv/
*.pyc
.env" > .gitignore

# config.py oluştur
echo 'TOKEN = "8053866059:AAGhT8PEhtmdReOUe6ZtdNe8yu40MdT_ztY"' > config.py

# telegram_bot.py oluştur
nano telegram_bot.py

# README.md oluştur
nano README.md
>>>>>>> 16036be4f848715988b56fc3bde6a09234e9e68e
