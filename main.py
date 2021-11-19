from bs4 import BeautifulSoup as bs
import libtorrent as lt
import cloudscraper
from utils import *
import subprocess
import datetime
import requests
import time
import os
import sys

href2 = []
magnet_dl = ""
names = []

welcome = r""" _____              ______ _ _
  ▄████ ▓█████▄▄▄█████▓   ▄▄▄█████▓ ██░ ██ ▓█████      █████▒██▓     ██▓▒██   ██▒ █    ██  ██▓███      ▐██▌ 
 ██▒ ▀█▒▓█   ▀▓  ██▒ ▓▒   ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀    ▓██   ▒▓██▒    ▓██▒▒▒ █ █ ▒░ ██  ▓██▒▓██░  ██▒    ▐██▌ 
▒██░▄▄▄░▒███  ▒ ▓██░ ▒░   ▒ ▓██░ ▒░▒██▀▀██░▒███      ▒████ ░▒██░    ▒██▒░░  █   ░▓██  ▒██░▓██░ ██▓▒    ▐██▌ 
░▓█  ██▓▒▓█  ▄░ ▓██▓ ░    ░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄    ░▓█▒  ░▒██░    ░██░ ░ █ █ ▒ ▓▓█  ░██░▒██▄█▓▒ ▒    ▓██▒ 
░▒▓███▀▒░▒████▒ ▒██▒ ░      ▒██▒ ░ ░▓█▒░██▓░▒████▒   ░▒█░   ░██████▒░██░▒██▒ ▒██▒▒▒█████▓ ▒██▒ ░  ░    ▒▄▄  
 ░▒   ▒ ░░ ▒░ ░ ▒ ░░        ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░    ▒ ░   ░ ▒░▓  ░░▓  ▒▒ ░ ░▓ ░░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░    ░▀▀▒ 
  ░   ░  ░ ░  ░   ░           ░     ▒ ░▒░ ░ ░ ░  ░    ░     ░ ░ ▒  ░ ▒ ░░░   ░▒ ░░░▒░ ░ ░ ░▒ ░         ░  ░ 
░ ░   ░    ░    ░           ░       ░  ░░ ░   ░       ░ ░     ░ ░    ▒ ░ ░    ░   ░░░ ░ ░ ░░              ░ 
      ░    ░  ░                     ░  ░  ░   ░  ░              ░  ░ ░   ░    ░     ░                  ░    
                                                                                                           
                                    """
print(Color.RED + welcome+'\n' + Color.END)

query = input(
    Color.ORANGE + 'Which film do you want to watch ?  \n \n'+Color.END)
print(Color.GREEN + '\n' f'Searching for "{query}" \n' + Color.END)
print(Color.ORANGE + 'which torrent site ?  \n  ' + Color.END)

torrent_site = ['1337x', 'Pirate Bay \n ']

for i, a in enumerate(torrent_site):
    print(str(i+1) + ')' + str(a))

torrent_choice = int(input())

if torrent_choice == 1:
    print(Color.GREEN + '\n' f'Searching 1337x \n' + Color.END)

    def t1337x_search(query):
        scraper = cloudscraper.create_scraper()
        url = 'https://1337x.to/search/'+query+'/1/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        source = scraper.get(url, headers=headers)

        soup = bs(source.text, 'html.parser')
        a = soup.find_all("a")
        td = soup.find_all("td", class_='coll-1 name')

        for tag in a:
            href = tag.attrs['href']
            if '/torrent/' in tag.get('href'):
                href2.append('https://1337x.to'+href)

        for name in td:
            names.append(name.text)

    t1337x_search(query)

    if len(names) >= 1:
        for i, a in enumerate(names[0:10]):
            print(str(i+1) + ')' + str(a)+'\n')

        print(Color.ORANGE + '\n'"Please Enter the index of the movie which you want to download or stream" + Color.END)
        user_choice = int(input())
        user_choice += i
    else:
        print(Color.RED + "Movie Not Found. Please try with different movie name. \n" + Color.RED)
        time.sleep(1)
        os.execl(sys.executable, sys.executable, *sys.argv)

    def t1337x_magnet(url):
        global href2, magnet_dl, i
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4594.111 Safari/537.36'}
        source = requests.get(href2[i], headers=headers)
        soup = bs(source.text, 'html.parser')

        for mag in soup.find_all("a"):
            href = mag.attrs['href']
            if 'magnet:' in href:
                magnet_dl += str(href)

    t1337x_magnet(magnet_dl)

elif torrent_choice == 2:
    print(Color.GREEN + '\n' f'Searching Pirate Bay \n' + Color.END)

    def pirateB_search(query):
        global magnet_dl
        magnet = []
        url = 'https://thepiratebay.party/search/' + query
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}

        source = requests.get(url, headers=headers)
        soup = bs(source.text, 'html.parser')

        links = soup.find_all('td')

        for mag in soup.find_all("a"):
            href = mag.attrs['href']
            if 'magnet:' in href:
                magnet.append(href)

        titles = [links[1].text, (links[9].text), links[17].text, links[25].text, links[33].text,
                  links[41].text, links[49].text, links[57].text, links[65].text, links[73].text]


        if len(titles) >= 1:
            for i, a in enumerate(titles[0:10]):
                print(str(i+1) + ')' + str(a))

        print(Color.ORANGE + '\n'"Please Enter the index of the movie which you want to download or stream" + Color.END)
        user_choice = int(input())
        if 1 <= user_choice <= 10:
            j = user_choice - 1
            magnet = magnet[j]
            titles = titles[j]
            magnet_dl += str(magnet)

            print(Color.GREEN + '\n' f'Downnloading {titles} \n' + Color.END)
        else:
            os.execl(sys.executable, sys.executable, *sys.argv)

    pirateB_search(query)

print(Color.ORANGE + '\n'"Do you want to download or to stream ?" + Color.END)

stream_choice = ['Download', 'Stream']

for i, a in enumerate(stream_choice):
    print(str(i+1) + ')' + str(a))

u_choice = int(input())

if u_choice == 1:
    def libtorrent_dl(url):
        global magnet_dl

        ses = lt.session()
        ses.listen_on(6881, 6891)

        params = {
            'save_path': '/home/becode/Documents/Torrent',
            'storage_mode': lt.storage_mode_t(2)
        }

        handle = lt.add_magnet_uri(ses, magnet_dl, params)
        ses.start_dht()

        begin = time.time()
        print(datetime.datetime.now())

        print(Color.GREEN + 'Downloading Metadata ...' + Color.END)
        while(not handle.has_metadata()):
            time.sleep(1)

        print(Color.GREEN + 'Got Metadata, Starting Torrent Download' + Color.END)
        print('Starting', handle.name())

        while(handle.status().state != lt.torrent_status.seeding):
            s = handle.status()
            state_str = ['queued', 'checking', 'downloading metadata'
                         'downloading', 'finished', 'seeding', 'allocating']
            print('% .2f %% complete (down: %.1f kb/s up: %.1f kb/s peers: %d) %s' %
                  (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
                   s.num_peers, state_str[s.state]))

            time.sleep(5)

        end = time.time()
        print(handle.name(), "COMPLETED")
        print("Elasped Time:", int((end-begin) // 60),
              "min: ", int((end - begin) % 60), 'sec : ')
        print(datetime.datetime.now())

    libtorrent_dl(magnet_dl)

elif u_choice == 2:
    def stream(magnet_dl):
        if sys.platform.startswith('linux'):
            cmd = []
            cmd.append("webtorrent")
            cmd.append("download")
            cmd.append(magnet_dl)
            print(Color.GREEN + 'streamming...' + Color.END)
            cmd.append('--vlc')
            subprocess.call(cmd)
        else:
            print("Option available with linux only")
            os.execl(sys.executable, sys.executable, *sys.argv)
stream(magnet_dl)
