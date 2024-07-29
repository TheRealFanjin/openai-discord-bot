## OpenAI Discord Bot

### Description
Uses the OpenAI API to offer both text and image generation through Discord.\
Use `.text {message}` for text generation and `.image {message}` for image generation.

### Try it out!
#### Every user gets 10 free text prompts and 2 free image prompts! Click the link to add the bot to your server:
https://discord.com/oauth2/authorize?client_id=1266867481239093375&permissions=93184&integration_type=0&scope=bot

### Or install it yourself
On Python 3.10 (could work on other Python versions, not guaranteed), run `pip install -r requirements.txt`. Then, enter your Discord bot token (requires Message Content Intent) and OpenAI token and rename `prod.env` to just `.env`. To invite your bot to your server with the necessary permissions, simply replace the `id` in the Discord OAuth link above with your OAuth client id.