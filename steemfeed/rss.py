from datetime import datetime
import json

import markdown
import pyatom
import steem

from cache_expire import cache_with_timeout
from mdx_gfm import GithubFlavoredMarkdownExtension

md = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()])


@cache_with_timeout(60)
def make_feed(userid):

    s = steem.Steem()
    account = s.get_account(userid)
    profile = json.loads(account['json_metadata'])['profile']

    feed = pyatom.AtomFeed(
        author=profile.get('name', userid),
        title=profile.get('name', userid),
        subtitle=profile.get('about'),
        url=f'https://steemit.com/@{userid}',
        logo=profile['profile_image'])

    for post in s.get_discussions_by_blog({'tag': userid, 'limit': 10}):
        feed.add(
            title=post['title'],
            author=post['author'],
            id=f'@kjwon15/{post["permlink"]}',
            url=f'https://steemit.com/{post["category"]}/@{post["author"]}/{post["permlink"]}',
            updated=datetime.strptime(post['last_update'], '%Y-%m-%dT%H:%M:%S'),
            content=md.convert(post['body']),
            content_type='html')

    return feed.to_string()
