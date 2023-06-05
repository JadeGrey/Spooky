import discord
from discord import app_commands
import random
import asyncpraw
import artintegration
import os
import asyncio
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

token = os.getenv("TOKEN")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "ping", description = "Delay between interactions")
async def first_command(interaction):
    await interaction.response.send_message('Pong! {0} '.format(round(client.latency, 3)) + "ms")

@tree.command(name = "meme", description = "MeMeS!!!!")
async def get_memes(interaction):

    reddit = asyncpraw.Reddit(
    client_id = os.getenv("RID"),
    client_secret = os.getenv("RSECRET"),
    user_agent = os.getenv("RAGENT"),
    username = os.getenv("RUSERNAME"),
    password = os.getenv("RPASSWORD")
)
    await interaction.response.send_message('Loading...')
    subreddit = await reddit.subreddit("memes")
    all_subs = []
    top = subreddit.top(limit=100)

    async for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    embed = discord.Embed(title=f'__{name}__', colour=discord.Colour.random(), timestamp=interaction.created_at, url=url)

    embed.set_image(url=url)
    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
    embed.set_footer(text='Here is your meme!')
    await interaction.edit_original_response(embed=embed)
    await interaction.edit_original_response(content=f'<https://reddit.com/r/{subreddit}/> :white_check_mark:')

@tree.command(name = "animals", description = "CUTE ANIMALS!!!!")
async def get_animals(interaction):

    reddit = asyncpraw.Reddit(
    client_id = os.getenv("RID"),
    client_secret = os.getenv("RSECRET"),
    user_agent = os.getenv("RAGENT"),
    username = os.getenv("RUSERNAME"),
    password = os.getenv("RPASSWORD")
)
    await interaction.response.send_message('Loading...')
    subreddit = await reddit.subreddit("cute")
    all_subs = []
    top = subreddit.top(limit=100)

    async for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    embed = discord.Embed(title=f'__{name}__', colour=discord.Colour.random(), timestamp=interaction.created_at, url=url)

    embed.set_image(url=url)
    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
    embed.set_footer(text='Here is your meme!')
    await interaction.edit_original_response(embed=embed)
    await interaction.edit_original_response(content=f'<https://reddit.com/r/{subreddit}/> :white_check_mark:')

@tree.command(name="credits", description="mentionable users")
async def make_embed(interaction):
    embed = discord.Embed(type="rich",
    title="Credits:",
    description="Created and Developed by: <@737486185466691585>\nInspiration: Starri, ᏕᎮᏋፈᏖᏒᏋ\n\nThanks to my inspirations for making me want to code this :)",
    color=0xf905c4)
    embed.set_footer(text="Graham is kewl")
    await interaction.response.send_message(embed=embed)

@tree.command(name="ai", description="generate art using different models (Midjourney but better)")
@app_commands.describe(model="Choose a model (anything is anime, realistic is realistic, midjourneys are concepts)")
@app_commands.describe(prompt="Describe your image (I have predefined tags to make it look better)")
@app_commands.describe(hidden="Only use for NSFW artwork, this disables the filter")
async def ai(interaction: discord.Interaction, model: Literal["anything-v3", "anything-v4", "anything-v5", "realistic-vision-v13", "midjourney-v4", "midjourney-papercut"], prompt: str, hidden: Literal["y", "n"] = "n"):
    hidden = str(hidden)

    await interaction.response.send_message("Sending...")
    if hidden == "y" and interaction.channel.is_nsfw() == False:
        await interaction.edit_original_response(content=f"Cannot generate NSFW image in <#{interaction.channel.id}>, retrying as SFW in 3s.")
        hidden = "n"
        await asyncio.sleep(3)
    file_path = await artintegration.run(interaction=interaction, prompt=prompt, nsfwp=hidden, typep=model )
    file = discord.File(fp=file_path, filename=f"AI_{model}_generated.png")
    embed=discord.Embed(title=f"{prompt}", color=0xfb0fff)
    embed.set_image(url=f"attachment://AI_{model}_generated.png")
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1075591461514518600/d198f8043be89a8a05d9cdd648706407.png?size=1024")
    embed.add_field(name="Model:", value=f"{model}", inline=True)
    embed.set_footer(text="Developed by: Jade#0420")
    await interaction.edit_original_response(content="Success!")
    await interaction.channel.send(file=file, embed=embed)

@tree.command(name="delete", guild=discord.Object(id=995137895985840149))
async def delete(interaction, message_link: str):

    parts = message_link.split('/')

    if len(parts) != 7 or parts[2] != "discord.com" or parts[3] != "channels":
        await interaction.channel.send("Invalid link!")
        return

    server_id = int(parts[4])
    channel_id = int(parts[5])
    message_id = int(parts[6])

    server = client.get_guild(server_id)
    if server is None:
        await interaction.channel.send("I'm not in the server!")
        return

    channel = server.get_channel(channel_id)
    if channel is None:
        await interaction.channel.send("I'm not in the channel!")
        return

    try:
        message = await channel.fetch_message(message_id)
        await message.delete()
        message1 = await interaction.channel.send("Message deleted successfully!")
        await message1.delete()
    except discord.NotFound:
        await interaction.channel.send("Message not found!")
    except discord.Forbidden:
        await interaction.channel.send("I don't have permissions to delete that message!")
    except discord.HTTPException as e:
        await interaction.channel.send(f"An error occurred: {e}")

@tree.command(name='sync', description='Owner only', guild=discord.Object(id=1115089214833446934))
async def sync_command(interaction: discord.Interaction):
    if interaction.user.id == 737486185466691585:
        await tree.sync()
        await interaction.response.send_message("Command tree synced!")
        print('Command tree synced.')
    else:
        await interaction.response.send_message('You must be the owner to use this command!')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over my spirits"))
    await tree.sync(guild=discord.Object(id=1115089214833446934))
    print("Ready!")

embed = discord.Embed(type="rich",
title="Credits:",
description="Created and Developed by: <@737486185466691585>\nInspiration: Starri, ᏕᎮᏋፈᏖᏒᏋ\n\nThanks to my inspirations for making me want to code this :)",
color=0xf905c4)
embed.set_footer(text="Graham is kewl")

client.run(token)
