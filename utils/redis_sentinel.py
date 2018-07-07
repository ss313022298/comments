# encoding:utf-8
from django.conf import settings
from redis.sentinel import Sentinel

sentinel = None
_cached_master_client = None
_cached_slave_client = None


def get_redis_conn(readonly=False):
    global sentinel, _cached_master_client, _cached_slave_client
    if not sentinel:
        sentinel = Sentinel(settings.REDIS_SENTINEL, socket_timeout=0.1)
    if not _cached_master_client:
        _cached_master_client = sentinel.master_for(
            settings.REDIS_SNS_CLUSTER_NAME)
    if not _cached_slave_client:
        _cached_slave_client = sentinel.slave_for(
            settings.REDIS_SNS_CLUSTER_NAME)
    return _cached_slave_client if readonly else _cached_master_client
