import face_recognition
import logging
import time
from random import randint
import instagram_scraper as insta
import json
import sys

# Logging Output default settings
logging.basicConfig(stream=sys.stdout, format='',
                    level=logging.INFO, datefmt=None)
log = logging.getLogger(__name__)


def random_sleep(number1, number2):
    ''' Random sleep between two numbers'''
    time_sleep = time.sleep(randint(number1, number2))
    return time_sleep


''' number of last photos scraped '''
number_last_photos = 20


def Convert(string):
    li = list(string.split(","))
    return li


# Scraping profiles
profiles = "abigailratchford,anastasiya_kvitko,marona_tanner"
profiles = Convert(profiles)

x = 0


def InstaImageScraper():
    ''' Scrape image on profiles '''
    imgScraper = insta.InstagramScraper(usernames=profiles,
                                        maximum=number_last_photos,
                                        media_metadata=True, latest=True,
                                        media_types=['image'])
    imgScraper.scrape()

    print("Images has been scraped")


InstaImageScraper()


def face_detection(path_to_image):
    ''' Face Detection for image '''
    image = face_recognition.load_image_file(path_to_image)
    face_locations = face_recognition.face_locations(image)
    # If no face located scrape the next profile
    if not face_locations:
        log.info("There is no Face Detected scraping next profile")
        log.info(profiles[x])
        random_sleep(1, 2)

    else:
        log.info("There is a Face Detected scraping and posting this image")
        log.info(profiles[x])
        random_sleep(1, 2)
        log.info("Media Id:" + str(media_id))
        log.info("Face Location: " + str(face_locations))
        log.info("Path to image: " + path_to_image)
        htmloutput()


def htmloutput():
    ''' open profilename in a profilename.html and create a website '''
    f = open(profiles[x] + ".html", "a+")
    f.write(
    f"""
    <html>
    <title>{profiles[x]} - Rank babes - Hottest babes online</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <body><div class="header"><div class="header-social-nav">
    <a href="http://instagram.com/japanheaven"><img class="icons"
    src="img/icons/instagram.svg"
    alt="instagram"
    height="25px"
    width="25px"
    /></a>
    <img class="icons"
    src="img/icons/facebook.svg"
    alt="facebook"
    height="25px"
    width="25px"
    /></div>
    <link rel="stylesheet" href="style.css">
    <h1><center>Rank Babes - Hottest babes online</center></h1>
    <div class="header-menu">
    <center>
    <a href ="scandinavia/">SCANDINAVIA</a> <a href ="russia/">RUSSIA</a> AFRICA INDIAN JAPANESE KOREAN</center>
    </div></div>
    <p>
    <div class "main">
    <center>
    <h1>{profiles[x]}</h1><p>
    <a href="https://www.instagram.com/p/ByqJI_EgpOh/"><img class="image" src="{instagram_image_link}"></img></a>
    <p>
    </center></div>

</body>
</html>
   """)


print("Created " + profiles[x] + ".html")
while x < len(profiles[x]):
    try:
        with open(profiles[x] + "/" + profiles[x] + ".json", "r") as j:
            json_data = json.load(j)
            u = 0
            try:
                while u < len(json_data["GraphImages"][u]["display_url"]):
                    newstr = (json_data["GraphImages"][u]["display_url"])
                    # Output media id of image
                    media_id = (json_data["GraphImages"][u]["id"])
                    instagram_image_link = newstr.split('&se')[0]
                    instagram_image_name = newstr.split('?')[0].split('/')[-1]
                    instagram_image_location = str(profiles[x]) + '/' + instagram_image_name
                    face_detection(instagram_image_location)
                    u += 1
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        pass
    print("test")
    x += 1
