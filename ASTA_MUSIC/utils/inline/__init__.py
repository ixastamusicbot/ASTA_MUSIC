from .extras import *
from .help import *
from .play import *
from .queue import *
from .settings import *
from .speed import *
from .start import *
from .sudolist import *

# Fix for telegram_markup import errors
from .play import stream_markup, stream_markup_timer

# Aliases for backward compatibility
telegram_markup = stream_markup
telegram_markup_timer = stream_markup_timer

# Dummy close_markup if not present in play.py
try:
    from .play import close_markup
except ImportError:
    from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    def close_markup(_):
        return InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="✖ Close", callback_data="close")]]
        )
