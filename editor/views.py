from django.core import serializers
from django.http import HttpResponse
from rest_framework import serializers as rserializers
from django.template.loader import get_template
import datetime
import json

from editor.models import Character, Advantage, AttributeAdvantage, Attribute


def home(request):
    now = datetime.datetime.now()
    logged_user = request.user
    t = get_template('home.html')
    characters = Character.objects.filter(owner=logged_user)
    html = t.render({'characters': characters, 'current_date': now, 'user': logged_user})
    return HttpResponse(html)


def editor(request):
    t = get_template('editor.html')
    logged_user = request.user
    html = t.render({'user': logged_user})
    return HttpResponse(html)


def advantages(request):
    advantages = Advantage.objects.filter(name__iregex=r'^.*' + request.GET['q'] + '.*$')
    print(advantages)
    response_data = serializers.serialize('json', advantages)
    return HttpResponse(response_data, content_type="application/json")


class AttributeAdvantageSerializer(rserializers.ModelSerializer):
    attribute_name = rserializers.SerializerMethodField()

    def get_attribute_name(self, obj):
        return obj.attribute.name

    class Meta:
        model = AttributeAdvantage
        exclude = ('id',)


class AdvantageSerializer(rserializers.ModelSerializer):
    bonuses = rserializers.SerializerMethodField()

    class Meta:
        model = Advantage
        fields = ('name', 'tier', 'cost', 'description', 'bonuses', 'conditions')

    def get_bonuses(self, obj):
        attributes_advantages = AttributeAdvantage.objects.filter(advantage_id=obj.id)
        print(AttributeAdvantageSerializer(attributes_advantages, many=True))
        return AttributeAdvantageSerializer(attributes_advantages, many=True).data


def advantage(request, advantage_id):
    advantage = Advantage.objects.get(id=advantage_id)
    ser = AdvantageSerializer(advantage)
    return HttpResponse(json.dumps(ser.data), content_type="application/json")