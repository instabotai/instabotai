from instabotai import ai
import argparse
from multiprocessing import Process, Queue

try:
    input = raw_input
except NameError:
    pass


COOKIES = {}
bot = ai.Bot(do_logout=True)

# Parse info from terminal
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('-user', type=str, help="user")
parser.add_argument('-sleep', type=int, help="sleep")
args = parser.parse_args()



username = str(args.u)
user = str(args.user)
ai.Bots.user_login(args.u, args.p)
ai.bot.api.get_self_username_info()
profilepic = ai.bot.api.last_json["user"]["profile_pic_url"]
followers_count = ai.bot.api.last_json["user"]["follower_count"]
following_count = ai.bot.api.last_json["user"]["following_count"]
media_count = ai.bot.api.last_json["user"]["media_count"]

def write_file(filename, text):
    with open(username + filename + ".txt", "w+") as f:
        f.write(text)
write_file("profilepic", str(profilepic))
write_file("followers_count", str(followers_count))
write_file("following_count", str(following_count))
write_file("media_count", str(media_count))



# Login
#bot.login(username=args.u, password=args.p, proxy=args.proxy, use_cookie=True)
#ai.Bots.follow_users_hashtag_ai("fitness, programming", 45)
#ai.Bots.follow_users_following_ai(args.user, args.sleep)
#ai.Bots.follow_users_ai("japanheaven", 40)
#ai.Bots.user_hashtag_comment("fitness, models, friends", "wow please follow me back, wow nice profile, awesome profile", 40)
#ai.Bots.like_hashtags("model", 45)
#ai.Bots.repost_users_images("japanheaven, timferris, ariana, sjaaybee", "#models", 40)
