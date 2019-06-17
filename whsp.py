from watson_developer_cloud import ToneAnalyzerV3
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
tone_analyzer = ToneAnalyzerV3(
    version='INSERT VERSION',
    username='INSERT USERNAME',
    password='INSERT PASSWORD',
    url='INSERT URL'
)

def request_until_succeed(url):
    req = Request(url)
    success = False
    i = 1
    while success is False and i < 6:
        i = i+1
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(30)
            print("Retrying.")

    return response.read()

def sendMessage(msg='Hi!'):
	web_obj = driver.find_element_by_xpath("//div[@class='_2S1VP copyable-text selectable-text']")
	web_obj.send_keys(msg)
	web_obj.send_keys(Keys.RETURN)

last_msgs=[]
url = "https://web.whatsapp.com/"
driver = webdriver.Firefox()
driver.get(url)
time.sleep(15)
while(True):
    driver.find_element_by_xpath("//span[@title='INSERT THE NAME OF THE PERSON/GROUP YOU WANT TO CHAT WITH']").click()
    msgs=driver.find_elements_by_xpath("//span[@class='selectable-text invisible-space copyable-text']")
    temp=[]
    for msg in msgs:
        tosend=False
        tone_analysis={}
        mood_set=set()
        if(msg.text not in last_msgs and 'moods :' not in msg.text):
            tosend=True
            temp.append(msg.text)
            tone_analysis = tone_analyzer.tone(
                {'text': msg.text},
                'application/json')
        
            document_tones_list=tone_analysis['document_tone']['tones']
            for tone in document_tones_list:
                #print(tone['tone_name'])
                mood_set.add(tone['tone_name'])
            try:
                sentence_tones_list=tone_analysis['sentences_tone']
                for sentence_tone in sentence_tones_list:
                    mood_set.add(x['tone_name'] for x in sentence_tone['tones'])
                mood_set.add(x['tone_id'] for x in tone_analysis['document_tone']['tones'])
            except:
                pass
        print(mood_set)
        allmoods=''
        for x in mood_set:
            allmoods=allmoods+str(x)+" "
        reply='"'+msg.text+'"'
        reply=reply+'\n'+"moods : "+allmoods
        if(tosend):
            last_msgs.append('"'+msg.text+'"')
            sendMessage(reply)
        time.sleep(2)
    if(len(last_msgs)>450):
        del last_msgs[:450]
    last_msgs.extend(temp)
    driver.refresh()
time.sleep(10)
