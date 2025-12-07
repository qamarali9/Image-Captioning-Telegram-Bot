Hi. This small repo conatins a script which adds image captioning functionality to a telegram bot. What that means is whenever someone uploads an image to the bot, the bot replies back with a caption (description/summary) for that image.

To use this code for its intended purpose, firstly you would need an authentication token for a bot from telegram. To do that follow the steps below (or you can refer here as well: https://core.telegram.org/bots/features#botfather):
-- Search for and connect with @BotFather on Telegram.
-- Issue /newbot command
-- You would be prompted to provide a name for the bot. Please do so. (Ex: "telegram_bot_yourName")
-- Then you would be prompted to choose a username for the bot (ending in 'bot'). Kindly do so. (Ex: "ImageCaptionGeneratorBot")
-- You will get a congratulations response with an access token. The token is a string, like 110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw, which is required to authorize the bot and send requests to the Bot API. Keep your token secure and store it safely, it can be used by anyone to control your bot.

Now clone the repo on your machine using command: [git clone https://github.com/qamarali9/Image-Captioning-Telegram-Bot.git]
Go to the cloned repo: [cd Image-Captioning-Telegram-Bot/]
Install the required dependencies, which will take some time (you might want to activate your virtual environment first): [pip install -r requirements.txt]
Now paste your token at the appropriate place in the code in image_captioning_telegram_bot.py in the line which is [TELEGRAM_BOT_TOKEN = "PUT-YOUR-TELEGRAM-BOT-ACCESS-TOKEN-HERE"]
Run the script (this will take some time for the first time as the (huge) models get downloaded): [python3 image_captioning_telegram_bot.py]

Now in telegram search for your bot (ex: @ImageCaptionGeneratorBot). Issue "/image" command. Upload an image. You should get a response containing a caption (description/summary) of the image along with 3 keywords. Enjoy!!
