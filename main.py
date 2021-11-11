VERSION = "v21.0 (11/11/21)"
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

# init stuff


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
async def viewword(ctx, *, word):
    stats = tools.tracked_word_stats(word.lower())
    desc = []
    if stats is None:
        await ctx.send(f"Word '{word}' does not exist")
        return
    for id_, count in stats.items():
        desc.append(f"{await tools.fullname_from_id(id_, bot)}: {count}")
    embed = discord.Embed(title="Tracking stats", description="\n".join(desc))
    embed.add_field(name="Last mentioned", value=f"<t:{tools.get_word_timing(word)}:f>, <t:{tools.get_word_timing(word)}:R>")
    embed.set_author(name=word.lower())
    await ctx.send(embed=embed)
@viewword.error
async def handle_error(ctx, error):
    await ctx.send(error, embed=help_embed('viewword', PREFIX))

@bot.command(name='list')
async def list_(ctx):
    words = tools.tracked_get_words()
    description = ""
    for word in words:
        description += f"**{word}** (last mentioned <t:{tools.get_word_timing(word)}:f>, <t:{tools.get_word_timing(word)}:R>)\n"
    embed = discord.Embed(title="List of tracked words", description=description)
    await ctx.send(embed=embed)
@list_.error
async def handle_error(ctx, error):
    await ctx.send(error, embed=help_embed('list', PREFIX))

@bot.event
async def on_command_error(_, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    raise error

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