from database.mongodb import get_log, set_log
from config import config
import openai
from discord.ext import commands

async def gpt3(self, stext):
    log = await get_log()
    openai.api_key = config['open_ai_token']

    prompt = f'{log}Human: {stext}\nAI:'

    response = openai.Completion.create(
        engine="davinci",
        prompt = prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        best_of=1,
        stop=['\nHuman']
    )
    set_log(log + f'Human: {stext}\nAI: {response.choices[0].text.strip()}\n')

    return response.choices[0].text.strip()

class Chatbot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if "!clear" in message.content.lower():
            return
        if "!ignore" in message.content.lower() or "!ig" in message.content.lower():
            return

        if (message.channel.id == 985973178901880872) and (message.author.id != 985969436001439834):
            response = await gpt3(self, message.content)
            n = 2000
            chunks = [response[i:i+n] for i in range(0, len(response), n)]

            for i in chunks:
                try:
                    await message.channel.send(i)
                except:
                    await message.channel.send("quebrei")

def setup(client):
    client.add_cog(Chatbot(client))
