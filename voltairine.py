import argparse
import random
import logging
import subprocess
import textwrap

import asyncio
import discord
import requests
import toml

client = discord.Client()

logger = logging.getLogger(__name__)


#@client.event#
#async def on_member_join(member):#
    #server = member.server#
    #fmt = 'Welcome {0.mention} to {1.name}! An injury to one is an injury to all!'#
    #await client.send_message(server, fmt.format(member, server))#

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
print('------')

insult1 = ["a Lazy", "a Stupid", " an Insecure", "an Idiotic", "a Slimy", "a Jerky", "a Smelly", "a Pompous", "a Communist", "a Dicknose", "a Pie-eating", "a Racist", "an Elitist", "a White Trash", "a Drug-Loving", "a Butterface", "a Tone Deaf", "an Ugly", "a Creepy"]
insult2 = ["Douche", "Ass", "Turd", "Rectum", "Butt", "Cock", "Shit", "Crotch", "Fascist", "Prick", "Jerk", "Taint", "Fuck", "Dick", "Boner", "Shart", "Nut", "Sphincter" ]
insult3 = ["Pilot", "Canoe", "Captain", "Pirate", "Hammer", "Knob", "Box", "Jockey", "Nazi", "Waffle", "Goblin", "Blossum", "Biscuit", "Clown", "Socket", "Monster", "Hound", "Dragon", "Balloon"]
compliment1 = ["a Gentle", "a Inviting", " an Obliging", "a Pleasant", "a Delightful", "a Considerate", "a Attractive", "a Helpful", "a Commendable", "a Courteous", "a Well-mannered", "a Ducky", "a Copacetic", "a Simpatico", "a Swell", "a Pleasurable", "a Peachy", "a Polite", "a Lovely"]
compliment2 = ["Gracious", "Civil", "Kindly", "Warm", "Sociable", "Approachable", "Breezy", "Congenial", "Dandy", "Marvelous", "Elegant", "Alluring", "Classy", "Fascinating", "Cute", "Dazzling", "Sublime", "Splendid" ]
compliment3 = ["Pilot", "Canoe", "Captain", "Pirate", "Hammer", "Knob", "Box", "Jockey", "Nazi", "Waffle", "Goblin", "Blossum", "Biscuit", "Clown", "Socket", "Monster", "Hound", "Dragon", "Balloon"]
ball = ['It is certain','It is decidedly so','Without a doubt','Yes, definitely','You may rely on it','As I see it, yes','Most likely','Outlook good','Yes','Signs point to yes','Reply hazy try again','Ask again later','Better not tell you now','Cannot predict now','Concentrate and ask again','Don\'t count on it','My reply is no','My sources say no','Outlook not so good','Very doubtful']
help_msg = ('''\
!help 
!4chan
!8ball
!acab
!afaq
!anarchism
!ancap
!ancom
!anfem
!anti-civ
!antifa
!bakunin
!bash
!bestshit
!bathroom
!bonanno
!bookchin
!bookclub
!bordiga
!bourge
!brd
!bread
!btfo
!bubbles
!catsnake
!chomsky
!cnt
!coffee
!coin 
!compliment
!cowsay 
!cyberpunk
!durruti
!encounter 
!ezln
!facepalm
!fascist
!feminism
!foucault
!fresh
!fullcommunism
!goldman
!gulag
!hacktheplanet
!horseshoe
!indeed
!insult
!kitty
!kronstadt
!kropotkin
!leftcom
!leftunity
!lenin
!lenny
!liberals
!linux
!makhno
!marx
!memes
!motivation
!mra
!mtw
!mutualism
!ohwell
!outside
!poblacht
!proudhon
!pusheen
!rainbowstalin
!reddit
!rsoc
!rules
!sexist
!sjw
!space
!sparkles
!spook
!stirner
!stirnerwave
!tankie
!tea
!trotsky
!trump
!usa
!vaporwave
!vegan
!vote''')

changelog = ('''
v0.1.1
-changed !gold to !inventory
-Added shop
-Added whisper
-Added insult
-Added RPG Dice Roller
-Added encounters
-Added potions
-Added fresh and wtf
v0.1.2
-added dozens of new commands
-added cowsay
v0.1.3
-added pyborg
-removed benned commands, now with Emma
v0.1.4
-added catsnake command
-added Foucault command
-fixed anticiv command
-added short urls to edu commands
''')

user_gold = {}
user_potions={}



async def build_saycow():
    return """
     \   ^__^
      \  (oo)\_______
         (__)\       )\/\\
             ||----w |
             ||     ||
    """

async def build_thinkcow():
    return """
     o   ^__^
      o  (oo)\_______
         (__)\       )\/\\
             ||----w |
             ||     ||
    """

async def build_box(body, length=40):
    bubble = []

    lines =  await normalize_text(body, length)

    bordersize = len(lines[0])

    bubble.append("  "  + "_" * bordersize)

    for index, line in enumerate(lines):
        border = get_border(lines, index)

        bubble.append("%s %s %s" % (border[0], line, border[1]))

    bubble.append("  " + "-" * bordersize)

    return "\n".join(bubble)

async def normalize_text(body, length):
    lines  = textwrap.wrap(body, length)
    if len(lines) == 0:
        return [""]
    maxlen = len(max(lines, key=len))
    return [ line.ljust(maxlen) for line in lines ]

def get_border(lines, index):
    if len(lines) < 2:
        return [ "<", ">" ]

    elif index == 0:
        return [ "/", "\\" ]

    elif index == len(lines) - 1:
        return [ "\\", "/" ]

    else:
        return [ "|", "|" ]


def learn(body):
    """thin wrapper for learn to switch to multiplex mode"""
    settings = toml.load("volt_settings.toml")
    if settings['pyborg']['multiplex']:
        ret = requests.post("http://{}:{}/learn".format(settings['pyborg']['server'], settings['pyborg']['port']), data={"body": body})
        if ret.status_code > 499:
            logger.error("Internal Server Error in pyborg_http. see logs.")
        else:
            ret.raise_for_status()

def reply(body):
    """thin wrapper for reply to switch to multiplex mode"""
    settings = toml.load("volt_settings.toml")
    if settings['pyborg']['multiplex']:
        ret = requests.post("http://{}:{}/reply".format(settings['pyborg']['server'], settings['pyborg']['port']), data={"body": body})
        if ret.status_code == requests.codes.ok:
            reply = ret.text
            logger.debug("got reply: %s", reply)
        elif ret.status_code > 499:
            logger.error("Internal Server Error in pyborg_http. see logs.")
            return
        else:
            ret.raise_for_status()
        return reply

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    elif message.content.startswith('!cowsay'):
        body = " ".join(message.content.split()[1:])
        cowsaid = await build_box(body, 40) + await build_saycow()
        await client.send_message(message.channel, '```txt\n{0}```'.format(cowsaid))

    elif message.content.startswith('!cowthink'):
        body = " ".join(message.content.split()[1:])
        cowsaid = await build_box(body, 40) + await build_thinkcow()
        await client.send_message(message.channel, '```txt\n{0}```'.format(cowsaid))

    elif message.content.startswith('!help'):
        await client.send_message(message.channel, help_msg)

    elif message.content.startswith('!changelog'):
        await client.send_message(message.channel, changelog)

    elif message.content.startswith('Voltairine, introduce yourself'):
        await client.send_message(message.channel, '```Hi everyone! I\'m Voltairine. Nice to meet you all```')

    elif message.content.startswith('!4chan'):
        await client.send_message(message.channel, '**ITS LITERALLY THE MOST TOXIC ASPECTS OF HUMANITY THROWN INTO A BLENDER AND PULSED INTO A SICKENING MASS OF SHIT, THATS BEEN SLOWLY FUCKING CREEPING INTO THE REAL WORLD AND JUST UGH 4CHAN IS KILLING THE WORLD**')

    elif message.content.startswith('!8ball'):
        j = random.randint(0,11)
        await client.send_message(message.channel, ball[j])

    elif message.content.startswith('!acab'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/acab1.png\nhttp://www.gooseberrycollective.net/bots/acab2.png')

    elif message.content.startswith('!afaq'):
        await client.send_message(message.channel, ':books: https://libcom.org/files/Iain%20McKay%20-%20Anarchist%20FAQ.pdf')

    elif message.content.startswith('!anarchism'):
        await client.send_message(message.channel, 'Anarchism is a social movement that seeks liberation from oppressive systems of control including but not limited to the state, capitalism, racism, sexism, speciesism, and religion. Anarchists advocate a self-managed, classless, stateless society without borders, bosses, or rulers where everyone takes collective responsibility for the health and prosperity of themselves and the environment.')

    elif message.content.startswith('!antifa'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/antifa.gif')

    elif message.content.startswith('!bathroom'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/bathroom.png')

    elif message.content.startswith('!bash'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/bash.gif')

    elif message.content.startswith('!berkman'):
        await client.send_message(message.channel, '**Alexander Berkman** (November 21, 1870 – June 28, 1936) was a leading member of the anarchist movement in the early 20th century, famous for both his political activism and his writing.Berkman was born in Vilnius, Lithuania and emigrated to the United States in 1888. He lived in New York City, where he became involved in the anarchist movement. He was the one-time lover and lifelong friend of anarchist Emma Goldman. In 1892, undertaking an act of propaganda of the deed, Berkman made an unsuccessful attempt to assassinate businessman Henry Clay Frick, for which he served 14 years in prison. His experience in prison was the basis for his first book, Prison Memoirs of an Anarchist.\nAfter his release from prison, Berkman served as editor of Goldman\'s anarchist journal, Mother Earth, and later established his own journal, The Blast. In 1917, Berkman and Goldman were sentenced to two years in jail for conspiracy against the newly instated draft. After their release from prison, they were arrested—along with hundreds of others—and deported to Russia. Initially supportive of that country\'s Bolshevik revolution, Berkman and Goldman soon became disillusioned, voicing their opposition to the Soviet\'s use of terror after seizing power and their repression of fellow revolutionaries.\n\n:books: **Prison Memoirs of an Anarchist **: http://bit.do/c7ap9\n\n:books: **Bolsheviks Shooting Anarchists** with Emma Goldman: http://bit.do/c7aqb \n\n:books: **The Russian Tragedy (A Review and An Outlook)**: http://bit.do/c7aqe \n\n:books: **What Is Communist Anarchism?**: http://bit.do/c7aqh \n\nhttp://www.gooseberrycollective.net/bots/berkman.png')

    elif message.content.startswith('!bonanno'):
        await client.send_message(message.channel, '**Alfredo Bonanno** was born 1937 in Catania, Italy, and is a main theorist of contemporary insurrectionary anarchism who wrote essays such as *Armed Joy* (*for which he was imprisoned for 18 months by the Italian government*). He is an editor of *Anarchismo Editions* and many other publications, only some of which have been translated into English. He has been involved in the anarchist movement for over thirty years.\n\n:books: **Armed Joy**: http://bit.do/c7as9\n\n:books: **The Anarchist Tension **: http://bit.do/c7atb \n\n:books: **From Riot to Insurrection**: http://bit.do/c7ate \n\n:books: **Insurrectionalist Anarchism — Part One **: http://bit.do/c7atj \n\nhttp://www.gooseberrycollective.net/bots/bonanno.jpg')

    elif message.content.startswith('!ancap'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/ancap1.png \n http://www.gooseberrycollective.net/bots/ancap2.png')

    elif message.content.startswith('!ancom'):
        await client.send_message(message.channel, 'A theory of anarchism which advocates the abolition of the state, capitalism, wage labour, and private property (while retaining respect for personal property), and in favour of common ownership of the means of production, direct democracy, and a horizontal network of voluntary associations and workers\' councils with production and consumption based on the guiding principle: "from each according to his ability, to each according to his need"\n\n:books: **Recommended Reading**:books: \n\n:closed_book:  **Anarchist communism - an introduction** http://bit.do/c7aqn\n\n:closed_book:  **A Short Introduction to Anarchist Communism**  http://bit.do/c7aqq')

    elif message.content.startswith('!anfem'):
        await client.send_message(message.channel, 'Anarchism and feminism have always been closely linked. Anfems see patriarchy as a manifestation of involuntary coercive hierarchy, that should be replaced by decentralized free association. It is an anti-authoritarianism, anti-capitalism, anti-oppressive philosophy, with the goal of creating an "equal ground" between males and females. The term "anarcha-feminism" suggests the social freedom and liberty of women, without needed dependence upon other groups or parties.\n\n:books: **Recommended Reading**:books: \n\n :closed_book:  **Anarchy and the Sex Question ** by Emma Goldman: http://bit.do/c7aqy\n\n:closed_book:  **The Question of Feminism ** by Lucia Sanchez Saornil: http://bit.do/c7aqD\n\nhttp://www.gooseberrycollective.net/bots/anfem.png')

    elif message.content.startswith('!anti-civ'):
        await client.send_message(message.channel, ':books: **The Network of Domination by Wolfi Landstreicher**: https://theanarchistlibrary.org/library/wolfi-landstreicher-the-network-of-domination\n:books: **Against His-story, Against Leviathan by Fredy Perlman**: https://theanarchistlibrary.org/library/fredy-perlman-against-his-story-against-leviathany\n:books: **What is Green Anarchy? **: https://theanarchistlibrary.org/library/anonymous-what-is-green-anarchy\n:books: **Desert**: https://theanarchistlibrary.org/library/anonymous-desert\n http://www.gooseberrycollective.net/bots/anticiv.png')

    elif message.content.startswith('!bakunin'):
        await client.send_message(message.channel, '**Mikhail Bakunin** (30 May 1814 – 1 July 1876) was a Russian revolutionary anarchist, and founder of collectivist anarchism. He is considered among the most influential figures of anarchism, and one of the principal founders of the social anarchist tradition. Bakunin saw revolution in terms of the overthrow of one oppressing class by another oppressed class and the destruction of political power as expressed as the state and social hierarchy. \n\n:books: **Statism and Anarchy**: http://bit.do/c7atw\n\n:books: **God and the State**: http://bit.do/c7atz\n\n:books: **Marxism, Freedom and the State**: http://bit.do/c7atA\n\n:books: **The Capitalist System**: http://bit.do/c7atC')

    elif message.content.startswith('!bestshit'):
        await client.send_message(message.channel, ':books: CONQUEST OF BREAD MOTHERFUCKER\nhttps://theanarchistlibrary.org/library/petr-kropotkin-the-conquest-of-bread \nABC OF ANARCHISM IF YOU LIKE IT IN SIMPLE ENGLISH! \nhttps://libcom.org/library/abc-anarchism-alexander-berkman \nCOMMUNIST MANIFESTO FOR THE CLASSIC SHIT :ok_hand: :ok_hand: :ok_hand:  \nhttps://www.marxists.org/archive/marx/works/1848/communist-manifesto/')

    elif message.content.startswith('!bookchin'):
        await client.send_message(message.channel, '**Murray Bookchin** (Jan 14, 1921 – July 30, 2006)[5] was an American anarchist and libertarian socialist author, orator, historian, and political theorist. A pioneer in the ecology movement, Bookchin initiated the critical theory of social ecology within anarchist, libertarian socialist, and ecological thought. He was the author of two dozen books covering topics in politics, philosophy, history, urban affairs, and ecology. \n\n:books: **Social Anarchism or Lifestyle Anarchism**: http://bit.do/c7atT \n\n:books: **The Ecology of Freedom**: http://bit.do/c7atV \n\n:books: **Post-Scarcity Anarchism**: http://bit.do/c7atX\n http://www.gooseberrycollective.net/bots/bookchin.png')

    elif message.content.startswith('!bookclub'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/bookclub.png\n\n\n:books: __**Anarchist Book Club**__ :books:\n\nJoin the Book Club! Discussion every Sunday at 17:00 EST in Voice. Text discussion anytime in #library channel. This week\' book is: \n\n :book: **Philosophy and Real Politics** by Raymond Geuss. https://we.riseup.net/goatgooseberry/raymond-geuss-philosophy-and-real-politics+377228')

    elif message.content.startswith('!books'):
        await client.send_message(message.channel, ':books: :books: \n* **Peter Marshall - Demanding the Impossible: A History of Anarchism**\n* **Clifford Harper - Anarchy: graphic guide** \n* **Peter Kropotkin - Conquest of Bread**\n* Peter Kropotkin - Mutual Aid\n* Alexander Berkman - The ABC of anarchism\n* Peter Gelderloos - Anarchy Works\n* Emma Goldman - Anarchism and Other Essays\n* Oscar Wilde - The Soul of Man Under Socialism\n* Marx/Engels - Manifesto of the Communist Party\n* **Ursula Le Guin - The Dispossessed**\n* Daniel Guérin - Anarchism: From Theory to Practice\n* Comité Invisible (The Invisible Committee) - The Coming Insurrection\n* Bob Black - The Abolition of Work\n* Karl Marx - Capital\n* Max Stirner - The Unique and His Property\n* Daniel Guerin - Anarchism: Theory and Practice\n* Colin Ward - Anarchism: A Short Introduction\n* Benjamin R. Tucker - Instead of a Book\n* Alexander Berkman - What is Anarchism?\n* Ken Knabb - The Joy of Revolution\n* **Crimethinc - Work**\n* Crimethinc - Days of War, Nights of Love\n* **Daniel Guerin - No Gods, No Masters**\n* The Organizational Platform of the General Union of Anarchists\n* Peter Arshinov - History of the Makhnovist Movement\n* **Prole.info - The Housing Monster**\n* **Prole.info - Abolish Restaurants**\n* Peter Gelderloos - How Nonviolence Protects the State\n* Mikhail Bakunin - God and the State\n* Mikhail Bakunin - Revolutionary Catechism\n* **David Graeber - Debt: The First 5000 Years**\n* Voltairine de Cleyre - Crime and Punishment')

    elif message.content.startswith('!bordiga'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/bordiga.png')

    elif message.content.startswith('!bourge'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/bourge.png')

    elif message.content.startswith('!brd'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/brd.png')

    elif message.content.startswith('!bread'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/bread.png')

    elif message.content.startswith('!btfo'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/btfo.gif')

    elif message.content.startswith('!bubbles'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/bubbles.png')
        
    elif message.content.startswith('!catsnake'):
        await client.send_message(message.channel, 'http://img-cache.cdn.gaiaonline.com/ebd06c23c8dc3f087cd6d6fc5f31cfb6/http://img.photobucket.com/albums/v633/in-dis-guise/7_CatSnake.jpg')

    elif message.content.startswith('!chart'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/chart1.png\nhttp://www.gooseberrycollective.net/bots/chart2.png')

    elif message.content.startswith('!chomsky'):
        await client.send_message(message.channel, '**Noam Chomsky** (Dec 7, 1928) is an American linguist, philosopher, cognitive scientist, historian, social critic, and political activist. Sometimes described as "the father of modern linguistics", Chomsky is also a major figure in analytic philosophy, and one of the founders of the field of cognitive science. \n\n :books: **Chomsky on Anarchism**: http://bit.do/c7aud\n\n:books: **Deterring Democracy**: http://bit.do/c7aui\n\n:books: **Manufacturing Consent**: http://bit.do/c7auk \n http://www.gooseberrycollective.net/bots/chomsky1.png')

    elif message.content.startswith('!cnt'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/cnt.png\nhttp://www.gooseberrycollective.net/bots/cnt1.png')

    elif message.content.startswith('!coffee'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/coffee.png')

    elif message.content.startswith('!communism'):
        await client.send_message(message.channel, 'A spectre:ghost::ghost: is haunting:ghost: :earth_africa:Europe:earth_africa: — the spectre :ghost:of communism☭☭☭☭. All the :muscle::muscle:powers of old Europe:muscle: have entered into a :pray: holy alliance :pray:to exorcise this spectre:ghost::ghost::ghost:: Pope :poop::poop:and Tsar:poop::thumbsdown::thumbsdown:, Metternich:poop: and Guizot:poop::poop::poop:')

    elif message.content.startswith('!cpusa'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/cpusa.png')

    elif message.content.startswith('!cyberpunk'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/cyberpunk.gif')

    elif message.content.startswith('!durruti'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/durruti.png')

    elif message.content.startswith('!ezln'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/ezlnisbae.png')
        
    elif message.content.startswith('!foucault'):
        await client.send_message(message.channel, '**Michel Foucault** (15 Oct 1926 – 25 June 1984) was a French philosopher, historian of ideas, social theorist, philologist and literary critic. His theories addressed the relationship between power and knowledge, and how they are used as a form of social control through societal institutions.\n\n :books: **Power/Knowledge** Power/Knowledge is a selection of content done by Foucault to encapsulate the vision for his overarching project. Recommended as a starting place for reading Foucault, especially Two Lectures.  http://bit.do/c7aoj \n\n:books:**History of Sexuality** http://bit.do/c7aoq \n\n:books: **Discipline and Punish: The Birth of the Prison**  http://bit.do/c7aor \n\n:books: **Society must be defended**  http://bit.do/c7aot \n\n:books: **Paul Rainbow Foucault Reader** http://bit.do/c7aox')

    elif message.content.startswith('!fullcommunism'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/fc.png')

    elif message.content.startswith('!facepalm'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/facepalm.png')

    elif message.content.startswith('!fascist'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/antifa2.png')

    elif message.content.startswith('!feminism'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/feminism.png\n```The struggle against patriarchy is an essential part of class conflict and the anarchist struggle against the state and capital. In essence, anarchist struggle is a necessary component of feminist struggle and vice versa.```')

    elif message.content.startswith('!fresh'):
        await client.send_message(message.channel, '```Now, this is a story all about how \nMy life got flipped-turned upside down \nAnd I\'d like to take a minute \n Just sit right there \nI\'ll tell you how I became the prince of a town called Bel-Air```')

    elif message.content.startswith('!goldman'):
        await client.send_message(message.channel, '**Emma Goldman** (June 27, 1869 – May 14, 1940) was an anarchist known for her political activism, writing, and speeches. She played a pivotal role in the development of anarchist political philosophy in North America and Europe in the first half of the 20th century.\n\n:books: **Anarchism and Other Essays**: http://bit.do/c7auF\n\n:books: **My Disillusionment in Russia** with Emma Goldman: http://bit.do/c7auH\n\n:books: **My Further Disillusionment in Russia**: http://bit.do/c7auL\n\n:books: **Voltairine De Cleyre**: http://bit.do/c7auN')

    elif message.content.startswith('!gulag'):
        await client.send_message(message.channel, 'https://libcom.org/history/gay-gulag')

    elif message.content.startswith('!hitler'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/hitler.png')

    elif message.content.startswith('!hacktheplanet'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/hacktheplanet.png')

    elif message.content.startswith('!horseshoe'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/horseshoe.png')

    elif message.content.startswith('!hoxha'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/hoxha.png')

    elif message.content.startswith('!ideology'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/ideology.png')

    elif message.content.startswith('!indeed'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/indeed.png')


    elif message.content.startswith('!kitty'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/kitty.png')

    elif message.content.startswith('!kronstadt'):
        await client.send_message(message.channel, 'http://www.veoh.com/watch/v18771330YDwTzP3g')

    elif message.content.startswith('!kropotkin'):
        await client.send_message(message.channel, '**Pyotr Kropotkin** (Dec 9, 1842 – February 8, 1921) was a Russian activist, scientist, and philosopher, who advocated anarchism. Kropotkin was a proponent of a decentralised communist society free from central government and based on voluntary associations of self-governing communities and worker-run enterprises. \n\n:books: **The Conquest of Bread **: http://bit.do/c7a5C\n\n:books: **The Commune of Paris **: http://bit.do/c7a5G\n\n:books: **Mutual Aid: A Factor of Evolution **: http://bit.do/c7a5K\n\n:books: **Communism and Anarchy**: http://bit.do/c7a5L')

    elif message.content.startswith('!leftcom'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/leftcom.jpg')

    elif message.content.startswith('!leftunity'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/love.png')

    elif message.content.startswith('!lenin'):
        await client.send_message(message.channel, 'a counter-revolutionary class traitor, who is responsible for the creation of the state-capitalist dictatorship known as the USSR. Along with other state-capitalist dictators such as Stalin and Mao, Lenin has tarnished the reputation of communism better than any capitalist or fascist ever could. http://www.gooseberrycollective.net/bots/lenin1.png\nhttp://www.gooseberrycollective.net/bots/lenin2.png')

    elif message.content.startswith('!lenny'):
        await client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')

    elif message.content.startswith('!liberals'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/liberals.gif')

    elif message.content.startswith('!linux'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/linux.png')

    elif message.content.startswith('!makhno'):
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=WGqkyHd1cZk')

    elif message.content.startswith('!malatesta'):
        await client.send_message(message.channel, '**Errico Malatesta** (14 December 1853 – 22 July 1932) was an Italian anarchist. He spent much of his life exiled from Italy and in total spent more than ten years in prison. Malatesta wrote and edited a number of radical newspapers and was also a friend of Mikhail Bakunin.\n\n:books: **At The Café **: http://bit.do/c7a5X\n\n:books: **Anarchism and Organization **: http://bit.do/c7a5Z \n\n:books: **Democracy and Anarchy **: http://bit.do/c7a54 \n\n:books: **Mutual Aid: An Essay  **: http://bit.do/c7a57 \nhttp://www.gooseberrycollective.net/bots/malatesta.jpg')

    elif message.content.startswith('!marx'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/marx1.png')

    elif message.content.startswith('!memes'):
        await client.send_message(message.channel, 'https://we.riseup.net/goatgooseberry/meme-commands')

    elif message.content.startswith('!misandry'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/misandry.png')

    elif message.content.startswith('!motivation'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/motivation.png')

    elif message.content.startswith('!mra'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/mra.jpg')

    elif message.content.startswith('!mtw'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/mtw.gif')

    elif message.content.startswith('!mutualism'):
        await client.send_message(message.channel, '"Mutualism is not a specific social, political or economic system. It is—at its core—an ethical philosophy. We begin with mutuality or reciprocity—the Golden Rule, more or less—and then seek to apply that principle in a variety of situations. As a result, under mutualism every meaningfully social relation will have the form of an anarchic encounter between equally unique individuals—free absolutes—no matter what layers of convention we pile on it." \n\n—Shawn P. Wilbur, *"Two-Gun Mutualism and The Golden Rule"* \n\nMutualism is an anti-capitalist economic theory and anarchist school of thought that advocates a society where each person might possess a means of production, either individually or collectively, with trade representing equivalent amounts of labor in a "freed market".\nMutualists believe that it is the state enforcement of capitalist property relations that alienates the working class from the means of production and subsistence and allows exploitation in the forms of profit, interest, and rents. Therefore, they wish to see private property abolished and replaced with possession-and-use, "the land to the cultivator, the mine to the miner, the tool to the laborer."\n\n:books: **Recommended reading**: :books: \n\n**[A Mutualist FAQ]** http://www.mutualist.org/id23.html\n **[Markets Not Capitalism]** https://goo.gl/YM4Gx1 \n**[What is Property?]** https://goo.gl/kkAgKx \n:books: **In-Depth**: :books:\n **[Studies in Mutualist Political Economy]** https://goo.gl/3rcWrn \n**[Kevin Carson\'s blog with links to his books]** http://mutualist.blogspot.ca/ \n**[humanispherian\'s blog with translations of Proudhon]** https://www.mutualism.info/ \n:books: **Further reading**: :books: \n**[C4SS Studies]** https://c4ss.org/content/category/studies \n**[Kevin Carson\'s suggested reading list]** http://www.mutualist.org/id6.html')

    elif message.content.startswith('!ohwell'):
        await client.send_message(message.channel, '¯\_(ツ)_/¯')

    elif message.content.startswith('!outside'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/outside.png')

    elif message.content.startswith('!poblacht'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/poblacht.png')

    elif message.content.startswith('!popcorn'):
        await client.send_message(message.channel, 'https://ipfs.pics/QmW3FgNGeD46kHEryFUw1ftEUqRw254WkKxYeKaouz7DJA')

    elif message.content.startswith('!proudhon'):
        await client.send_message(message.channel, '**Pierre-Joseph Proudhon** (15 January 1809 – 19 January 1865) was a French politician and the founder of mutualist philosophy. He was the first person to declare himself an anarchist and is widely regarded as one of the ideology\'s most influential theorists. Proudhon is even considered by many to be the "father of anarchism". He became a member of the French Parliament after the revolution of 1848, whereafter he referred to himself as a federalist.\n\n:books: **What is Property?**: http://bit.do/c7a6n\n\n:books: **System of Economical Contradictions**: http://bit.do/c7a6s\n\n:books: **God is Evil, Man is Free **: http://bit.do/c7a6z\n\n:books: **General Idea of the Revolution in the Nineteenth Century**: http://bit.do/c7a6E\n\nhttp://www.gooseberrycollective.net/bots/proudhon1.png')

    elif message.content.startswith('!pusheen'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/pusheen1.png\nhttp://www.gooseberrycollective.net/bots/pusheen2.png\nhttp://www.gooseberrycollective.net/bots/pusheen3.png\nhttp://www.gooseberrycollective.net/bots/pusheen4.png')

    elif message.content.startswith('!rainbowstalin'):
        await client.send_message(message.channel, 'http://rainbowstalin5.ytmnd.com/')

    elif message.content.startswith('!reddit'):
        await client.send_message(message.channel, 'http://gooseberrycollective.net/doku.php?id=radical_reddit')

    elif message.content.startswith('!revolution'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/revolution.png')

    elif message.content.startswith('!rsoc'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/rsoc1.png\nhttp://www.gooseberrycollective.net/bots/rsoc2.png')

    elif message.content.startswith('!rules'):
        await client.send_message(message.channel, 'http://pastebin.com/KpfbM3iC')

    elif message.content.startswith('!stirnerwave'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/stirnerwave.png')

    elif message.content.startswith('!sjw'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/sjw.png')

    elif message.content.startswith('!space'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/space.png')

    elif message.content.startswith('!sparkles'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/sparkles.gif')

    elif message.content.startswith('!spook'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/spook.png')

    elif message.content.startswith('!stirner'):
        await client.send_message(message.channel, '**Max Stirner** (October 25, 1806 – June 26, 1856) was a German philosopher. He is often seen as one of the forerunners of nihilism, existentialism, psychoanalytic theory, postmodernism, and anarchism, especially of individualist anarchism.\n\n:books: **The Ego and His Own **: http://bit.do/c7a6R\n\n:books: **Art and Religion **: http://bit.do/c7a6T\n\n:books: **The False Principle of Our Education **: http://bit.do/c7a6X\n\n:books: **Stirner’s Critics **: http://bit.do/c7a6Y\n\nhttp://www.gooseberrycollective.net/bots/stirner.gif')

    elif message.content.startswith('!source'):
        await client.send_message(message.channel, 'https://github.com/gooseberrycollective/voltairine')

    elif message.content.startswith('!tankie'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/tankie1.png')

    elif message.content.startswith('!tarot'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/tarot.png')

    elif message.content.startswith('!trotsky'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/trotsky.jpg')

    elif message.content.startswith('!trump'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/trump1.png')

    elif message.content.startswith('!tea'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/tea.png')

    elif message.content.startswith('!usa'):
        await client.send_message(message.channel, '"The US has done a numerous amount of unspeakable crimes against humanity"')

    elif message.content.startswith('!vaporwave'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/vaporwave.png')

    elif message.content.startswith('!vegan'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/vegan.png')

    elif message.content.startswith('!vote'):
        await client.send_message(message.channel, 'http://www.gooseberrycollective.net/bots/vote.png')

    elif message.content.startswith('!whisper'):
        await client.send_message(message.author, 'pssst')
        
    elif message.content.startswith('!insult'):
        j = random.randint(0,18)
        k = random.randint(0,17)
        l = random.randint(0,18)
        await client.send_message(message.channel, '```You\'re ' + insult1[j] + ' ' + insult2[k] + ' ' + insult3[l] + '```')

    elif message.content.startswith('!compliment'):
        j = random.randint(0,18)
        k = random.randint(0,17)
        l = random.randint(0,18)
        await client.send_message(message.channel, '```You\'re ' + compliment1[j] + ' ' + compliment2[k] + ' ' + compliment3[l] + '```')

    elif message.content.startswith('!coin'):
        j = random.randint(1,2)
        if j == 1:
            await client.send_message(message.channel, '```Heads!```')
        else:
            await client.send_message(message.channel, '```Tails!```')
            
    elif message.content.startswith('!d4'):
        j = random.randint(1,4)
        await client.send_message(message.channel, '```Rolling a d4\nRolled a ' + str(j) + '```')

    elif message.content.startswith('!d6'):
        j = random.randint(1,6)
        await client.send_message(message.channel, '```Rolling a d6\nRolled a ' + str(j) + '```')

    elif message.content.startswith('!d8'):
        j = random.randint(1,8)
        await client.send_message(message.channel, '```Rolling a d8\nRolled a ' + str(j) + '```')

    elif message.content.startswith('!d10'):
        j = random.randint(1,10)
        await client.send_message(message.channel, '```Rolling a d10\nRolled a ' + str(j) + '```')

    elif message.content.startswith('!d12'):
        j = random.randint(1,12)
        await client.send_message(message.channel, '```Rolling a d12\nRolled a ' + str(j) + '```')
    elif message.content.startswith('!d20'):
        j = random.randint(1,20)
        await client.send_message(message.channel, '```Rolling a d20\nRolled a ' + str(j) + '```')

    elif message.content.startswith('!swing'):
        j = random.randint(0,1)
        if j == 0:
            msg = 'They miss, burrying their sword into the ground'
        elif j == 1:
            msg = 'They hit. Cleaving the enemy in two'
        await client.send_message(message.channel,'```' +  message.author.name + ' swings their mighty sword\n' +msg+'```')

    elif message.content.startswith('!inventory'):
        if message.author not in user_gold:
           user_gold[message.author] = 0
        if message.author not in user_potions:
            user_potions[message.author] = 0

        await client.send_message(message.channel, '```'+message.author.name+' has '+str(user_gold[message.author])+' gold and '+str(user_potions[message.author])+' potions```')

    elif message.content.startswith('!encounter'):
        k = random.randint(0,3)
        enemy = ['ancap', 'tankie', 'fascist', 'liberal', 'trump', 'cop']
        enemy_pic = ['https://ipfs.pics/ipfs/QmUq6F6NbYznU9y65Pc17gG8rSBx9w42224FneG3EspgXX','https://ipfs.pics/QmRCh7AFfyL3ZSXCbF6ax6NjkrMwCCqgar8RoajCYp6Zot','https://ipfs.pics/QmSrPJqzc8dzni8EwvGMg3GJuNLrL4pwgfRNgeM68ZwF1s','https://ipfs.pics/QmTD8o6ZZ4Ppd4sbTMjY9Cf7SXmt7uTZdwuHwojyTLNtcs','https://ipfs.pics/QmdLNzYbiSfkEKp2mDotu1yCRabi43iopkFxdJBfaKJW93','https://ipfs.pics/QmcdWyBSp78n65VhxrFHgvLhjvfkA7FyKtTtwAnFx3Rszp']
        enemy_hp = [15,15, 17, 10, 15,20]
        enemy_hp_l = int(enemy_hp[k])
        player_hp = 20
        player_dmg = 0
        enemy_dmg = 0
        await client.send_message(message.channel, enemy_pic[k]+'\n```A '+enemy[k]+' appears!```')

        while enemy_hp_l > 0 and player_hp > 0:
            await client.send_message(message.channel, '```The '+enemy[k]+' has ' + str(enemy_hp_l) + ' hp \n'+message.author.name+' has ' + str(player_hp) + ' hp```')
            msg = await client.wait_for_message(author=message.author)
            if msg.content == 'attack' or msg.content == '!sttack':
                player_dmg = random.randint(1,12)
                enemy_hp_l = (enemy_hp_l - player_dmg)
                if enemy_hp_l < 0:
                    enemy_hp_l = 0
            elif msg.content == 'potion':
                if message.author not in user_potions:
                    user_potions[message.author] = 0
                if user_potions[message.author] > 0:
                    user_potions[message.author] -=1
                    player_hp +=5
                    await client.send_message(message.channel, '``` '+message.author.name+' used a potion. Their hp went up by 5```')
                    continue
                elif user_potions[message.author] == 0:
                    await client.send_message(message.channel, '```'+message.author.name+' fumbles around in their bag for a potion that isn\'t there')
            else:
                await client.send_message(message.channel, '```Accepted input, attack, potion```')

            if enemy_hp_l <= 0:
                gold = random.randint(1, 8)
                await client.send_message(message.channel, '```'+message.author.name+' defeats the '+enemy[k]+' and finds ' + str(gold) + ' gold!```')
                if message.author not in user_gold:
                    user_gold[message.author] = gold
                else:
                    user_gold[message.author] += gold
                break
                
            enemy_dmg = random.randint(1,12)
            player_hp = (player_hp - enemy_dmg)
            await client.send_message(message.channel, '```'+message.author.name+' swings, dealing ' + str(player_dmg) + ' damage.\nThe '+enemy[k]+' swings, dealing '+ str(enemy_dmg) +' damage.```')  
        
            if player_hp <= 0:
                await client.send_message(message.channel, '```The '+enemy[k]+' overpowers '+message.author.name+' and they black out```')

    elif message.content.startswith ('!shop'):
        if message.author not in user_gold:
            user_gold[message.author] = 0
        if message.author not in user_potions:
            user_potion[message.author] = 0
        await client.send_message(message.channel, '```Welcome to the shop!```\nPotion - 5g')
        msg = await client.wait_for_message(author=message.author)
        if msg.content == 'potion' or msg.content == 'Potion':
            if user_gold[message.author]<5:
                await client.send_message(message.channel, 'You don\'t have enough gold to buy this item')
            user_potions[message.author]+=1
            user_gold[message.author]-=5
            await client.send_message(message.channel, '```'+message.author.name+' bought a potion.\nThank you for visiting the shop!```')

    else:
        # general chat ai goes here
        settings = toml.load("volt_settings.toml")
        if settings['pyborg']['learning']:
            # check if we're allowed to learn here
            if message.channel.name not in settings['discord']['ignored_channels']:
                learn(message.content)
        if message.content.startswith("<@{}>".format(client.user.id)):
            clean = clean_msg(message)
            msg = reply(clean)
            logger.debug("on message: %s" % msg)
            if msg:
                logger.debug("Sending message...")
                msg = msg.replace("#nick", str(message.author.mention))
                await client.send_message(message.channel, msg)
#    elif message.content.startswith('!d100'):
#       await User.mention(message.author)
#        yield from client.send_message(message.channel, 'Rolled a ' + random.randint(1,100))


def clean_msg(message):
    return ' '.join(message.content.split()[1:])

if __name__ == '__main__':
    settings = toml.load("volt_settings.toml")
    client.run(settings['token'])
