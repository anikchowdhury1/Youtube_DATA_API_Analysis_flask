import os
import flask
from flask import current_app, request, redirect, make_response, jsonify
from googleapiclient.discovery import build
from flask_restplus import Namespace, Resource, fields
from http import HTTPStatus

namespace = Namespace('channel/videos/tags/stats', 'Get the tags & stats of all videos of a channel-id')

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()

    return response['items']




# This will get us a list of videos from a playlist.
# Note a page of results has a max value of 50 so we will
# need to loop over our results with a pageToken
def get_video_list(youtube, upload_id):
    video_list = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=upload_id,
        maxResults=50
    )
    next_page = True
    while next_page:
        response = request.execute()
        data = response['items']

        for video in data:
            video_id = video['contentDetails']['videoId']
            if video_id not in video_list:
                video_list.append(video_id)

        # Do we have more pages?
        if 'nextPageToken' in response.keys():
            next_page = True
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=upload_id,
                pageToken=response['nextPageToken'],
                maxResults=50
            )
        else:
            next_page = False

    return video_list




# Once we have our video list we can pass it to this function to get details.
# Again we have a max of 50 at a time so we will use a for loop to break up our list.
# check key exists
def get_video_details(youtube, video_list):
    stats_list=[]

    # Can only get 50 videos at a time.
    for i in range(0, len(video_list), 50):
        request= youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_list[i:i+50]
        )

        data = request.execute()
        for video in data['items']:
            id = video['id']
            title=video['snippet']['title'] if 'title' in video['snippet'] else None
            published=video['snippet']['publishedAt'] if 'publishedAt' in video['snippet'] else None
            description=video['snippet']['description'] if 'description' in video['snippet'] else None
            tag_count= len(video['snippet']['tags'] if 'tags' in video['snippet'] else [])
            tags = video['snippet']['tags'] if 'tags' in video['snippet'] else None
            statistics = video['statistics'] if 'statistics' in video else None
            view_count=video['statistics'].get('viewCount',0)
            like_count=video['statistics'].get('likeCount',0)
            dislike_count=video['statistics'].get('dislikeCount',0)
            comment_count=video['statistics'].get('commentCount',0)
            stats_dict=dict(id = id, title=title, description=description, published=published, tag_count=tag_count, tags = tags, statistics = statistics, view_count=view_count, like_count=like_count, dislike_count=dislike_count, comment_count=comment_count)
            stats_list.append(stats_dict)

    return stats_list


@namespace.route('/<string:channel_id>')
class ChannelVideoStats(Resource):
    '''Get the tags & stats of all videos of a channel-id'''

    @namespace.response(404, 'Channel-id not found')
    @namespace.response(500, 'Internal Server error')
    # @namespace.marshal_with(ChannelVideoStats_model)
    def get(self, channel_id):
        '''Get the tags & stats of all videos of a channel-id'''
        channel_stats = get_channel_stats(youtube, channel_id)
        upload_id = channel_stats[0]['contentDetails']['relatedPlaylists']['uploads']
        video_list = get_video_list(youtube, upload_id)
        video_data = get_video_details(youtube, video_list)
        return jsonify(video_data)


