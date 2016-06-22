import requests
import sqlite3
from datetime import datetime


def start():
    # Vars
    url = 'https://api.twitch.tv/kraken/streams?limit=100'

    # Init
    conn = sqlite3.connect('streamers.db')
    sql = conn.cursor()

    # Logic
    try:
        response = requests.get(url)
        json = response.json()
        streams = json['streams']

        dbdata = []
        for i in range(0, len(streams)):
            s = streams[i]
            dbdata.append((
                s['channel']['_id'],
                s['channel']['name'],
                s['viewers'],
                s['channel']['views'],
                s['channel']['followers'],
                s['average_fps'],
                int(s['channel']['mature'] == True),
                str(s['channel']['game']),
                str(s['channel']['status']),
                s['channel']['language'],
                s['channel']['broadcaster_language'],
                s['channel']['created_at'],
                str(s['channel']['delay']),
                s['is_playlist'],
                datetime.utcnow()))

        query = 'INSERT INTO channellog (\
    channel_id, name, viewers, channel_views, followers, avg_fps, mature, game, status, language, \
    broadcaster_language, created_at, delay, is_playlist, utc_timestamp) \
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        sql.executemany(query, dbdata)
        conn.commit()

        # Close
        conn.close()

        # Output
        return "Added top 100 channels to log."
    except requests.exceptions.RequestException as e:
        return e
    except sqlite3.Error as e:
        return e
