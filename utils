from telethon.tl.types import InputPhoneContact, PeerChannel, PeerUser

# send message to user
    async def send_message_normal(self, msg):
        try:
            await self.client.send_message(
                entity=msg.entity,
                message=msg.message,
                reply_to=msg.reply_to,
                silent=True,
                background=True
            )
            print("# Success | Message delivered to " + str(msg.entity))
        except:
            print("# Error | Unable to send the message")

    # Get message information from replied message (sender)
    async def get_sender_id(self, message):
        sender_id = message.sender_id
        sender_entity = await self.client.get_entity(int(sender_id))
        user_username = sender_entity.username if sender_entity.username else None
        show_username = f"`@{user_username}`\n" if user_username else ""

        sender = {
            "username" : show_username,
            "chat_id" : message.chat_id,
            "user_id" : sender_id,
            "message_id" : message.id
        }

        return sender


    # Get message information from replied message (forwarded)
    async def get_forwarded_id(self, message):
        if message.forward:
            data = message.forward
            if isinstance(data.from_id, PeerChannel):
                from_id = data.from_id.channel_id
                from_id = "-100" + str(from_id)
            elif isinstance(data.from_id, PeerUser):
                from_id = data.from_id.user_id
            
            entity = await self.client.get_entity(int(from_id))
            username = entity.username if entity.username else None
            show_username = f"`@{username}`\n" if username else ""
            try:
                name = entity.title 
            except:
                name = entity.first_name
            message_id = data.channel_post if data.channel_post else None
            show_message_id = f"Message ID : `{message_id}`\n" if message_id else ""
            forwarded = {
                "username" : show_username,
                "id" : from_id,
                "name" : name,
                "message_id" : show_message_id
            }
            return forwarded
        return None
