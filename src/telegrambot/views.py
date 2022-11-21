from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from telegrambot.models import TgUser
from telegrambot.serializers import TgUserSerializer
from telegrambot.tg.client import TgClient
from todolist import settings


# Create your views here.
class VerificationView(GenericAPIView):
    model = TgUser
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        s: TgUserSerializer = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)

        tg_user: TgUser = s.validated_data['tg_user']
        tg_user.user = self.request.user
        tg_user.save(update_fields=('user',))

        instance_s: TgUserSerializer = self.get_serializer(tg_user)
        TgClient(settings.BOT_TOKEN).send_message(tg_user.chat_id, 'верификация успешна')
        return Response(instance_s.data)