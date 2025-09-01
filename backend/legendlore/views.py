from django.shortcuts import render
from itertools import chain
from random import random, randint, choice, choices
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ArmorSerializer, WeaponSerializer, SpellSerializer, ItemSerializer, ShopItemSerializer
from .models import Armor, Weapon, Spell, Item
from .references import NOUNS, ADJECTIVES


class ArmorView(viewsets.ModelViewSet):
  serializer_class = ArmorSerializer
  queryset = Armor.objects.all()

class WeaponView(viewsets.ModelViewSet):
  serializer_class = WeaponSerializer
  queryset = Weapon.objects.all()

class SpellView(viewsets.ModelViewSet):
  serializer_class = SpellSerializer
  queryset = Spell.objects.all()

class ItemView(viewsets.ModelViewSet):
  serializer_class = ItemSerializer
  queryset = Item.objects.all()

class ShopView(APIView):
  VALID_SHOP_SIZES = ["extra_small", "small", "medium", "large", "extra_large"]
  VALID_SHOP_TYPES = [ "GEN", "ARM", "AMM", "CLS", "CLO", "CON", "JWL", "SCR", "TAT", "WND", "WPN"]

  def get(self, request):
    shop_size = request.query_params.get('shop_size', None)
    shop_type = request.query_params.get('shop_type', None)

    errors = {}
    if shop_size not in self.VALID_SHOP_SIZES:
      errors['shop_size'] = f"Invalid value '{shop_size}'. Must be one of {self.VALID_SHOP_SIZES}."
    if shop_type not in self.VALID_SHOP_TYPES:
      errors['shop_type'] = f"Invalid value '{shop_type}'. Must be one of {self.VALID_SHOP_TYPES}."

    if errors:
      return Response({'errors': errors}, status=400)

    shop_items = generate_random_shop(shop_size, shop_type)

    # Group items by rarity
    grouped = {
      'mundane_items': [item for item in shop_items if item.rarity == 'M'],
      'common_items': [item for item in shop_items if item.rarity == 'C'],
      'uncommon_items': [item for item in shop_items if item.rarity == 'U'],
      'rare_items': [item for item in shop_items if item.rarity == 'R'],
      'very_rare_items': [item for item in shop_items if item.rarity == 'V'],
      'legendary_items': [item for item in shop_items if item.rarity == 'L'],
    }
    # Serialize each group
    data = {
      key: ShopItemSerializer(items, many=True).data
      for key, items in grouped.items()
    }

    # need to check duplicates / quantities
    sanitized_items = {
      'mundane_items': [],
      'common_items': [],
      'uncommon_items': [],
      'rare_items': [],
      'very_rare_items': [],
      'legendary_items': [],
    }
    for rarity, items in data.items():
      for item in items:
        try:
          next(i for i in sanitized_items[rarity] if i['item_name'] == item['item_name'])['quantity'] += item['quantity']
        except StopIteration:
          sanitized_items[rarity].append(item)

    return Response(sanitized_items)
  
def generate_random_shop(shop_size: str, shop_type: str):
  if shop_type == "GEN":
    items = Item.objects.all()
  else:
    items = Item.objects.filter(category=shop_type)

  common_and_mundane_items = [i for i in items if i.rarity == "C" or i.rarity == "M"]
  uncommon_items = [i for i in items if i.rarity == "U"]
  rare_items = [i for i in items if i.rarity == "R"]
  very_rare_items = [i for i in items if i.rarity == "V"]
  legendary_items = [i for i in items if i.rarity == "L"]

  shop_items = []
  
  match shop_size:
    case "extra_small":
      common_and_mundane_count = randint(5,10)
      uncommon_count = randint(1,4)
      rare_count = int(random() <= 0.3333)
      very_rare_count = 0
      legendary_count = 0
    case "small":
      common_and_mundane_count = randint(6,12)
      uncommon_count = randint(4,8)
      rare_count = randint(0,3)
      very_rare_count = int(random() <= 0.3333)
      legendary_count = 0
    case "medium":
      common_and_mundane_count = randint(8,16)
      uncommon_count = randint(6,12)
      rare_count = randint(2,8)
      very_rare_count = randint(0,2)
      legendary_count = 0
    case "large":
      common_and_mundane_count = randint(10,20)
      uncommon_count = randint(10,15)
      rare_count = randint(8,14)
      very_rare_count = randint(2,6)
      legendary_count = int(random() <= 0.3333)
    case "extra_large":
      common_and_mundane_count = randint(12,25)
      uncommon_count = randint(10,15)
      rare_count = randint(12,20)
      very_rare_count = randint(6,12)
      legendary_count = randint(1,5)
  
  if len(common_and_mundane_items) > 0:
    shop_items.extend(choices(common_and_mundane_items, k=common_and_mundane_count))
  if len(uncommon_items) > 0:
    shop_items.extend(choices(uncommon_items, k=uncommon_count))
  if len(rare_items) > 0:
    shop_items.extend(choices(rare_items, k=rare_count))
  if len(very_rare_items) > 0:
    shop_items.extend(choices(very_rare_items, k=very_rare_count))
  if len(legendary_items) > 0:
    shop_items.extend(choices(legendary_items, k=legendary_count))

  return sorted(shop_items)

@api_view(['GET'])
def shop_name_view(request):
  return Response(f"The {choice(ADJECTIVES)} {choice(NOUNS)}")
