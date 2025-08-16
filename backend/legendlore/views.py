from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ArmorSerializer, WeaponSerializer, SpellSerializer, ItemSerializer
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
