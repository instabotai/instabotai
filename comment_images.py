from instabotai import ai
import argparse

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
parser.add_argument('-comment', type=str, help="comment")
parser.add_argument('-sleep', type=int, help="sleep")


args = parser.parse_args()
username = str(args.u)
user = str(args.user)

print(user)
# Login
ai.Bots.user_login(args.u, args.p)
#bot.login(username=args.u, password=args.p, proxy=args.proxy, use_cookie=True)
#ai.Bots.follow_users_hashtag_ai("fitness, programming", 45)
#ai.Bots.watch_stories(args.user, args.sleep)
#ai.Bots.follow_users_followers_ai(args.user, args.sleep)
#ai.Bots.follow_users_following_ai(args.user, args.sleep)
#ai.Bots.follow_users_ai("japanheaven", 40)
ai.Bots.user_hashtag_comment(args.u, args.comment, args.sleep)
#ai.Bots.user_hashtag_comment("fitness, models, friends", "wow please follow me back, wow nice profile, awesome profile", 40)
#ai.Bots.like_hashtags("model", 45)
#ai.Bots.like_following(user, args.sleep)
#ai.Bots.like_followers("japanheaven", 40)
#ai.Bots.repost_users_images("japanheaven, timferris, ariana, sjaaybee", "#models", 40)
