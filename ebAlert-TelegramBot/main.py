import os
import subprocess
from telegram       import Update
from telegram.ext   import ApplicationBuilder, ContextTypes, CommandHandler

token = os.environ.get("TOKEN") or "Your_secret_key"
allowed_chat = os.environ.get("CHAT_ID") or "Your_chat_id"

help_message = "## ebay-Kleinanzeigen-Alert Bot ##\n" \
               "/list - prints all URLs currently watched\n" \
               "/add <URL> - adds passed URL and watches it in the future\n" \
               "/remove <ID> - removes URL by ID, doesn't watch anymore"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != allowed_chat:
        return

    await show_help(update, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="ekAlert bot ready to scrape!"
    )

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != allowed_chat:
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_message
    )

async def list_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != allowed_chat:
        return

    command = "ebAlert links --show"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=output.decode()
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != allowed_chat:
        return

    if len(context.args) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please use format: /add <id>"
        )
        return

    url = str(context.args[0])
    if "ebay-kleinanzeigen.de" not in url.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please provide a valid ebay-Kleinanzeigen URL"
        )
        return

    command = "ebAlert links --add_url '" + url + "'"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=output.decode()
    )


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != allowed_chat:
        return

    if len(context.args) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please use format: /remove <id>"
        )
        return

    link_id = str(context.args[0])
    command = "ebAlert links --remove_link " + link_id
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=output.decode()
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('list', list_links))
    application.add_handler(CommandHandler('remove', remove))
    application.add_handler(CommandHandler('add', add))
    application.add_handler(CommandHandler('help', show_help))

    application.run_polling()
