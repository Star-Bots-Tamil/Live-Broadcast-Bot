import logging
import re
import asyncio
import aiohttp
import traceback
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

source_channel_str3 = config("SOURCE_CHANNEL3")
source_channel3 = [int(channel_id.strip()) for channel_id in source_channel_str3.split(' ')]

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
    destination_channels3 = config("DESTNATION_CHANNELS3", cast=int)
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
