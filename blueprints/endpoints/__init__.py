from flask import Blueprint
from flask_restplus import Api
from blueprints.endpoints.channel_video_stats import namespace as channel_video_stats_ns
from blueprints.endpoints.max_channels import namespace as max_channels_ns
from blueprints.endpoints.tags import namespace as tags
from blueprints.endpoints.video_performances import namespace as video_performance
blueprint = Blueprint('endpoints', __name__, url_prefix='/api')

api_extension = Api(
    blueprint,
    title='Youtube API Analysis',
    version='1.0',
    description='Application for processing Youtube API for fetching\
        chennel info, video list info, tags, stats, tracking stats of videos and maximum channel list',
    doc='/v1'
)

api_extension.add_namespace(channel_video_stats_ns)
api_extension.add_namespace(max_channels_ns)
api_extension.add_namespace(tags)
api_extension.add_namespace(video_performance)
