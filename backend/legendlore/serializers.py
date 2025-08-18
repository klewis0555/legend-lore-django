from rest_framework import serializers
from .models import Armor, Weapon, Spell, Item

class ArmorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Armor
    fields = ('id', 'name', 'price', 'category')

class WeaponSerializer(serializers.ModelSerializer):
  class Meta:
    model = Weapon
    fields = (
      'id',
      'name',
      'price',
      'damage_type',
      'weapon_class',
      'martial',
      'ranged',
      'mastery',
      'ammunition',
      'finesse',
      'heavy',
      'light',
      'loading',
      'reach',
      'thrown',
      'two_handed',
      'versatile'
    )

class SpellSerializer(serializers.ModelSerializer):
  class Meta:
    model = Spell
    fields = ('id', 'name', 'level', 'school')

class ItemSerializer(serializers.ModelSerializer):
  armor_options = serializers.SlugRelatedField(
    many=True,
    slug_field='name',
    queryset=Armor.objects.all(),
    allow_null=True
  )

  weapon_options = serializers.SlugRelatedField(
    many=True,
    slug_field='name',
    queryset=Weapon.objects.all(),
    allow_null=True
  )

  spell_options = serializers.SlugRelatedField(
    many=True,
    slug_field='name',
    queryset=Spell.objects.all(),
    allow_null=True
  )

  class Meta:
    model = Item
    fields = (
      'id',
      'name',
      'price',
      'attunement',
      'rarity',
      'category',
      'armor_options',
      'weapon_options',
      'spell_options'
    )
