import logging
import re
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from decouple import config
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import pack_bot_file_id

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

destination_channels_str = config("DESTNATION_CHANNELS")
destination_channels = [int(channel_id.strip()) for channel_id in destination_channels_str.split(',')]

replacement_link = config("MY_LINK", default=None)
replacement_username = config("MY_USERNAME", default=None)

logger.info("Starting...")

try:
    api_id = config("APP_ID", cast=int)
    api_hash = config("HASH")
#    string_session = config("STRING_SESSION")
#    user_client = TelegramClient(StringSession(string_session), api_id, api_hash)
#    user_client.start()
    bot_token = config("TOKEN")
    source_channel = config("SOURCE_CHANNELS", cast=int)
    admin_user_id = config("ADMIN_USER_ID", cast=int)
    datgbot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
except Exception as e:
    logger.error(f"Error initializing the bot: {str(e)}")
    logger.error("Bot is quitting...")
    exit()

@datgbot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(
        f"""Hi 👋🏻 {event.sender.first_name},
I'm [Auto Forward Star Bots](https://t.me/Auto_Forward_Star_Bot) to Maintain Your Channels. I am very useful for the Channel Admin who have many Channels.

See /help for more Details.

Maintained By :- [Star Bots Tamil](https://t.me/Star_Bots_Tamil)""",
        buttons=[
            Button.url("Update Channel", url="https://t.me/Star_Bots_Tamil"),
        ],[
            Button.url("Add me to Your Channel", url="https://t.me/Auto_Forward_Star_Bot?startchannel=StarBots&admin"),
            Button.url("Add My Channels", url="https://t.me/TG_Karthik"),
        ],
        link_preview=False,
    )

@datgbot.on(events.NewMessage(pattern="/help"))
async def help(event):
    user_id = event.sender_id
    if user_id == admin_user_id:
        try:
            await event.reply("**Help**\n\n**❄About this bot:\n➡This bot will send all new posts from the source channel to one or more channels (without the forwarded tag)!**\n\n**❄How to use me?\n🏮Add the account to the channels.\n🏮Make me an admin in destination channels.\n🏮Now all new messages would be autoposted on the linked channels!!**\n\n**Liked the bot?** [Get Code](https://t.me/WolfOfficials)", link_preview=False)
        except Exception as e:
            logger.error(f"Error processing /help command: {str(e)}")
    else:
        await event.reply("You are not authorized to use the bot.")

@datgbot.on(events.NewMessage(pattern="/id"))
async def get_ids(event):
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await datgbot.send_message(
                event.chat_id,
                "**Chat ID :- `{}`\nUser ID :- `{}`**".format(
                    str(event.chat_id), str(r_msg.from_id), bot_api_file_id
                ),
            )
        else:
            await datgbot.send_message(
                event.chat_id,
                "**Chat ID :- `{}`\nUser ID :- `{}`**".format(
                    str(event.chat_id), str(r_msg.from_id)
                ),
            )
    else:
        await datgbot.send_message(
            event.chat_id, "**Chat ID :- `{}`**".format(str(event.chat_id))
        )

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
            logger.error(f"Failed to forward the message: {str(e)}")


logger.info("Bot has started.")
datgbot.run_until_disconnected()
