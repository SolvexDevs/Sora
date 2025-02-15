import discord
from discord.ext import commands
from lib.req import send_prompt_to_llm

class MentionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if f"<@{self.bot.user.id}>" in message.content:
            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not prompt:
                return

            if message.reference:
                referenced_message = await message.channel.fetch_message(message.reference.message_id)
                prompt = f"{referenced_message.content}\n\n{prompt}"

            thinking_message = await message.channel.send("考え中...")

            try:
                response_text = await send_prompt_to_llm(prompt)
            except Exception as e:
                await thinking_message.edit(content=f"An error occurred: {e}")
                return

            await thinking_message.edit(content=response_text)

async def setup(bot):
    await bot.add_cog(MentionCog(bot))
