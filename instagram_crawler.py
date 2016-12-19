import json
from tapioca_instagram import Instagram
from conf_parser import config

api = Instagram(access_token=config['instagram']['access_token'])

users = api.user_search().get(params={'q': 'samukasmk'})

user_id = users().data['data'][0]['id']

posts = api.user_media_recent(id=user_id).get(params={'count': 3})

for page in posts().pages():
    print('----')
    print(json.dumps(page().data))
    print('----')
