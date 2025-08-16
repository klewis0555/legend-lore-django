from rest_framework import serializers
from .models import Armor, Weapon, Spell, Item

class ArmorSerializer(serializers.ModelSerializer):
  category = serializers.CharField(source='get_category_display')
  class Meta:
    model = Armor
    fields = ('id', 'name', 'price', 'category')

class WeaponSerializer(serializers.ModelSerializer):
  damage_type = serializers.CharField(source='get_damage_type_display')
  weapon_class = serializers.CharField(source='get_weapon_class_display')
  mastery = serializers.CharField(source='get_mastery_display')
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
  school = serializers.CharField(source='get_school_display')
  class Meta:
    model = Spell
    fields = ('id', 'name', 'level', 'school')

class ItemSerializer(serializers.ModelSerializer):
  rarity = serializers.CharField(source='get_rarity_display')
  category = serializers.CharField(source='get_category_display')
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
