import logging
import re
import asyncio
import aiohttp
import traceback
import pymongo
from datetime import datetime
from telethon import TelegramClient, events, Button, sync
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel, PeerChat, PeerUser
from telethon.utils import get_display_name
from telethon.tl.functions.users import GetFullUserRequest
from decouple import config
from aiohttp import web

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

destination_channels_str = config("DESTNATION_CHANNELS")
destination_channels = [int(channel_id.strip()) for channel_id in destination_channels_str.split(',')]
destination_channels_str2 = config("DESTNATION_CHANNELS2")
destination_channels2 = [int(channel_id.strip()) for channel_id in destination_channels_str2.split(',')]

destination_channels_str3 = config("DESTNATION_CHANNELS3")
destination_channels3 = [int(channel_id.strip()) for channel_id in destination_channels_str3.split(',')]
destination_channels_str4 = config("DESTNATION_CHANNELS4")
destination_channels4 = [int(channel_id.strip()) for channel_id in destination_channels_str4.split(',')]

app = web.Application()

replacement_link = config("MY_LINK", default=None)
replacement_username = config("MY_USERNAME", default=None)
replacement_web_link = config("WEB_LINK", default=None)
replacement_link2 = config("MY_LINK2", default=None)
replacement_username2 = config("MY_USERNAME2", default=None)
replacement_web_link2 = config("WEB_LINK2", default=None)

replacement_link3 = config("MY_LINK3", default=None)
replacement_username3 = config("MY_USERNAME3", default=None)
replacement_web_link3 = config("WEB_LINK3", default=None)
replacement_link4 = config("MY_LINK4", default=None)
replacement_username4 = config("MY_USERNAME4", default=None)
replacement_web_link4 = config("WEB_LINK4", default=None)

logger.info("Starting...")

try:
    api_id = config("APP_ID", cast=int)
    api_hash = config("HASH")
    bot_token = config("TOKEN")
    string_session = config("STRING_SESSION")
    user_client = TelegramClient(StringSession(string_session), api_id, api_hash)
    user_client.start()
    source_channel = config("SOURCE_CHANNEL", cast=int)
    source_channel2 = config("SOURCE_CHANNEL2", cast=int)
    source_channel3 = config("SOURCE_CHANNEL3", cast=int)
    source_channel4 = config("SOURCE_CHANNEL4", cast=int)
    admin_user_id = config("ADMIN_USER_ID", cast=int)
    StarBotsTamil = TelegramClient('starbot', api_id, api_hash).start(bot_token=bot_token)
except Exception as e:
    logger.error(f"Error initializing the bot: {str(e)}")
    logger.error("Bot is quitting...")
    exit()

@StarBotsTamil.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(
        f"""**Hi 👋🏻 {event.sender.first_name},
I'm [Auto Forward Star Bots](https://t.me/Auto_Forward_Star_Bot) to Maintain Your Channels. I am very useful for the Channel Admin who have many Channels.

See /help for more Details.

Maintained By :- [Star Bots Tamil](https://t.me/Star_Bots_Tamil)**""",
        buttons=[
            [Button.url("Update Channel", url="https://t.me/Star_Bots_Tamil")],
            [Button.url("Add me to Your Channel", url="https://t.me/Auto_Forward_Star_Bot?startchannel=StarBots&admin"),
            Button.url("Add My Channels", url="https://t.me/TG_Karthik")],
        ],
        link_preview=False,
    )

@StarBotsTamil.on(events.NewMessage(pattern="/help"))
async def help(event):
    await event.reply(
        f"""**Hi 👋🏻 {event.sender.first_name},
    
Here is a list of usable Commands :-
♦️ /start :- Check if 😊 I'm Alive
♦️ /forward :- to Request to add Source And Distinction Channels ID (Direct Request to Admin)
♦️ /help :- This is Bot's Features
♦️ /about :- to Know About Me 😁
♦️ /id :- Get Your 🆔
Just Send /id in Private Chat/Group/Channel and i will Reply it's ID.
    
Help :-
    
❄ About This Bot :-
➡ This Bot will Send all New Posts From the Source Channel to one or More Channels (without the Forwarded Tag)!
    
❄ How to Use Me?
🏮 Add the Bot to the Channels.
🏮 Make me an Admin in Destination Channels.
🏮Now all new Messages Would be Autoposted on the Linked Channels.!!
    
Liked the Bot? [Get Source Code](https://t.me/TG_Karthik)**""",
        buttons=[
            [Button.url("Update Channel", url="https://t.me/Star_Bots_Tamil")],
            [Button.url("Add me to Your Channel", url="https://t.me/Auto_Forward_Star_Bot?startchannel=StarBots&admin"),
            Button.url("Add My Channels", url="https://t.me/TG_Karthik")],
        ],
        link_preview=False,
    )

@StarBotsTamil.on(events.NewMessage(pattern="/about"))
async def about(event):
    await event.reply(
        f"""**🤖 My Name :- [Auto Forward Star Bots](https://t.me/Auto_Forward_Star_Bot)
    
🧑🏻‍💻 Developer :- Karthik

🧑🏻‍🤝‍🧑🏻 My Best Friend :- {event.sender.first_name}

📝 Language :- Python3

📚 Framework :- Telethon

📡 Hosted on :- VPS

📢 Updates Channel :- [Star Bots Tamil](https://t.me/Star_Bots_Tamil)**""",
        buttons=[
            [Button.url("Update Channel", url="https://t.me/Star_Bots_Tamil")],
            [Button.url("Add me to Your Channel", url="https://t.me/Auto_Forward_Star_Bot?startchannel=StarBots&admin"),
            Button.url("Add My Channels", url="https://t.me/TG_Karthik")],
        ],
        link_preview=False,
    )

@StarBotsTamil.on(events.NewMessage(pattern="/forward"))
async def forward(event):
    await event.reply(
        f"""**Hi 👋🏻 {event.sender.first_name},
    
Request Your Forward Channels**""",
        buttons=[
            [Button.url("Update Channel", url="https://t.me/Star_Bots_Tamil")],
            [Button.url("Add me to Your Channel", url="https://t.me/Auto_Forward_Star_Bot?startchannel=StarBots&admin"),
            Button.url("Add My Channels", url="https://t.me/TG_Karthik")],
        ],
        link_preview=False,
    )

@StarBotsTamil.on(events.NewMessage(pattern="/id"))
async def get_id(event):
    chat = await event.get_chat()
    if not chat:
        return

    if isinstance(chat, PeerUser):  # Private chat with the bot
        await event.respond(f"**💁🏻 Your ID is :-** `{chat.user_id}`", parse_mode='markdown')

    result = f"**👥 User ID :-** `{chat.id}`\n"
    if isinstance(chat, PeerChat) and chat.message_thread_id:
        result += f"**💬 Forum/Topic ID :-** `{chat.message_thread_id}`\n"

    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()

        if reply_message.forward.sender_id:  # Forwarded user
            sender = reply_message.forward.sender_id
            forwarder = reply_message.sender_id
            #user_entity = await StarBotsTamil.get_entity(forwarder)
            #full_user = await StarBotsTamil(GetFullUserRequest(user_entity))
            #display_name = full_user.user.first_name if full_user.user else "Unknown User" # Assuming you want the first name
            result += f"**💁🏻 Original Sender ID :-** `{sender}`\n"
            result += f"**⏩ Forwarder ID :-** `{forwarder}`"

        if reply_message.forward.chat_id:  # Forwarded channel
            channel = await StarBotsTamil.get_entity(reply_message.forward.chat_id)
            forwarder = reply_message.sender_id
            #user_entity = await StarBotsTamil.get_entity(forwarder)
            #full_user = await StarBotsTamil(GetFullUserRequest(user_entity))
            #display_name = full_user.user.first_name if full_user.user else "Unknown User"
            result += f"**💬 Channel {channel.title} ID :-** `-100{channel.id}`\n"
            result += f"**⏩ Forwarder ID :-** `{forwarder}`"

    await event.respond(result, parse_mode='markdown')

# MongoDB connection setup
def init_db():
    client = pymongo.MongoClient("mongodb+srv://KarthikMovies:KarthikUK007@cluster0.4l5byki.mongodb.net/?retryWrites=true&w=majority")  # Change the URI for remote DB if needed
    db = client["channel_data"]  # Database name
    collection = db["channels"]  # Collection name
    return collection

# Insert or Update Channel Info in MongoDB
def set_channel(user_id, source_channel_id, destination_channel_ids, original_text, replace_text, my_link, web_link, my_username, command_type):
    collection = init_db()

    # Prepare data to insert or update
    channel_data = {
        "user_id": user_id,
        "source_channel_id": source_channel_id,
        "destination_channel_ids": destination_channel_ids,
        "original_text": original_text,
        "replace_text": replace_text,
        "my_link": my_link,
        "web_link": web_link,
        "my_username": my_username,
        "title": title,
        "command_type": command_type
    }

    # Insert or update the document
    collection.update_one(
        {"user_id": user_id},  # Filter by user_id
        {"$set": channel_data},  # Update the document with the new data
        upsert=True  # If the document doesn't exist, insert it
    )

@StarBotsTamil.on(events.NewMessage(pattern="/set_channel 1"))
async def set_channel_command_1(event):
    user_id = event.sender_id
    args = event.message.text.split()

    # Ensure there are enough arguments
    if len(args) < 9:
        await event.reply("Usage: /set_channel 1 <source_channel_id> <destination_channel_ids> <original:replace> <my_link> <web_link> <my_username> <title>")
        return

    source_channel_id = args[1]
    destination_channel_ids = args[2].split(',')
    original_text, replace_text = args[3].split(':')
    my_link = None if args[4] == "None" else args[4]
    web_link = None if args[5] == "None" else args[5]
    my_username = None if args[6] == "None" else args[6]
    title = ' '.join(args[7:])  # Everything after the 7th index is the title

    # Prepare data to store in MongoDB
    data = {
        "user_id": user_id,
        "command_type": 1,
        "source_channel_id": source_channel_id,
        "destination_channel_ids": destination_channel_ids,
        "original_text": original_text,
        "replace_text": replace_text,
        "my_link": my_link,
        "web_link": web_link,
        "my_username": my_username,
        "title": title  # Save title in the database
    }

    # Insert or update the document in the database
    collection = init_db()
    collection.update_one(
        {"user_id": user_id, "command_type": 1},
        {"$set": data},
        upsert=True
    )

    await event.reply(f"Channel settings have been updated for Command Type 1 with title '{title}'")

@StarBotsTamil.on(events.NewMessage(pattern="/get_channel 1"))
async def get_channel_command_1(event):
    user_id = event.sender_id

    # Fetch channel data from MongoDB for command_type 1
    collection = init_db()
    channel_data = collection.find_one({"user_id": user_id, "command_type": 1})

    if channel_data:
        # Extracting relevant information including title
        title = channel_data.get("title", "No title set")
        source_channel_id = channel_data.get("source_channel_id")
        destination_channel_ids = channel_data.get("destination_channel_ids")
        original_text = channel_data.get("original_text")
        replace_text = channel_data.get("replace_text")
        my_link = channel_data.get("my_link") if channel_data.get("my_link") else "None"
        web_link = channel_data.get("web_link")
        my_username = channel_data.get("my_username")

        # Sending the response to the user with all the stored information
        await event.reply(f"""
        Command Type: 1
        Title: {title}
        Source Channel ID: {source_channel_id}
        Destination Channel IDs: {', '.join(map(str, destination_channel_ids))}
        Original Text: {original_text}
        Replace Text: {replace_text}
        My Link: {my_link}
        Web Link: {web_link}
        My Username: {my_username}
        """)
    else:
        await event.reply("No channel information found for Command Type 1. Please set your channel using /set_channel.")

# First Forward 
async def replace_links_in_message(message):
    if replacement_web_link:
        message = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', replacement_web_link, message)
    if replacement_link:
        message = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link, message)
    if replacement_username:
        message = re.sub(r'@[\w]+', replacement_username, message)
    message = message.replace('/ql', '/qbleech')
    return message

async def replace_links_in_caption(caption):
    if replacement_web_link:
        caption = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', replacement_web_link, caption)
    if replacement_link:
        caption = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link, caption)
    if replacement_username:
        caption = re.sub(r'@[\w]+', replacement_username, caption)
    caption = caption.replace('/ql', '/qbleech')
    return caption

# Second Forward 
async def replace_links_in_message2(message):
    if replacement_web_link2:
        message = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', replacement_web_link2, message)
    if replacement_link2:
        message = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link2, message)
    if replacement_username2:
        message = re.sub(r'@[\w]+', replacement_username2, message)
    message = message.replace('/ql', '/qbleech2')
    return message

async def replace_links_in_caption2(caption):
    if replacement_web_link2:
        caption = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', replacement_web_link2, caption)
    if replacement_link2:
        caption = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link2, caption)
    if replacement_username2:
        caption = re.sub(r'@[\w]+', replacement_username2, caption)
    caption = caption.replace('/ql', '/qbleech2')
    return caption

# Third Forward
async def replace_links_in_message3(message):
    if replacement_web_link3:
        message = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', replacement_web_link3, message)
    if replacement_link3:
        message = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link3, message)
    if replacement_username3:
        message = re.sub(r'@[\w]+', replacement_username3, message)
    message = message.replace('/qbleech2', '/qbleech')
    return message

async def replace_links_in_caption3(caption):
    if replacement_web_link3:
        caption = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', replacement_web_link3, caption)
    if replacement_link3:
        caption = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link3, caption)
    if replacement_username3:
        caption = re.sub(r'@[\w]+', replacement_username3, caption)
    caption = caption.replace('/qbleech2', '/qbleech')
    return caption

# Fourth Forward
async def replace_links_in_message4(message):
    if replacement_web_link4:
        message = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', replacement_web_link4, message)
    if replacement_link4:
        message = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link4, message)
    if replacement_username4:
        message = re.sub(r'@[\w]+', replacement_username4, message)
    message = message.replace('/qbleech2', '/qbleech')
    return message

async def replace_links_in_caption4(caption):
    if replacement_web_link4:
        caption = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', replacement_web_link4, caption)
    if replacement_link4:
        caption = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link4, caption)
    if replacement_username4:
        caption = re.sub(r'@[\w]+', replacement_username4, caption)
    caption = caption.replace('/qbleech2', '/qbleech')
    return caption

# First Forward 
forwarded_messages = {}

@user_client.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    user_id = event.sender_id
    if not event.is_private:
        try:
            message = event.message
            message_id = message.id  # Use message ID as a key to track the message
            if message_id in forwarded_messages:
                time_sent = forwarded_messages[message_id]
                time_elapsed = (datetime.now() - time_sent).total_seconds()
                if time_elapsed < 300:  # 5 minutes
                    return  # Don't forward if it's less than 5 minutes
            if message.media:
                if getattr(message, 'message', None):
                    replaced_caption = await replace_links_in_caption(message.message)
                    message.message = replaced_caption
                for destination_channel_id in destination_channels:
                    await event.client.send_message(destination_channel_id, message, link_preview=False)
            else:
                replaced_message = await replace_links_in_message(message.text)
                for destination_channel_id in destination_channels:
                    await event.client.send_message(destination_channel_id, replaced_message, link_preview=False)

            forwarded_messages[message_id] = datetime.now()
            await asyncio.sleep(300)
            for destination_channel_id in destination_channels:
                await event.client.send_message(destination_channel_id, message, link_preview=False)

        except Exception as e:
            logger.error(f"Failed to forward the message: {str(e)}")
            
# second forward
forwarded_messages2 = {}

@user_client.on(events.NewMessage(chats=source_channel2))
async def forward_message(event):
    user_id = event.sender_id
    if not event.is_private:
        try:
            message = event.message
            message_id = message.id  # Use message ID as a key to track the message
            if message_id in forwarded_messages2:
                time_sent = forwarded_messages2[message_id]
                time_elapsed = (datetime.now() - time_sent).total_seconds()
                if time_elapsed < 300:  # 5 minutes
                    return  # Don't forward if it's less than 5 minutes
            if message.media:
                if getattr(message, 'message', None):
                    replaced_caption2 = await replace_links_in_caption2(message.message)
                    message.message = replaced_caption2
                for destination_channel_id in destination_channels2:
                    await event.client.send_message(destination_channel_id, message, link_preview=False)
            else:
                replaced_message2 = await replace_links_in_message2(message.text)
                for destination_channel_id in destination_channels2:
                    await event.client.send_message(destination_channel_id, replaced_message2, link_preview=False)

            forwarded_messages2[message_id] = datetime.now()
            await asyncio.sleep(300)
            for destination_channel_id in destination_channels2:
                await event.client.send_message(destination_channel_id, message, link_preview=False)

        except Exception as e:
            logger.error(f"Failed to forward the message: {str(e)}")

# Third Forward 
@user_client.on(events.NewMessage(chats=source_channel3))  # Changed source_channel2 to source_channel3
async def forward_message(event):
    user_id = event.sender_id
    if event.message.text == "Bot Started!":
        return
    if not event.is_private:
        try:
            if event.message.media:
                if getattr(event.message, 'message', None):
                    replaced_caption3 = await replace_links_in_caption3(event.message.message)  # Changed to replace_links_in_caption3
                    event.message.message = replaced_caption3
                for destination_channel_id in destination_channels3:  # Changed to destination_channels3
                    await event.client.send_message(destination_channel_id, event.message)
            else:
                replaced_message3 = await replace_links_in_message3(event.message.text)  # Changed to replace_links_in_message3
                for destination_channel_id in destination_channels3:  # Changed to destination_channels3
                    await event.client.send_message(destination_channel_id, replaced_message3)

        except Exception as e:
            logger.error(f"Failed to forward the message: {str(e)}")

# Fourth Forward 
@user_client.on(events.NewMessage(chats=source_channel4))  # Changed source_channel3 to source_channel4
async def forward_message(event):
    user_id = event.sender_id
    if event.message.text == "Bot Started!":
        return
    if not event.is_private:
        try:
            if event.message.media:
                if getattr(event.message, 'message', None):
                    replaced_caption4 = await replace_links_in_caption4(event.message.message)  # Changed to replace_links_in_caption4
                    event.message.message = replaced_caption4
                for destination_channel_id in destination_channels4:  # Changed to destination_channels4
                    await event.client.send_message(destination_channel_id, event.message)
            else:
                replaced_message4 = await replace_links_in_message4(event.message.text)  # Changed to replace_links_in_message4
                for destination_channel_id in destination_channels4:  # Changed to destination_channels4
                    await event.client.send_message(destination_channel_id, replaced_message4)

        except Exception as e:
            logger.error(f"Failed to forward the message: {str(e)}")

#Define your aiohttp web server handler
async def root_route_handler(request):
    return web.json_response(text="Bot Maintenance By :- https://telegram.me/Star_Bots_Tamil")

# Define your custom route for receiving updates from Telegram
async def telegram_webhook_handler(request):
    try:
        data = await request.json()
        await StarBotsTamil.process_updates(data)
    except Exception as e:
        print(f"Error processing Telegram update: {e}")
    return web.Response()

# Define your ping server
async def ping_server():
    sleep_time = config("PING_INTERVAL", cast=int)
    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(config("URL")) as resp:
                    logging.info("Pinged server with response: {}".format(resp.status))
        except TimeoutError:
            logging.warning("Couldn't connect to the site URL..!")
        except Exception:
            traceback.print_exc()

# Your main function
async def main():
    webhook_path = config("WEBHOOK_PATH")
    app.router.add_post(webhook_path, telegram_webhook_handler)
    app.router.add_get("/", root_route_handler)

# Start the web server
    port = config("PORT", cast=int)
    webhook_address = config("WEBHOOK_ADDRESS")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, webhook_address, port)
    await site.start()
    # Start the Telethon client and ping server concurrently
    await asyncio.gather(StarBotsTamil.run_until_disconnected(), ping_server())
    logger.info("Bot has Started.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
