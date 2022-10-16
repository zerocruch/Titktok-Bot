import json
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
from time import sleep
import requests
from os import remove, system
import pyautogui
import pyperclip
import pyttsx3



#put your caption on  caption.txt each per line
#the base image change it depending on your needs

engine = pyttsx3.init()

#put your twitter api , secret , bearer here

api = ""

secret = ""

bearer = ""




# twiter acount id here you can get it from 
# https://tweeterid.com/
twiter_id = ""



open_tiktok_upload_and_firefox = "start firefox https://www.tiktok.com/upload"
kill_firefox = "TASKKILL /IM firefox.exe /F"

#video title on tiktok
tiktok_video_title = ""

caption = (600, 320)
caption_file = "caption.txt"
select_file = (200, 660)
select_bar = (600, 60)
select_path = "result_video"
file_name_bar = (300, 470)
post = (600, 870)

while True:
    try:
        file = open("last_tweet_id.txt", "r+")
        last_tweet_id = file.readline()
        file.close()

        # get elon last tweet id and text
        url = f'https://api.twitter.com/2/users/{twiter_id}/tweets?max_results=5'
        headers = {'Authorization': f'Bearer {bearer}'}
        response = requests.request('GET', url, headers=headers)
        x = json.loads(response.text)
        tweet_text = x["data"][0]["text"]
        tweet_id = x["data"][0]["id"]
        # print(x["data"][0])

        # check if it's the same tweet

        if last_tweet_id != tweet_id:
            # remove old image and video
            try:
                remove(f"result_image\\{last_tweet_id}.png")
                remove(f"result_video\\{last_tweet_id}.mp4")
            except Exception:
                pass
            # write last tweet id to static file
            file = open("last_tweet_id.txt", "w")
            file.write(tweet_id)
            file.close()
            # fix and edit text according to image
            w = 20
            h = 120
            split_on = 50
            test_text = tweet_text
            final_text = ""
            start = 0
            max_level = 6
            word_length = len(test_text) // 50 if len(test_text) % 50 == 0 else (len(test_text) // 50) + 1
            if word_length <= max_level:
                for _ in range(word_length):
                    try:
                        final_text += (
                                    test_text[start:test_text.index(" ", start + split_on, start + split_on + 10)] + "\n")
                        start = test_text.index(" ", start + split_on, start + split_on + 10)
                    except Exception:
                        final_text += (test_text[start:] + "\n")
                        start = len(test_text)

            else:
                for _ in range(max_level):
                    try:
                        final_text += (
                                    test_text[start:test_text.index(" ", start + split_on, start + split_on + 10)] + "\n")
                        start = test_text.index(" ", start + split_on, start + split_on + 10)
                    except Exception:
                        final_text += (test_text[start:] + "\n")
                        start = len(test_text)
                final_text += (test_text[start:start + split_on - 5] + ".....")

            # export image
            img = Image.open('img\\baseimage.png')
            I1 = ImageDraw.Draw(img)
            myFont = ImageFont.truetype('arial.ttf', 20)
            I1.text((w, h), final_text, fill=(255, 255, 255), font=myFont)
            image_save_location = f"result_image\\{tweet_id}.png"
            img.save(image_save_location)

            # create video
            video_save_location = f"result_video\\{tweet_id}.mp4"
            clips = []
            clip1 = ImageClip(
                f"result_image\\{tweet_id}.png").set_duration(
                10)
            clips.append(clip1)
            video_clip = concatenate_videoclips(clips, method='compose')
            video_clip.write_videofile(video_save_location, fps=24, remove_temp=True, codec="libx264", audio_codec="aac")

            # publish video to tiktok

            # upload(video_save_location)


            print(f"New Tweet ! {tweet_text}")
            engine.say("New Tweet Dont Touch ! ")
            engine.runAndWait()
            sleep(5)
            # open tiktok on firefox
            system(open_tiktok_upload_and_firefox)
            sleep(10)

            # click on caption
            pyautogui.click(caption)

            # write title
            pyautogui.typewrite(tiktok_video_title)

            # open caption file and write them
            file = open(caption_file, 'r')
            for line in file.readlines():
                pyperclip.copy('#')
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.typewrite(line)
                sleep(1.5)
                pyautogui.typewrite(["enter"])

            # click on select file
            sleep(1)
            pyautogui.click(select_file)
            sleep(1)
            # click on select bar and select path
            pyautogui.click(select_bar)
            sleep(1)
            pyperclip.copy(select_path)
            pyautogui.hotkey('ctrl', 'v')
            sleep(1)
            pyautogui.typewrite(["enter"])
            sleep(1)

            # select name of video
            pyautogui.click(file_name_bar)
            pyautogui.typewrite(f"{tweet_id}.mp4")
            pyautogui.click(file_name_bar)
            sleep(1)
            pyautogui.typewrite(["enter"])
            sleep(20)

            # post
            pyautogui.click(post)
            sleep(10)

            # kill firefox
            system(kill_firefox)
        else:
            pass
            # print("nope")
            # engine.say("Nope Nothing New")
            # engine.runAndWait()
        sleep(20)
    except Exception as e:
        print(f'Something Went Wrong : Error Info --> {e}')
