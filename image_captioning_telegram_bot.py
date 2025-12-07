import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from PIL import Image
import requests
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
from io import BytesIO

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b", load_in_8bit=True, device_map={"": 0}, dtype=torch.float16
)  # doctest: +IGNORE_RESULT

async def caption_image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # image = Image.open(BytesIO(update.message.photo[-1].get_file()))
    new_file = await context.bot.get_file(update.message.photo[-1].file_id)
    photo_bytes = BytesIO()
    await new_file.download_to_memory(photo_bytes)
    photo_bytes.seek(0)
    image = Image.open(photo_bytes)

    inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)

    generated_ids = model.generate(**inputs)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=generated_text)

if __name__ == '__main__':
    application = ApplicationBuilder().token('8454636377:AAHxm3ydk8s1FLJtXJ736nsbVdGUnZzjlnw').build()

    # start_handler = CommandHandler('image', caption_image)
    photo_handler = MessageHandler(filters.PHOTO, caption_image)
    application.add_handler(photo_handler)

    application.run_polling()
