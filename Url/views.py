from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR

from User.models import User
from .models import Url
from .serializers import UrlSerializer
from rest_framework.views import APIView
import logging
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

log = logging.getLogger('my_logger')


class UrlView(APIView):
    """
    API endpoint для Url.
    """

    @permission_classes([AllowAny])
    def get(self, request, pk=None):
        session = request.query_params.get('session')
        if session is None:
            return Response({'error': 'Session not found'}, status=HTTP_400_BAD_REQUEST)
        user = None
        try:
            user = User.objects.get(session_id=session)
        except User.DoesNotExist as e:
            log.error('User not found by session')
            return Response({'error': 'User not found by session'}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            log.error(e)
            return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        if pk is not None:
            key = 'url'
            log.info('Trying to get url by pk = {}'.format(pk))
            try:
                url = Url.objects.get(pk=pk)
                result = UrlSerializer(url).data
            except Url.DoesNotExist as e:
                log.error(str(e))
                return Response({'error': str(e)}, status=HTTP_200_OK)
            except Exception as e:
                log.error(e)
                return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({key: result})
        else:
            key = 'urls'
            if 'urls_{}'.format(session) in cache:
                log.info('Get urls from cache')
                return Response(cache.get('urls'), status=HTTP_200_OK)
            else:
                log.info('Trying to get all urls')
                try:
                    urls = Url.objects.prefetch_related('user').filter(user__id=user.id)
                    result = UrlSerializer(urls, many=True).data
                    cache.set('urls', result, timeout=CACHE_TTL)
                except Exception as e:
                    log.error(e)
                    return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

                return Response({key: result}, status=HTTP_200_OK, headers={'Content-type': 'application/json'})

    def post(self, request):
        log.info('Try to create new url')
        key = 'short'
        message = ''
        status = HTTP_201_CREATED
        try:
            serializer = UrlSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                url = serializer.save()
                message = url.short
                cache.delete('urls_{}'.format(url.user.session_id))
        except ValidationError as e:
            status = HTTP_400_BAD_REQUEST
            message = e
            key = 'error'
        except Exception as e:
            status = HTTP_500_INTERNAL_SERVER_ERROR
            message = e
            key = 'error'
        if status is not HTTP_201_CREATED:
            log.error(message)

        return Response({key: message}, status=status)

    def put(self, request, pk):
        log.info('Try to update url by pk = {}'.format(pk))
        key = 'success'
        status = HTTP_200_OK
        message = 'Url {} updated successfully'.format(pk)
        try:
            url = Url.objects.get(pk=pk)
            serializer = UrlSerializer(instance=url, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                cache.delete('urls_{}'.format(url.user.session_id))
        except ValidationError as e:
            key = 'error'
            message = e
            status = HTTP_400_BAD_REQUEST
        except Url.DoesNotExist as e:
            key = 'error'
            message = e
            status = HTTP_404_NOT_FOUND
        except Exception as e:
            key = 'error'
            message = e
            status = HTTP_500_INTERNAL_SERVER_ERROR
        if status is not HTTP_200_OK:
            log.error(message)

        return Response({key: message}, status=status)

    def delete(self, request, pk):
        log.info('Try to delete url by id = {}'.format(pk))
        key = 'success'
        status = HTTP_200_OK
        message = 'Url with id `{}` has been deleted.'.format(pk)
        try:
            url = Url.objects.get(pk=pk)
            session = url.user.session_id
            url.delete()
            cache.delete('urls_{}'.format(session))
        except Url.DoesNotExist as e:
            key = 'error'
            message = e
            status = HTTP_404_NOT_FOUND
        except Exception as e:
            key = 'error'
            message = e
            status = HTTP_500_INTERNAL_SERVER_ERROR
        if status is not HTTP_200_OK:
            log.error(e)

        return Response({key: message}, status=status)