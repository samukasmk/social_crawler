import csv
from datetime import datetime
from tapioca_twitter import Twitter

from conf_parser import config
from csv_writer import write_post_csv

def get_twitter_posts(twitter_api, **api_params):
    """
    Returns a generator with a dict post row
    >>> api = Twitter(api_key='...',
                      api_secret='...',
                      access_token='...',
                      access_token_secret='...')

    >>> for post_dict in get_twitter_posts(twitter_api=api, screen_name='samukasmk'):
    ...     print(post_dict)
    { 'post_text': 'I am a twitter text', 'user_id': 68425610, 'tags': '',
      'user_name': 'samukasmk', 'type_id': 2, 'post_id': 696712667050995713,
      'total_likes': None, 'image': None, 'posted_at': '2016-02-08T15:10:18+00:00' }
    """

    posts = twitter_api.statuses_user_timeline().get(params=api_params)

    for page in posts().pages(max_pages=5):
        post = page().data
        post_row = dict(type_id=2,
                        post_id=post['id'],
                        post_text=post['text'],
                        posted_at=datetime.strptime(
                            post['created_at'], "%a %b %d %X %z %Y").isoformat(),
                        user_name=post['user']['screen_name'],
                        user_id=post['user']['id'],
                        tags=', '.join(
                            [ d['text'] for d in post['entities']['hashtags'] ]),
                        total_likes=None)

        if 'media' in post['entities'].keys() \
            and len(post['entities']['media']) > 0 \
            and 'media_url' in post['entities']['media'][0].keys():
            post_row['image'] = post['entities']['media'][0]['media_url']
        else:
            post_row['image'] = None

        yield post_row


def twitter_crawler(user_name, **timeline_kwargs):

    api = Twitter(api_key=config['twitter']['api_key'],
        api_secret=config['twitter']['api_secret'],
        access_token=config['twitter']['access_token'],
        access_token_secret=config['twitter']['access_token_secret'])

    post_rows = get_twitter_posts(api, screen_name=user_name, **timeline_kwargs)

    file_path = 'raw_data/twitter_{}.csv'.format(
        datetime.now().isoformat().replace(':', '_'))

    write_post_csv(file_path, post_rows)


if __name__ == '__main__':
    twitter_crawler(user_name='samukasmk', count=200)
