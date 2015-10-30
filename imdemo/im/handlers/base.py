# -*- coding: utf8 -*-
"""
    imdemo.sockjs.handlers.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Inherits from sockjs.tornado.SockJSConnection.
"""

import functools

from sockjs.tornado import SockJSConnection
from nsq import Error

from imdemo.common.const import NSQ_INBOX_TOPIC
from imdemo.common.mq.producer import nsq_producer
from imdemo.im.store.clients import clients


class BaseSockJSConnection(SockJSConnection):

    def publish_callback(self, conn, data, topic, msg):
        if isinstance(data, Error):
            nsq_producer.pub(topic, msg)

    def publish_to_nsq(self, payload, topic=None):
        """Push message (topic, payload) to nsq server.

        :param str topic: Topic name
        :param str payload: Message body
        """
        topic = topic or NSQ_INBOX_TOPIC
        callback = functools.partial(
            self.publish_callback, topic=topic, msg=payload)
        nsq_producer.pub(topic, payload, callback)

    def add_client(self, key):
        """Add client when client online.

        :param str key
        """
        clients.add_client(key, self)

    def remove_client(self, key):
        """Remove client when client offline.

        :param str key
        """
        clients.remove_client(key)

    def has_client(self, key):
        """Check whether current process has this client.

        :param str key
        """
        return clients.has_client(key)

    def get_client(self, key):
        """Get client by key.

        :param str key
        :return: SockJS Session object or None.
        """
        return clients.get_client(key)