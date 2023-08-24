def main():
    import os
    import random
    import time
    import urllib.request
    from bs4 import BeautifulSoup

    if not os.path.exists("eliyabot.html"):
        print("Please save the current Collection Tracker HTML as eliyabot.html in same directory as scraper.")
        exit(1)

    html = None
    with open("eliyabot.html", "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")

    char_list = soup.find("ul", class_="charList")
    for char in char_list.find_all("li", class_="unit"):
        art = char.find("img", class_="mainArt")
        if art is None:
            continue

        name = art["src"].split("/")[-2]
        out_loc = "../../wf_char_art/" + name + ".png"
        if os.path.exists(out_loc):
            continue

        art_url = "https://eliya-bot.herokuapp.com" + art["src"]
        print("req: " + art_url)
        req = urllib.request.urlopen(art_url)
        data = req.read()
        with open(out_loc, "wb") as f:
            f.write(data)

        sleep = random.randint(500, 1500) / 1000.0
        time.sleep(sleep)


if __name__ == '__main__':
    main()
