import os
import discord
import time
import random
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    def has_roles(member, roles):
        return any(role.name in roles for role in member.roles)

    allowed_roles = ['Donos', 'Socios']

    if message.content.startswith('he!say '):
        if has_roles(message.author, allowed_roles):
            text_to_say = message.content[len('he!say '):]
            await message.channel.send(text_to_say)
        else:
            await message.channel.send("Você não tem permissão para usar este comando.")

    elif message.content.startswith('he!say_server_info '):
        if has_roles(message.author, allowed_roles):
            text_to_say = message.content[len('he!say_server_info '):]

            channel_name = '》❗server-info'
            target_channel = discord.utils.get(message.guild.channels, name=channel_name)

            if target_channel is not None:
                await target_channel.send(text_to_say)
            else:
                print(f'Channel "{channel_name}" not found')
        else:
            await message.channel.send("Você não tem permissão para usar este comando.")

    elif message.content == 'he!help':
        commands = [
            ("he!say", "Bot Repete Tudo que Você Disser!"),
            ("he!say_server_info", "Bot Manda a Mensagem que Você Quer no Server Info"),
            ("he!ping", "Mostra Quantos ms o Bot Está Demorando Para Responder"),
            ("he!calculator", "Bot Vai Fazer Qualquer Conta Que Você Pedir"),
            ("he!decision", "O Bot Vai Tomar a Decisão! Para Usar o Comando Da Forma Correta Escreva As Opções Como Por Exemplo: 1. Fulano 2. Fulaninho 3. Fulanão"),
            ("he!spam", "Manda Mensagem na DM da Pessoa Marcada"),
            ("he!crypto", "O Bot Vai Cotar o BTC e o ETH em Tempo Real em BRL"),
            ("he!br-en", "O Bot Ira Traduzir de Português para Ingles"),
            ("he!en-br", "O Bot Ira Traduzir de Ingles para Português"),
            ("he!ship", "Calcula a química entre duas pessoas"),
        ]

        embeds = []
        commands_per_page = 10
        for i in range(0, len(commands), commands_per_page):
            embed = discord.Embed(title="Help Commands", description="List of available commands:", color=0x00ff00)
            for name, desc in commands[i:i+commands_per_page]:
                embed.add_field(name=name, value=desc, inline=False)
            embed.set_footer(text="Bot by Brrxis")
            embeds.append(embed)

        for embed in embeds:
            await message.channel.send(embed=embed)

    elif message.content == 'he!ping':
        start_time = time.time()

        temp_message = await message.channel.send("Calculando...")
        end_time = time.time()
        latency = round((end_time - start_time) * 1000)

        embed = discord.Embed(title=":ping_pong: Pong!", description=f"Pong: {latency} ms", color=0x00ff00)
        await temp_message.edit(content="", embed=embed)

    elif message.content.startswith('he!calculator '):
        expression = message.content[len('he!calculator '):]
        try:
            result = eval(expression)
            await message.channel.send(f"Resultado: {result}")
        except Exception as e:
            await message.channel.send(f"Erro ao calcular: {e}")

    elif message.content.startswith('he!decision '):
        options_text = message.content[len('he!decision '):]
        options = [opt.strip() for opt in options_text.split() if opt.strip()]
        if len(options) < 2:
            await message.channel.send("Por favor, forneça pelo menos duas opções para tomar a decisão.")
        else:
            choice = random.choice(options)
            await message.channel.send(f"A decisão é: {choice}")

    elif message.content.startswith('he!spam '):
        if has_roles(message.author, allowed_roles):
            try:
                member = message.mentions[0]
                content = message.content[len('he!spam '):].strip()

                if content.startswith('http'):
                    await member.send(content)
                else:
                    await member.send(content=content)
                await message.channel.send(f"Mensagem enviada para {member.name} na DM.")
            except IndexError:
                await message.channel.send("Nenhum usuário mencionado.")
        else:
            await message.channel.send("Você não tem permissão para usar este comando.")

    elif message.content == 'he!crypto':
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=brl'
        try:
            response = requests.get(url)
            data = response.json()
            btc_value = data['bitcoin']['brl']
            eth_value = data['ethereum']['brl']
            embed = discord.Embed(title="Cotação de Criptomoedas em Tempo Real", color=0x00ff00)
            embed.add_field(name="BTC", value=f"R${btc_value}", inline=False)
            embed.add_field(name="ETH", value=f"R${eth_value}", inline=False)
            await message.channel.send(embed=embed)
        except Exception as e:
            await message.channel.send(f"Erro ao obter a cotação das criptomoedas: {e}")

    elif message.content.startswith('he!br-en '):
        text_to_translate = message.content[len('he!br-en '):]
        try:
            translated = GoogleTranslator(source='pt', target='en').translate(text_to_translate)
            await message.channel.send(translated)
        except Exception as e:
            await message.channel.send(f"Erro ao traduzir: {e}")

    elif message.content.startswith('he!en-br '):
        text_to_translate = message.content[len('he!en-br '):]
        try:
            translated = GoogleTranslator(source='en', target='pt').translate(text_to_translate)
            await message.channel.send(translated)
        except Exception as e:
            await message.channel.send(f"Erro ao traduzir: {e}")

    elif message.content.startswith('he!ship '):
        pair = message.content[len('he!ship '):].strip().lower()
        percentage = random.randint(0, 100)

        if percentage <= 40:
            emoji = ":broken_heart:"
        elif percentage <= 70:
            emoji = ":heart:"
        else:
            emoji = ":fire: :flushed: :smiling_face_with_3_hearts:"

        embed = discord.Embed(title="Ship Calculator", description=f"{emoji} {pair.title()} {percentage}% de química {emoji}", color=0xff69b4)
        await message.channel.send(embed=embed)

try:
    token = os.getenv('DISCORD_BOT_TOKEN')
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
except Exception as e:
    print(f"An error occurred: {e}")
