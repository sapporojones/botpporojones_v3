import datetime as dt
import praw
import pytz
import random
import requests

from dotenv import load_dotenv
from os import getenv

# initialize program components
load_dotenv()


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

sarcasm_pre_text = "hello world!"


# sarcasm test
def test_sarcasm():
    sarcasm_pre_text = "hello world!"
    post_list = []
    i = 0
    end_text = ""

    for l in sarcasm_pre_text:
        chance = random.randint(1, 100)
        if chance >= 50:
            post_list.append(sarcasm_pre_text[i].upper())
        else:
            post_list.append(sarcasm_pre_text[i].lower())
        i += 1

    for l, x in enumerate(post_list):
        end_text = end_text + x

    assert len(end_text) > 0


def test_d100():
    roll = str(random.randint(1, 100))
    response = "You rolled a " + roll
    assert int(roll) >= 1


def test_d():
    en = 100
    roll = str(random.randint(1, int(en)))
    response = f"You rolled a {roll}"
    assert int(roll)
    assert int(roll) >= 1


def test_f():
    base_url = "http://yerkee.com/api/fortune"
    fortune_raw = requests.get(base_url)
    fortune_json = fortune_raw.json()
    fortune_text = fortune_json["fortune"]
    assert len(fortune_text) > 0
    assert fortune_raw.status_code == 200


def test_stock():
    ticker = 'INTC'
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
    assert len(response) > 0
    assert json_output.status_code == 200


def test_r():
    sub_reddit = "subaru"
    random_submission = reddit.subreddit(sub_reddit).random()
    if random_submission.over_18 == True:
        submission_url = "Adult content detected, not posting"
    else:
        submission_url = reddit.submission(random_submission).url
    assert submission_url[:4] == 'http'


def test_rnew():
    sub_reddit = 'subaru'
    random_submission = reddit.subreddit(sub_reddit).new(limit=1)
    x = []
    for id in random_submission:
        x.append(id.url)
    y = x[0]
    assert y[:4] == 'http'


def test_time():
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

    assert str(pac_obj)[11:16][2] == ':'


def test_pilot():
    character_name = 'Sapporo Jones'
    data = f'["{character_name}"]'
    char_search = requests.post(
        "https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en",
        data,
    )
    char_search_json = char_search.json()
    if len(char_search_json) <= 0:
        response = "Character not found, verify spelling and try again."
    else:
        # char_id = char_search_json["character"][0]
        char_id = char_search_json["characters"][0]["id"]

        character_id = str(char_id)
        line1 = f"\n **PILOT SEARCH RESULTS:** \n"
        line2 = f"**ZKB:** https://zkillboard.com/character/{character_id}/\n"
        line3 = f"**EVEWHO:** https://evewho.com/character/{character_id}/\n"
        line4 = f"**TEST Auth:** https://auth.pleaseignore.com/eve/character/{character_id}/\n"

        response = line1 + line2 + line3 + line4

    assert character_id == '772506501'


def test_corp():
    corp_name = 'The Subaru Legacy'
    data = f'["{corp_name}"]'
    corp_search = requests.post(
        "https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en",
        data,
    )
    corp_search_json = corp_search.json()
    if len(corp_search_json) <= 0:
        response = "Character not found"
    else:
        corp_id = corp_search_json["corporations"][0]["id"]

        corp_id = str(corp_id)
        line1 = f"\n **PILOT SEARCH RESULTS:** \n"
        line2 = f"**ZKB:** https://zkillboard.com/corporation/{corp_id}/\n"
        line3 = f"**EVEWHO:** https://evewho.com/corporation/{corp_id}/\n"
        line4 = f"**DOTLAN:** http://evemaps.dotlan.net/corp/{corp_id}/\n"

        response = line1 + line2 + line3 + line4

    assert corp_id == '98440609'


def test_alice():
    alice_name = "Test Alliance Please Ignore"
    data = f'["{alice_name}"]'
    alice_search = requests.post(
        "https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en",
        data,
    )
    alice_search_json = alice_search.json()
    if len(alice_search_json) <= 0:
        response = "Character not found"
    else:
        alice_id = alice_search_json["alliances"][0]["id"]

        alice_id = str(alice_id)
        line1 = f"\n **PILOT SEARCH RESULTS:** \n"
        line2 = f"**ZKB:** https://zkillboard.com/alliance/{alice_id}/\n"
        line3 = f"**EVEWHO:** https://evewho.com/alliance/{alice_id}/\n"
        line4 = f"**DOTLAN:** http://evemaps.dotlan.net/alliance/{alice_id}/\n"

        response = line1 + line2 + line3 + line4
    assert alice_id == '498125261'