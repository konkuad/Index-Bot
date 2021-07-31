import os
import discord
import numpy as np
import pandas as pd
import jellyfish

intents = discord.Intents.default()
intents.members = True

TOKEN = 'ODA0NjQ4ODg2OTMyNzM0MDAz.YBPZrA.BwznX4-v1-1TgxonII2V8s6KSM4'
client = discord.Client()

names = []
similar_indices = []
indices = []
genre = []

@client.event
async def on_ready():
    
    global names
    global similar_indices
    global indices
    global genre 
    
    df = pd.read_csv('Anime Profiles.csv')
    names = list(df['Anime Title'])
    similar_indices = list(df['similar indices'])
    indices = list(df['Unnamed: 0'])
    genre = list(df['genre'])
    
    print('Ready!')
    
@client.event
async def on_message(message):
    
    global names
    global similar_indices
    global genre
    
    def similarscore(name,key):
        key = key.lower()
        score = []
        name = name.split(' ')

        for word in name:
            word = word.lower()

            score.append(jellyfish.levenshtein_distance(word,key))

        return np.min(score)

    if message.author == client.user:
        return
    
    elif message.content.startswith('$n'):
        await message.channel.send('----------------------------------')
        keys = str(message.content)[3:].split(' ')
        scores = []
        
        for name in names:
            a = []
            for key in keys:
                a.append(similarscore(name,key))
            scores.append(np.sum(a))
            
        scores = np.array(scores)
            
        best = [i for i in range(len(scores)) if scores[i] == np.min(scores)]
        
        best = np.random.choice(best, size=6, replace = False)
        
        for index in best:
            await message.channel.send('Similar Name : '+str(names[index])+' id = '+str(index))
        await message.channel.send('----------------------------------')
        
    elif message.content.startswith('$ri'):
        await message.channel.send('----------------------------------')
        index = str(message.content)[4:]
        try:
            index = int(index)
            similar = similar_indices[index].replace('[','').replace(']','').split(', ')[1:]
            
            a = 0
            
            for i in similar:
                if a != 0:
                    i = int(i)
                    await message.channel.send('Recommended Anime = '+str(names[i])+' id = '+str(i)+'\n')
                a += 1
            
        except ValueError:
            await message.channel.send('index must be integer')
        await message.channel.send('----------------------------------')
        
    elif message.content.startswith('$rn'):
        await message.channel.send('----------------------------------')
        keys = str(message.content)[4:].split(' ')
        scores = []
        
        for name in names:
            a = []
            for key in keys:
                a.append(similarscore(name,key))
            scores.append(np.sum(a))
            
        scores = np.array(scores)
            
        best = [i for i in range(len(scores)) if scores[i] == np.min(scores)]
        
        index = np.random.choice(best)
        
        index = int(index)
        similar = similar_indices[index].replace('[','').replace(']','').split(', ')[1:]
        a = 0
        for i in similar:
            if a != 0:
                i = int(i)
                await message.channel.send('Recommended Anime = '+str(names[i])+' id = '+str(i)+'\n')
            a += 1
        await message.channel.send('----------------------------------')
            
    elif message.content.startswith('$info'):
        await message.channel.send('----------------------------------')
        index = str(message.content)[6:]
        try:
            index = int(index)
            await message.channel.send('Anime Name = '+str(names[index])+'\n\n')
            await message.channel.send('Genre = '+str(genre[index])+'\n\n')
        except ValueError:
            await message.channel.send('index must be integer')
        await message.channel.send('----------------------------------')
        
    
client.run(TOKEN)