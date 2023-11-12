import bot
import random
import openai
import discord
from discord.ext import commands

TOKEN = "MTA2NDg4NDQwNDkwMTY1NDYwMA.GTUnUa.PEfDvyTlDQ3l3d1lXoNZPDW5m6ZHma2EbSU2c8"
OPENAI_API_KEY = "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"  # OpenAI API-Schlüssel
openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

# Event-Handler, um auf Nachrichten zu reagieren
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Verhindere, dass der Bot auf seine eigenen Nachrichten reagiert

    # Reagiere auf bestimmte Nachrichteninhalte
    if "Hallo" in message.content:
        await message.channel.send(f"Hallo, {message.author.mention}!")

    if "Zufallszahl" in message.content:
        random_number = random.randint(1, 100)
        await message.channel.send(f"Zufallszahl: {random_number}")

    # Du kannst hier weitere Bedingungen hinzufügen, um auf bestimmte Nachrichten zu reagieren

    await bot.process_commands(message)  # Wichtig, um auch Befehle zu verarbeiten

@bot.event
async def on_ready():
    print(f'{bot.user} ist jetzt aktiv!')


bot = commands.Bot(command_prefix='!', intents=intents)

# Hier fügen wir eine Variable für die Bot-Rolle hinzu (ersetze 'BOT_ROLL_ID' durch die tatsächliche ID der Bot-Rolle)
BOT_ROLE_ID = 743466111949078659

# Erstelle eine Liste der erlaubten Spiele
allowed_games = ["Apex Legends", "Valorant", "Fortnite", "Genshin Impact"]

@bot.event
async def on_ready():
    print(f'{bot.user} ist jetzt aktiv!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!unlock'):
        if str(message.author.id) == BOT_ROLE_ID:
            role_name = message.content.split('!unlock ')[1]
            role = discord.utils.get(message.guild.roles, name=role_name)
            if role:
                await message.author.add_roles(role)
                await message.channel.send(f'Du hast die Rolle {role.name} freigeschaltet.')
            else:
                await message.channel.send(f'Die Rolle "{role_name}" wurde nicht gefunden.')
        else:
            await message.channel.send("Du hast nicht die Berechtigung, diese Rolle freizuschalten.")

    if message.content.startswith('!game_role'):
        game = message.content.split('!game_role ')[1]
        if game in allowed_games:
            role = discord.utils.get(message.guild.roles, name=game)
            if role:
                await message.author.add_roles(role)
                await message.channel.send(f'Du hast die Rolle {role.name} erhalten.')
            else:
                await message.channel.send(f'Die Rolle "{game}" wurde nicht gefunden.')
        else:
            await message.channel.send('Das Spiel ist nicht in der Liste der erlaubten Spiele.')

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.name == "game-roles-channel":  # Ersetze 'game-roles-channel' durch den Namen des Kanals, in dem die Rollen-Reaktionen erlaubt sind
        if reaction.emoji == '🎮':  # Passe das Emoji an, das für die Rollenzuweisung verwendet wird
            role_name = reaction.message.content  # Der Name der Rolle entspricht dem Inhalt der Nachricht
            role = discord.utils.get(reaction.message.guild.roles, name=role_name)
            if role:
                await user.add_roles(role)

bot = commands.Bot(command_prefix='!', intents=intents)

# Liste der Kanal-IDs, die automatisch erweitert und gelöscht werden sollen
channel_ids = [719855896720572446, 719856094813356042, 719856139856117800, 719856420383621272, 719856828552577084]

# Reaction roles
#@bot.event
#async def on_reaction_add(reaction, user):
#    channel_id =   # Replace with the ID of the channel where reactions are allowed
#    emoji_id =   # Replace with the ID of the emoji used for the reaction
#    role_id =   # Replace with the ID of the role to be assigned
#
#    if reaction.message.channel.id == channel_id and reaction.emoji.id == emoji_id:
#        role = discord.utils.get(reaction.message.guild.roles, id=role_id)
#        if role:
#            await user.add_roles(role)

@bot.event
async def on_ready():
    print(f'{bot.user} ist jetzt aktiv!')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel and not before.channel.members:
        # Der Kanal wurde verlassen und hat keine Mitglieder mehr
        if before.channel.id in channel_ids:
            await before.channel.delete()
    elif after.channel and after.channel.id in channel_ids:
        # Ein Benutzer ist einem der Kanäle beigetreten, erstelle einen neuen Kanal
        category = before.channel.category  # Nutze die Kategorie des ursprünglichen Kanals
        new_channel_name = f"Channel {len(after.channel.members) + 1}"
        new_channel = await category.create_voice_channel(new_channel_name)
        await member.move_to(new_channel)

