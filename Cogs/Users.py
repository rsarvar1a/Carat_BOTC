import nextcord
from nextcord.ext import commands

import utility


class Users(commands.Cog):
    def __init__(self, bot: commands.Bot, helper: utility.Helper):
        self.bot = bot
        self.helper = helper

    @commands.command()
    async def AddPlayer(self, ctx, game_number, players: commands.Greedy[nextcord.Member]):
        """Gives the appropriate game role to the given users.
        You can provide a user by ID, mention/ping, or nickname, though giving the nickname may find the wrong user."""
        if len(players) == 0:
            await utility.dm_user(ctx.author, "Usage: >AddPlayer [game number] [at least one user]")
            return

        player_names = [p.display_name for p in players]
        if self.helper.authorize_st_command(ctx.author, game_number):
            # React on Approval
            await utility.start_processing(ctx)
            for player in players:
                await player.add_roles(self.helper.get_game_role(game_number))
            await utility.dm_user(ctx.author,
                                  "You have assigned the game role for game " + str(game_number) +
                                  " to " + ", ".join(player_names))
            await utility.finish_processing(ctx)
        else:
            await utility.deny_command(ctx, "You are not the current ST for game " + str(game_number))

        await self.helper.log(
            f"{ctx.author.mention} has run the AddPlayer command on {', '.join(player_names)} for game {game_number}")

    @commands.command()
    async def RemovePlayer(self, ctx, game_number, players: commands.Greedy[nextcord.Member]):
        """Removes the appropriate game role from the given users.
        You can provide a user by ID, mention/ping, or nickname, though giving the nickname may find the wrong user."""
        if len(players) == 0:
            await utility.dm_user(ctx.author, "Usage: >RemovePlayer [game number] [at least one user]")
            return

        player_names = [p.display_name for p in players]
        if self.helper.authorize_st_command(ctx.author, game_number):
            # React on Approval
            await utility.start_processing(ctx)
            game_role = self.helper.get_game_role(game_number)
            for player in players:
                await player.remove_roles(game_role)
            await utility.dm_user(ctx.author,
                                  "You have removed the game role for game " + str(game_number) +
                                  " from " + ", ".join(player_names))
            await utility.finish_processing(ctx)
        else:
            await utility.deny_command(ctx, "You are not the current ST for game " + str(game_number))

        await self.helper.log(f"{ctx.author.mention} has run the RemovePlayer command "
                              f"on {', '.join(player_names)} for game {game_number}")

def setup(bot: commands.Bot):
    bot.add_cog(Users(bot, utility.Helper(bot)))
