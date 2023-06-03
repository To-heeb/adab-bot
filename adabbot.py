"""
    Simple Bot to reply to Get Notes And.

    First, a few handler functions are defined. Then, those functions are passed to
    the Dispatcher and registered at their respective places.
    Then, the bot is started and runs until we press Ctrl-C on the command line.

    Usage:
    Basic Echobot example, repeats messages.
    Press Ctrl-C on the command line or send a signal to the process to stop the
    bot.
"""

import os
from dotenv import load_dotenv
import datetime
import logging

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ChatMemberHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "none")

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, CHOOSINGCHAPTER = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    markup = get_main_menu_keyboard()
    await update.message.reply_text(
        "\n اَلسَلامُ عَلَيْكُم وَرَحْمَةُ اَللهِ وَبَرَكاتُهُ"
        "\n"
        "Hi! I am Adabul-Mufrad Bot. \n"
        "I am here to provide you with notes and audios from Adabul-Mufrad class based the chapter you have selected. \n"
        "Please select the format you want to receive as your response. \n"
        "Click on Cancel to stop talking to me.\n\n",
        reply_markup=markup,
    )
    
    return CHOOSING
    
def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Helper function for formatting the main menu keyboard."""
    reply_keyboard = [
        ["Note", "Audio"],
        ["Note & Audio"],
        ["Cancel"]
    ]
    return ReplyKeyboardMarkup(
        reply_keyboard,
        one_time_keyboard=True,
        input_field_placeholder="Choose a format..."
    )


def get_chapters_menu_keyboard() -> ReplyKeyboardMarkup:
    """Helper function for formatting the chapters menu keyboard."""
    reply_keyboard = [
        ["wait", "for", "now"],
        ["work", "in", "progress"],
        ["Cancel"]
    ]
    
    return reply_keyboard


async def selected_format(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Ask the for the format they want thier response in."""
        user = update.message.from_user
        text = update.message.text
        
        keyboard_chapter_options = get_chapters_menu_keyboard()
        context.user_data["format"] = text
        logger.info("User %s select the format %s .", user.first_name, text)
        
        if text == "Cancel":
            await update.message.reply_text(
                "You cancelled the conversation \n"
                "Bye! I hope I can still be of help again some day. \n"
                "                     اَلسَلامُ عَلَيْكُم وَرَحْمَةُ اَللهِ وَبَرَكاتُهُ", 
                reply_markup=ReplyKeyboardRemove(),
            )
            return ConversationHandler.END
        
        await update.message.reply_text(
           "Please choose from the following chapters:",
            reply_markup=ReplyKeyboardMarkup(
            keyboard_chapter_options,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Choose an option...",),
        )

        return CHOOSINGCHAPTER
    
async def selected_chapter(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ask the for the chapter they waant to access."""
        user = update.message.from_user
        text = update.message.text
         
        #cancel_conversation(Update,text)
        if text == "Cancel":
            await update.message.reply_text(
                "You cancelled the conversation \n"
                "Bye! I hope I can still be of help again some day. \n"
                "                     اَلسَلامُ عَلَيْكُم وَرَحْمَةُ اَللهِ وَبَرَكاتُهُ", 
                reply_markup=ReplyKeyboardRemove(),
            )
            return ConversationHandler.END
    
        context.user_data["category"] = text
        logger.info("User %s select the chapter %s .", user.first_name, text)



async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
         "\n اَلسَلامُ عَلَيْكُم وَرَحْمَةُ اَللهِ وَبَرَكاتُهُ"
         " I hope I have been of help to you \n"
         " Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
          "You cancelled the conversation \n"
          "Bye! I hope I can still be of help again some day. \n"
          "                     اَلسَلامُ عَلَيْكُم وَرَحْمَةُ اَللهِ وَبَرَكاتُهُ", 
          reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

   # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                 MessageHandler(
                    filters.Regex("^(Note|Audio|Note & Audio)$"), selected_format
                ),
                MessageHandler(filters.Regex("^Cancel$"), cancel),
            ],
            CHOOSINGCHAPTER :[
                 MessageHandler(
                    filters.TEXT & ~(filters.COMMAND),
                    selected_chapter,
                ),
                MessageHandler(filters.Regex("^Cancel$"), cancel),
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
