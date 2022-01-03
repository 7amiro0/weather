"""File create data base."""

import sqlite3
import json
import requests
import datetime

list_cordinat = [('50.45', '30.52'), ('49.42', '32.06'),
                 ('48.51', '32.25'), ('47.90', '33.38'),
                 ('46.47', '30.73')]
list_name = ['Kyiv', 'Cherkasy',
             'Kropyvnytski', 'Kryvyy Rih',
             'Odesa']

con = sqlite3.connect('exempl.db')
table = con.cursor()

try:
    table.execute('CREATE TABLE weather (date text, temp text, pcp text, clouds text,' \
                  'pressure text, humidity text, wind_speed text, name_city text)')

except sqlite3.OperationalError:
    table.execute('DELETE FROM weather')
    con.commit()

for coordinates in range(len(list_cordinat)):
    link = requests.get('https://api.openweathermap.org/data/2.5/' \
                        'onecall?lat='+list_cordinat[coordinates][0]+'&lo' \
                        'n='+list_cordinat[coordinates][1]+'&exclude=current' \
                        ',minutely,hourly&appid=8f6fe32c8781671c86b0e9941a7f061f')
    text_insert = json.loads(link.text.strip())
    for day in range(7):
        info = (str(datetime.datetime.fromtimestamp \
                (int(text_insert['daily'][day]['dt'])) \
                    .strftime('%d.%m.%Y')),
                str(int(-273.15+float(text_insert['daily'][day]['temp']['day']))),
                str(int(text_insert['daily'][day]['pop'])*100),
                str(text_insert['daily'][day]['clouds']),
                str(text_insert['daily'][day]['pressure']),
                str(text_insert['daily'][day]['humidity']),
                str(int(text_insert['daily'][day]['wind_speed'])),
                list_name[coordinates])
        table.execute("INSERT INTO weather VALUES (?, ?, ?, ?,?, ?, ?, ?)", info)

con.commit()
con.close()
