import discord

def help_embed(command, prefix):
    if command == "info":
        embed = discord.Embed(title=f"{command}", description="View bot info")
        embed.add_field(name="Example", value=f"`{prefix}{command}`", inline=False)
    elif command == "ping":
        embed = discord.Embed(title=f"{command}", description="Connection test, response test and uptime")
        embed.add_field(name="Example", value=f"`{prefix}{command}`", inline=False)
    elif command == "help":
        embed = discord.Embed(title=f"{command}", description="View help pages")
        embed.add_field(name="Example", value=f"`{prefix}{command}`", inline=False)
    elif command == "add":
        embed = discord.Embed(title=f"{command} <word>", description="Add a word to the tracker")
        embed.add_field(name="Parameters", value="**word:** The word to add")
        embed.add_field(name="Example", value=f"`;{command} word`", inline=False)
        embed.add_field(name="Permissions", value="Administrator, or be 7d")
    elif command == "remove":
        embed = discord.Embed(title=f"{command} <word>", description="Remove a word from the tracker")
        embed.add_field(name="Parameters", value="**word:** The word to remove")
        embed.add_field(name="Example", value=f"`;{command} word`", inline=False)
        embed.add_field(name="Permissions", value="Administrator, or be 7d")
    elif command == "viewuser":
        embed = discord.Embed(title=f"{command} [user]", description="View a user's stats")
        embed.add_field(name="Parameters", value="**user:** The user to view")
        embed.add_field(name="Example", value=f"`;{command} @7d`", inline=False)
    elif command == "viewword":
        embed = discord.Embed(title=f"{command} <word>", description="View a word's stats")
        embed.add_field(name="Parameters", value="**word:** The word to view")
        embed.add_field(name="Example", value=f"`;{command} cursed_word`", inline=False)
    elif command == "list":
        embed = discord.Embed(title=f"{command}", description="View a list of tracked words")
        embed.add_field(name="Example", value=f"`;{command}`", inline=False)
    else:
        embed = discord.Embed(title="Wordcounter", description=f"Prefix: `{prefix}`")
        embed.add_field(name="Bot-related", value="info, ping, help")
        embed.add_field(name="Functions", value="add, remove, viewuser, viewword, list")
    embed.set_author(name="Command help")
    return embed