# ruff: noqa: E402
import os
from datetime import datetime
from logging import Formatter
from asyncio import gather

from pytz import timezone
from pyrogram import idle

from config import Config
from . import LOGGER, bot_loop
from .core.EchoClient import EchoBot
from .core.plugs import add_plugs
from .helper.utils.db import database
from .helper.utils.bot_cmds import _get_bot_commands


async def main():
    await database._load_all()

    def changetz(*args):
        return datetime.now(timezone(Config.TIMEZONE)).timetuple()

    Formatter.converter = changetz

    await gather(
        EchoBot.start(),
    )
    await EchoBot.bot.set_bot_commands(_get_bot_commands())

    add_plugs()

    if os.path.isfile(".restartmsg"):
        try:
            with open(".restartmsg") as f:
                chat_id, msg_id = map(int, f.read().splitlines())

            now = datetime.now(timezone(Config.TIMEZONE)).strftime(
                "%d/%m/%Y %I:%M:%S %p"
            )

            await EchoBot.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=f"<b>Restarted Successfully!</b>\n<code>{now}</code>",
            )

            os.remove(".restartmsg")
        except Exception as e:
            LOGGER.error(f"{e}")

    LOGGER.info("All EchoBot Services Started")

    await idle()

    await EchoBot.stop()


bot_loop.run_until_complete(main())
bot_loop.run_forever()
