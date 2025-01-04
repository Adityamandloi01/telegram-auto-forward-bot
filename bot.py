from pyrogram import Client, filters
from pyrogram.types import Message

# Bot credentials
API_ID = 29169450  # Replace with your actual API ID
API_HASH = "5cbe63ac7df6f9d036fb59c3587c5216"  # Replace with your actual API Hash
BOT_TOKEN = "7781239916:AAGxJTjNwlW_8ssksZKNZBEBj3_x-P98t8k"  # Replace with your Bot Token

# Source channel details
SOURCE_CHANNEL = -1001234567890  # Replace with your source channel ID

# Initialize the bot
app = Client("auto_forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Variable to store the target channel
target_channel = None

@app.on_message(filters.command("settarget") & filters.private)
async def set_target(client, message: Message):
    global target_channel
    try:
        # Extract the channel ID or username from the command
        target_channel = message.text.split(" ", 1)[1]
        await message.reply(f"✅ Target channel has been set to: `{target_channel}`")
    except IndexError:
        await message.reply("❌ Please provide a valid channel ID or username. Example: `/settarget @targetchannel`")

@app.on_message(filters.command("gettarget") & filters.private)
async def get_target(client, message: Message):
    global target_channel
    if target_channel:
        await message.reply(f"🎯 Current target channel is: `{target_channel}`")
    else:
        await message.reply("❌ No target channel has been set yet. Use `/settarget` to set one.")

@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_message(client, message: Message):
    global target_channel
    if not target_channel:
        print("❌ Target channel is not set. Use /settarget to configure it.")
        return

    try:
        # Forward the message to the target channel
        await message.forward(target_channel)
        print(f"✅ Forwarded message to {target_channel}: {message.text}")
    except Exception as e:
        print(f"❌ Error forwarding message: {e}")

if __name__ == "__main__":
    app.run()
