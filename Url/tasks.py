from datetime import timedelta, datetime

from Url.models import Url
import logging

from User.models import User
from short_urls.celery import app

log = logging.getLogger('my_logger')

OLD_TASK_DATE = datetime.now() - timedelta(days=7)


def remove_url(pk: int):
    try:
        Url.objects.get(pk).delete()
    except Url.DoesNotExist as e:
        log.error('Can not delete url with id = {}. {}'. format(pk, e))
        return
    except Exception as e:
        log.error('Some what wrong. {}'. format(e))
        return


@app.task
def remove_old_url_starter():
    log.info('Start task remove_old_url')
    for url in Url.objects.filter(created_at__lt=OLD_TASK_DATE):
        remove_url(url.pk)
