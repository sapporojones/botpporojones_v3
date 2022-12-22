import datetime as dt
import discord
import praw
import pytz
import random
import requests

from discord.ext import commands
from dotenv import load_dotenv
from os import getenv


# initialize program components
load_dotenv()


# initialize discord components
bot = commands.Bot(command_prefix="!")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


# load env vars
discord_client_token = getenv("DISCORD_CLIENT_TOKEN")
reddit_client_id = getenv("REDDIT_CLIENT_ID")
reddit_client_secret = getenv("REDDIT_CLIENT_SECRET")
reddit_password = getenv("REDDIT_PASSWORD")
reddit_username = getenv("REDDIT_USERNAME")
stockmarket_key = getenv("STOCKMARKET_KEY")


# Reddit oauth initialization
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    password=reddit_password,
    user_agent="testscript by /u/sapporojones",
    username=reddit_username,
)


###########################
# Bot commands below here #
###########################


@bot.command(
    name="sarcasm",
    help="Takes a string of text and converts it to sarcasm text",
)
async def sarcasm(ctx, pre_text):
    post_list = []
    i = 0
    end_text = ""

    for l in pre_text:
        chance = random.randint(1, 100)
        if chance >= 50:
            post_list.append(pre_text[i].upper())
        else:
            post_list.append(pre_text[i].lower())
        i += 1

    for l, x in enumerate(post_list):
        end_text = end_text + x
    await ctx.send(end_text)


@bot.command(name="d100", help="Roll the d100 to determine the fate of the alliance.")
async def d100(ctx):
    roll = str(random.randint(1, 100))
    response = "You rolled a " + roll
    await ctx.send(response)


@bot.command(
    name="d",
    help="Roll the arbitrary sided die because you want to for some reason.",
)
async def d(ctx, en):
    roll = str(random.randint(1, int(en)))
    response = f"You rolled a {roll}"
    await ctx.send(response)


@bot.command(name="f", help="a fortune")
async def f(ctx):
    base_url = "http://yerkee.com/api/fortune"
    fortune_raw = requests.get(base_url)
    fortune_json = fortune_raw.json()
    fortune_text = fortune_json["fortune"]
    await ctx.send(fortune_text)


@bot.command(name="stock", help="stock quote lookup")
async def stock(ctx, ticker):
    query = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={stockmarket_key}"
    json_output = requests.get(query)
    data = json_output.json()
    response = (
        "Here's some information about that security you requested:\n"
        + "The current price is: "
        + data["Global Quote"]["05. price"]
        + "\n"
        + "The current change is: "
        + data["Global Quote"]["09. change"]
        + "\n"
        + "The change percent of that is: "
        + data["Global Quote"]["10. change percent"]
        + "\n"
        + "The security opened at: "
        + data["Global Quote"]["02. open"]
        + "\n"
        + "The security closed last at: "
        + data["Global Quote"]["08. previous close"]
    )
    await ctx.send(response)


@bot.command(name="r", help="returns a random image post from the specified subreddit")
async def r(ctx, sub_reddit):
    random_submission = reddit.subreddit(sub_reddit).random()
    if random_submission.over_18 == True:
        submission_url = "Adult content detected, not posting"
    else:
        submission_url = reddit.submission(random_submission).url
    await ctx.send(submission_url)


@bot.command(name="rnew", help="returns a new image post from the specified subreddit")
async def rnew(ctx, sub_reddit):
    random_submission = reddit.subreddit(sub_reddit).new(limit=1)
    x = []
    for id in random_submission:
        x.append(id.url)
    y = x[0]
    await ctx.send(y)


@bot.command(name="time", help="current time for a variety of timezones")
async def time(ctx):
    tz_london = pytz.timezone("Europe/London")
    tz_moscow = pytz.timezone("Europe/Moscow")
    tz_pac = pytz.timezone("America/Los_Angeles")
    tz_mtn = pytz.timezone("America/Denver")
    tz_cnt = pytz.timezone("America/Mexico_City")
    tz_est = pytz.timezone("America/New_York")
    tz_sydney = pytz.timezone("Australia/Sydney")

    now_obj = dt.datetime.now(pytz.utc)
    uk_obj = now_obj.astimezone(tz_london)
    rus_obj = now_obj.astimezone(tz_moscow)
    pac_obj = now_obj.astimezone(tz_pac)
    mtn_obj = now_obj.astimezone(tz_mtn)
    cnt_obj = now_obj.astimezone(tz_cnt)
    est_obj = now_obj.astimezone(tz_est)
    autz_obj = now_obj.astimezone(tz_sydney)

    l1 = f"\n **The Current Time Is:** \n"
    l2 = f"**Pacific (USTZ):** {str(pac_obj)[11:16]} \n"
    l3 = f"**Mountain (USTZ):** {str(mtn_obj)[11:16]} \n"
    l4 = f"**Central (USTZ):** {str(cnt_obj)[11:16]} \n"
    l5 = f"**Eastern (USTZ):** {str(est_obj)[11:16]} \n"
    l6 = f"**London:(GMT)** {str(uk_obj)[11:16]} \n"
    l7 = f"**Moscow (RUTZ):** {str(rus_obj)[11:16]} \n"
    l8 = f"**Sydney (AUTZ):** {str(autz_obj)[11:16]} \n"
    l9 = f"**EVE Time (UTC):** {str(now_obj)[11:16]} \n"

    response = l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9

    await ctx.send(response)


@bot.command(name="pilot", help="get various urls about a given pilot name")
async def pilot(ctx, character_name):
    data = f'["{character_name}"]'
    char_search = requests.post(
        "https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en",
        data,
    )
    char_search_json = char_search.json()
    if len(char_search_json) <= 0:
        response = "Character not found, verify spelling and try again."
    else:
        char_id = char_search_json["character"][0]

        character_id = str(char_id)
        line1 = f"\n **PILOT SEARCH RESULTS:** \n"
        line2 = f"**ZKB:** https://zkillboard.com/character/{character_id}/\n"
        line3 = f"**EVEWHO:** https://evewho.com/character/{character_id}/\n"
        line4 = f"**TEST Auth:** https://auth.pleaseignore.com/eve/character/{character_id}/\n"

        response = line1 + line2 + line3 + line4

    await ctx.send(response)


@bot.command(name="corp", help="get various urls about a given eve corporation")
async def corp(ctx, corp_name):
    data = f'["{corp_name}"]'
    corp_search = requests.post(
        "https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en",
        data,
    )
    corp_search_json = corp_search.json()
    if len(corp_search_json) <= 0:
        response = "Character not found"
    else:
        corp_id = corp_search_json["corporation"][0]

        corp_id = str(corp_id)
        line1 = f"\n **PILOT SEARCH RESULTS:** \n"
        line2 = f"**ZKB:** https://zkillboard.com/corporation/{corp_id}/\n"
        line3 = f"**EVEWHO:** https://evewho.com/corporation/{corp_id}/\n"
        line4 = f"**DOTLAN:** http://evemaps.dotlan.net/corp/{corp_id}/\n"

        response = line1 + line2 + line3 + line4

    await ctx.send(response)


@bot.command(name="alice", help="get various urls about a given alliance")
async def corp(ctx, alice_name):
    data = f'["{alice_name}"]'
    alice_search = requests.post(
        "https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en",
        data,
    )
    alice_search_json = alice_search.json()
    if len(alice_search_json) <= 0:
        response = "Character not found"
    else:
        alice_id = alice_search_json["corporation"][0]

        alice_id = str(alice_id)
        line1 = f"\n **PILOT SEARCH RESULTS:** \n"
        line2 = f"**ZKB:** https://zkillboard.com/alliance/{alice_id}/\n"
        line3 = f"**EVEWHO:** https://evewho.com/alliance/{alice_id}/\n"
        line4 = f"**DOTLAN:** http://evemaps.dotlan.net/alliance/{alice_id}/\n"

        response = line1 + line2 + line3 + line4

    await ctx.send(response)


#####################################
# Nothing below here but client.run #
#####################################
client.run(discord_client_token)
