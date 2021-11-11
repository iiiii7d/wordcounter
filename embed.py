import discord
import tools

def help_embed(command, prefix):
    embed = None
    if command == "info":
        embed = discord.Embed(title=f"{command}", description="View bot info")
        embed.add_field(name="Example", value=f"`{prefix}{command}`", inline=False)
    elif command == "ping":
        embed = discord.Embed(title=f"{command}", description="Connection test, response test and uptime")
        embed.add_field(name="Example", value=f"`{prefix}{command}`", inline=False)
    elif command == "help":
        embed = discord.Embed(title=f"{command}", description="View help pages")
        embed.add_field(name="Example", value=f"`{prefix}{command}`", inline=False)
    else:
        embed = discord.Embed(title="Wordcounter", description=f"Prefix: `{prefix}`")
        embed.add_field(name="Bot-related", value="info, ping")
        embed.add_field(name="Functions", value="-")
    embed.set_author(name="Command help")
    return embed