import os
from instabot import Bot
import argparse
import time
#import threading
import random
import sys, stat
from mtcnn.mtcnn import MTCNN
import cv2
import random
import shutil

try:
    input = raw_input
except NameError:
    pass

COOKIES = {}
bot = Bot(do_logout=True)

class Bots(object):
    def __init__(self):
        self.points = 1000

    def watch_stories(username, time_sleep):
        Bots.save_user_info(ig_username, "Starting story viewer")
        user_to_get_likers_of = bot.get_user_id_from_username(username)
        time_sleep = int(time_sleep)
        current_user_id = user_to_get_likers_of
        total_stories = 0
        error_sleep = 0
        error_sleeps = 0

        while True:
            try:
                # GET USER FEED
                if not bot.api.get_user_feed(current_user_id):
                    print("Can't get feed of user_id=%s" % current_user_id)
                    Bots.save_user_info(ig_username, "Can't get feed of user_id=%s" % current_user_id)


                # GET MEDIA LIKERS
                user_media = random.choice(bot.api.last_json["items"])
                if not bot.api.get_media_likers(media_id=user_media["pk"]):
                    Bots.save_user_info(ig_username,
                        "Can't get media likers of media_id='%s' by user_id='%s'"
                        % (user_media["pk"], current_user_id)
                    )
                likers = bot.api.last_json["users"]
                liker_ids = [
                    str(u["pk"]) for u in likers if not u["is_private"] and "latest_reel_media" in u
                ][:20]

                # WATCH USERS STORIES
                if bot.watch_users_reels(liker_ids):
                    time.sleep(time_sleep)
                    Bots.save_user_info(ig_username, "sleeping for " + str(time_sleep) + " seconds")
                    bot.logger.info("Total stories viewed: %d" % bot.total["stories_viewed"])
                    Bots.save_user_info(ig_username, "Total stories viewed: %d" % bot.total["stories_viewed"])
                    error_sleep = 0
                    error_sleeps = 0
                    if bot.total["stories_viewed"] > 1900:
                        total_stories += 2000
                        Bots.save_user_info(ig_username, "Total stories watched " + str(total_stories))
                        print("Total stories watched " + str(total_stories))
                        bot.total["stories_viewed"] = 0
                        print("sleeping for 420 sec")
                        Bots.save_user_info(ig_username, "sleeping for 420 sec")
                        Bots.payment_system()
                        time.sleep(420 + random.random())
                    if total_stories > 19000:
                        time.sleep(500)
                        Bots.save_user_info(ig_username, "sleeping for 500 seconds")

            # CHOOSE RANDOM LIKER TO GRAB HIS LIKERS AND REPEAT
                current_user_id = random.choice(liker_ids)
                if random.random() < 0.05:
                    time.sleep(1)
                    current_user_id = user_to_get_likers_of
                    bot.logger.info("Sleeping and returning back to original user_id=%s"% current_user_id)
                    Bots.save_user_info(ig_username, "Sleeping and returning back to original user_id=%s"% current_user_id)
                    time.sleep(10 * random.random() + 1)
                    error_sleep += 1
                    if error_sleep == 2:
                        error_sleep = 0
                        print("sleeping for 1640 seconds")
                        Bots.save_user_info(ig_username, "sleeping for 320 seconds")
                        time.sleep(16 + random.random())

            except Exception as e:
                # If something went wrong - sleep long and start again
                bot.logger.info(e)
                error_sleeps += 1
                if error_sleeps == 50:
                    bot.logger.info("sleeping for 310 seconds")
                    Bots.save_user_info(ig_username, "sleeping for 310 seconds")
                    time.sleep(312 + random.random())
                Bots.change_password_on_block()
                print(bot.api.total_challenge)
                current_user_id = user_to_get_likers_of
                time.sleep(20 * random.random() + 5)

    def change_password_on_block():
        with open(ig_username + "check_blocked.txt", "w+") as f:
            blocked = f.read()
            blocked = str(blocked)
            if blocked == "3":
                Bots.save_user_info(ig_username, "Change password")
                bot.logger.info("password changed")
                x = random.randrange(1, 3)
                new_password = ig_password + str(x)
                bot.api.change_password(new_password)
                bot.logger.info("logged in")
                bot.api.login(username="japanheaven", password=new_password)
                blocked = f.write("0")

    def save_user_info(username, logoutput):
        global ig_username
        ig_username = username
        with open("static/" + username + 'info.txt', 'a+')as f:
            s = f.read()
            f.seek(0)
            f.write(logoutput + "<hr>\n" + s)

    def user_login(username=None, password=None, proxys=None):
        username = username
        global ig_password
        ig_password = password
        proxys = None
        bot.api.login(username=username, password=password, proxy=proxys, use_cookie=True, is_threaded=True)
        Bots.save_user_info(username, "logged in as " + username)

    def face_detection(username):
        x = 0
        ''' Get user media and scan it for a face'''
        user_id = bot.get_user_id_from_username(username)
        medias = bot.get_user_medias(user_id, filtration=False)
        for media in medias:
            while x < 1:
                try:
                    bot.logger.info(media)
                    path = bot.download_photo(media, folder=username)
                    img = cv2.imread(path)
                    detector = MTCNN()
                    detect = detector.detect_faces(img)
                    if not detect:
                        Bots.save_user_info(ig_username, "no face detected " + bot.get_link_from_media_id(media))
                        bot.logger.info("save user info")
                        bot.logger.info("no face detected " + bot.get_link_from_media_id(media))
                        x += 1

                    elif detect:
                        Bots.save_user_info(ig_username, "there was a face detected")
                        bot.logger.info("save user info")
                        bot.logger.info("there was a face detected")
                        bot.api.like(media)
                        display_url = bot.get_link_from_media_id(media)
                        bot.logger.info("liked " + display_url + " by " + username)
                        Bots.save_user_info(ig_username, "liked " + display_url + " by " + username)
                        Bots.payment_system()
                        x += 1
                    else:
                        x += 1

                except Exception as e:
                    Bots.save_user_info(ig_username, str(e))
                    bot.logger.info(e)
                    x += 1
            shutil.rmtree(username, ignore_errors=True) # Remove dir username after scanning


    def face_detection_repost(username, caption):
        x = 0
        ''' Get user media and scan it for a face'''
        user_id = bot.get_user_id_from_username(username)
        medias = bot.get_user_medias(user_id, filtration=False)
        for media in medias:
            while x < 1:
                try:
                    bot.logger.info(media)
                    path = bot.download_photo(media, folder=username)
                    img = cv2.imread(path)
                    detector = MTCNN()
                    detect = detector.detect_faces(img)
                    if not detect:
                        bot.logger.info("no face detected " + bot.get_link_from_media_id(media))
                        Bots.save_user_info(ig_username, "no face detected " + bot.get_link_from_media_id(media))
                        x += 1

                    elif detect:
                        bot.logger.info("there was a face detected")
                        Bots.save_user_info(ig_username, "==> There was a face detected! <==")
                        bot.api.upload_photo(path, caption=caption)
                        does_exist = bot.get_media_comments(media, only_text=True)
                        if str(username) in does_exist:
                            x += 1
                            print("image has been commented")
                        else:
                            display_url = bot.get_link_from_media_id(media)
                            bot.logger.info("reposted " + display_url + " by " + username)
                            Bots.save_user_info(ig_username, "reposted " + display_url + " by " + username)
                            Bots.payment_system()
                            x += 1
                    else:
                        x += 1

                except Exception as e:
                    bot.logger.info(e)
                    x += 1
                    Bots.save_user_info(ig_username, str(e))
            shutil.rmtree(username, ignore_errors=True) # Remove dir username after scanning

    def face_detection_follow(username):
        Bots.save_user_info(ig_username, "No Worries pls wait 10-120 seconds")
        x = 0
        ''' Get user media and scan it for a face'''
        user_id = bot.get_user_id_from_username(username)
        medias = bot.get_user_medias(user_id, filtration=False)
        for media in medias:
            while x < 1:
                try:
                    bot.logger.info(media)
                    path = bot.download_photo(media, folder=username)
                    img = cv2.imread(path)
                    detector = MTCNN()
                    detect = detector.detect_faces(img)
                    if not detect:
                        bot.logger.info("no face detected " + bot.get_link_from_media_id(media))
                        Bots.save_user_info(ig_username, "no face detected " + bot.get_link_from_media_id(media))

                        x += 1

                    elif detect:
                        bot.logger.info("there was a face detected")
                        Bots.save_user_info(ig_username, "there was a face detected")

                        bot.api.follow(user_id)
                        does_exist = bot.get_media_comments(media, only_text=True)
                        if str(username) in does_exist:
                            x += 1
                            bot.logger.info("user has been followed")
                        else:
                            display_url = bot.get_link_from_media_id(media)
                            Bots.save_user_info(ig_username, "followed " +  username)
                            bot.logger.info("followed " +  username)
                            Bots.payment_system()
                            x += 1
                    else:
                        x += 1

                except Exception as e:
                    bot.logger.info(e)
                    x += 1
                    Bots.save_user_info(ig_username, str(e))
            shutil.rmtree(username, ignore_errors=True) # Remove dir username after scanning

    def face_detection_comment(username, comment):
        x = 0
        ''' Get user media and scan it for a face'''
        user_id = bot.get_user_id_from_username(username)
        medias = bot.get_user_medias(user_id, filtration=False)
        for media in medias:
            while x < 1:
                try:
                    bot.logger.info(media)
                    path = bot.download_photo(media, folder=username)
                    img = cv2.imread(path)
                    detector = MTCNN()
                    detect = detector.detect_faces(img)
                    if not detect:
                        bot.logger.info("no face detected " + bot.get_link_from_media_id(media))
                        Bots.save_user_info(ig_username, "no face detected " + bot.get_link_from_media_id(media))
                        x += 1

                    elif detect:
                        comment = Bots.convert_usernames_to_list(comment)
                        comment = random.choice(comment)
                        bot.logger.info("there was a face detected")
                        Bots.save_user_info(ig_username, "there was a face detected")

                        bot.api.comment(media, comment)
                        does_exist = bot.get_media_comments(media, only_text=True)
                        if str(username) in does_exist:
                            x += 1
                            print("image has been commented")
                        else:
                            display_url = bot.get_link_from_media_id(media)
                            bot.logger.info("commented " + display_url + " by " + username)
                            Bots.save_user_info(ig_username, "commented " + display_url + " by " + username)
                            Bots.payment_system()
                            x += 1
                    else:
                        x += 1

                except Exception as e:
                    Bots.save_user_info(ig_username, "wait 1 min")
                    bot.logger.info(e)
                    x += 1
            shutil.rmtree(username, ignore_errors=True) # Remove dir username after scanning

    def like_followers(username, time_sleep):
        Bots.save_user_info(ig_username, "Scraping users pls wait 2-4 min")
        time.sleep(60)
        user_id = bot.get_user_id_from_username(username)
        followers = bot.get_user_followers(user_id, nfollows=6000)

        for user in followers:
            pusername = bot.get_username_from_user_id(user)
            Bots.face_detection(pusername)
            time.sleep(int(time_sleep))


    def like_following(username, time_sleep):
        Bots.save_user_info(ig_username, "Scraping users pls wait 2-4 min")
        time.sleep(60)
        user_id = bot.get_user_id_from_username(username)
        following = bot.get_user_following(user_id)

        for user in following:
            pusername = bot.get_username_from_user_id(user)
            Bots.face_detection(pusername)
            time.sleep(int(time_sleep))

    def like_hashtags(hashtag, time_sleep):
        '''
        like hashtags
        @params: hashtag (string),
        @params: time_sleep (int),
        '''
        Bots.save_user_info(ig_username, "Scraping users pls wait 2-4 min")
        time.sleep(60)
        hashtags = bot.get_hashtag_users(hashtag)
        while True:
            hashtags = Bots.convert_usernames_to_list(hashtag)
            for hashtag in hashtags:
                hashtags = bot.get_hashtag_users(hashtag)
                bot.logger.info("Hashtag selected: " + hashtag)
                for user in hashtags:
                    pusername = bot.get_username_from_user_id(user)
                    Bots.face_detection(pusername)
                    time.sleep(int(time_sleep))

    def user_hashtag_comment(hashtag, comment, time_sleep):
        '''
        comment a user hashtags
        @params: hashtag (string),
        @params: comment (sting),
        @params: time_sleep (int),
        '''
        while True:
            hashtags = Bots.convert_usernames_to_list(hashtag)
            for hashtag in hashtags:
                hashtags = bot.get_hashtag_users(hashtag)
                bot.logger.info("Hashtag selected: " + hashtag)
                for user in hashtags:
                    pusername = bot.get_username_from_user_id(user)
                    Bots.face_detection_comment(pusername, comment)
                    time.sleep(int(time_sleep))

    def media_hashtag_comment(hashtags, comment, time_sleep):
        '''
        comment a media hashtags
        @params: hashtags (string),
        @params: comment[sting),
        @params: time_sleep(int),
        '''
        Bots.save_user_info(ig_username, "Scraping users pls wait 2-4 min")
        while True:
            hashtags = Bots.convert_usernames_to_list(hashtags)
            for hashtag in hashtags:
                hashtags = bot.get_total_hashtag_medias(hashtag)
                for user in hashtags:
                    pusername = bot.get_username_from_user_id(user)
                    Bots.face_detection_comment(pusername, comment)
                    time.sleep(int(time_sleep))

    def unfollow_users():
        bot.unfollow_everyone()

    def unfollow_non_followers():
        bot.unfollow_non_followers()

    def convert_usernames_to_list(usernames):
        newlist = []
        ''' convert usernames or hashtags to a list '''
        try:
            for username in usernames.split(", "):
                newlist.append(username)
            list_usernames = newlist

        except:
            for username in usernames.split(","):
                newlist.append(username)
            list_usernames = newlist

        else:
            usernames = list_usernames
        return list_usernames

    def repost_users_images(usernames, caption, time_sleep):
        '''
        get users images and repost them
        @params: usernames (string),
        @params: caption (sting),
        @params: time_sleep(int),
        '''
        print(usernames)
        Usernames = Bots.convert_usernames_to_list(usernames)
        print(Usernames)
        for username in Usernames:
            Bots.face_detection_repost(username, caption)
            time.sleep(time_sleep)

    def get_points():
        try:
            points = open(ig_username + "x.txt", "r")
            print("points")
            output = points.read()
            points.close()
            points = output
            if not points:
                Bots.stop()
            return points
        except:
            points = open(ig_username + "x.txt", "w")
            os.chmod(ig_username + "x.txt", 0o777)


            points.write("50")
            print("points")
            output = points.read()
            points.close()
            points = output
            return points


    def stop():
        print("Buy 20.000 more COINS send 0.001 BTC to 12R5b4rLyNL8cC2HYQi5NpdPNaaAxPnmfe")
        print("To get key when bought talk to us here: https://web.telegram.org/#/im?p=@instabotai")
        exit()

    def payment_system():
        points = Bots.get_points()
        print("You Have :" + str(points) + " coins left")
        Bots.save_user_info(ig_username, "You Have :" + str(points) + " coins left")
        increase = open(ig_username + "x.txt", "w+")
        points = int(points)
        points -= 1
        if points < 0:
            increase.write("0")
            print("Buy More Coins Here https://www.patreon.com/instabotai")
            Bots.save_user_info(ig_username, "Buy for 1 month for only $29 with unlimited tasks <a href='https://www.fiverr.com/hourapp/manage-your-instagram-account-with-ai'> Here!</a>")
            print("To get key when bought talk to us here: https://web.telegram.org/#/im?p=@instabotai")
            Bots.stop()
        increase.write(str(points))
        increase.close()
        print("=" * 30)
        Bots.save_user_info(ig_username, "=" * 30)
        Bots.save_user_info(ig_username, "Buy 1 month for only $29 with unlimited tasks<a href='https://www.fiverr.com/hourapp/manage-your-instagram-account-with-ai' target='_blank'> Here!</a>")
        print("Buy 20.000 more COINS send 0.001 BTC to 12R5b4rLyNL8cC2HYQi5NpdPNaaAxPnmfe")
        print("To get key when bought talk to us here: https://web.telegram.org/#/im?p=@instabotai")
        Bots.save_user_info(ig_username, "For support talk to us here: <a href='https://web.telegram.org/#/im?p=@instabotai' target='_blank'> Here!</a>")


    def activate_code(code):
        if code == "AAAEASDCCF" :
            points = Bots.get_points()
            points += 1000
            print("You have activated your code")
        elif code == "BBBSDRGTY" :
            points = Bots.get_points()
            points += 1000
            print("You have activated your code")
        elif code == "CCCAASDRT" :
            points = Bots.get_points()
            points = int(points)
            points = points + 1000
            points = str(points)
            print(points)
            with open(ig_username + "x.txt", "w+") as f:
                f.write(points)
            print("You have activated your code")
        else:
            print("wrong code")

    def follow_users_following_ai(username, time_sleep):
        Bots.save_user_info(ig_username, "Scraping users pls wait 2-4 min")
        while True:
            try:
                username = Bots.convert_usernames_to_list(username)
                for user in username:
                    user_id = bot.get_user_id_from_username(user)
                    followings = bot.get_user_following(user_id, nfollows=2000)
                    for user_id in followings:
                        username = bot.get_username_from_user_id(user_id)
                        Bots.face_detection_follow(username)
                        time_sleep = int(time_sleep)
                        time.sleep(time_sleep)
            except:
                user_id = bot.get_user_id_from_username(username)
                followings = bot.get_user_following(user_id, nfollows=2000)
                for user_id in followings:
                    username = bot.get_username_from_user_id(user_id)
                    Bots.face_detection_follow(username)
                    time_sleep = int(time_sleep)
                    time.sleep(time_sleep)


    def follow_users_followers_ai(username, time_sleep):
        Bots.save_user_info(ig_username, "Scraping users pls wait 2-4 min")
        while True:
            try:
                username = Bots.convert_usernames_to_list(username)
                for user in username:
                    user_id = bot.get_user_id_from_username(user)
                    followers = bot.get_user_followers(user_id, nfollows=2000)
                    for user_id in followers:
                        username = bot.get_username_from_user_id(user_id)
                        Bots.face_detection_follow(username)
                        time_sleep = int(time_sleep)
                        time.sleep(time_sleep)
            except:
                user_id = bot.get_user_id_from_username(username)
                followers = bot.get_user_followers(user_id, nfollows=2000)
                for user_id in followers:
                    username = bot.get_username_from_user_id(user_id)
                    Bots.face_detection_follow(username)
                    time_sleep = int(time_sleep)
                    time.sleep(time_sleep)


    def follow_users_hashtag_ai(hashtag, time_sleep):
        Bots.save_user_info(ig_username, "Scraping users pls wait 2-4 min")
        while True:
            hashtags = Bots.convert_usernames_to_list(hashtag)
            for hashtag in hashtags:
                hashtags = bot.get_hashtag_users(hashtag)
                for user in hashtags:
                    username = bot.get_username_from_user_id(user)
                    Bots.face_detection_follow(username)
                    time.sleep(time_sleep)
