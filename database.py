from pymongo import MongoClient
from decouple import config

class Database:
    def __init__(self):
        self.client = MongoClient(config("MONGO_URI"))  # MongoDB URI from config
        self.db = self.client.get_database()  # Default database
        self.channels_collection = self.db.channels  # Collection for channels data
        self.replacements_collection = self.db.replacements  # Collection for replacement data

    def add_channel(self, source_channel, source_channel_name, destination_channels=None, my_link='', web_link='', my_username=''):
        """
        Add a new channel entry to the database.
        """
        channel_data = {
            "source_channel": source_channel,
            "source_channel_name": source_channel_name,
            "destination_channels": destination_channels or [],
            "my_link": my_link,
            "web_link": web_link,
            "my_username": my_username,
        }
        self.channels_collection.update_one(
            {"source_channel": source_channel},
            {"$set": channel_data},
            upsert=True
        )

    def get_channel(self, source_channel):
        """
        Retrieve a channel's data based on the source_channel.
        """
        return self.channels_collection.find_one({"source_channel": source_channel})

    def remove_channel(self, source_channel):
        """
        Remove a channel entry from the database.
        """
        self.channels_collection.delete_one({"source_channel": source_channel})

    def add_replacement(self, replacement_key, replacement_value):
        """
        Add replacement link details to the database.
        """
        replacement_data = {
            "replacement_key": replacement_key,
            "replacement_value": replacement_value
        }
        self.replacements_collection.update_one(
            {"replacement_key": replacement_key},
            {"$set": replacement_data},
            upsert=True
        )

    def get_replacement(self, replacement_key):
        """
        Retrieve a replacement link value by its key.
        """
        replacement = self.replacements_collection.find_one({"replacement_key": replacement_key})
        if replacement:
            return replacement["replacement_value"]
        return None

    def remove_replacement(self, replacement_key):
        """
        Remove a replacement entry from the database.
        """
        self.replacements_collection.delete_one({"replacement_key": replacement_key})

# Example usage of the Database class:
if __name__ == "__main__":
    db = Database()

    # Retrieve source channels and destination channels from config (simulating loading from .env)
    source_channel = config("SOURCE_CHANNEL", cast=int)
    source_channel2 = config("SOURCE_CHANNEL2", cast=int)
    source_channel3 = config("SOURCE_CHANNEL3", cast=int)
    source_channel4 = config("SOURCE_CHANNEL4", cast=int)

    # Retrieve destination channels for each source
    destination_channels1 = [config("DESTNATION_CHANNELS", cast=int)]
    destination_channels2 = [config("DESTNATION_CHANNELS2", cast=int)]
    destination_channels3 = [config("DESTNATION_CHANNELS3", cast=int)]
    destination_channels4 = [config("DESTNATION_CHANNELS4", cast=int)]

    # Retrieve replacement links and usernames
    my_link = config("MY_LINK", default="")
    web_link = config("WEB_LINK", default="")
    my_username = config("MY_USERNAME", default="")
    
    my_link2 = config("MY_LINK2", default="")
    web_link2 = config("WEB_LINK2", default="")
    my_username2 = config("MY_USERNAME2", default="")
    
    my_link3 = config("MY_LINK3", default="")
    web_link3 = config("WEB_LINK3", default="")
    my_username3 = config("MY_USERNAME3", default="")
    
    my_link4 = config("MY_LINK4", default="")
    web_link4 = config("WEB_LINK4", default="")
    my_username4 = config("MY_USERNAME4", default="")

    # Add channels and associated data to the database
    db.add_channel(source_channel, "Source Channel 1", destination_channels1, my_link, web_link, my_username)
    db.add_channel(source_channel2, "Source Channel 2", destination_channels2, my_link2, web_link2, my_username2)
    db.add_channel(source_channel3, "Source Channel 3", destination_channels3, my_link3, web_link3, my_username3)
    db.add_channel(source_channel4, "Source Channel 4", destination_channels4, my_link4, web_link4, my_username4)

    # Example to fetch and print a channel's details
    print(db.get_channel(source_channel))
    print(db.get_channel(source_channel2))

    # Add replacement text
    db.add_replacement("MY_LINK", my_link)
    db.add_replacement("MY_USERNAME", my_username)

    # Example to fetch and print a replacement link
    print(db.get_replacement("MY_LINK"))
    print(db.get_replacement("MY_USERNAME"))

    # Remove a replacement and a channel
    db.remove_replacement("MY_LINK")
    db.remove_channel(source_channel)
