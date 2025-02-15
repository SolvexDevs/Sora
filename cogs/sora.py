import discord
from discord.ext import commands
import aiohttp

API_SERVER_URL = "http://192.168.1.7:11434/api/chat"

class MentionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if self.bot.user.mentioned_in(message):
            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not prompt:
                return

            thinking_message = await message.channel.send("考え中...")

            headers = {"Content-Type": "application/json"}
            json = {
                "model": "hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF",
                "stream": False,
                "messages": [
                    {
                        "role": "system",
                        "content": "あなたはSakanaAI株式会社が開発したTinySwallowです。優秀なアシスタントです。"
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            }

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(API_SERVER_URL, headers=headers, json=json) as response:
                        response.raise_for_status()
                        data = await response.json()
            except aiohttp.ClientError as e:
                await thinking_message.edit(content=f"HTTP error occurred: {e}")
                return
            except Exception as e:
                await thinking_message.edit(content=f"An error occurred: {e}")
                return

            message_content = data.get('message', {}).get('content', 'No response text')
            await thinking_message.edit(content=message_content)

async def setup(bot):
    await bot.add_cog(MentionCog(bot))