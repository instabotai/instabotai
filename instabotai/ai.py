import os
from instabot import Bot
import argparse
import time
import threading
import random
import sys
from mtcnn.mtcnn import MTCNN
import cv2
import json
import random
import logging

try:
    input = raw_input
except NameError:
    pass

COOKIES = {}
bot = Bot(do_logout=True)

class Bots(object):
    def __init__(self):
        self.points = 1000

    def user_login(username, password):
        bot.api.login(username=username, password=password, proxy=None, use_cookie=True, is_threaded=True)

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
                        bot.logger.info("no face detected " + bot.get_link_from_media_id(media))
                        x += 1

                    elif detect:
                        bot.logger.info("there was a face detected")
                        bot.api.like(media)
                        display_url = bot.get_link_from_media_id(media)
                        bot.logger.info("liked " + display_url + " by " + username)
                        Bots.payment_system()
                        x += 1
                    else:
                        x += 1

                except Exception as e:
                    bot.logger.info(e)
                    x += 1


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
                        x += 1

                    elif detect:
                        bot.logger.info("there was a face detected")
                        bot.api.upload_photo(path, caption=caption)
                        does_exist = bot.get_media_comments(media, only_text=True)
                        if str(username) in does_exist:
                            x += 1
                            print("image has been commented")
                        else:
                            display_url = bot.get_link_from_media_id(media)
                            bot.logger.info("reposted " + display_url + " by " + username)
                            Bots.payment_system()
                            x += 1
                    else:
                        x += 1

                except Exception as e:
                    bot.logger.info(e)
                    x += 1

    def face_detection_follow(username):
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
                        x += 1

                    elif detect:
                        bot.logger.info("there was a face detected")
                        bot.api.follow(user_id)
                        does_exist = bot.get_media_comments(media, only_text=True)
                        if str(username) in does_exist:
                            x += 1
                            bot.logger.info("user has been followed")
                        else:
                            display_url = bot.get_link_from_media_id(media)
                            bot.logger.info("followed " +  username)
                            Bots.payment_system()
                            x += 1
                    else:
                        x += 1

                except Exception as e:
                    bot.logger.info(e)
                    x += 1

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
                        x += 1

                    elif detect:
                        comment = Bots.convert_usernames_to_list(comment)
                        comment = random.choice(comment)
                        bot.logger.info("there was a face detected")
                        bot.api.comment(media, comment)
                        does_exist = bot.get_media_comments(media, only_text=True)
                        if str(username) in does_exist:
                            x += 1
                            print("image has been commented")
                        else:
                            display_url = bot.get_link_from_media_id(media)
                            bot.logger.info("commented " + display_url + " by " + username)
                            Bots.payment_system()
                            x += 1
                    else:
                        x += 1

                except Exception as e:
                    bot.logger.info(e)
                    x += 1

    def like_followers(username, time_sleep):
        user_id = bot.get_user_id_from_username(username)
        followers = bot.get_user_followers(user_id)

        for user in followers:
            pusername = bot.get_username_from_user_id(user)
            Bots.face_detection(pusername)
            time.sleep(int(time_sleep))


    def like_following(username, time_sleep):
        user_id = bot.get_user_id_from_username(username)
        following = bot.get_user_following(user_id)

        for user in following:
            pusername = bot.get_username_from_user_id(user)
            Bots.face_detection(pusername)
            time.sleep(int(time_sleep))

    def like_hashtags(hashtag, time_sleep):
        hashtags = bot.get_hashtag_users(hashtag)
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
        while True:
            hashtags = Bots.convert_usernames_to_list(hashtags)
            for hashtag in hashtags:
                hashtags = bot.get_total_hashtag_medias(hashhtag)
                for user in hashtags:
                    pusername = bot.get_username_from_user_id(user)
                    Bots.face_detection_comment(pusername, comment)
                    time.sleep(int(time_sleep))

    def unfollow_users():
        bot.unfollow_everyone()

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
        points = open("x.txt", "r")
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
        increase = open("x.txt", "w")
        points = int(points)
        points -= 1
        if points < 0 :
            print("Buy 20.000 more COINS send 0.001 BTC to 12R5b4rLyNL8cC2HYQi5NpdPNaaAxPnmfe")
            print("To get key when bought talk to us here: https://web.telegram.org/#/im?p=@instabotai")
            Bots.stop()
        increase.write(str(points))
        increase.close()
        print("=" * 30)
        print("Buy 20.000 more COINS send 0.001 BTC to 12R5b4rLyNL8cC2HYQi5NpdPNaaAxPnmfe")
        print("To get key when bought talk to us here: https://web.telegram.org/#/im?p=@instabotai")

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
            with open("x.txt", "w+") as f:
                f.write(points)
            print("You have activated your code")
        else:
            print("wrong code")

    def follow_users_following_ai(username, time_sleep):
        while True:
            username = Bots.convert_usernames_to_list(username)
            for user in username:
                user_id = bot.get_user_id_from_username(user)
                followings = bot.get_user_following(user_id)
                for user_id in followings:
                    username = bot.get_username_from_user_id(user_id)
                    Bots.face_detection_follow(username)
                    time.sleep(time_sleep)

    def follow_users_followers_ai(username, time_sleep):
        while True:
            username = Bots.convert_usernames_to_list(username)
            for user in username:
                user_id = bot.get_user_id_from_username(user)
                followers = bot.get_user_followers(user_id)
                for user_id in followers:
                    username = bot.get_username_from_user_id(user_id)
                    Bots.face_detection_follow(username)
                    time.sleep(time_sleep)

    def follow_users_hashtag_ai(hashtag, time_sleep):
        while True:
            hashtags = Bots.convert_usernames_to_list(hashtag)
            for hashtag in hashtags:
                hashtags = bot.get_hashtag_users(hashtag)
                for user in hashtags:
                    username = bot.get_username_from_user_id(user)
                    Bots.face_detection_follow(username)
                    time.sleep(time_sleep)
