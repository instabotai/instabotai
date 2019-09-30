import argparse
import threading
import os
from multiprocessing import Pool
import sys
import time
import random
sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot
from instabotai import ai

try:
    input = raw_input
except NameError:
    pass


COOKIES = {}
bot = ai.Bot(do_logout=True)

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()
username = str(args.u)


# Check if user cookie exist
bot.login(username=args.u, password=args.p, proxy=args.proxy, use_cookie=True)

def comment_user():
    ai.Bots.user_hashtag_comment("fitness, models, friends", "wow please follow me back", 10)

def like_hashtags():
    ai.Bots.like_hashtags("model", 4)
#ai.Bots.like_following("japanheaven", 20)
#ai.Bots.like_followers("japanheaven", 20)
#ai.Bots.repost_users_images("japanheaven, timferris, ariana, sjaaybee", "#models", 10)



thread1 = threading.Timer(5.0, comment_user)
thread2 = threading.Timer(3.0, like_hashtags)
#thread3 = threading.Timer(7.0, reply_messages)
#thread4 = threading.Timer(10.0, reply_pending_messages)
thread1.start()
thread2.start()
#thread3.start()
#thread4.start()

