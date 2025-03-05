import anvil.tables as tables
from anvil.tables import app_tables
import anvil.users
import anvil.server
from datetime import datetime


@anvil.server.callable
def get_channels():
    if anvil.users.get_user():
        return app_tables.channels.search()
    return []


@anvil.server.callable
def add_message(channel, message):
    if anvil.users.get_user():
        app_tables.messages.add_row(from_user=anvil.users.get_user(), message=message, when=datetime.now(), to_channel=channel)

    
@anvil.server.callable
def get_messages(channel):
    if anvil.users.get_user():
        return app_tables.messages.search(tables.order_by('when', ascending=False), to_channel=channel)
