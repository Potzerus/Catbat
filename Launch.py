import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="°")
channel = 531199506528600064
emoji = 706604994929098833
batted = []


@bot.event
async def on_ready():
    appli = await bot.application_info()
    print("Logged in! bot invite: https://discordapp.com/api/oauth2/authorize?client_id=" +
          str(appli.id) + "&permissions=0&scope=bot")
    global channel
    channel = await bot.fetch_channel(channel)
    global emoji
    user = await bot.fetch_user(125660719323676672)
    if user.dm_channel is None:
        await user.create_dm()
    emoji = (await (user).dm_channel.fetch_message(emoji)).reactions[0]


@bot.event
async def on_raw_reaction_add(payload):
    message = await (await bot.fetch_channel(payload.channel_id)).fetch_message(payload.message_id)
    reaction = None
    for react in message.reactions:
        if react == emoji:
            reaction = react
            if reaction.count > 2:
                if reaction.message.id in batted:
                    return
                if len(batted) == 50:
                    batted.pop(0)
                batted.append(reaction.message.id)
                embed = discord.Embed()
                if len(message.content) != 0:
                    embed.set_author(name="%s" % message.content)
                if len(message.attachments) != 0:
                    embed.set_image(url=message.attachments[0].url)
                embed.add_field(name="Jump to message", value=message.jump_url, inline=False)
                embed.set_footer(text="%s#%s in #%s" % (message.author.name, message.author.discriminator, message.channel.name),icon_url=message.author.avatar_url)
                await channel.send(embed=embed)
                return


bot.run(open("Token.txt").read())
