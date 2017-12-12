# -*- coding: utf-8 -*-

from werobot.replies import WeChatReply, TextReply, ArticlesReply, MusicReply, Article
from werobot.utils import is_string


def create_reply(reply, message=None):
    if isinstance(reply, WeChatReply) or isinstance(reply, TextReply):
        return reply.render()
    elif is_string(reply):
        reply = TextReply(message=message, content=reply)
        return reply.render()
    elif isinstance(reply, list) and all([len(x) == 4 for x in reply]):
        if len(reply) > 10:
            raise AttributeError("Can't add more than 10 articles"
                                 " in an ArticlesReply")
        r = ArticlesReply(message=message)
        for article in reply:
            article = Article(*article)
            r.add_article(article)
        return r.render()
    elif isinstance(reply, list) and 3 <= len(reply) <= 4:
        if len(reply) == 3:
            # 如果数组长度为3， 那么高质量音乐链接的网址和普通质量的网址相同。
            reply.append(reply[-1])
        title, description, url, hq_url = reply
        reply = MusicReply(
            message=message,
            title=title,
            description=description,
            url=url,
            hq_url=hq_url
        )
        return reply.render()
