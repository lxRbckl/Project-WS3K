# WS3K by Alex Arbuckle #


# Import <
from json import load, dump
from discord import Intents
from selenium import webdriver
from time import sleep as timeSleep
from discord.ext.commands import Bot
from asyncio import sleep as asyncioSleep
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# >


# Declaration <
WS3K = Bot(command_prefix = '', intents = Intents.all())
username, password = '', ''
token = ''

# >


async def jsonLoad():
    '''  '''

    with open('WS3K.json', 'r') as fileVariable:

        return load(fileVariable)


async def jsonDump(arg):
    ''' arg : dict '''

    with open('WS3K.json', 'w') as fileVariable:

        dump(arg, fileVariable, indent = 4)


@WS3K.event
async def on_ready():
    '''  '''

    # Webdriver <
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)

    # >

    # Logging In <
    setting = await jsonLoad()

    driver.get('https://discord.com/login'), timeSleep(1)
    driver.find_element_by_xpath(setting['usernamePath']).send_keys(username), timeSleep(0.2)
    driver.find_element_by_xpath(setting['passwordPath']).send_keys(password), timeSleep(0.2)
    driver.find_element_by_xpath(setting['loginPath']).click(), timeSleep(5)

    # >

    # Algorithm <
    while (True):

        setting = await jsonLoad()
        for channel in setting['channel']:

            try:

                driver.get(channel), timeSleep(1)
                driver.find_element_by_xpath(setting['checkPath'])

                await WS3K.get_user(setting['authorId']).send(':bell: {}'.format(channel))
                await asyncioSleep(setting['alertRate'])

            except Exception as e:

                print(e)
                await asyncioSleep(setting['sleepRate'])

        await asyncioSleep(setting['sleepRate'])

    # >


@WS3K.command(aliases = ['add', 'Add'])
async def addChannel(ctx, arg):
    '''  '''

    dictVariable = await jsonLoad()

    if (arg not in dictVariable['channel']):

        dictVariable['channel'].append(arg)

        await jsonDump(dictVariable)
        await ctx.channel.send(f'Channel {arg} was added.', delete_after = 60)

    else:

        await ctx.channel.send(f'Channel {arg} already exists.', delete_after = 60)


@WS3K.command(aliases = ['remove', 'Remove'])
async def removeChannel(ctx, arg):
    '''  '''

    dictVariable = await jsonLoad()

    if (arg in dictVariable['channel']):

        dictVariable['channel'].remove(arg)

        await jsonDump(dictVariable)
        await ctx.channel.send(f'Channel {arg} was removed.', delete_after = 60)

    else:

        await ctx.channel.send(f'Channel {arg} does not exist.', delete_after = 60)


@WS3K.command(aliases = ['show', 'Show'])
async def showChannel(ctx):
    '''  '''

    dictVariable = await jsonLoad()
    strVariable = ''.join(f'{i}\n' for i in dictVariable['channel'])

    await ctx.channel.send(strVariable, delete_after = 60)


WS3K.run(token)
