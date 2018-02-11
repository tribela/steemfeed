from datetime import datetime

import markdown
import pyatom
import steem

from mdx_gfm import GithubFlavoredMarkdownExtension

md = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()])


def make_feed(userid):

    feed = pyatom.AtomFeed(
        title=f'Steemit feed from {userid}',
        url=f'https://steemit.com/@{userid}',
        author=userid)

    s = steem.Steem()

    for post in s.get_discussions_by_blog({'tag': userid, 'limit': 10}):
        feed.add(
            title=post['title'],
            id=f'@kjwon15/{post["permlink"]}',
            url=f'https://steemit.com/{post["category"]}/@{post["author"]}/{post["permlink"]}',
            updated=datetime.strptime(post['last_update'], '%Y-%m-%dT%H:%M:%S'),
            content=md.convert(post['body']),
            content_type='html')

    return feed.to_string()
