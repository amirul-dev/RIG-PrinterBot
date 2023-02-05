import telegram.ext
import datetime
import sqlite3

API_TOKEN = '6192052073:AAG4BUiDbqCg7Y2TgEEL6GzNYC4MGAa04Uc'

updater = telegram.ext.Updater(API_TOKEN, use_context=True)

def start_printing(update, context):
    # Get the required details from the user
    start_time = datetime.datetime.now()
    expected_duration = context.args[0]
    nozzle_size = context.args[1]
    filament_material = context.args[2]

    # Save the details to the database
    conn = sqlite3.connect('printer.db')
    c = conn.cursor()
    c.execute("INSERT INTO printer (start_time, expected_duration, nozzle_size, filament_material) VALUES (?,?,?,?)", (start_time, expected_duration, nozzle_size, filament_material))
    conn.commit()
    conn.close()

    update.message.reply_text('Printing started successfully!')

def update_printing(update, context):
    # Get the new details from the user
    expected_duration = context.args[0]
    nozzle_size = context.args[1]
    filament_material = context.args[2]

    # Update the details in the database
    conn = sqlite3.connect('printer.db')
    c = conn.cursor()
    c.execute("UPDATE printer SET expected_duration=?, nozzle_size=?, filament_material=?", (expected_duration, nozzle_size, filament_material))
    conn.commit()
    conn.close()

    update.message.reply_text('Printing details updated successfully!')

def status(update, context):
    # Retrieve the current status from the database
    conn = sqlite3.connect('printer.db')
    c = conn.cursor()
    c.execute("SELECT * FROM printer ORDER BY start_time DESC LIMIT 1")
    result = c.fetchone()
    conn.close()

    if result:
        start_time, expected_duration, nozzle_size, filament_material = result
        elapsed_time = datetime.datetime.now() - start_time
        remaining_time = expected_duration - elapsed_time

        update.message.reply_text(f'Printer status: \nStart time: {start_time} \nExpected duration: {expected_duration} \nNozzle size: {nozzle_size} \nFilament material: {filament_material} \nTime remaining: {remaining_time}')
    else:
        update.message.reply_text('No printing is currently in progress.')



updater.dispatcher.add_handler(telegram.CommandHandler('start', start_printing))
updater.dispatcher.add_handler(telegram.CommandHandler('update', update_printing))
updater.dispatcher.add_handler(telegram.CommandHandler('status', status))

updater.start_polling()
updater.id
