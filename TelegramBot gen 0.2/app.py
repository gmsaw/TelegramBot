from typing import Final, List
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from laprak import ralat, generate_variations_rk
from gendocx import *

TOKEN: Final = "7199270076:AAElLVjPu1WpmpbAmpD6fnYd8Q_hN2XfXAg"
BOT_USERNAME: Final = "@gmsawBot"

# Define conversation states
ASKING_NAME = 0
ASKING_MENU = 1
ASKING_NUMBER_LIST = 2
ASKING_VARIATION_PROPERTY = 3
ASKING_RALAT = 4
ASKING_NUMBER_OF_RALAT = 5
ASKING_RALAT_NUMBER_LIST = 6

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo, bantu pengembangan bot dengan follow ig @gmsaw_")

async def info_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Siapa namamu?")
    return ASKING_NAME

async def received_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    await update.message.reply_text(f"Halo, {user_name}! Ini adalah info yang kamu minta.")
    return ConversationHandler.END

async def laprak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pilih menu berikut:\n1. Variasi\n2. Ralat\n3. Multi Ralat\nKetik 'exit' untuk keluar.")
    return ASKING_MENU

async def received_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_choice = update.message.text.strip().lower()
    if menu_choice == "1":
        context.user_data['choice'] = "variasi"
        await update.message.reply_text("Masukkan properti yang dibutuhkan: 'angka, banyak data, angka di belakang koma' contoh: 10, 8, 4")
        return ASKING_VARIATION_PROPERTY
    elif menu_choice == "2":
        context.user_data['choice'] = "ralat"
        await update.message.reply_text("Masukkan angka, dipisahkan dengan koma (contoh: 2, 3, 4, 5):")
        return ASKING_NUMBER_LIST
    elif menu_choice == "3":
        context.user_data['choice'] = "multiralat"
        await update.message.reply_text("Berapa banyak ralat yang akan diproses?")
        return ASKING_NUMBER_OF_RALAT
    elif menu_choice == "exit":
        await update.message.reply_text("Terima kasih telah menggunakan bot ini!")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Pilihan tidak valid. Mohon pilih menu 1, 2, atau ketik 'exit' untuk keluar.")
        return ASKING_MENU

async def process_variation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        props = update.message.text.strip().split(',')
        if len(props) != 3:
            raise ValueError("Jumlah properti tidak sesuai.")
        
        number = float(props[0].strip())
        n = int(props[1].strip())
        u = int(props[2].strip())

        variations = generate_variations_rk(number, n, u)
        response_message = f"Variasi dari angka {number} dengan {n} variasi dan {u} angka di belakang koma:\n{variations}"
        
        await update.message.reply_text(response_message)
        await update.message.reply_text("Pilih menu berikut:\n1. Variasi\n2. Ralat\n3. Multi Ralat\nKetik 'exit' untuk keluar.")
        return ASKING_MENU
    except ValueError:
        await update.message.reply_text("Mohon masukkan jumlah properti yang valid.")
        return ASKING_VARIATION_PROPERTY

async def received_number_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number_list_str = update.message.text
    context.user_data['number_list_str'] = number_list_str  # Save the number list string in user data
    await update.message.reply_text("Jumlah nol belakang koma?")
    return ASKING_RALAT

async def process_ralat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        number_list_str = context.user_data['number_list_str']  # Retrieve the number list string from user data
        number_list = [float(num.strip()) for num in number_list_str.split(',')]
        decimal_places = int(update.message.text)
        data, x_bar, x_min_x_bar, x_min_x_bar_2, sum_x_min_x_bar_2, delta_x1, delta_x, rn1, rn, rk = ralat(number_list, len(number_list), decimal_places)
        response_message = (
            f"List data anda adalah: {data}\n"
            f"Rata-rata: {x_bar}\n"
            f"x - x_bar: {x_min_x_bar}\n"
            f"(x - x_bar)^2: {x_min_x_bar_2}\n"
            f"Sum: {sum_x_min_x_bar_2}\n"
            f"Delta_x: {delta_x}\n"
            f"Rn: {rn}\n"
            f"Rk: {rk}"
        )
        
        await update.message.reply_text(response_message)
        await update.message.reply_text("Pilih menu berikut:\n1. Variasi\n2. Ralat\n3. Multi Ralat\nKetik 'exit' untuk keluar.")
        return ASKING_MENU
    except ValueError:
        await update.message.reply_text("Mohon masukkan angka yang valid.")
        return ASKING_NUMBER_LIST  # Stay in the same state to re-prompt for a valid number

async def ask_ralat_number_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        number_of_ralat = int(update.message.text)
        context.user_data['number_of_ralat'] = number_of_ralat
        context.user_data['current_ralat'] = 1
        await update.message.reply_text(f"Masukkan angka untuk ralat 1, dipisahkan dengan koma (contoh: 2, 3, 4, 5):")
        return ASKING_RALAT_NUMBER_LIST
    except ValueError:
        await update.message.reply_text("Mohon masukkan angka yang valid.")
        return ASKING_NUMBER_OF_RALAT

async def process_ralat_number_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        current_ralat = context.user_data['current_ralat']
        number_of_ralat = context.user_data['number_of_ralat']
        
        number_list_str = update.message.text
        number_list = [float(num.strip()) for num in number_list_str.split(',')]
        context.user_data[f'number_list_{current_ralat}'] = number_list
        
        all_data = []
        all_x_bar = [] 
        all_x_min_x_bar = [] 
        all_x_min_x_bar_2 = []
        all_sum_x_min_x_bar_2 = [] 
        all_delta_x1 = [] 
        all_delta_x = [] 
        all_rn1 = [] 
        all_rn = [] 
        all_rk = []
        
        
        if current_ralat < number_of_ralat:
            context.user_data['current_ralat'] += 1
            await update.message.reply_text(f"Masukkan angka untuk ralat {current_ralat + 1}, dipisahkan dengan koma (contoh: 2, 3, 4, 5):")
            return ASKING_RALAT_NUMBER_LIST
        
        # Process all ralat and create documents
        for i in range(1, number_of_ralat + 1):
            number_list = context.user_data[f'number_list_{i}']
            # Process ralat (assuming all have the same decimal places for simplicity)
            data, x_bar, x_min_x_bar, x_min_x_bar_2, sum_x_min_x_bar_2, delta_x1, delta_x, rn1, rn, rk = ralat(number_list, len(number_list), 4)
            all_data.append(data)
            all_x_bar.append(x_bar) 
            all_x_min_x_bar.append(x_min_x_bar) 
            all_x_min_x_bar_2.append(x_min_x_bar_2)
            all_sum_x_min_x_bar_2.append(sum_x_min_x_bar_2) 
            all_delta_x1.append(delta_x1) 
            all_delta_x.append(delta_x) 
            all_rn1.append(rn1) 
            all_rn.append(rn) 
            all_rk.append(rk)
                  
        title = "MultiRalat"
        filename = f'{title}.docx'
        ralat_to_docx(title, number_of_ralat, all_data, all_x_bar, all_x_min_x_bar, all_x_min_x_bar_2, all_sum_x_min_x_bar_2, all_delta_x1, all_delta_x, all_rn1, all_rn, all_rk)
        
        # Send the document
        await update.message.reply_document(document=open(filename, 'rb'), filename=filename)
        
        await update.message.reply_text("Semua ralat telah diproses dan dokumen telah dikirim.")
        await update.message.reply_text("Pilih menu berikut:\n1. Variasi\n2. Ralat\n3. Multi Ralat\nKetik 'exit' untuk keluar.")
        return ASKING_MENU
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text("Mohon masukkan angka yang valid.")
        return ASKING_RALAT_NUMBER_LIST

def handle_response(text: str) -> str:
    processed: str = text.lower()
    if "hello" in processed:
        return "hy"
    if "makasi" in processed:
        return "sama-sama"
    if "bot username" in processed:
        return BOT_USERNAME
    return "kocak lu"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    response: str = handle_response(text)
    
    print('Bot: ', response)
    # Send the response back to the user
    await update.message.reply_text(response)
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Define the conversation handler with states for the /info and /laprak commands
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('info', info_start), CommandHandler('laprak', laprak_command)],
    states={
        ASKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_name)],
        ASKING_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_menu)],
        ASKING_NUMBER_LIST: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_number_list)],
        ASKING_VARIATION_PROPERTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_variation)],
        ASKING_RALAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_ralat)],
        ASKING_NUMBER_OF_RALAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_ralat_number_list)],
        ASKING_RALAT_NUMBER_LIST: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_ralat_number_list)],
    },
    fallbacks=[],
    )

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=5)