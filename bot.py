from pyrogram import Client, filters
from pyrogram.types import Message

# Bot credentials
API_ID = 29169450
API_HASH = "5cbe63ac7df6f9d036fb59c3587c5216"
BOT_TOKEN = "7781239916:AAGxJTjNwlW_8ssksZKNZBEBj3_x-P98t8k"

# Initialize the bot
app = Client("auto_forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Variables to store source and target channels (stored dynamically)
source_channel = None
target_channel = None

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply(
        "👋 Welcome to the Auto Forward Bot!\n\n"
        "Use the following commands to set up:\n"
        "1️⃣ `/setsource <channel_username or ID>` - Set the source channel.\n"
        "2️⃣ `/getsource` - Get the current source channel.\n"
        "3️⃣ `/settarget <channel_username or ID>` - Set the target channel.\n"
        "4️⃣ `/gettarget` - Get the current target channel.\n\n"
        "Once configured, messages from the source channel will be automatically forwarded to the target channel!"
    )

@app.on_message(filters.command("setsource") & filters.private)
async def set_source(client, message: Message):
    global source_channel
    try:
        # Extract source channel from the command
        source_channel = message.text.split(" ", 1)[1]
        await message.reply(f"✅ Source channel set to: `{source_channel}`")
    except IndexError:
        await message.reply("❌ Please provide a valid channel username or ID. Example: `/setsource @sourcechannel`")

@app.on_message(filters.command("getsource") & filters.private)
async def get_source(client, message: Message):
    global source_channel
    if source_channel:
        await message.reply(f"📤 Current source channel: `{source_channel}`")
    else:
        await message.reply("❌ No source channel set. Use `/setsource` to configure one.")

@app.on_message(filters.command("settarget") & filters.private)
async def set_target(client, message: Message):
    global target_channel
    try:
        # Extract target channel from the command
        target_channel = message.text.split(" ", 1)[1]
        await message.reply(f"✅ Target channel set to: `{target_channel}`")
    except IndexError:
        await message.reply("❌ Please provide a valid channel username or ID. Example: `/settarget @targetchannel`")

@app.on_message(filters.command("gettarget") & filters.private)
async def get_target(client, message: Message):
    global target_channel
    if target_channel:
        await message.reply(f"🎯 Current target channel: `{target_channel}`")
    else:
        await message.reply("❌ No target channel set. Use `/settarget` to configure one.")

@app.on_message(filters.chat(source_channel))
async def forward_message(client, message: Message):
    global target_channel
    if not target_channel:
        print("❌ Target channel not set. Use /settarget to configure it.")
        return

    try:
        # Forward message from source to target channel
        await message.forward(target_channel)
        print(f"✅ Forwarded message to {target_channel}: {message.text}")
    except Exception as e:
        print(f"❌ Error while forwarding message: {e}")

if __name__ == "__main__":
    app.run()
