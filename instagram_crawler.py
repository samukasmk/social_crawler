from datetime import datetime
from tapioca_instagram import Instagram

from conf_parser import config
from csv_writer import write_post_csv

api = Instagram(access_token=config['instagram']['access_token'])

def get_instagram_posts(instagram_api, user_name, **user_media_kwargs):
    """
    Returns a generator with a dict post row
    >>> api = Instagram(access_token='...')

    >>> for post_dict in get_instagram_posts(instagram_api=api, user_name='samukasmk'):
    ...     print(post_dict)
    { 'type_id': 1, 'post_id': '17851381516028449', 'user_name': 'samukasmk',
      'post_text': '#noenergy #candlelight #vintage', 'user_id': '31836448',
      'total_likes': 9, 'tags': 'noenergy, candlelight, vintage', 'posted_at': '2015-01-14T00:01:40',
      'image': 'https://scontent.cdninstagram.com/t51.2885-15/e15/10899092_888856164479996_321474702_n.jpg' }
    """
    # Get user id by user name
    users_found = api.user_search().get(params={'q': user_name, 'count': 1})
    user_id = users_found().data['data'][0]['id']
    # Get posts of user
    posts = api.user_media_recent(id=user_id).get(params=user_media_kwargs)

    for page in posts().pages(max_pages=5):
        post = page().data
        post_row = dict(type_id=1,
                        post_id=post['id'],
                        post_text=post['caption']['text'] \
                            if post['caption'] is not None else None,
                        posted_at=datetime.fromtimestamp(
                            float(post['created_time'])).isoformat(),
                        user_name=post['user']['username'],
                        user_id=post['user']['id'],
                        tags=', '.join(post['tags']),
                        total_likes=post['likes']['count'],
                        image=post['images']['standard_resolution']['url'])
        yield post_row


def instagram_crawler(user_name, **user_media_kwargs):

    api = Instagram(access_token=config['instagram']['access_token'])

    post_rows = get_instagram_posts(api, user_name, **user_media_kwargs)

    file_path = 'raw_data/instagram_{}.csv'.format(
        datetime.now().isoformat().replace(':', '_'))

    write_post_csv(file_path, post_rows)


if __name__ == '__main__':
    instagram_crawler(user_name='samukasmk', count=200)
