from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ArmorSerializer, WeaponSerializer, SpellSerializer, ItemSerializer
from .models import Armor, Weapon, Spell, Item

ALL_EXCLUDE = ['_state']
ARMOR_EXCLUDE = ALL_EXCLUDE + ['category']
WEAPON_EXCLUDE = ALL_EXCLUDE + ['damage_type', 'weapon_class', 'mastery']
SPELL_EXCLUDE = ALL_EXCLUDE + ['school']
ITEM_EXCLUDE = ALL_EXCLUDE + ['rarity', 'category']

class ArmorView(viewsets.ModelViewSet):
  serializer_class = ArmorSerializer
  queryset = Armor.objects.all()

  def list(self, request):
    # to_exclude = ['_state', 'category']
    all_armors = []
    for armor in Armor.objects.all():
      armor_dict = { key: value for key, value in armor.__dict__.items() if key not in ARMOR_EXCLUDE }
      armor_dict.update({'category': armor.get_category_display()})
      all_armors.append(armor_dict)

    return Response(all_armors)
  
  def retrieve(self, request, *args, **kwargs):
    armor = Armor.objects.get(id=kwargs['pk'])
    armor_dict = { key: value for key, value in armor.__dict__.items() if key not in ARMOR_EXCLUDE }
    armor_dict.update({'category': armor.get_category_display()})
    return Response(armor_dict)

class WeaponView(viewsets.ModelViewSet):
  serializer_class = WeaponSerializer
  queryset = Weapon.objects.all()

  def list(self, request):
    # to_exclude = ['_state', 'damage_type', 'weapon_class', 'mastery']
    all_weapons = []
    for weapon in Weapon.objects.all():
      weapon_dict = { key: value for key, value in weapon.__dict__.items() if key not in WEAPON_EXCLUDE }
      weapon_dict.update(
        {
          
          'damage_type': weapon.get_damage_type_display(),
          'weapon_class': weapon.get_weapon_class_display(),
          'mastery': weapon.get_mastery_display()
        }
      )
      all_weapons.append(weapon_dict)
    
    return Response(all_weapons)
  
  def retrieve(self, request, *args, **kwargs):
    weapon = Weapon.objects.get(id=kwargs['pk'])
    weapon_dict = { key: value for key, value in weapon.__dict__.items() if key not in WEAPON_EXCLUDE }
    weapon_dict.update(
        {
          
          'damage_type': weapon.get_damage_type_display(),
          'weapon_class': weapon.get_weapon_class_display(),
          'mastery': weapon.get_mastery_display()
        }
      )
    return Response(weapon_dict)

class SpellView(viewsets.ModelViewSet):
  serializer_class = SpellSerializer
  queryset = Spell.objects.all()

  def list(self, request):
    # to_exclude = ['_state', 'school']
    all_spells = []
    for spell in Spell.objects.all():
      spell_dict = { key: value for key, value in spell.__dict__.items() if key not in SPELL_EXCLUDE }
      spell_dict.update({'school': spell.get_school_display()})
      all_spells.append(spell_dict)

    return Response(all_spells)
  
  def retrieve(self, request, *args, **kwargs):
    spell = Spell.objects.get(id=kwargs['pk'])
    spell_dict = { key: value for key, value in spell.__dict__.items() if key not in SPELL_EXCLUDE }
    spell_dict.update({'school': spell.get_school_display()})
    return Response(spell_dict)

class ItemView(viewsets.ModelViewSet):
  serializer_class = ItemSerializer
  queryset = Item.objects.all()

  def list(self, request):
    # to_exclude = ['_state', 'rarity', 'category']
    all_items = []
    for item in Item.objects.all():
      item_dict = { key: value for key, value in item.__dict__.items() if key not in ITEM_EXCLUDE }
      item_dict.update(
        {
          'rarity': item.get_rarity_display(),
          'category': item.get_category_display(),
        }
      )
      all_items.append(item_dict)
    
    return Response(all_items)
  
  def retrieve(self, request, *args, **kwargs):
    item = Item.objects.get(id=kwargs['pk'])
    item_dict = { key: value for key, value in item.__dict__.items() if key not in SPELL_EXCLUDE }
    item_dict.update(
      {
        'rarity': item.get_rarity_display(),
        'category': item.get_category_display(),
      }
    )
    return Response(item_dict)

@api_view(['GET'])
def generate_shop(request):
  print(f"data: {request.data}")

  return Response("Test")

