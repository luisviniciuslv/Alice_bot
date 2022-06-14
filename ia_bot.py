import openai
import discord
from dotenv import load_dotenv
import os
import random

load_dotenv()
def gpt3(stext):
    openai.api_key = os.getenv("api_key")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=stext,
            temperature=0.3,
            max_tokens=1000,
            top_p=0.5,
            frequency_penalty=0.5,
            presence_penalty=0.4,
    )
    return response.choices[0].text


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if "!ignore" in message.content.lower() or "!ig" in message.content.lower():
            return
        if "!50" in message.content:
            num = random.randint(0, 2)
            if num == 1:
                response = "sim"
            else:
                response = "não"
            await message.channel.send(response)
            return

        if message.content == "!clear" and message.author.id == 597492835662692371:
            await message.channel.purge(limit=1000000)
            return
        if (message.channel.id == 985973178901880872) and (message.author.id != 985969436001439834):
            pensando = await message.channel.send('pensando...')
            response = gpt3(message.content)
            n = 2000
            chunks = [response[i:i+n] for i in range(0, len(response), n)]
            await pensando.delete()

            for i in chunks:
                try:
                    await message.channel.send(i)
                except:
                    await message.channel.send("quebrei")

client = MyClient()
client.run(os.getenv("bot_token"))
