from aiogram.utils import keyboard


def get_main_menu_keyboard() -> keyboard.ReplyKeyboardBuilder:
    """"""
    
    builder = keyboard.ReplyKeyboardBuilder()

    builder.button(text="Create reminder")
    builder.button(text="View reminders")
    builder.button(text="Update reminder")
    builder.button(text="Delete reminder")

    builder.adjust(2, 2)
    
    return builder
