from __future__ import annotations
import re

from typing import TYPE_CHECKING

import aiomcrcon
import discord
from discord.ext import commands

import config

if TYPE_CHECKING:
    from bot import Winry

    from .utils.context import Context


MC_COLOUR_REGEX = re.compile('§[a-zA-Z0-9]')


class Admin(commands.Cog):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot: Winry):
        self.bot: Winry = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='stafftools', id=314348604095594498)

    async def cog_check(self, ctx: Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(is_hidden=True)
    async def rcon(self, ctx: Context, *, command: str):
        """Sends a command via the Minecraft RCON protocol"""
        async with aiomcrcon.Client(
            config.mc_ip,
            config.mc_port,
            config.mc_password
        ) as client:
            resp = await client.send_cmd(command)
        content = MC_COLOUR_REGEX.sub('', resp[0])
        await ctx.send(content)


async def setup(bot):
    await bot.add_cog(Admin(bot))
