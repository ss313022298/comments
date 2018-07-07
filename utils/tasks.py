
import logging
from django.core import signals
from celery.decorators import task
from django.core.cache import cache


logger = logging.getLogger("default")


WAIT_DURATION = (
    60, 10 * 60, 20 * 60, 30 * 60, 1 * 60 * 60, 3 *60 * 60,
    5 * 60 * 60, 14 * 60 * 60, 24 * 60 * 60
)


@task()
def start_notify(sender, module, handle, param):
    _module = __import__(module, globals(), locals(), ['*'])
    if not getattr(_module, handle):
        return
    func = getattr(_module, handle)
    try:
        signals.request_started.send(sender=sender)
        if not func(param):
            raise Exception('%s.%s run fail' % (module, handle))
        logger.debug('%s.%s run success' % (module, handle))
        return True
    except BaseException as exc:
        logger.exception(exc)
        raise start_notify.retry(
            countdown=get_countdown(sender), max_retries=9, exc=exc)
    finally:
        signals.request_finished.send(sender=sender)


def get_countdown(sender):
    count = cache.get('start_notify_%s' % sender)
    if count is None:
        count = 0
    else:
        count = int(count) + 1
    cache.set('start_notify_%s' % sender, count, WAIT_DURATION[count] + 60)
    return WAIT_DURATION[count]
