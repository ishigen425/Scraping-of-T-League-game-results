import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
from player_data_func import get_team_link, get_player_data, get_player_link
import config as conf

conn = mysql.connector.connect(
    host = conf.host,
    port = conf.port,
    user = conf.user,
    password = conf.password,
    database = conf.database
)

cur = conn.cursor()

basicurl = "https://tleague.jp"
link = get_team_link()
try:
    cur.execute("DELETE FROM player;")
    for i in link:
        url = basicurl + i + "player/"
        tmp = "?season=2018"
        player_list_url = get_player_link(url + tmp)
        for player_index, player_url in enumerate(player_list_url):
            player_url = url + player_url 
            player_data = get_player_data(player_url)
            execute_str = "INSERT INTO player VALUES ('{}','{}','{}',{},{},'{}',{},{});".format(
                player_data[0].strip(), i[6:-1], player_data[1].strip(), player_data[2], player_data[3], 
                player_data[4].strip(), player_data[5] or 'NULL', player_data[6] or 'NULL'
            )
            cur.execute(execute_str)
except:
    conn.rollback()
    raise

conn.commit()
