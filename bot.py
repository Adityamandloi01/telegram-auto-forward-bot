from pyrogram import Client, filters

# Replace these with your credentials
API_ID = "YOUR_API_ID"          # Get this from https://my.telegram.org
API_HASH = "YOUR_API_HASH"      # Get this from https://my.telegram.org
BOT_TOKEN = "7781239916:AAGxJTjNwlW_8ssksZKNZBEBj3_x-P98t8k"  # Your bot token from BotFather

# Source and target channel IDs (replace with actual channel IDs or usernames)
SOURCE_CHANNEL = -1001234567890  # Replace with your source channel ID
TARGET_CHANNEL = -1009876543210  # Replace with your target channel ID

# Initialize the bot
app = Client("auto_forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_message(client, message):
    try:
        await message.forward(TARGET_CHANNEL)
        print(f"Forwarded: {message.text}")
    except Exception as e:
        print(f"Error: {e}")

if name == "main":
    app.run()