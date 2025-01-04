from pyrogram import Client, filters
from pyrogram.types import Message

# Userbot credentials
API_ID = 29169450  # Your API ID
API_HASH = "5cbe63ac7df6f9d036fb59c3587c5216"  # Your API Hash

# Initialize the userbot with a session file
app = Client("userbot_session", api_id=API_ID, api_hash=API_HASH)

# Variables to store source and target channels (set via commands)
source_channel = None
target_channel = None

# Set source channel using /setsource command
@app.on_message(filters.command("setsource") & filters.private)
async def set_source(client, message: Message):
    global source_channel
    try:
        source_channel = message.text.split(" ", 1)[1]
        await message.reply(f"✅ Source channel set to: `{source_channel}`")
    except IndexError:
        await message.reply("❌ Please provide a valid channel username or ID.")

# Set target channel using /settarget command
@app.on_message(filters.command("settarget") & filters.private)
async def set_target(client, message: Message):
    global target_channel
    try:
        target_channel = message.text.split(" ", 1)[1]
        await message.reply(f"✅ Target channel set to: `{target_channel}`")
    except IndexError:
        await message.reply("❌ Please provide a valid channel username or ID.")

# Forward messages from the source channel to the target channel
@app.on_message(filters.chat(source_channel))
async def forward_message(client, message: Message):
    global target_channel
    if target_channel:
        try:
            await message.forward(target_channel)
            print(f"✅ Forwarded message to {target_channel}: {message.text}")
        except Exception as e:
            print(f"❌ Error while forwarding message: {e}")
    else:
        print("❌ Target channel not set. Use /settarget to configure it.")

# Start the bot
if __name__ == "__main__":
    app.run()
