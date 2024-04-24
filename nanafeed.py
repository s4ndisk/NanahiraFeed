import discord
import os 
from dotenv import load_dotenv

#load .env variables
load_dotenv()

nanahi = discord.bot

# announce when bot is up in the CLI
@nanahi.event
async def on_ready():
  print(f'{nanahi.user} is online and ready!')

# slash command to provide link to the github repo
@nanahi.slash_command(name='#AD', description='shameful plug'
  async def ad(ctx: discord.ApplicationContext):
    await ctx.respond('https://github.com/s4ndisk/nanafeed.py') # make this a clean embed later on

cog_list = [
  'x-twitter',
  'spotify',
  'youtube'
]

for cog in cogs_list:
    nanahi.load_extension(f'cogs.{cog}')

nanahi.run(os.getenv('TOKEN'))
