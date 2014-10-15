# -*- coding: utf-8 -*-

import logging

import slumber

from . import API


class ComputeAPIItem(object):

    def __init__(self, compute_api, data=None):
        self._compute_api = compute_api
        self.data = data
        for key, value in data.items():
            setattr(self, key, value)

    def query(self):
        """ Interface """
        raise NotImplementedError()


class ComputeAPIItemUUID(ComputeAPIItem):

    kind = None

    name = None
    modification_date = None
    creation_date = None
    organization = None
    id = None

    def query(self):
        return getattr(
            self._compute_api.query(),
            '{}s'.format(self.kind)
        )(self.data['id'])

    def delete(self):
        return self.query().delete()


class ImageItem(ComputeAPIItemUUID):

    kind = 'image'

    public = None
    extra_volumes = None
    arch = None
    root_volume = None


class SnapshotItem(ComputeAPIItemUUID):

    kind = 'snapshot'

    base_volume = None
    volume_type = None
    state = None
    size = None


class VolumeItem(ComputeAPIItemUUID):

    kind = 'volume'

    export_uri = None
    server = None
    size = None


class ServerItem(ComputeAPIItemUUID):

    kind = 'server'

    tags = None
    state_detail = None
    image = None
    public_ip = None
    state = None
    private_ip = None
    volumes = None
    dynamic_public_ip = None

    def action(self, action):
        return self.query().action.post({'action': action})

    def poweron(self):
        return self.action('poweron')

    def poweroff(self):
        return self.action('poweroff')

    def reboot(self):
        return self.action('reboot')

    def powertoggle(self):
        try:
            return self.poweroff()
        except slumber.exceptions.HttpClientError as exc:
            if exc.response.status_code == 400:
                return self.poweron()


class IpItem(ComputeAPIItemUUID):

    kind = 'ip'

    address = None
    server = None


class ComputeAPI(API):
    """ Interacts with OCS Compute API.
    """

    base_url = 'https://api.cloud.online.net'

    def servers(self, **filters):
        try:
            response = self.query().servers.get(**filters)

        except slumber.exceptions.HttpClientError as exc:
            raise

        return [
            ServerItem(self, server)
            for server in response.get('servers', [])
        ]

    def create_server(self, **attributes):
        try:
            return self.query().servers.post(data=attributes).get('server', {})

        except (slumber.exceptions.HttpServerError,
                slumber.exceptions.HttpClientError) as e:
            if e.response.status_code in (429, 502):
                create_server()
            else:
                logging.error(e.response.text)
                raise e

    def images(self, **filters):
        try:
            response = self.query().images.get(**filters)

        except slumber.exceptions.HttpClientError as exc:
            raise

        return [
            ImageItem(self, image)
            for image in response.get('images', [])
        ]

    def create_image(self, **attributes):
        try:
            return self.query().images.post(data=attributes).get('image', {})

        except (slumber.exceptions.HttpServerError,
                slumber.exceptions.HttpClientError) as e:
            if e.response.status_code in (429, 502):
                create_image()
            else:
                logging.error(e.response.text)
                raise e

    def volumes(self, **filters):
        try:
            response = self.query().volumes.get(**filters)

        except slumber.exceptions.HttpClientError as exc:
            raise

        return [
            VolumeItem(self, volume)
            for volume in response.get('volumes', [])
        ]

    def create_volume(self, **attributes):
        try:
            return self.query().volumes.post(data=attributes).get('volume', {})

        except (slumber.exceptions.HttpServerError,
                slumber.exceptions.HttpClientError) as e:
            if e.response.status_code in (429, 502):
                create_volume()
            else:
                logging.error(e.response.text)
                raise e

    def snapshots(self, **filters):
        try:
            response = self.query().snapshots.get(**filters)

        except slumber.exceptions.HttpClientError as exc:
            raise

        return [
            SnapshotItem(self, snapshot)
            for snapshot in response.get('snapshots', [])
        ]

    def create_snapshot(self, **attributes):
        try:
            return self.query().snapshots.post(data=attributes) \
                                         .get('snapshot', {})

        except (slumber.exceptions.HttpServerError,
                slumber.exceptions.HttpClientError) as e:
            if e.response.status_code in (429, 502):
                create_snapshot()
            else:
                logging.error(e.response.text)
                raise e

    def ips(self, **filters):
        try:
            response = self.query().ips.get(**filters)

        except slumber.exceptions.HttpClientError as exc:
            raise

        return [
            IpItem(self, ip)
            for ip in response.get('ips', [])
        ]

    def create_ip(self, **attributes):
        try:
            return self.query().ips.post(data=attributes).get('ip', {})

        except (slumber.exceptions.HttpServerError,
                slumber.exceptions.HttpClientError) as e:
            if e.response.status_code in (429, 502):
                create_ip()
            else:
                logging.error(e.response.text)
                print e
                raise e
