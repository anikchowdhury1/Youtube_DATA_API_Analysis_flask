import os
from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from http import HTTPStatus
from googleapiclient.discovery import build


namespace = Namespace('channel/videos/tags/', 'filter the videos by tags')

# tag_example = {'id': 1,
#                'name': 'Tag name'}

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# filter videos by Tag
def video_details_by_tag(youtube, tag):
    video_details_list = []
    request = youtube.search().list(
        part="snippet",
        maxResults=50,
        order="date",
        publishedAfter="2021-05-26T05:40:00+00:00",
        publishedBefore="2021-05-27T05:40:00+00:00",
        q=tag,
        type="video",
        videoType="any",
        prettyPrint=True,
    )

    next_page = True

    while next_page:
        response = request.execute()
        video_data = response['items']

        for video in video_data:
            video_data_dict = {
                "id": video['id']['videoId'],
                "url": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                "thumbnails": video['snippet']['thumbnails']['high']['url'],
                "title": video['snippet']['title'],
            }

            if video_data_dict not in video_details_list:
                video_details_list.append(video_data_dict)

        # Do we have more pages?
        if 'nextPageToken' in response.keys():
            next_page = True
            request = youtube.search().list(
                part="snippet",
                maxResults=50,
                order="date",
                publishedAfter="2021-05-26T05:40:00+00:00",
                publishedBefore="2021-05-27T05:40:00+00:00",
                q=tag,
                pageToken=response['nextPageToken'],
                type="video",
                videoType="any",
                prettyPrint=True,
            )
        else:
            next_page = False

    return video_details_list


@namespace.route('/<string:tag>')
class Tag(Resource):
    '''Get the videos filtered by tag'''

    @namespace.response(404, 'Related videos by this tag not found!')
    @namespace.response(500, 'Internal Server error')
    # @namespace.marshal_with(tag_model)
    def get(self, tag):
        '''Get the videos filtered by tag'''
        video_details_list = video_details_by_tag(youtube, tag)
        total_tagged_videos =len(video_details_list)
        return jsonify({'Number of tagged videos': total_tagged_videos,
                        'Tagged Videos Details': video_details_list})
