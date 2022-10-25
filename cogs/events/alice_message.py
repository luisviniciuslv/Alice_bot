import openai
from config import config
from discord.ext import commands


def gpt3(stext):
    openai.api_key = config['open_ai_token']
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=stext,
            temperature=0.4,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2
    )
    return response.choices[0].text

class AI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if "!ignore" in message.content.lower() or "!ig" in message.content.lower():
            return

        if "!clear" in message.content.lower():
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

def setup(client):
    client.add_cog(AI(client))