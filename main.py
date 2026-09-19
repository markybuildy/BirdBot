import random, time

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import pickle, os

import csv, urllib.request, zipfile, io



# Discord stuff.

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)



# Get bird banding codes.

my_url = 'https://www.birdpop.org/docs/misc/IBPAOU.zip'

with urllib.request.urlopen(my_url) as response:
    my_splendiferous_read = response.read()

with zipfile.ZipFile(io.BytesIO(my_splendiferous_read)) as my_zip:
    with my_zip.open(my_zip.namelist()[0]) as my_delightful_file:
        my_sexy_csv = my_delightful_file.read().decode('utf-8')

my_wondrous_reader = csv.DictReader(io.StringIO(my_sexy_csv))

my_lovely_codes = {row['SPEC']: row['COMMONNAME'] for row in my_wondrous_reader}



# Get AviList taxonomy list.

bird_order = {}

if os.path.exists('avilist_taxa.csv'):
    with open('avilist_taxa.csv', encoding='utf-8-sig') as csvfile:
        the_other_reader = csv.DictReader(csvfile)
        bird_order = {row['English (United States)']: row['Sequence'] for row in the_other_reader}

else:
    print("Please download AviList taxonomy data.")


class BirdCount:
    def __init__(self):
        self.birds = {}
        self.birdtimes = {}
        self.commands = ['add','done','help','print','remove','rename', 'set']
        self.cmdhelp = {
            "add": "Add birds.",
            "done": "Complete session.",
            "help": "Show this help menu.",
            "move": "Move birds.",
            "print": "Print current checklist.",
            "remove": "Remove birds.",
            "rename": "Rename a bird to something else.",
            'start': 'Create a checklist.',
            "set": "Set a bird's quantity.",
            "sort": "Change sorting method for checklist.",
            "users": "Show currently active checklists."
        }
        self.formats = {
            "add": '.add <bird_name> <count>',
            "help": '.help <command>',
            "move": '.move <old_name> <new_name> <count>',
            "remove": '.remove <bird_name> <count>',
            "rename": '.rename <old_name> <new_name>',
            "done": '.done',
            "print": '.print <@user>',
            "start": '.start',
            "set": '.set <bird_name> <count>',
            "sort": '.sort <alpha OR chrono OR taxa>',
            "users": ".users"
        }

    def add_bird(self, bird_name, count):
        if bird_name in self.birds:
            self.birds[bird_name] += count
            return f"Added **{count}x** {bird_name}. **{self.birds[bird_name]}** seen total!"

        elif bird_name.upper() in my_lovely_codes:
            if my_lovely_codes[bird_name.upper()] in self.birds:
                self.birds[my_lovely_codes[bird_name.upper()]] += count
                return f"Added **{count}x** {my_lovely_codes[bird_name.upper()]}. **{self.birds[my_lovely_codes[bird_name.upper()]]}** seen total!"
            else:
                self.birds[my_lovely_codes[bird_name.upper()]] = count
                self.birdtimes[my_lovely_codes[bird_name.upper()]] = time.time_ns()
                return f"Added **{count}x** {my_lovely_codes[bird_name.upper()]}."

        else:
            self.birds[bird_name] = count
            self.birdtimes[bird_name] = time.time_ns()
            return f"Added **{count}x** {bird_name}."

    def remove_bird(self, bird_name, count):
        temp_name = ''
        if bird_name in self.birds:
            temp_name = bird_name
        elif bird_name.upper() in my_lovely_codes and my_lovely_codes[bird_name.upper()] in self.birds:
            temp_name = my_lovely_codes[bird_name.upper()]
        if temp_name:
            if count == -1:
                count = self.birds[temp_name]
                self.birds.pop(temp_name)
                self.birdtimes.pop(temp_name)
                return f"Removed **{count}x** {temp_name}. **0** remain."
            if count > self.birds[temp_name]:
                return "Not enough birds to remove."
            else:
                self.birds[temp_name] -= count
                if self.birds[temp_name] == 0:
                    self.birds.pop(temp_name)
                    self.birdtimes.pop(temp_name)
                    return f"Removed **{count}x** {temp_name}. **0** remain."
                return f"Removed **{count}x** {temp_name}. **{self.birds[temp_name]}** remain."
        return f'"{bird_name}" does not exist.'


    def print_results(self, sort):
        if len(self.birds) != 0:
            result = ''
            if sort == 'alpha':
                for bird in sorted(self.birds, key = str.lower):
                    result += f'\n- {bird} **x{self.birds.get(bird)}**'
            elif sort == 'chrono':
                for bird in sorted(self.birdtimes.items(), key = lambda pair: pair[1]):
                    result += f'\n- {bird[0]} **x{self.birds.get(bird[0])}**'
            elif sort == 'taxonomy':
                current_bird_order = {}
                fake_birds = []
                for bird in self.birds.keys():
                    if bird in bird_order:
                        current_bird_order[bird] = int(bird_order[bird])
                    else:
                        fake_birds.append(bird)
                for bird in sorted(current_bird_order.items(), key = lambda pair: pair[1]):
                    result += f'\n- {bird[0]} **x{self.birds.get(bird[0])}**'
                for fake_bird in fake_birds:
                    result += f'\n- {fake_bird} **x{self.birds.get(fake_bird)}**'

            return result
        else:
            return "No birds seen. Better luck next time!"

    def rename(self, old_name, new_name):
        temp_name = old_name
        if old_name.upper() in my_lovely_codes and my_lovely_codes[old_name.upper()] in self.birds:
            temp_name = my_lovely_codes[old_name.upper()]

        new_temp = ''
        new_bool = False
        if new_name in self.birds:
            new_temp = new_name
        elif new_name.upper() in my_lovely_codes:
            new_bool = True
            if my_lovely_codes[new_name.upper()] in self.birds:
                new_temp = my_lovely_codes[new_name.upper()]

        if not new_temp:
            if not new_bool:
                self.birds[new_name] = self.birds[temp_name]
                self.birdtimes[new_name] = self.birdtimes[temp_name]
                self.birds.pop(temp_name)
                self.birdtimes.pop(temp_name)
                return f"Renamed **{temp_name}** to **{new_name}**."
            self.birds[my_lovely_codes[new_name.upper()]] = self.birds[temp_name]
            self.birdtimes[my_lovely_codes[new_name.upper()]] = self.birdtimes[temp_name]
            self.birds.pop(temp_name)
            self.birdtimes.pop(temp_name)
            return f"Renamed **{temp_name}** to **{my_lovely_codes[new_name.upper()]}**."

        return f'"{new_temp}" already exists.'

        # return f'"{old_name}" does not exist.'

    def move(self, old_name, new_name, count):
        temp_name = old_name
        if old_name.upper() in my_lovely_codes and my_lovely_codes[old_name.upper()] in self.birds:
            temp_name = my_lovely_codes[old_name.upper()]

        if count > self.birds[temp_name]:
            return "Not enough birds to move."

        new_temp = ''
        if new_name in self.birds:
            new_temp = new_name
        elif new_name.upper() in my_lovely_codes and my_lovely_codes[new_name.upper()] in self.birds:
            new_temp = my_lovely_codes[new_name.upper()]

        if new_temp:
            if count == -1:
                count = self.birds[temp_name]
                self.birds[new_temp] += self.birds[temp_name]
                self.birds.pop(temp_name)
                self.birdtimes.pop(temp_name)
            else:
                self.birds[new_temp] += count
                self.birds[temp_name] -= count
                if self.birds[temp_name] == 0:
                    self.birds.pop(temp_name)
                    self.birdtimes.pop(temp_name)
            return f"Moved **{count}x** {temp_name} to {new_temp}."

        return f'"{new_name}" does not exist.'

        # return f'"{old_name}" does not exist.'

    def set(self, bird_name, count):
        if bird_name.upper() not in my_lovely_codes and bird_name not in self.birdtimes:
            self.birdtimes[bird_name] = time.time_ns()
        elif bird_name.upper() in my_lovely_codes and my_lovely_codes[bird_name.upper()] not in self.birdtimes:
            self.birdtimes[my_lovely_codes[bird_name.upper()]] = time.time_ns()

        if count == 0:
            return self.remove_bird(bird_name, -1)

        if bird_name.upper() not in my_lovely_codes:
            self.birds[bird_name] = count
            return f'Set {bird_name} to **{count}**.'
        else:
            self.birds[my_lovely_codes[bird_name.upper()]] = count
            return f'Set {my_lovely_codes[bird_name.upper()]} to **{count}**.'


# Create local file to save unfinished checklists.

if not os.path.exists('birdcount_users.pickle') or os.path.getsize('birdcount_users.pickle') == 0:
    with open('birdcount_users.pickle', 'wb') as f:
        pickle.dump({}, f)

with open('birdcount_users.pickle', 'rb') as f:
    birdcount_users = pickle.load(f)

birdusers_sort = {}

sort_aliases = {'alpha': 'alpha', 'alphabet': 'alpha', 'alphabetic': 'alpha', 'alphabetical': 'alpha', 'alphabetically': 'alpha',
                'chrono': 'chrono', 'chronological': 'chrono', 'chronologically': 'chrono', 'time': 'chrono', 'timed': 'chrono',
                'tax': 'taxonomy', 'taxa': 'taxonomy', 'taxo': 'taxonomy', 'taxon': 'taxonomy', 'taxonomy': 'taxonomy', 'taxonomically': 'taxonomy', 'family': 'taxonomy'}

sort_messages = {'alpha': 'alphabetically', 'chrono': 'by time observed', 'taxonomy': 'by family'}

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.custom, name="custom", state=".help"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "ping" in message.content.lower().split():
        await message.reply("Pong!")

    if "pong" in message.content.lower().split():
        await message.reply("Ping!")

    if "thank you birdbot" in message.content.lower():
        r = random.randint(1,7)
        if r <= 3:
            await message.reply("My pleasure!")
        elif r <= 6:
            await message.reply("No problem!")
        else:
            await message.reply("FUCK YOU!!!")

    if "hello birdbot" in message.content.lower():
        r = random.randint(1, 7)
        if r <= 3:
            await message.reply("Hi!")
        elif r <= 6:
            await message.reply("Lovely day for birding!")
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
        with open('birdcount_users.pickle', 'wb') as f:
            pickle.dump(birdcount_users, f)
        birdusers_sort[ctx.author.id] = "chrono"
        r = random.randint(1,4)
        if r == 1:
            await ctx.reply(f'Let the adventure begin, <@{ctx.author.id}>!')
        elif r == 2:
            await ctx.reply(f'Best of luck, <@{ctx.author.id}>!')
        elif r == 3:
            await ctx.reply(f'The best time to go birding was yesterday. The second best time is now.')
        else:
            await ctx.reply(f'Checklist started for <@{ctx.author.id}>.')

@bot.command()
async def help(ctx):
    birCount = BirdCount()

    userinput = ctx.message.content.lower()
    segments = userinput.split()

    if len(segments) == 1:
        reply = ''
        for command in birCount.cmdhelp:
            reply += ("- " + command + ": " + birCount.cmdhelp[command] + '\n')
        embed = discord.Embed(title = 'List of available commands:',colour = discord.Colour.brand_green(), description = reply + '\n')
        embed.set_footer(text = f'Enter "help <command>" for the format of that specific command.')
        await ctx.reply(embed=embed)

    elif len(segments) == 2:
        if str(segments[1]).lower() in birCount.formats:
            # await ctx.reply(birCount.formats[segments[1]])
            await ctx.reply(embed=discord.Embed(title = f'{birCount.cmdhelp[str(segments[1]).lower()]}', colour = discord.Colour.brand_green(), description = birCount.formats[segments[1]]))
        else:
            await ctx.reply(f'"{segments[1]}" is not a valid command.')


    # await ctx.send(f"Hello <@{801956525454917634}>!")

@bot.command()
async def add(ctx):
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

    await ctx.reply(birdcount_users[ctx.author.id].add_bird(name, count))

    with open('birdcount_users.pickle', 'wb') as f:
        pickle.dump(birdcount_users, f)

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
        count = -1
        name = " ".join(segments[1:])

    if not name:
        await ctx.reply("Please enter a name.")
        return

    await ctx.reply(birdcount_users[ctx.author.id].remove_bird(name, count))

    with open('birdcount_users.pickle', 'wb') as f:
        pickle.dump(birdcount_users, f)

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

    else:
        await ctx.reply("Please enter a valid quantity.")
        return

    if len(segments) == 1:
        await ctx.reply("Please enter a name.")
        return

    await ctx.reply(birdcount_users[ctx.author.id].set(name, count))

    with open('birdcount_users.pickle', 'wb') as f:
        pickle.dump(birdcount_users, f)

@bot.command()
async def rename(ctx):
    userinput = ctx.message.content.lower()
    segments = userinput.split()

    if not ctx.author.id in birdcount_users:
        await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")
        return

    if len(segments) < 3:
        await ctx.reply("Please enter two valid names.")
        return

    # Searches for the longest match
    longest = 0

    for i in range(1, len(segments)):
        trial_name = " ".join(segments[1:i])
        if trial_name.upper() in my_lovely_codes and my_lovely_codes[trial_name.upper()] in birdcount_users[ctx.author.id].birds:
            longest = i
            break
        if trial_name in birdcount_users[ctx.author.id].birds:
            longest = i

    if longest == 0:
        await ctx.reply("Please enter two valid names.")
        return

    old = " ".join(segments[1:longest])
    new = " ".join(segments[longest:])

    await ctx.reply(birdcount_users[ctx.author.id].rename(old, new))

    with open('birdcount_users.pickle', 'wb') as f:
        pickle.dump(birdcount_users, f)

@bot.command()
async def move(ctx):
    userinput = ctx.message.content.lower()
    segments = userinput.split()

    if not ctx.author.id in birdcount_users:
        await ctx.reply(f'No checklist active for <@{ctx.author.id}>.')
        return

    if len(segments) < 3:
        await ctx.reply("Please enter two valid names.")
        return

    count = -1

    # Searches for the longest match
    longest = 0

    if segments[-1] == '0':
        await ctx.reply("Please enter a valid quantity.")
        return

    if segments[-1].isdigit():
        count = int(segments[-1])
        segments.pop()

    for i in range(1, len(segments)):
        trial_name = " ".join(segments[1:i])
        if trial_name.upper() in my_lovely_codes and my_lovely_codes[trial_name.upper()] in birdcount_users[ctx.author.id].birds:
            longest = i
            break
        if trial_name in birdcount_users[ctx.author.id].birds:
            longest = i

    old = " ".join(segments[1:longest])
    new = " ".join(segments[longest:])

    if longest == 0:
        await ctx.reply("Please enter two valid names.")
        return

    await ctx.reply(birdcount_users[ctx.author.id].move(old, new, count))

    with open('birdcount_users.pickle', 'wb') as f:
        pickle.dump(birdcount_users, f)

@bot.command()
async def print(ctx):
    userinput = ctx.message.content.lower()
    segments = userinput.split()
    if len(segments) == 1:
        if ctx.author.id not in birdcount_users:
            await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")

        else:
            if len(birdcount_users[ctx.author.id].birds) != 0:
                temp = '\n'
                temp += (birdcount_users[ctx.author.id].print_results(birdusers_sort[ctx.author.id]))
                temp += ('\n' + '\n' + f'**Keep it up, <@{ctx.author.id}>!** 🤩')
                embed = discord.Embed(title = f"Current checklist for {ctx.author.display_name}:", description=temp, colour=discord.Colour.green())
                embed.set_footer(text=f"Species seen: {len(birdcount_users[ctx.author.id].birds)}")
                await ctx.reply(embed=embed)
            else:
                await ctx.reply("You haven't seen any birds yet. 🥀🥀")
    else:
        temp_str = int(str(segments[1])[2:-1])

        if temp_str not in birdcount_users:
            await ctx.reply(f"No checklist active for {segments[1]}.")

        else:
            if len(birdcount_users[temp_str].birds) != 0:
                temp = '\n'
                temp += (birdcount_users[temp_str].print_results(birdusers_sort[segments[1]]))
                temp += ('\n' + '\n' + f"**All in a day's work for {segments[1]}.** 😎")
                temp_user = ctx.guild.get_member(temp_str)
                embed = discord.Embed(title=f"Current checklist for {temp_user.display_name}:", description=temp, colour=discord.Colour.green())
                embed.set_footer(text=f"Species seen: {len(birdcount_users[temp_str].birds)}")
                await ctx.reply(embed=embed)
            else:
                await ctx.reply(f"{segments[1]} hasn't seen any birds yet. 🥀🥀")

@bot.command()
async def done(ctx):
    if ctx.author.id not in birdcount_users:
        await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")
        return

    if len(birdcount_users[ctx.author.id].birds) != 0:
        temp = '\n'
        temp += (birdcount_users[ctx.author.id].print_results(birdusers_sort[ctx.author.id]))
        temp += ('\n' + '\n' + '**What a fruitful session!** 😄 😄 ')
        embed = discord.Embed(title="Total birds seen:", description=temp, colour=discord.Colour.green())
        embed.set_footer(text=f"Species seen: {len(birdcount_users[ctx.author.id].birds)}")
        await ctx.reply(embed=embed)
    else:
        await ctx.reply(birdcount_users[ctx.author.id].print_results(birdusers_sort[ctx.author.id]))

    birdcount_users.pop(ctx.author.id)

    with open('birdcount_users.pickle', 'wb') as f:
        pickle.dump(birdcount_users, f)

@bot.command()
async def sort(ctx):
    userinput = ctx.message.content.lower()
    segments = userinput.split()

    if ctx.author.id not in birdcount_users:
        await ctx.reply(f"No checklist active for <@{ctx.author.id}>.")
        return

    if len(segments) != 2 or segments[-1] not in sort_aliases:
        await ctx.reply("Please enter a valid sorting method. Use `.help sort` for more info.")
        return

    birdusers_sort[ctx.author.id] = sort_aliases[segments[-1]]
    await ctx.reply(f'Sorted {sort_messages[sort_aliases[segments[-1]]]}.')

@bot.command()
async def users(ctx):
    if len(birdcount_users) == 0:
        await ctx.reply("No active checklists.")
        return

    temp = ''

    for user in birdcount_users:
        if ctx.guild.get_member(int(user)):
            temp += f'\n- <@{user}>: **{len(birdcount_users[user].birds)}** species seen'

    temp += '\n' + "\n**The birds aren't gonna bird themselves!**"
    embed = discord.Embed(title="Currently active checklists:", description=temp, colour=discord.Colour.green())
    await ctx.reply(embed=embed)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)