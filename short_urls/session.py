import random
import string

from django.utils.deprecation import MiddlewareMixin


class SessionMiddleware(MiddlewareMixin):
    """Сохраняем сгенеированный ключ в сессию """

    def process_request(self, request):
        """Генерируем случайный набор сиволов и записываем в сессию"""
        lettersAndDigits = string.ascii_letters + string.digits
        session_id = ''.join((random.choice(lettersAndDigits) for i in range(50)))

        if not request.session.get('session_id') :
            request.session['session_id'] = session_id

        return None
