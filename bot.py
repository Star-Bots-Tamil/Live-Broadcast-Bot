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

app = web.Application()

logger.info("Starting...")

try:
    api_id = config("APP_ID", cast=int)
    api_hash = config("HASH")
    bot_token = config("TOKEN")
    string_session = config("STRING_SESSION")
    user_client = TelegramClient(StringSession(string_session), api_id, api_hash)
    user_client.start()
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

def set_channel(user_id, source_channel_id, destination_channel_ids, original_text, replace_text, my_link, web_link, my_username, command_type):
    collection = init_db()
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
    collection.update_one(
        {"user_id": user_id},  # Filter by user_id
        {"$set": channel_data},  # Update the document with the new data
        upsert=True  # If the document doesn't exist, insert it
    )

def get_channel(user_id):
    collection = init_db()
    channel_data = collection.find_one({"user_id": user_id})
    if channel_data:
        return channel_data
    else:
        return None

@StarBotsTamil.on(events.NewMessage(pattern="/set_channel"))
async def set_channel_command(event):
    if event.sender_id not in admin_user_id:
        await event.reply("You do not have permission to use this command.")
        return
    user_id = event.sender_id
    args = event.message.text.split()
    if len(args) < 9:
        await event.reply("Usage: /set_channel <command_type> <source_channel_id> <destination_channel_ids> <original:replace> <my_link> <web_link> <my_username> <title>")
        return
    command_type = int(args[1])  # Get command_type (1, 2, 3, or 4)
    source_channel_id = args[2]
    destination_channel_ids = args[3].split(',')
    original_text, replace_text = args[4].split(':')
    my_link = None if args[5] == "None" else args[5]
    web_link = None if args[6] == "None" else args[6]
    my_username = None if args[7] == "None" else args[7]
    title = ' '.join(args[8:])  # Everything after the 8th index is the title
    data = {
        "user_id": user_id,
        "command_type": command_type,
        "source_channel_id": source_channel_id,
        "destination_channel_ids": destination_channel_ids,
        "original_text": original_text,
        "replace_text": replace_text,
        "my_link": my_link,
        "web_link": web_link,
        "my_username": my_username,
        "title": title  # Save title in the database
    }
    collection = init_db()
    collection.update_one(
        {"user_id": user_id, "command_type": command_type},
        {"$set": data},
        upsert=True
    )
    await event.reply(f"Channel settings have been updated for Command Type {command_type} with title '{title}'")

@StarBotsTamil.on(events.NewMessage(pattern="/get_channel"))
async def get_channel_command(event):
    user_id = event.sender_id
    if event.sender_id not in admin_user_id:
        await event.reply("You do not have permission to use this command.")
        return
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply("Usage: /get_channel <command_type>")
        return

    command_type = int(args[1])  # Get command_type (1, 2, 3, or 4)
    collection = init_db()
    channel_data = collection.find_one({"user_id": user_id, "command_type": command_type})

    if channel_data:
        response = f"Command Type {command_type} settings for user {user_id}:\n"
        response += f"Source Channel ID: {channel_data['source_channel_id']}\n"
        response += f"Destination Channel IDs: {', '.join(channel_data['destination_channel_ids'])}\n"
        response += f"Original Text: {channel_data['original_text']}\n"
        response += f"Replace Text: {channel_data['replace_text']}\n"
        response += f"My Link: {channel_data['my_link'] if channel_data['my_link'] else 'None'}\n"
        response += f"Web Link: {channel_data['web_link'] if channel_data['web_link'] else 'None'}\n"
        response += f"My Username: {channel_data['my_username'] if channel_data['my_username'] else 'None'}\n"
        response += f"Title: {channel_data['title']}\n"
    else:
        response = f"No settings found for Command Type {command_type} for user {user_id}."
    await event.reply(response)

async def replace_links_in_message(message, web_link, my_link, my_username, original_text, replace_text):
    if web_link:
        message = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', web_link, message)
    if my_link:
        message = re.sub(r'https?://t\.me\S*|t\.me\S*', my_link, message)
    if my_username:
        message = re.sub(r'@[\w]+', my_username, message)
    message = message.replace(original_text, replace_text)
    return message

async def replace_links_in_caption(caption, web_link, my_link, my_username, original_text, replace_text):
    if web_link:
        caption = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', web_link, caption)
    if my_link:
        caption = re.sub(r'https?://t\.me\S*|t\.me\S*', my_link, caption)
    if my_username:
        caption = re.sub(r'@[\w]+', my_username, caption)
    caption = caption.replace(original_text, replace_text)
    return caption

command_type_to_channels = {
    1: ["source_channel"],  # Command type 1 has these channels
    2: ["source_channel_2"],  # Command type 2 has these channels
    3: ["source_channel_3"],  # Command type 3 has these channels
    4: ["source_channel_4"],  # Command type 4 has these channels
    5: ["source_channel_5"],  # Command type 5 has these channels
}

source_channel = command_type_to_channels.get(1, [])  # Get channels for command type 1
if source_channel:
    @user_client.on(events.NewMessage(chats=source_channel[0]))  # Listen to the source channel for command type 1
    async def forward_message(event, command_type=1):  # Pass command_type explicitly
        user_id = event.sender_id
        if event.message.text == "Bot Started!":
            return
        channel_data = get_channel(user_id)
        if not channel_data:
            logger.error(f"No data found for user_id: {user_id}")
            return  # If no data is found for the user, do not proceed
        command_type_data = next((config for config in channel_data if config.get("command_type") == command_type), None)
        if not command_type_data:
            logger.error(f"No settings found for command_type {command_type} for user_id: {user_id}")
            return  # If no settings are found for the identified command_type, skip processing
        destination_channels = command_type_data.get("destination_channel_ids", [])
        original_text = command_type_data.get("original_text", "")
        replace_text = command_type_data.get("replace_text", "")
        my_link = command_type_data.get("my_link", "")
        web_link = command_type_data.get("web_link", "")
        my_username = command_type_data.get("my_username", "")
        logger.info(f"Handling command_type {command_type} for user {user_id}: destination_channels={destination_channels}")
        if not event.is_private:
            try:
                if event.message.media:  # If the message contains media
                    if getattr(event.message, 'message', None):  # If the media has a caption
                        replaced_caption = await replace_links_in_caption(event.message.message, web_link, my_link, my_username, original_text, replace_text)
                        event.message.message = replaced_caption
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, event.message)
                
                else:  # If the message is just text
                    replaced_message = await replace_links_in_message(event.message.text, web_link, my_link, my_username, original_text, replace_text)
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, replaced_message)

            except Exception as e:
                logger.error(f"Failed to forward the message for command_type {command_type}: {str(e)}")
                
# For command type 2, create a similar listener for source channel 2
source_channel_2 = command_type_to_channels.get(2, [])  # Get channels for command type 2
if source_channel_2:
    @user_client.on(events.NewMessage(chats=source_channel_2[0]))  # Listen to the source channel for command type 2
    async def forward_message(event, command_type=2):  # Pass command_type explicitly
        user_id = event.sender_id
        if event.message.text == "Bot Started!":
            return
        channel_data = get_channel(user_id)
        if not channel_data:
            logger.error(f"No data found for user_id: {user_id}")
            return  # If no data is found for the user, do not proceed
        command_type_data = next((config for config in channel_data if config.get("command_type") == command_type), None)
        if not command_type_data:
            logger.error(f"No settings found for command_type {command_type} for user_id: {user_id}")
            return  # If no settings are found for the identified command_type, skip processing
        destination_channels = command_type_data.get("destination_channel_ids", [])
        original_text = command_type_data.get("original_text", "")
        replace_text = command_type_data.get("replace_text", "")
        my_link = command_type_data.get("my_link", "")
        web_link = command_type_data.get("web_link", "")
        my_username = command_type_data.get("my_username", "")
        logger.info(f"Handling command_type {command_type} for user {user_id}: destination_channels={destination_channels}")
        if not event.is_private:
            try:
                if event.message.media:  # If the message contains media
                    if getattr(event.message, 'message', None):  # If the media has a caption
                        replaced_caption = await replace_links_in_caption(event.message.message, web_link, my_link, my_username, original_text, replace_text)
                        event.message.message = replaced_caption
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, event.message)
                
                else:  # If the message is just text
                    replaced_message = await replace_links_in_message(event.message.text, web_link, my_link, my_username, original_text, replace_text)
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, replaced_message)

            except Exception as e:
                logger.error(f"Failed to forward the message for command_type {command_type}: {str(e)}")

# For command type 3, create a similar listener for source channel 3
source_channel_3 = command_type_to_channels.get(3, [])  # Get channels for command type 3
if source_channel_3:
    @user_client.on(events.NewMessage(chats=source_channel_3[0]))  # Listen to the source channel for command type 3
    async def forward_message(event, command_type=3):  # Pass command_type explicitly
        user_id = event.sender_id
        if event.message.text == "Bot Started!":
            return
        channel_data = get_channel(user_id)
        if not channel_data:
            logger.error(f"No data found for user_id: {user_id}")
            return  # If no data is found for the user, do not proceed
        command_type_data = next((config for config in channel_data if config.get("command_type") == command_type), None)
        if not command_type_data:
            logger.error(f"No settings found for command_type {command_type} for user_id: {user_id}")
            return  # If no settings are found for the identified command_type, skip processing
        destination_channels = command_type_data.get("destination_channel_ids", [])
        original_text = command_type_data.get("original_text", "")
        replace_text = command_type_data.get("replace_text", "")
        my_link = command_type_data.get("my_link", "")
        web_link = command_type_data.get("web_link", "")
        my_username = command_type_data.get("my_username", "")
        logger.info(f"Handling command_type {command_type} for user {user_id}: destination_channels={destination_channels}")
        if not event.is_private:
            try:
                if event.message.media:  # If the message contains media
                    if getattr(event.message, 'message', None):  # If the media has a caption
                        replaced_caption = await replace_links_in_caption(event.message.message, web_link, my_link, my_username, original_text, replace_text)
                        event.message.message = replaced_caption
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, event.message)
                
                else:  # If the message is just text
                    replaced_message = await replace_links_in_message(event.message.text, web_link, my_link, my_username, original_text, replace_text)
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, replaced_message)

            except Exception as e:
                logger.error(f"Failed to forward the message for command_type {command_type}: {str(e)}")

# For command type 4, create a similar listener for source channel 4
source_channel_4 = command_type_to_channels.get(4, [])  # Get channels for command type 4
if source_channel_4:
    @user_client.on(events.NewMessage(chats=source_channel_4[0]))  # Listen to the source channel for command type 4
    async def forward_message(event, command_type=4):  # Pass command_type explicitly
        user_id = event.sender_id
        if event.message.text == "Bot Started!":
            return
        channel_data = get_channel(user_id)
        if not channel_data:
            logger.error(f"No data found for user_id: {user_id}")
            return  # If no data is found for the user, do not proceed
        command_type_data = next((config for config in channel_data if config.get("command_type") == command_type), None)
        if not command_type_data:
            logger.error(f"No settings found for command_type {command_type} for user_id: {user_id}")
            return  # If no settings are found for the identified command_type, skip processing
        destination_channels = command_type_data.get("destination_channel_ids", [])
        original_text = command_type_data.get("original_text", "")
        replace_text = command_type_data.get("replace_text", "")
        my_link = command_type_data.get("my_link", "")
        web_link = command_type_data.get("web_link", "")
        my_username = command_type_data.get("my_username", "")
        logger.info(f"Handling command_type {command_type} for user {user_id}: destination_channels={destination_channels}")
        if not event.is_private:
            try:
                if event.message.media:  # If the message contains media
                    if getattr(event.message, 'message', None):  # If the media has a caption
                        replaced_caption = await replace_links_in_caption(event.message.message, web_link, my_link, my_username, original_text, replace_text)
                        event.message.message = replaced_caption
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, event.message)
                
                else:  # If the message is just text
                    replaced_message = await replace_links_in_message(event.message.text, web_link, my_link, my_username, original_text, replace_text)
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, replaced_message)

            except Exception as e:
                logger.error(f"Failed to forward the message for command_type {command_type}: {str(e)}")

# For command type 5, create a similar listener for source channel 5
source_channel_5 = command_type_to_channels.get(5, [])  # Get channels for command type 5
if source_channel_5:
    @user_client.on(events.NewMessage(chats=source_channel_5[0]))  # Listen to the source channel for command type 5
    async def forward_message(event, command_type=5):  # Pass command_type explicitly
        user_id = event.sender_id
        if event.message.text == "Bot Started!":
            return
        channel_data = get_channel(user_id)
        if not channel_data:
            logger.error(f"No data found for user_id: {user_id}")
            return  # If no data is found for the user, do not proceed
        command_type_data = next((config for config in channel_data if config.get("command_type") == command_type), None)
        if not command_type_data:
            logger.error(f"No settings found for command_type {command_type} for user_id: {user_id}")
            return  # If no settings are found for the identified command_type, skip processing
        destination_channels = command_type_data.get("destination_channel_ids", [])
        original_text = command_type_data.get("original_text", "")
        replace_text = command_type_data.get("replace_text", "")
        my_link = command_type_data.get("my_link", "")
        web_link = command_type_data.get("web_link", "")
        my_username = command_type_data.get("my_username", "")
        logger.info(f"Handling command_type {command_type} for user {user_id}: destination_channels={destination_channels}")
        if not event.is_private:
            try:
                if event.message.media:  # If the message contains media
                    if getattr(event.message, 'message', None):  # If the media has a caption
                        replaced_caption = await replace_links_in_caption(event.message.message, web_link, my_link, my_username, original_text, replace_text)
                        event.message.message = replaced_caption
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, event.message)
                
                else:  # If the message is just text
                    replaced_message = await replace_links_in_message(event.message.text, web_link, my_link, my_username, original_text, replace_text)
                    for destination_channel_id in destination_channels:
                        await event.client.send_message(destination_channel_id, replaced_message)

            except Exception as e:
                logger.error(f"Failed to forward the message for command_type {command_type}: {str(e)}")
                
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
