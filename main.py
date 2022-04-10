import json

import requests
from bs4 import BeautifulSoup

def trans_both(text, source, target):
    key = "AIzaSyCx7GnPPww1_v0pEagGRWHh82jJKH5xyG8"

    data = {
        "q": text,
        "source": source,
        "target": target
    }

    response = requests.post("https://translation.googleapis.com/language/translate/v2?key=" + key, data=data)

    response = str(response.text)

    return json.loads(response)["data"]["translations"][0]["translatedText"]


def trans_one(text, target):
    key = "AIzaSyCx7GnPPww1_v0pEagGRWHh82jJKH5xyG8"

    data = {
        "q": text,
        "target": target
    }

    response = requests.post("https://translation.googleapis.com/language/translate/v2?key=" + key, data=data)

    response = str(response.text)

    return json.loads(response)["data"]["translations"][0]["translatedText"]


global soup
global driver

auto_detect = False
running = True

search_url = "https://en.wikipedia.org/w/index.php?search=\n\t&title=Special%3ASearch&fulltext=1&ns0=1"
base_url = "https://en.wikipedia.org/"


def connect(url):
    global soup
    response = requests.post(url)
    soup = BeautifulSoup(response.text, "lxml")


def search_wiki(term):
    temp_url = search_url.replace("\n\t", term)
    connect(temp_url)

    search_cont = soup.find("ul", {"class": "mw-search-results"})
    search_results = search_cont.find_all("li")
    search_urls = []
    search_titles = []
    search_summaries = []
    for each in search_results:
        if search_results.index(each) > 9:
            break
        else:
            temp_element = each.find('div', {'class': 'mw-search-result-heading'}).find('a')
            search_urls.append(temp_element['href'])
            search_titles.append(temp_element['title'])

    print("Which of these did you mean?\n")
    for each in range(len(search_titles)):
        print(f"{each + 1}) {search_titles[each]}")

    num = int(input()) - 1

    print("\n")

    search_titles = search_titles[num]
    search_urls = base_url + search_urls[num]

    connect(search_urls)

    summary = ""
    count = 0
    while summary == "":
        x = soup.find("div", {"class": "mw-parser-output"})
        y = x.find_all("p")
        summary = str(y[count].get_text()).strip()
        count += 1
    summary_split = summary.split(".")
    try:
        search_summaries = (summary_split[0] + summary_split[1])
    except:
        search_summaries = summary

    return [search_titles, search_urls, search_summaries]


def get_response(message):
    url = "https://waifu.p.rapidapi.com/path"

    querystring = {f"user_id": "sample_user_id", "message": {message}, "from_name": "Monty", "to_name": "Girl",
                   "situation": "teacher and student"}

    payload = {}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Host": "waifu.p.rapidapi.com",
        "X-RapidAPI-Key": "cdf3508a51mshbe5af6a133567edp158282jsn632c685a4d38"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    return str(response.text).replace("Monty Said: ", "")


print("Welcome to Monty chatting services")
print("Through this application you get the honor of talking with Monty")
print("But do be careful he can quite naughty at times")

input("\nPlease press enter to continue")

print("\n\nThis chatbot has been handcrafted with many abilities, such as translate, Wikipedia, etc\n")

languages = {1: "en",
             2: "fr",
             3: "es",
             0: "auto"}
try:
    rep_my_lang = int(
        input("What language would you like to use:\n\n0. Auto-detect\n1. English\n2. French\n3. Spanish\n"))
except:
    rep_my_lang = -1

if rep_my_lang == 0:
    auto_detect = True

while rep_my_lang not in languages.keys():
    rep_my_lang = int(input(f"Please input a valid number between 1 and {len(languages) - 1} or -1:"))
try:
    rep_mon_lang = int(input("\n\nWhat language would you like Monty to use:\n\n1. English\n2. French\n3. Spanish\n"))
except:
    rep_mon_lang = -1
while rep_mon_lang not in languages.keys():
    rep_mon_lang = int(input(f"Please input a valid number between 1 and {len(languages)}:"))

print("\n\nTHANK YOU! \n Lastly, if Monty's being naughty, please type 'Exit' to quit the program\n\n")

while (running):

    msg = input("Me: ")



    if msg == "Exit" or msg == "Exit".lower() or msg == "Exit".upper():
        running = False
        break

    if "check wiki for" in msg:
        temp = search_wiki(msg.replace("check wiki for", "").strip())

        print(f"This is what I found for {temp[0]} : {temp[2]}")
        print(f"Find more information at :  {temp[1]}\n\n")


    else:

        if languages[rep_my_lang] == "en":
            msg = msg
        elif auto_detect:
            msg = trans_one(msg, "en")
        else:
            msg = trans_both(msg, languages[rep_my_lang], "en")

        res = get_response(msg)

        if languages[rep_mon_lang] == "en":
            print(res)
        else:
            print(trans_both(res,"en",languages[rep_mon_lang]))






