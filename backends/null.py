#!/usr/bin/env python

import logging

import backends

LOG = logging.getLogger('backend.driver')


class NullBackend(backends.ConfigurationBackend):
    def __init__(self, config):
        LOG.debug('initializing null backend')
        self.config = config

    def get_cluster_settings(self, cluster_name):
        pass

    def set_cluster_settings(self, cluster_name, settings):
        pass

    def get_node_settings(self, node_name):
        pass

    def set_node_settings(self, node_name, settings):
        pass

    def add_node_to_cluster(self, node_name, cluster_name):
        pass

    def set_node_role(self, node_name, role_name):
        pass