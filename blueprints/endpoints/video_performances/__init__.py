import os
from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
import sqlite3
from http import HTTPStatus

namespace = Namespace('channel/videos/performance/', 'filter the videos by video performance')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "youtube_data.db")



def dictFactory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



@namespace.route('/<string:performance>')
class VideoPerformance(Resource):
    '''Get the videos filtered by performance'''

    @namespace.response(404, 'Related performance parameter (i.e. \'Very Good\'/ \'Good\'/ \'Average\'/ \'Below Average\'/ \'Bad\') not found!')
    @namespace.response(500, 'Internal Server error')
    def get(self, performance):
        '''Get the tags & stats of all videos of a channel-id'''

        conn = sqlite3.connect(db_path)
        conn.row_factory = dictFactory
        cur = conn.cursor()
        query = "select id, title, view_count, like_count, dislike_count, comment_count from youtube_data where performance='%s';"
        filtered_data = cur.execute(query % performance).fetchall()

        result = jsonify(filtered_data)
        print(db_path)
        print(result)

        return jsonify(filtered_data)