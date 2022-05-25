from __future__ import annotations
import re

from typing import TYPE_CHECKING

import aiomcrcon
import discord
from discord.ext import commands

import config
from cogs.utils.config import Config

if TYPE_CHECKING:
    from bot import Winry

    from .utils.context import Context


MC_COLOUR_REGEX = re.compile('§[a-zA-Z0-9]')


class Admin(commands.Cog):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot: Winry):
        self.bot: Winry = bot
        self.whitelist: Config[str] = Config('whitelist.json', loop=bot.loop)

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name='stafftools', id=314348604095594498)

    async def cog_check(self, ctx: Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    async def _exec_rcon(self, command: str) -> str:
        async with aiomcrcon.Client(
            config.mc_ip,
            config.mc_port,
            config.mc_password
        ) as client:
            resp = await client.send_cmd(command)
        content = MC_COLOUR_REGEX.sub('', resp[0])
        return content

    @commands.group('whitelist', is_hidden=True)
    async def _whitelist(self, ctx: Context):
        if ctx.subcommand_passed:
            return

    @_whitelist.command('add', aliases=['+'], is_hidden=True)
    async def whitelist_add(self, ctx: Context, target: discord.User, uuid: str):
        """Whitelists a given target with their UUID"""
        await self._exec_rcon(f'whitelist add {uuid}')
        await self.whitelist.put(target.id, uuid)
        await ctx.send(f'Successfully whitelisted {target} ({uuid})')

    @_whitelist.command('del', aliases=['remove', '-'], is_hidden=True)
    async def whitelist_del(self, ctx: Context, target: discord.User):
        """Removes a person from the current whitelist"""
        uuid = self.whitelist.get(target.id)
        await self._exec_rcon(f'whitelist remove {uuid}')
        await self.whitelist.remove(target.id)
        await ctx.send(f'Successfully removed {target} from the whitelist.')

    @_whitelist.command('list', is_hidden=True)
    async def whitelist_list(self, ctx: Context):
        """Lists currently whitelisted users."""
        results = []
        for user_id, uuid in self.whitelist:
            user = await self.bot.try_user(int(user_id))
            results.append(f'{user} ({uuid})')

        if not results:
            await ctx.send('There are no whitelisted users.')
            return

        await ctx.send('\n'.join(results))

    @commands.command(is_hidden=True)
    async def rcon(self, ctx: Context, *, command: str):
        """Sends a command via the Minecraft RCON protocol"""
        res = await self._exec_rcon(command)
        await ctx.send(res)


async def setup(bot):
    await bot.add_cog(Admin(bot))
