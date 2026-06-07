# BirdBot
BirdBot is my first attempt at making a Discord bot, retroactive to 2025-07-18. No AI was used.

## Project Goals
- Add & remove birds seen while in the field.
- Print checklist of said birds.

## Usage Guide

In Discord, view list of commands with the `.help` command.

### Setup (Windows)

**1)** Clone the repository:
```
git clone https://github.com/markybuildy/BirdBot
cd BirdBot
```

**2)** Download the required packages:
```
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**3)** Set up bot token by creating a `.env` file with the following line:
```
DISCORD_TOKEN=<DISCORD BOT TOKEN HERE>
```
**4)** Run the bot with:
```
python main.py
```

## Backstory
&nbsp; &nbsp; &nbsp; &nbsp; I had always wanted to write my own Discord bot ever since my friend [Julian](https://github.com/cucumberbolts) created one for our server in 2021, but I couldn't think of anything it could be used for. That all changed, however, when the very same Julian, on a whim, gifted me a book about our local birds four years later, kickstarting my biggest and ongoing hobby-slash-obsession. I quickly fell into the birding rabbithole (birdhole?), and by the time summer vacation hit, I had seen over 70 species of birds, as well as having spent practically my entire bank account on a camera setup specifically to capture birds. I was ready to bird the fuck out of my China trip, which was to last all of July.

&nbsp; &nbsp; &nbsp; &nbsp; The first half of the trip was exhilarating. We travelled all across the country, never staying in the same city for more than a couple of days. Of course, I had my new camera poised and ready for avifauna the entire time. However, after we arrived at my grandparents' house where we would remain for the rest of the trip, I soon grew bored from the monotonous day-by-day. One day during this arduously lacklustre period, while out birding, I decided to count how many of each bird I saw (or as we say in the birding community, "keeping a checklist"). My method for doing so was rather crude: every time I saw a quantity of a species of bird, I would note it down in my private Discord server. For example, upon running into a pair of Azure-winged Magpies, I typed "magpie x2" and sent it in Discord. The process had a plethora of flaws, notably the grueling process of counting up all the tallies of each bird after the excursion, which took forever. *Wouldn't it be nice,* I thought, *if the counting process was automated?* And that was when inspiration struck.

&nbsp; &nbsp; &nbsp; &nbsp; It had been two years since I wrote the AP Computer Science A exam, which wasn't even in Python. I had much work to do if I wanted to write a Discord bot from scratch. Luckily, I had nothing but time. I started by writing a proof-of-concept program in an effort to brainstorm ideas and reacclimate to coding, which is included in this repository as the `test.py` file. After much troubleshooting and many YouTube tutorials, I had managed to transfer my ideas to a fully-fledged (haha) up-and-running Discord bot. On the morning of July 20th, 2025, BirdBot was alive.

&nbsp; &nbsp; &nbsp; &nbsp; Thanks are owed to [Julian Poon](https://github.com/cucumberbolts), who helped me with writing and troubleshooting BirdBot, and who ran a Tailscale server on his Raspberry Pi for me to connect to and bypass the Chinese firewall.

