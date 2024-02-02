import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from anonfile import AnonFile

# Replace with your Telegram bot API key
TELEGRAM_API_KEY = 'YOUR_TELEGRAM_API_KEY'

# Replace with your Anonfile API key
ANONFILE_API_KEY = 'YOUR_ANONFILE_API_KEY'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the File Uploader Bot! Send me any file, and I will upload it to Anonfile and send you the link.')

def handle_file(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file_path = file.download()

    anonfile = AnonFile(ANONFILE_API_KEY)
    upload_response = anonfile.upload(file_path)

    if upload_response['status']:
        file_link = upload_response['data']['file']['url']['short']
        update.message.reply_text(f'File uploaded successfully! Here is the link: {file_link}')
    else:
        update.message.reply_text('Error uploading the file. Please try again.')

    # Optionally, you can remove the local file after uploading to Anonfile
    os.remove(file_path)

def main() -> None:
    updater = Updater(TELEGRAM_API_KEY)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_file))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
