from django.contrib import admin
from .models import Armor, Weapon, Spell, Item

class ArmorAdmin(admin.ModelAdmin):
  list_display = ('name', 'price', 'category')

class WeaponAdmin(admin.ModelAdmin):
  list_display = (
    'name',
    'price',
    'damage_type',
    'weapon_class',
    'mastery',
    'martial',
    'ranged',
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

class SpellAdmin(admin.ModelAdmin):
  list_display = ('name', 'level', 'school')

class ItemAdmin(admin.ModelAdmin):
  list_display = ('name', 'price', 'attunement', 'rarity', 'category')

# Register your models here.

admin.site.register(Armor, ArmorAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Spell, SpellAdmin)
admin.site.register(Item, ItemAdmin)
