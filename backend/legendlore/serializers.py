import random
from rest_framework import serializers
from .models import Armor, Weapon, Spell, Item

class ArmorSerializer(serializers.ModelSerializer):
  armor_category = serializers.CharField(source='get_category_display', read_only=True)
  category = serializers.CharField(write_only=True)

  class Meta:
    model = Armor
    fields = ('id', 'name', 'price', 'category', 'armor_category')

class WeaponSerializer(serializers.ModelSerializer):
  damage_type = serializers.CharField(write_only=True)
  damage = serializers.CharField(source='get_damage_type_display', read_only=True)
  weapon_class = serializers.CharField(write_only=True)
  weapon_type = serializers.CharField(source='get_weapon_class_display', read_only=True)
  mastery = serializers.CharField(write_only=True)
  weapon_mastery = serializers.CharField(source='get_mastery_display', read_only=True)

  class Meta:
    model = Weapon
    fields = (
      'id',
      'name',
      'price',
      'damage_type',
      'damage',
      'weapon_class',
      'weapon_type',
      'martial',
      'ranged',
      'mastery',
      'weapon_mastery',
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
  school_of_magic = serializers.CharField(source='get_school_display', read_only=True)
  school = serializers.CharField(write_only=True)

  class Meta:
    model = Spell
    fields = ('id', 'name', 'level', 'school', 'school_of_magic')

class ItemSerializer(serializers.ModelSerializer):
  item_category = serializers.CharField(source='get_category_display', read_only=True)
  category = serializers.CharField(write_only=True)
  item_rarity = serializers.CharField(source='get_rarity_display', read_only=True)
  rarity = serializers.CharField(write_only=True)

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
      'item_rarity',
      'category',
      'item_category',
      'armor_options',
      'weapon_options',
      'spell_options'
    )

class ShopItemSerializer(serializers.ModelSerializer):
  item_name = serializers.SerializerMethodField()
  category = serializers.SerializerMethodField()
  random_price = serializers.SerializerMethodField()
  quantity = serializers.SerializerMethodField()
  
  class Meta:
    model = Item
    fields = ['item_name', 'random_price', 'category', 'attunement', 'quantity']
  
  def to_representation(self, instance: Item):
    options = None
    if instance.armor_options.exists():
      options = instance.armor_options.all()
    elif instance.weapon_options.exists():
      options = instance.weapon_options.all()
    elif instance.spell_options.exists():
      options = instance.spell_options.all()
    
    self._random_option = random.choice(options) if options is not None else None
    return super().to_representation(instance)
  
  def get_item_name(self, obj: Item):
    return obj.name.replace('___', self._random_option.name) if self._random_option else obj.name

  def get_category(self, obj: Item):
    return obj.get_category_display()
  
  def get_random_price(self, obj: Item):
    min_price = int(obj.price * 0.75)
    max_price = int(obj.price * 1.25)
    random_price = random.randint(min_price, max_price)
    if self._random_option and hasattr(self._random_option, 'price'):
      random_price += self._random_option.price # if the item has an armor or weapon option, add its price
      if type(self._random_option) == Weapon and self._random_option.ranged:
        random_price *= 1.25 # if the weapon is ranged, increase price by 25%
        if self._random_option.weapon_class == "FRM":
          random_price *= 1.5 # if the weapon is a firearm, increase price by 50%
    
    return int(random_price)
  
  def get_quantity(self, obj: Item):
    return random.randint(1, 5) if obj.category in ["CON", "AMM"] else 1