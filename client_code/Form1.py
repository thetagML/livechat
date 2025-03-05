from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.users


class Form1(Form1Template):
    def __init__(self, **properties):
        # You must call self.init_components() before doing anything else in this function
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        anvil.users.login_with_form()
        self.refresh_data_bindings()

        self.drop_down_channel.items = [
            (channel["name"], channel)
            for channel in anvil.server.call_s("get_channels")
        ]
        self.get_messages()

    def current_user_email(self):
        if anvil.users.get_user() is not None:
            return anvil.users.get_user()["email"]
        return "Nobody"

    def get_messages(self):
        self.repeating_panel_1.items = anvil.server.call_s(
            "get_messages", self.drop_down_channel.selected_value
        )

    def button_send_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.send_message()

    def text_box_message_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.send_message()

    def send_message(self):
        anvil.server.call(
            "add_message",
            self.drop_down_channel.selected_value,
            self.text_box_message.text,
        )
        self.get_messages()
        self.text_box_message.text = ""

    def drop_down_channel_change(self, **event_args):
        """This method is called when an item is selected"""
        self.get_messages()

    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds"""
        self.get_messages()

    def link_log_out_click(self, **event_args):
        """This method is called when the link is clicked"""
        anvil.users.logout()
        self.refresh_data_bindings()
        anvil.users.login_with_form()
        self.refresh_data_bindings()
