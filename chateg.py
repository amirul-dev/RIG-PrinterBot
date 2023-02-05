#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import datetime
import sqlite3

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

OPTION, START_TIME, DURATION, NOZZLE, NOZZLE, STATUS  = range(6)

starttime = datetime.datetime.now()
nozzle_size = 0.8

option_keyboard = [["Add current printing data", "Check status of printer"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks if the user need an update or a status check"""
    logger.info("Bot started, asking for option")
    reply_keyboard = [["Add current printing data", "Check status of printer"]]
    await update.message.reply_text(
        f"Welcome to RIG PrinterBot 1.0 🤖🎨 \n\nDo you need to add current printing details, or check printer status. \n\nChoose from the following.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Choose from below"
         ),     
    )

    return OPTION

    
async def starttime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the start time and asks for the expected duration."""
    start_time = datetime.datetime.now()
    logger.info("Start time: %s", start_time)
    await update.message.reply_text(
        f'Printing start time have been recorded as: {start_time.strftime(r"%I:%M %p - %b %d")}. \n \nEnter the expected duration of printing in HH,MM format',
    )

    return DURATION


async def duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the printing duration and asks nozzle size"""
    user = update.message.from_user
    logger.info("Duration of printing of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [["0.2", "0.3", "0.4", "0.8"]]
    await update.message.reply_text(
        f"Which nozzle are you using",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Nozzle?"
         ),
    )
    return NOZZLE

async def nozzle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """saves nozzle and goodbye"""
    logger.info("Nozzle is %s", update.message.text)
    await update.message.reply_text(
        "Happy printing"
    )
    return ConversationHandler.END

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """shows status and goodbye"""
    logger.info("Status is: %s", update.message.text)
    await update.message.reply_text(
        "Happy printing"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6192052073:AAG4BUiDbqCg7Y2TgEEL6GzNYC4MGAa04Uc").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            OPTION: [MessageHandler(
                    filters.Regex(f"^({option_keyboard[0][0]})$"), starttime
                ),
                MessageHandler(filters.Regex(f"^({option_keyboard[0][1]})$"), status),
            ],
            START_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, starttime)],
            DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, duration)],
            NOZZLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, nozzle)],
            STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, status)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()