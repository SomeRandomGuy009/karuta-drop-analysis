import discord
import sqlite3
import os

conn = sqlite3.connect('card_database.sqlite')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character TEXT,
        series TEXT,
        wishlist INTEGER,
        UNIQUE(character, series)
    )
''')

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author.id == 646937666251915264:
        embed = message.embeds[0]
        if embed.title != "Character Lookup":
            return
        
        description_lines = embed.description.split('\n')
        
        character = description_lines[0].split('**')[1]
        
        series = description_lines[1].split('**')[1]
        
        if 'Wishlisted' in description_lines[2]:
            wishlist_str = description_lines[2].split('**')[1]
        elif 'Wishlisted' in description_lines[3]:
            wishlist_str = description_lines[3].split('**')[1]
        else:
            wishlist_str = '0'

        if wishlist_str.isdigit(): 
            wishlist = int(wishlist_str)
        else:
            wishlist_str = wishlist_str.replace(',', '')
            wishlist = int(wishlist_str)


        c.execute('SELECT * FROM cards WHERE character=? AND series=?', (character, series))
        existing_card = c.fetchone()

        if existing_card:
            c.execute('UPDATE cards SET wishlist=? WHERE id=?', (wishlist, existing_card[0]))
            conn.commit()
        else:
            c.execute('INSERT INTO cards (character, series, wishlist) VALUES (?, ?, ?)', (character, series, wishlist))
            conn.commit()

client.run(os.getenv('TOKEN'))
