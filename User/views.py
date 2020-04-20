from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_500_INTERNAL_SERVER_ERROR


from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
import logging
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

log = logging.getLogger('my_logger')


class UserView(APIView):
    """
    API endpoint для User.
    """

    def get(self, request, pk=None):
        status = HTTP_200_OK
        if pk is not None:
            key = 'user'
            try:
                user = User.objects.get(pk=pk)
                message = UserSerializer(user).data
            except User.DoesNotExist as e:
                key = 'error'
                message = e
                status = HTTP_404_NOT_FOUND
            except Exception as e:
                key = 'error'
                message = e
                status = HTTP_500_INTERNAL_SERVER_ERROR

            return Response({key: message}, status=status)
        else:
            key = 'users'
            if 'users' in cache:
                return Response(cache.get('users'), status=HTTP_200_OK)
            else:
                users = User.objects.all()
                try:
                    message = UserSerializer(users, many=True).data
                    cache.set('users', message, timeout=CACHE_TTL)
                except Exception as e:
                    key = 'error'
                    message = e
                    status = HTTP_500_INTERNAL_SERVER_ERROR
                if status is not HTTP_200_OK:
                    log.error(message)

                return Response({key: message}, status=status)

    def post(self, request):
        key = 'id'
        status = HTTP_201_CREATED
        message = ''
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                message = user.id
                cache.delete('users')
        except ValidationError as e:
            key = 'error'
            status = HTTP_400_BAD_REQUEST
            message = e
        except Exception as e:
            key = 'error'
            status = HTTP_500_INTERNAL_SERVER_ERROR
            message = e
        if status is not HTTP_201_CREATED:
            log.error(message)

        return Response({key: message}, status=status)

    def put(self, request, pk):
        key = 'success'
        status = HTTP_200_OK
        message = 'Record with id: {}, updated'.format(pk)
        try:
            saved_user = User.objects.get(pk=pk)
            serializer = UserSerializer(instance=saved_user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                cache.delete('users')
        except User.DoesNotExist as e:
            key = 'error'
            status = HTTP_404_NOT_FOUND
            message = e
        except ValidationError as e:
            key = 'error'
            status = HTTP_400_BAD_REQUEST
            message = e
        except Exception as e:
            key = 'error'
            status = HTTP_500_INTERNAL_SERVER_ERROR
            message = e
        if status is not HTTP_200_OK:
            log.error(message)

        return Response({key: message}, status=status)

    def delete(self, request, pk):
        key = 'success'
        status = HTTP_200_OK
        message = 'Record with id: {}, delete'.format(pk)

        try:
            user = User.objects.get(pk=pk)
            user.delete()
            cache.delete('users')
        except User.DoesNotExist as e:
            key = 'error'
            status = HTTP_404_NOT_FOUND
            message = e
        except Exception as e:
            key = 'error'
            status = HTTP_500_INTERNAL_SERVER_ERROR
            message = e
        if status is not HTTP_200_OK:
            log.error(message)

        return Response({key: message}, status=status)
