import discord
from discord.ext import commands
from discord.utils import get
import openai

TOKEN = "MTA2NDg4NDQwNDkwMTY1NDYwMA.GTUnUa.PEfDvyTlDQ3l3d1lXoNZPDW5m6ZHma2EbSU2c8"
OPENAI_API_KEY = "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"  # OpenAI API-Schlüssel

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

# XP Calculation: A dictionary to store user XP
user_xp = {}

# XP calculation method (add this function to calculate XP)
def calculate_xp(user_id, xp_earned):
    user_xp[user_id] = user_xp.get(user_id, 0) + xp_earned

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said: '{user_message}' ({channel})")

    if user_message[0] == '!':
        await bot.process_commands(message)  # Process bot commands
    else:
        await input == msg(message, user_message, is_private=False)
        
    # Calculate and award XP for messages sent
    xp_earned = 1
    user_id = message.author.id
    calculate_xp(user_id, xp_earned)

# Command to check XP
@bot.command()
async def xp(ctx):
    member = ctx.author
    xp = user_xp.get(member.id, 0)
    await ctx.send(f'{member.mention} hat {xp} XP.')

# Role Assignment
@bot.command()
async def role (ctx, role_name: str):  # role_name als Pflichtargument hinzugefügt
    member = ctx.author
    role = get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f'{member.mention} hat die Rolle {role.name} erhalten.')
    else:
        await ctx.send(f'Die Rolle "{role_name}" existiert nicht.')


# Special Role Unlock
@bot.command()
async def unlock(ctx, role_name):
    member = ctx.author
    member_role = get(ctx.guild.roles, name="Member")
    if member_role in member.roles:
        special_role = get(ctx.guild.roles, name=role_name)
        if special_role and special_role not in member.roles:
            await member.add_roles(special_role)
            await ctx.send(f'{member.mention} hat die Rolle {special_role.name} freigeschaltet.')

# Game Role Reactions
@bot.command()
async def rearole(ctx, role_name):
    allowed_game_roles = ["Apex Legends", "Valorant", "Fortnite", "Genshin Impact"]
    if role_name in allowed_game_roles:
        role = get(ctx.guild.roles, name=role_name)
        member = ctx.author
        if role:
            if role in member.roles:
                await ctx.send(f'Du hast die Rolle {role.name} bereits.')
            else:
                await member.add_roles(role)
                await ctx.send(f'Du hast die Rolle {role.name} erhalten.')
        else:
            await ctx.send('Die angegebene Rolle existiert nicht.')
    else:
        await ctx.send('Das Spiel ist nicht in der Liste der erlaubten Spiele.')

# Send Message to Channel
@bot.command()
async def msg(ctx, channel_name, message):
    channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
    if channel:
        await channel.send(message)
    else:
        await ctx.send(f'Der Kanal "{channel_name}" wurde nicht gefunden.')

# Auto-create and move to voice channels
@bot.event
async def voice_on(member, before, after):
    if before.channel is None and after.channel is not None:
        # Ein Benutzer ist einem Voice-Chat beigetreten
        category = discord.utils.get(member.guild.categories, name="Voice Channels")  # Kategorie für generierte Kanäle
        if category:
            new_channel_name = f"{member.display_name}'s Channel"
            new_channel = await member.guild.create_voice_channel(new_channel_name, category=category)
            await member.move_to(new_channel)

# User Help Command #ask_gpt
@bot.command()
async def h(ctx):
    help_message = """
    **Bot-Befehle:**
    - `!xp`: Zeigt deine aktuelle XP an.
    - `!grole <Rollenname>`: Weist dir die angegebene Rolle zu.
    - `!unlock <Rollenname>`: Schaltet spezielle Rollen frei.
    - `!rearole <Rollenname>`: Gamerolle
    - `!msg <Kanalname> <Nachricht>`: Sendet eine Nachricht in einen anderen Kanal.
    - `!h`: Zeigt Hilfe an.
    - `!gpt <Nachricht>`: Sendet eine GPT-3-Antwort an die angegebene Nachricht.
    - `!voice_on`: Erstellt einen Tempoäreren Voice Channel.
    - `!clear <Anzahl>`: Löscht die angegebene Anzahl der Nachrichten. 
    """
    await ctx.send(help_message)

# GPT
openai.api_key = OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f'{bot.user} ist jetzt aktiv!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!ask_gpt'):
        user_input = message.content.split('!ask_gpt ')[1]
        response = gpt(user_input)
        await message.channel.send(response)

    await bot.process_commands(message)

def gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",  # Wähle den gewünschten GPT-3-Engine
        prompt=prompt,
        max_tokens=50  # Anzahl der Tokens in der Antwort anpassen
    )
    return response.choices[0].text

bot.run(TOKEN)
