"""
    Watch user likers stories!
    This script could be very useful to attract
    someone's audience to your account.
    
    Dependencies:
        pip install -U instabot
    Run:
      python watch_stories.py -u username -p password

    Change user to scrape:
    Change line 35 in this file.

    Notes:
        You can change file and add there your comments.
"""

import os
import sys
import time
import random
import argparse
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

# in case if you just downloaded zip with sources
sys.path.append(os.path.join(sys.path[0], '../../'))


bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)


if len(sys.argv) >= 10:
    bot.logger.info(
        """
            Going to get '%s' likers and watch their stories
            (and stories of their likers too).
        """ % (sys.argv[1])
    )
    user_to_get_likers_of = bot.convert_to_user_id(sys.argv[1])
else:
    bot.logger.info(
        """
            Going to get your likers and watch their stories
            (and stories of their likers too).
            You can specify username of another user to start
            (by default we use you as a starting point).
        """
    )
    user_to_get_likers_of = bot.get_user_id_from_username("maskofshiva")

current_user_id = user_to_get_likers_of
total_stories = 0
error_sleep = 0
error_sleeps = 0

while True:
    try:
        # GET USER FEED
        if not bot.api.get_user_feed(current_user_id):
            print("Can't get feed of user_id=%s" % current_user_id)

        # GET MEDIA LIKERS
        user_media = random.choice(bot.api.last_json["items"])
        if not bot.api.get_media_likers(media_id=user_media["pk"]):
            print(
                "Can't get media likers of media_id='%s' by user_id='%s'"
                % (user_media["pk"], current_user_id)
            )
        likers = bot.api.last_json["users"]
        liker_ids = [
            str(u["pk"]) for u in likers if not u["is_private"] and "latest_reel_media" in u
        ][:20]

        # WATCH USERS STORIES
        if bot.watch_users_reels(liker_ids):
            bot.logger.info("Total stories viewed: %d" % bot.total["stories_viewed"])
            error_sleep = 0
            error_sleeps = 0
            if bot.total["stories_viewed"] > 1900:
                total_stories += 2000
                print("Total stories watched " + str(total_stories))
                bot.total["stories_viewed"] = 0
                print("sleeping for 310 sec")
                time.sleep(310 + random.random())

    # CHOOSE RANDOM LIKER TO GRAB HIS LIKERS AND REPEAT
        current_user_id = random.choice(liker_ids)
        if random.random() < 0.05:
            current_user_id = user_to_get_likers_of
            bot.logger.info("Sleeping and returning back to original user_id=%s"% current_user_id)
            time.sleep(3 * random.random() + 1)
            error_sleep += 1
            if error_sleep == 3:
                print("sleeping for 1780 seconds")
                time.sleep(1780 + random.random())

    except Exception as e:
        # If something went wrong - sleep long and start again
        bot.logger.info(e)
        error_sleeps += 1
        if error_sleeps == 2:
            print("sleeping for 1780 seconds")
            time.sleep(1780 + random.random())

        current_user_id = user_to_get_likers_of
        time.sleep(5 * random.random() + 5)
