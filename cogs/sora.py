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

            thinking_message = await message.channel.send("考え中...")

            try:
                response_text = await send_prompt_to_llm(prompt)
            except Exception as e:
                await thinking_message.edit(content=f"An error occurred: {e}")
                return

            await thinking_message.edit(content=response_text)

        elif message.reference and message.reference.resolved and message.reference.resolved.author == self.bot.user:
            original_message = message.reference.resolved
            combined_prompt = f"オリジナルメッセージ: {original_message.content}\それに対する返信: {message.content}"

            thinking_message = await message.channel.send("考え中...")

            try:
                response_text = await send_prompt_to_llm(combined_prompt)
            except Exception as e:
                await thinking_message.edit(content=f"An error occurred: {e}")
                return

            await thinking_message.edit(content=response_text)

async def setup(bot):
    await bot.add_cog(MentionCog(bot))
