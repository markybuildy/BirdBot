import random

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

class BirdCount:
    def __init__(self):
        self.birds = {}
        self.commands = ['add','done','help','print','remove','rename', 'set']
        self.cmdhelp = {
            "add": "Add birds.",
            "done": "Complete session.",
            "help": "Show this help menu.",
            "print": "Print current checklist.",
            "remove": "Remove birds.",
            "rename": "Rename a bird to something else.",
            'start': 'Create a checklist.',
            "set": "Set a bird's quantity."
        }
        self.formats = {
            "add": '.add <bird_name> <count>',
            "help": '.help <command>',
            "remove": '.remove <bird_name> <count>',
            "rename": '.rename <old_name> <new_name>',
            "done": '.done',
            "print": '.print',
            "start": '.start',
            "set": '.set <bird_name> <count>'
        }


    def add_bird(self, bird_name, count):
        if bird_name in self.birds:
            self.birds[bird_name] += count
            #return f"Added **{count}x** {bird_name}. **{bird_name}** seen total!"
            return ("Added **" + str(count) + "x** " + bird_name + ". **" + str(self.birds[bird_name]) + "** seen total!")
        else:
            self.birds[bird_name] = count
            return ("Added **" + str(count) + "x** " + bird_name + ".")

    def remove_bird(self, bird_name, count):
        if bird_name in self.birds:
            if count > self.birds[bird_name]:
                return("Not enough birds to remove.")
            else:
                self.birds[bird_name] -= count
                if self.birds[bird_name] == 0:
                    self.birds.pop(bird_name)
                    return ("Removed **" + str(count) + "x** " + bird_name.capitalize() + ". **0** remain.")
                return("Removed **" + str(count) + "x** " + bird_name.capitalize() + ". **" + str(self.birds[bird_name]) + "** remain.")

        else:
            return('"' + bird_name + '" does not exist.')

    def print_results(self):
        if len(self.birds) != 0:
            result = ''
            for bird in self.birds:
                result += ('\n- '+ bird + " **x" + str(self.birds.get(bird)) + '**')
            return result
        else:
            return("No birds seen. Better luck next time!")

    def rename(self, old_name, new_name):
        if old_name in self.birds:
            if new_name not in self.birds:
                self.birds[new_name] = self.birds[old_name]
                self.birds.pop(old_name)
                return("Renamed **" + old_name + "** to **" + new_name + "**.")
            else:
                return('"' + new_name + '" already exists.')

        else:
            return('"' + old_name + '" does not exist.')

    def set(self, bird_name, count):
        self.birds[bird_name] = count
        return('Set "' + bird_name + '" to **' + str(count) + '**.')

birdcount_users = {}

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.custom, name="custom", state=".help"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "ping" in message.content.lower():
        await message.reply("Pong!")

    if "pong" in message.content.lower():
        await message.reply("Ping!")

    if "thank you birdbot" in message.content.lower():
        r = random.randint(1,7)
        if r <= 3:
            await message.reply("My pleasure!")
        elif r <= 6:
            await message.reply("No problem!")
        else:
            await message.reply("FUCK YOU!!!")


    await bot.process_commands(message)


#actual commands start here

@bot.command()
async def start(ctx):
    if ctx.author.id in birdcount_users:
        await ctx.reply('You already have an active checklist!')
    else:
        birdcount_users[ctx.author.id] = BirdCount()
        await ctx.reply(f'Let the adventure begin, <@{ctx.author.id}>!')

@bot.command()
async def help(ctx):
    birCount = BirdCount()

    userinput = ctx.message.content.lower()
    segments = userinput.split()

    if len(segments) == 1:
        reply = ''
        for command in birCount.cmdhelp:
            reply += ("- " + command + ": " + birCount.cmdhelp[command] + '\n')
        embed = discord.Embed(title = 'List of available commands:',colour = discord.Colour.brand_green(), description = reply + '\n Enter "help <command>" for the format of that specific command.')
        await ctx.reply(embed=embed)

    elif len(segments) == 2:
        if segments[1].lower() in birCount.formats:
            await ctx.reply(birCount.formats[segments[1]])
        else:
            await ctx.reply('"' + segments[1] + '" is not a valid command.')

    # await ctx.send(f"Hello <@{801956525454917634}>!")

@bot.command()
async def add(ctx):
    userinput = ctx.message.content.lower()
    segments = userinput.split()

    if not ctx.author.id in birdcount_users:
        await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")

    if segments[-1].isdigit():
        count = int(segments[-1])
        name = " ".join(segments[1:-1])

        if count < 1:
            await ctx.reply("Please enter a valid quantity.")
            return
    else:
        count = 1
        name = " ".join(segments[1:])

    if not name:
        await ctx.reply("Please enter a name.")
        return

    await ctx.reply(birdcount_users[ctx.author.id].add_bird(name, count))

@bot.command()
async def remove(ctx):
    userinput = ctx.message.content.lower()
    segments = userinput.split()

    if not ctx.author.id in birdcount_users:
        await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")
        return

    if segments[-1].isdigit():
        count = int(segments[-1])
        name = " ".join(segments[1:-1])

        if count < 1:
            await ctx.reply("Please enter a valid quantity.")
            return
    else:
        count = 1
        name = " ".join(segments[1:])

    if not name:
        await ctx.reply("Please enter a name.")
        return

    await ctx.reply(birdcount_users[ctx.author.id].remove_bird(name, count))

@bot.command()
async def set(ctx):
    userinput = ctx.message.content.lower()
    segments = userinput.split()

    if not ctx.author.id in birdcount_users:
        await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")
        return

    if segments[-1].isdigit():
        count = int(segments[-1])
        name = " ".join(segments[1:-1])

        if count < 1:
            await ctx.reply("Please enter a valid quantity.")
            return
    else:
        count = 1
        name = " ".join(segments[1:])

    if not name:
        await ctx.reply("Please enter a name.")
        return

    await ctx.reply(birdcount_users[ctx.author.id].set(name, count))

@bot.command()
async def rename(ctx):
    userinput = ctx.message.content.lower()
    segments = userinput.split()

    if not ctx.author.id in birdcount_users:
        await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")

    # Searches for the longest match
    longest = 0

    for i in range(1, len(segments)):
        trial_name = " ".join(segments[1:i])
        if trial_name in birdcount_users[ctx.author.id].birds:
            longest = i

    if longest == 0:
        await ctx.reply("Name not found in current list")
        return

    old = " ".join(segments[1:longest])
    new = " ".join(segments[longest:])
    await ctx.reply(birdcount_users[ctx.author.id].rename(old, new))

@bot.command()
async def print(ctx):
    userinput = ctx.message.content.lower()

    if ctx.author.id not in birdcount_users:
        await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")

    else:
        if len(birdcount_users[ctx.author.id].birds) != 0:
            temp = '\n'
            temp += (birdcount_users[ctx.author.id].print_results())
            temp += ('\n' + '\n' + '**Keep it up, champ!** 🤩')
            embed = discord.Embed(title = "Current checklist:", description=temp, colour=discord.Colour.green())
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("You haven't seen any birds yet. 🥀🥀")

@bot.command()
async def done(ctx):
    userinput = ctx.message.content.lower()

    if ctx.author.id not in birdcount_users:
        await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")

    else:
        if len(birdcount_users[ctx.author.id].birds) != 0:
            temp = '\n'
            temp += (birdcount_users[ctx.author.id].print_results())
            temp += ('\n' + '\n' + '**What a fruitful session!** 😄 😄 ')
            embed = discord.Embed(title="Total birds seen:", description=temp, colour=discord.Colour.green())
            await ctx.reply(embed=embed)
            birdcount_users.pop(ctx.author.id)
        else:
            await ctx.reply(birdcount_users[ctx.author.id].print_results())
            birdcount_users.pop(ctx.author.id)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)