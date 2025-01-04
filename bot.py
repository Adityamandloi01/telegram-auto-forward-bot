from pyrogram import Client, filters
from pyrogram.types import Message
import json
import os

# Define the path to store configuration
config_file = 'bot_config.json'

# Function to load configuration from a file
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

# Function to save configuration to a file
def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)

# Load the initial config (empty if not set)
config = load_config()

# Default config if not set by user
default_config = {
    "source_channel": "",
    "target_channel": "",
    "api_id": "29169450",  # Your API ID
    "api_hash": "5cbe63ac7df6f9d036fb59c3587c5216",  # Your API Hash
    "bot_token": "YOUR_BOT_TOKEN"  # Your Bot Token
}

# Update default config with saved config (if any)
config = {**default_config, **config}

# Create a Pyrogram Client
app = Client("forward_bot", api_id=config["api_id"], api_hash=config["api_hash"], bot_token=config["bot_token"])

# Command to set the source channel
@app.on_message(filters.command("set_source_channel"))
async def set_source_channel(client: Client, message: Message):
    channel_username = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    if channel_username:
        config["source_channel"] = channel_username
        save_config(config)
        await message.reply(f"Source channel updated to {channel_username}")
    else:
        await message.reply("Please provide the channel username. Example: /set_source_channel @your_source_channel")

# Command to set the target channel
@app.on_message(filters.command("set_target_channel"))
async def set_target_channel(client: Client, message: Message):
    channel_username = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    if channel_username:
        config["target_channel"] = channel_username
        save_config(config)
        await message.reply(f"Target channel updated to {channel_username}")
    else:
        await message.reply("Please provide the channel username. Example: /set_target_channel @your_target_channel")

# Command to set the bot token (for future updates if needed)
@app.on_message(filters.command("set_bot_token"))
async def set_bot_token(client: Client, message: Message):
    bot_token = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    if bot_token:
        config["bot_token"] = bot_token
        save_config(config)
        await message.reply(f"Bot token updated successfully.")
    else:
        await message.reply("Please provide the bot token. Example: /set_bot_token YOUR_BOT_TOKEN")

# Command to start the bot (check current settings)
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    source_channel = config["source_channel"]
    target_channel = config["target_channel"]
    
    if not source_channel or not target_channel:
        await message.reply("Please set both the source and target channels first. Use /set_source_channel and /set_target_channel.")
    else:
        await message.reply(f"Bot started. Forwarding from {source_channel} to {target_channel}.")

# Function to handle the message forwarding from the source channel to the target channel
@app.on_message(filters.channel & filters.chat(lambda message: message.chat.username == config["source_channel"]))
async def forward_message(client, message):
    try:
        if config["target_channel"]:
            await client.forward_messages(config["target_channel"], message.chat.id, message.message_id)
            print(f"Message forwarded to {config['target_channel']}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Run the bot
app.run()
