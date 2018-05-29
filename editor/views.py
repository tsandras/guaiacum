from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import serializers as rserializers
from django.template.loader import get_template
import json

from editor.models import Character, Advantage, AttributeAdvantage, Attribute
from guaiacum import settings


def home(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    logged_user = request.user
    t = get_template('home.html')
    characters = Character.objects.filter(owner=logged_user)
    html = t.render({'characters': characters, 'user': logged_user})
    return HttpResponse(html)


def editor(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    t = get_template('editor.html')
    logged_user = request.user
    html = t.render({'user': logged_user})
    return HttpResponse(html)


def advantages(request):
    advantages = Advantage.objects.filter(name__iregex=r'^.*' + request.GET['q'] + '.*$')
    response_data = serializers.serialize('json', advantages)
    return HttpResponse(response_data, content_type="application/json")


def save_character(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    character = Character.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        nickname=request.POST['nickname'],
        total_pc=request.POST['total_pc'],
        owner_id=user.id
    )
    for advantage_id in request.POST.getlist('advantages[]'):
        character.advantages.add(Advantage.objects.get(id=advantage_id))
    return HttpResponse("Save !", content_type="text/plain")


class AttributeAdvantageSerializer(rserializers.ModelSerializer):
    attribute_name = rserializers.SerializerMethodField()

    def get_attribute_name(self, obj):
        return obj.attribute.name

    class Meta:
        model = AttributeAdvantage
        fields = '__all__'


class AdvantageSerializer(rserializers.ModelSerializer):
    bonuses = rserializers.SerializerMethodField()

    class Meta:
        model = Advantage
        fields = ('id', 'name', 'tier', 'cost', 'description', 'bonuses', 'conditions')

    def get_bonuses(self, obj):
        attributes_advantages = AttributeAdvantage.objects.filter(advantage_id=obj.id)
        return AttributeAdvantageSerializer(attributes_advantages, many=True).data


def advantage(request, advantage_id):
    advantage = Advantage.objects.get(id=advantage_id)
    ser = AdvantageSerializer(advantage)
    return HttpResponse(json.dumps(ser.data), content_type="application/json")