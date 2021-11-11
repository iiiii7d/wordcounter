VERSION = ""
PREFIX = ","
import time
initstart = int(round(time.time() * 1000))

import discord
from discord.ext import commands
import os
import traceback
from typing import Optional

import tools
import keep_alive
from embed import help_embed

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        TOKEN = input("Token: ")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

class NoPermission(commands.CheckFailure):
    pass
def admin_only():
    async def predicate(ctx):
        if ctx.author.guild_permissions.administrator or ctx.author.id == 644052617500164097:
            return True
        raise NoPermission('**You are not an admin or 7d**')  
    return commands.check(predicate)

@bot.command()
async def info(ctx):
    await ctx.send(f"**Wordcounter by 7d**\nVersion {VERSION}")

@bot.command()
async def ping(ctx):
    ms = (ctx.message.id >> 22) + 1420070400000
    await ctx.send(tools.dedent(f"""**Pong!
    ```Client latency: {str(round(bot.latency * 1000, 5))}ms
    Response time: {str(int(round(time.time() * 1000)) - ms)}ms
    Uptime: {tools.ms_to_time(int(round(time.time() * 1000)) - initstart)}```**"""))

bot.remove_command('help')
@bot.command(name='help')
async def help_(ctx, *args):
    await ctx.send(embed=help_embed(' '.join(args), PREFIX))

@bot.command(name='eval')
@admin_only()
async def eval_(ctx, *, exp):
    try:
        await ctx.send(f"`{await eval(' '.join(exp))}`")
    except:
        try:
            await ctx.send(f"`{eval(' '.join(exp))}`")
        except:
            try: await ctx.send("```"+traceback.format_exc()+"```")
            except: print(traceback.format_exc())
@eval_.error
async def handle_error(ctx, error):
    if isinstance(error, NoPermission):
        await ctx.send(error)
    else:
        await ctx.send(error)


@bot.command()
@admin_only()
async def add(ctx, *, word):
    tools.tracked_add_word(word.lower())
    await ctx.send(f"Added `{word.lower()}` to tracker")
@add.error
async def handle_error(ctx, error):
    if isinstance(error, NoPermission):
        await ctx.send(error)
    else:
        await ctx.send(error, embed=help_embed('add', PREFIX))

@bot.command()
@admin_only()
async def remove(ctx, *, word):
    tools.tracked_remove_word(word.lower())
    await ctx.send(f"Removed `{word.lower()}` from tracker")
@remove.error
async def handle_error(ctx, error):
    if isinstance(error, NoPermission):
        await ctx.send(error)
    else:
        await ctx.send(error, embed=help_embed('remove', PREFIX))

@bot.command()
async def viewuser(ctx, user: Optional[discord.Member]=None):
    if user is None: user = ctx.author
    stats = tools.tracked_user_stats(user.id)
    embed = discord.Embed(title="Tracking stats", description="\n".join(f"{word}: {count}" for word, count in stats.items()))
    embed.set_author(name=await tools.fullname_from_id(user.id, bot), icon_url=(await bot.fetch_user(user.id)).avatar_url)
    await ctx.send(embed=embed)
@viewuser.error
async def handle_error(ctx, error):
    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.send(error)
    else:
        await ctx.send(error, embed=help_embed('viewuser', PREFIX))

@bot.command()
async def viewword(ctx, word):
    stats = tools.tracked_word_stats(' '.join(word).lower())
    desc = []
    for id_, count in stats.items():
        desc.append(f"{await tools.fullname_from_id(id_, bot)}: {count}")
    embed = discord.Embed(title="Tracking stats", description="\n".join(desc))
    embed.set_author(name=' '.join(word).lower())
    await ctx.send(embed=embed)
@viewword.error
async def handle_error(ctx, error):
    await ctx.send(error, embed=help_embed('viewuser', PREFIX))

@bot.event
async def on_message(message: discord.Message):
    try:
        if message.author == bot.user:
            return
        elif not message.content.startswith(PREFIX) or message.content == PREFIX:
            if tools.scan_content_for_tracker(message.author.id, message.content):
                await message.add_reaction("👀")
            return
        await bot.process_commands(message)

        '''@staticmethod
            async def cmd_track():
                if args.subcmd == "add":
                    if not (message.author.guild_permissions.administrator or message.author.id == 644052617500164097):
                        await message.channel.send("**You are not an admin or 7d**")
                        return
                    tools.tracked_add_word(' '.join(args.word).lower())
                    await message.channel.send(f"Added `{' '.join(args.word).lower()}` to tracker")
                elif args.subcmd == "remove":
                    if not (message.author.guild_permissions.administrator or message.author.id == 644052617500164097):
                        await message.channel.send("**You are not an admin or 7d**")
                        return
                    tools.tracked_remove_word(' '.join(args.word).lower())
                    await message.channel.send(f"Removed `{' '.join(args.word).lower()}` from tracker")
                elif args.subcmd == "viewuser":
                    if args.user is not None:
                        id_ = await tools.get_user_id(args.user, client)
                        if id_ is None:
                            await message.channel.send("**:x: User not found**")
                            return
                    stats = tools.tracked_user_stats(id_)
                    user = await client.fetch_user(id_)
                    embed = discord.Embed(title="Tracking stats", description="\n".join(f"{word}: {count}" for word, count in stats.items()))
                    embed.set_author(name=await tools.fullname_from_id(id_, client), icon_url=user.avatar_url)
                    await message.channel.send(embed=embed)
                elif args.subcmd == "viewword":
                    stats = tools.tracked_word_stats(' '.join(args.word).lower())
                    desc = []
                    for id_, count in stats.items():
                        desc.append(f"{await tools.fullname_from_id(id_, client)}: {count}")
                    embed = discord.Embed(title="Tracking stats", description="\n".join(desc))
                    embed.set_author(name=' '.join(args.word).lower())
                    await message.channel.send(embed=embed)
                elif args.subcmd == "list":
                    words = tools.tracked_get_words()
                    embed = discord.Embed(title="List of tracked words", description="\n".join(words))
                    await message.channel.send(embed=embed)
                else:
                    pass'''

    except:
        if "SystemExit: 0" in traceback.format_exc(): pass
        elif "discord.errors.Forbidden: 403 Forbidden (error code: 50001): Missing Access" in traceback.format_exc() or \
             "discord.errors.Forbidden: 403 Forbidden (error code: 50013): Missing Permissions" in traceback.format_exc():
            await message.channel.send("**Not enough perms:**\n```"+traceback.format_exc()+"```")
        else:
            try: await message.channel.send("```"+traceback.format_exc()+"```")
            except: print(traceback.format_exc())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="your mum"))
    print("Logged in as " + str(bot.user.name) + " (" + str(bot.user.id) + ")")
    print("Setup in " + str((int(round(time.time() * 1000)) - initstart)/1000) + "s")

keep_alive.keep_alive()

bot.run(TOKEN)