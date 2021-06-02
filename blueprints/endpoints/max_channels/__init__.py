import os
from flask import request, jsonify
from flask_restplus import Namespace, Resource, reqparse, fields
from googleapiclient.discovery import build

namespace = Namespace(
    'channel_lists/max/',
    'Returns the maximum number of channels on given start date and end date')

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


# Function to get the maximum number of channels
# It will also contain the upload playlist ID we can use to grab videos.
def get_channel_lists(youtube, start_date, end_date):
    channel_list = []
    request = youtube.search().list(
        part="snippet",
        channelType="any",
        maxResults=50,
        order="date",
        publishedAfter=start_date,
        publishedBefore=end_date,
        type="channel"
    )

    next_page = True

    while next_page:
        response = request.execute()
        channels = response['items']

        for channel in channels:
            channel_id = channel['id']['channelId']
            if channel_id not in channel_list:
                channel_list.append(channel_id)

        # Do we have more pages?
        if 'nextPageToken' in response.keys():
            next_page = True
            request = youtube.search().list(
                part="snippet",
                channelType="any",
                maxResults=50,
                order="date",
                pageToken=response['nextPageToken'],
                publishedAfter=start_date,
                publishedBefore=end_date,
                type="channel"
            )
        else:
            next_page = False

    return len(channel_list)


parser = reqparse.RequestParser()
parser.add_argument('start_date', type=str, help='The value is an RFC 3339 formatted date-time value (1970-01-01T00:00:00Z)')
parser.add_argument('end_date', type=str, help='The value is an RFC 3339 formatted date-time value (1970-01-01T00:00:00Z)')


@namespace.route('')
class MaxChannels(Resource):

    @namespace.response(200, 'Give maximum number of channels')
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(parser)
    def get(self):
        '''Return max number of channels'''

        start_date = request.args.get('start_date') if 'start_date' in request.args else ''
        end_date = request.args.get('end_date') if 'end_date' in request.args else ''
        max_channel_list = get_channel_lists(youtube, start_date, end_date)
        return jsonify({'max_channel': max_channel_list,
                        'start_date': start_date,
                        'end_date': end_date})
