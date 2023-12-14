import logging
import re
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from decouple import config

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

destination_channels_str = config("DESTNATION_CHANNELS")
destination_channels = [int(channel_id.strip()) for channel_id in destination_channels_str.split(',')]
destination_channels_str2 = config("DESTNATION_CHANNELS2")
destination_channels2 = [int(channel_id.strip()) for channel_id in destination_channels_str2.split(',')]

replacement_link = config("MY_LINK", default=None)
replacement_username = config("MY_USERNAME", default=None)
replacement_link2 = config("MY_LINK2", default=None)
replacement_username2 = config("MY_USERNAME2", default=None)

logger.info("Starting...")

try:
    api_id = config("APP_ID", cast=int)
    api_hash = config("HASH")
#    string_session = config("STRING_SESSION")
#    user_client = TelegramClient(StringSession(string_session), api_id, api_hash)
#    user_client.start()
    bot_token = config("TOKEN")
    source_channel = config("SOURCE_CHANNEL", cast=int)
    source_channel2 = config("SOURCE_CHANNEL2", cast=int)
    admin_user_id = config("ADMIN_USER_ID", cast=int)
    datgbot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
except Exception as e:
    logger.error(f"Error initializing the bot: {str(e)}")
    logger.error("Bot is quitting...")
    exit()

@datgbot.on(events.NewMessage(pattern="/start"))
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

@datgbot.on(events.NewMessage(pattern="/help"))
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

@datgbot.on(events.NewMessage(pattern="/about"))
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

@datgbot.on(events.NewMessage(pattern="/forward"))
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

@datgbot.on(events.NewMessage(pattern="/id"))
async def getid(event):
    try:
        await get_id(update)
    except Exception as e:
        logger.error(f"Failed get id :- {str(e)}")

# First Forward 
async def replace_links_in_message(message):
    if replacement_link:
        message = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link, message)
    if replacement_username:
        message = re.sub(r'@[\w]+', replacement_username, message)
    return message

async def replace_links_in_caption(caption):
    if replacement_link:
        caption = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link, caption)
    if replacement_username:
        caption = re.sub(r'@[\w]+', replacement_username, caption)
    return caption

# Second Forward 
async def replace_links_in_message2(message):
    if replacement_link2:
        message = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link2, message)
    if replacement_username2:
        message = re.sub(r'@[\w]+', replacement_username2, message)
    return message

async def replace_links_in_caption2(caption):
    if replacement_link2:
        caption = re.sub(r'https?://t\.me\S*|t\.me\S*', replacement_link2, caption)
    if replacement_username2:
        caption = re.sub(r'@[\w]+', replacement_username2, caption)
    return caption

# First Forward 
@datgbot.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    user_id = event.sender_id
    if not event.is_private:
        try:
            if event.message.media:
                if getattr(event.message, 'message', None):
                    replaced_caption = await replace_links_in_caption(event.message.message)
                    event.message.message = replaced_caption
                for destination_channel_id in destination_channels:
                    await event.client.send_message(destination_channel_id, event.message)
            else:
                replaced_message = await replace_links_in_message(event.message.text)
                for destination_channel_id in destination_channels:
                    await event.client.send_message(destination_channel_id, replaced_message)
        except Exception as e:
            logger.error(f"Failed to First Forward the message: {str(e)}")

# Second Forward 
@datgbot.on(events.NewMessage(chats=source_channel2))
async def forward_message(event):
    user_id = event.sender_id
    if not event.is_private:
        try:
            if event.message.media:
                if getattr(event.message, 'message', None):
                    replaced_caption2 = await replace_links_in_caption2(event.message.message)
                    event.message.message = replaced_caption2
                for destination_channel_id in destination_channels2:
                    await event.client.send_message(destination_channel_id, event.message)
            else:
                replaced_message2 = await replace_links_in_message2(event.message.text)
                for destination_channel_id in destination_channels2:
                    await event.client.send_message(destination_channel_id, replaced_message)
        except Exception as e:
            logger.error(f"Failed to Second Forward the message: {str(e)}")

logger.info("Bot has started.")
datgbot.run_until_disconnected()
