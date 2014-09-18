# -*- coding: utf-8 -*-

from . import API


class ComputeAPIItem(object):

    base_path = ''

    def __init__(self, compute_api, data=None):
        self._compute_api = parent_api
        self.data = data

    def query(self):
        return self._compute_api.query(self.base_path)

    # def __get__(self, key): return self.data.get(key)


class ServerItem(ComputeAPIItem):

    @property
    def base_path(self):
        return 'servers/{}'.format(self.data['id'])

    def poweron(self):
        return self.query().actions().post({'action': 'poweron'})

    def poweroff(self):
        return self.query().actions().post({'action': 'poweroff'})

    def reset(self, hard=False):
        if hard:
            return self.query().actions().post({'action': 'resethard'})
        else:
            return self.query().actions().post({'action': 'resetsoft'})


class ComputeAPI(API):

    base_url = 'https://api.cloud.online.net'

    def servers(self, **filters):
        try:
            response = self.query().servers().get()

        except slumber.exceptions.HttpClientError as exc:
            if exc.response.status_code == 404:
                raise BadToken()

            if exc.response.status_code == 410:
                raise ExpiredToken()

            raise

        return [
            ServerItem(self, server)
            for server in response.get('servers', [])
        ]
