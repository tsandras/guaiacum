from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import serializers as rserializers
from django.template.loader import get_template
import json

from editor.models import Character, Advantage, AttributeAdvantage, Attribute, UserProfile, Label, AttributeCharacter
from editor.pages.models import Page
from guaiacum import settings
from querystring_parser import parser

from django.views.decorators.clickjacking import xframe_options_exempt


def home(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    logged_user = request.user
    t = get_template('home.html')
    characters = Character.objects.filter(owner=logged_user)
    pages = Page.objects.all()
    html = t.render({'characters': characters, 'pages': pages, 'user': logged_user})
    return HttpResponse(html)


def editor_new(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    t = get_template('editor.html')
    logged_user = request.user
    html = t.render({'user': logged_user, 'http_host': request.META['HTTP_HOST']})
    return HttpResponse(html)


def editor(request, character_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    t = get_template('editor.html')
    logged_user = request.user

    if character_id:
        character = Character.objects.get(id=character_id)
        advantages = []
        for advantage in character.advantages.all():
            attributes_advantages = AttributeAdvantage.objects.filter(advantage_id=advantage.id)
            aa = AttributeAdvantageSerializer(attributes_advantages, many=True).data
            advantages.append({'name': advantage.name, 'id': advantage.id, 'attribute_advantages': aa})
        attributes_character = AttributeCharacter.objects.filter(character_id=character_id)
    else:
        character = None
        advantages = None
        attributes_character = None
    html = t.render(
        {'user': logged_user,
         'character': character,
         'advantages': advantages,
         'attributes': attributes_character,
         'http_host': request.META['HTTP_HOST']
         }
    )
    return HttpResponse(html)


@xframe_options_exempt
def attributes_phy(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    t = get_template('attribute.html')
    lab = Label.objects.filter(name='Physique').first()
    attributes = Attribute.objects.filter(labels__in=[lab])
    html = t.render({'attributes': attributes})
    return HttpResponse(html)

@xframe_options_exempt
def attributes_men(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    t = get_template('attribute.html')
    lab = Label.objects.filter(name='Mental').first()
    attributes = Attribute.objects.filter(labels__in=[lab])
    html = t.render({'attributes': attributes})
    return HttpResponse(html)


@xframe_options_exempt
def attributes_mag(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    t = get_template('attribute.html')
    lab = Label.objects.filter(name='Magique').first()
    attributes = Attribute.objects.filter(labels__in=[lab])
    html = t.render({'attributes': attributes})
    return HttpResponse(html)


@xframe_options_exempt
def attributes_con(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    t = get_template('attribute.html')
    lab = Label.objects.filter(name='Connaissance').first()
    attributes = Attribute.objects.filter(labels__in=[lab])
    html = t.render({'attributes': attributes})
    return HttpResponse(html)


@xframe_options_exempt
def attributes_com(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    t = get_template('attribute.html')
    lab = Label.objects.filter(name='Compétence').first()
    attributes = Attribute.objects.filter(labels__in=[lab])
    html = t.render({'attributes': attributes})
    return HttpResponse(html)


@xframe_options_exempt
def attributes_his(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    t = get_template('attribute.html')
    lab = Label.objects.filter(name='Historique').first()
    attributes = Attribute.objects.filter(labels__in=[lab])
    html = t.render({'attributes': attributes})
    return HttpResponse(html)


@xframe_options_exempt
def page(request, page_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    t = get_template('page.html')
    page = Page.objects.get(id=page_id)
    user_profile = UserProfile.objects.filter(user=user).first()
    if user_profile is None or page is None:
        return redirect('home')

    character = user_profile.character
    sections = character.get_sections_for(page)
    html = t.render({'character': character, 'sections': sections, 'page': page})
    return HttpResponse(html)


@xframe_options_exempt
def pages(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    t = get_template('pages.html')
    user = request.user
    user_profile = UserProfile.objects.filter(user=user).first()
    if user_profile is None:
        return redirect('home')

    character = user_profile.character
    selected_pages = []
    pages = Page.objects.all()
    for page in pages:
        sections = character.get_sections_for(page)
        if sections:
            page.max_level = len(sections)
            selected_pages.append(page)

    html = t.render({'character': character, 'pages': selected_pages})
    return HttpResponse(html)


def advantages(request):
    advantages = Advantage.objects.filter(name__iregex=r'^.*' + request.GET['q'] + '.*$')
    response_data = serializers.serialize('json', advantages)
    return HttpResponse(response_data, content_type="application/json")


def attributes(request):
    attributes = Attribute.objects.filter(name__iregex=r'^.*' + request.GET['q'] + '.*$')
    response_data = serializers.serialize('json', attributes)
    return HttpResponse(response_data, content_type="application/json")


def save_character(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    character = Character.objects.filter(first_name=request.POST['first_name']).filter(last_name=request.POST['last_name']).first()

    if character is None:
        character = Character.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            nickname=request.POST['nickname'],
            total_pc=request.POST['total_pc'],
            owner_id=user.id
        )
    for advantage_id in request.POST.getlist('advantages[]'):
        character.advantages.add(Advantage.objects.get(id=advantage_id))

    post_dict = parser.parse(request.POST.urlencode())
    AttributeCharacter.objects.filter(character_id=character.id).delete()
    if 'attributes' in post_dict.keys():
        for attribute_id, bonus in post_dict['attributes'].items():
            AttributeCharacter.objects.create(attribute_id=attribute_id, character_id=character.id, bonus=bonus)

    return HttpResponse("Save !", content_type="text/plain")


def delete_advantage(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    character = Character.objects.get(id=request.POST['character_id'])
    advantage = Advantage.objects.get(id=request.POST['advantage_id'])
    character.advantages.remove(advantage)
    return HttpResponse("Delete !", content_type="text/plain")


class AttributeAdvantageSerializer(rserializers.ModelSerializer):
    attribute_name = rserializers.SerializerMethodField()
    attribute_id = rserializers.SerializerMethodField()

    def get_attribute_name(self, obj):
        return obj.attribute.name

    def get_attribute_id(self, obj):
        return obj.attribute.id

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


class AttributeSerializer(rserializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


def advantage(request, advantage_id):
    advantage = Advantage.objects.get(id=advantage_id)
    ser = AdvantageSerializer(advantage)
    return HttpResponse(json.dumps(ser.data), content_type="application/json")


def attribute(request, attribute_id):
    attribute = Attribute.objects.get(id=attribute_id)
    ser = AttributeSerializer(attribute)
    return HttpResponse(json.dumps(ser.data), content_type="application/json")