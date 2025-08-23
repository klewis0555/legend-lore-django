from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ArmorSerializer, WeaponSerializer, SpellSerializer, ItemSerializer, ShopItemSerializer
from .models import Armor, Weapon, Spell, Item


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
  def get(self, request):
    shop_size = request.query_params.get('shop_size', None)
    shop_type = request.query_params.get('shop_type', None)
    shop_items = generate_random_shop(shop_size, shop_type)
    serializer = ShopItemSerializer(shop_items, many=True)
    return Response(serializer.data)
  
def generate_random_shop(shop_size, shop_type):
  return [Item.objects.get(id=1)]
