from User.models import User
from .models import Url, Hit
from rest_framework import serializers


class UrlSerializer(serializers.ModelSerializer):
    session = serializers.CharField()
    ip = serializers.CharField(required=False)
    user_agent = serializers.CharField(required=False)
    referer = serializers.CharField(required=False)
    class Meta:
        model = Url
        fields = '__all__'

    def to_representation(self, obj):
        result = super().to_representation(obj)
        result.pop('session')
        result.pop('ip')
        result.pop('user_agent')
        result.pop('referer')

        return result

    def create(self, validated_data):
        session = validated_data.pop('session', None)
        ip = validated_data.pop('ip', None)
        user_agent = validated_data.pop('user_agent', None)
        referer = validated_data.pop('referer', None)

        url = Url.objects.create(**validated_data)
        if session is not None:
            user, created = User.objects.get_or_create(session_id=session)
            url.user = user
            url.save()
        hit = {'url': url}
        if ip is not None:
            hit['ip'] = ip
        if user_agent is not None:
            hit['user_agent'] = user_agent
        if referer is not None:
            hit['referer'] = referer
        if len(hit) > 1:
            Hit.objects.create(**hit)
        return url

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.short = validated_data.get('short', instance.short)
        instance.full = validated_data.get('full', instance.full)
        instance.save()

        return instance
