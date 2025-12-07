# Imports for telegram bot's functionality
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
# Imports for Image processing and caption generation (blip2)
from PIL import Image
import requests
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
from io import BytesIO

device = "cuda" if torch.cuda.is_available() else "cpu" # setting device to cuda if available, else to cpu

# Fetching pretrained models
processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b", load_in_8bit=True, device_map={"": 0}, dtype=torch.float16
)  # doctest: +IGNORE_RESULT

# The caption_image functionality is the heart of this script. It gets triggered whenever an image is uploaded to the bot.
async def caption_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # First we fetch the image 
    new_file = await context.bot.get_file(update.message.photo[-1].file_id) # Telegram stores the photo in multiple sizes, we fetch the last (largest) one
    photo_bytes = BytesIO()
    await new_file.download_to_memory(photo_bytes)
    photo_bytes.seek(0)
    image = Image.open(photo_bytes)
    # Then we run the pre-trained models on it to generate the caption
    inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)
    generated_ids = model.generate(**inputs)
    caption_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    # We again run the pretrained models on the image but this time with a prompt to generate 3 associated keywords
    prompt = "Question: What are the 3 distinct things you would associate with this image? Answer:"
    inputs = processor(images=image, text=prompt, return_tensors="pt").to("cuda", torch.float16)
    generated_ids = model.generate(**inputs)
    tags = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    # Then we send the reply with the generated text
    generated_text = "Caption: " + caption_text + "\nTags:\n" + tags
    await context.bot.send_message(chat_id=update.effective_chat.id, text=generated_text)

# The ask functionality gets triggered whenever the user issues /ask command to the bot
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This bot follows track 2 (Option B) of the assesment and provides caption for an uploaded image, after '/image' command. Please type '/help' for usage.")

# The image functionality gets triggered whenever the user issues /image command to the bot
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Image Captioning Bot at your service. Please upload an image for description.")

# The echo functionality gets triggered whenever user provides some text (except the commands) as input
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You said: '" + update.message.text +"'\nPlease type '/help' (without quotes) to get help about usage.")

# The help_display functionality gets triggered whenever the user issues /help command to the bot
async def help_display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Image Captioning Bot. Usage: type '/image' command (without quotes) and then upload an image, for which the bot will generate a caption and provide relevant tags.")

# The unkown functionality gets triggered whenever the user issues an unrecognized command
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. Please type '/help' (without quotes) to get help about usage.")

# This is where your telegram token goes
TELEGRAM_BOT_TOKEN = "PUT-YOUR-TELEGRAM-BOT-ACCESS-TOKEN-HERE"

# The application is created and the appropriate handlers (functions) are registered to it.
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    ask_handler = CommandHandler('ask', ask)
    application.add_handler(ask_handler)

    help_handler = CommandHandler('help', help_display)
    application.add_handler(help_handler)

    image_handler = CommandHandler('image', image)
    application.add_handler(image_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND) & (~filters.PHOTO), echo)
    application.add_handler(echo_handler)

    photo_handler = MessageHandler(filters.PHOTO, caption_image)
    application.add_handler(photo_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()

