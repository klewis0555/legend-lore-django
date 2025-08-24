# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand
from ...references import ARMOR, WEAPONS, SPELLS, ITEMS
from ...models import *
import random

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

""" Create objects without clearing data """
MODE_SEED = 'seed'

class Command(BaseCommand):
  help = "seed database for testing and development."

  def add_arguments(self, parser):
    parser.add_argument('--mode', type=str, help="Mode")

  def handle(self, *args, **options):
    self.stdout.write('seeding data...')
    run_seed(self, options['mode'] or MODE_SEED)
    self.stdout.write('done.')


def clear_data():
  """Deletes all the table data"""
  print("Delete Armor instances")
  Armor.objects.all().delete()
  print("Delete Weapon instances")
  Weapon.objects.all().delete()
  print("Delete Spell instances")
  Spell.objects.all().delete()
  print("Delete Item instances")
  Item.objects.all().delete()

def create_armors():
  print("Creating Armors")
  for armor in ARMOR:
    Armor.objects.create(name=armor['name'], price=armor['price'], category=armor['category'])

def create_weapons():
  print("Creating Weapons")
  for weapon in WEAPONS:
    Weapon.objects.create(
      name=weapon['name'],
      price=weapon['price'],
      damage_type=weapon['damage_type'],
      weapon_class=weapon['weapon_class'],
      martial=weapon['martial'],
      ranged=weapon['ranged'],
      mastery=weapon['mastery'],
      ammunition=weapon['ammunition'],
      finesse=weapon['finesse'],
      heavy=weapon['heavy'],
      light=weapon['light'],
      loading=weapon['loading'],
      reach=weapon['reach'],
      thrown=weapon['thrown'],
      two_handed=weapon['two_handed'],
      versatile=weapon['versatile']
    )

def create_spells():
  print("Creating Spells")
  for spell in SPELLS:
    Spell.objects.create(name=spell['name'], level=spell['level'], school=spell['school'])

def create_items():
  print("Creating Items")
  for item in ITEMS:
    Item.objects.create(
      name=item['name'],
      price=item['price'],
      attunement=item['attunement'],
      rarity=item['rarity'],
      category=item['category'],
    )
    item_object=Item.objects.get(name=item['name'])
    item['armor_query'] != None and item_object.armor_options.set(Armor.objects.filter(item['armor_query']))
    item['weapon_query'] != None and item_object.weapon_options.set(Weapon.objects.filter(item['weapon_query']))
    item['spell_query'] != None and item_object.spell_options.set(Spell.objects.filter(item['spell_query']))
    


def run_seed(self, mode=MODE_SEED):
  """ Seed database based on mode

  :param mode: refresh / clear / seed (default)
  :return:
  """
  # Clear data from tables
  if mode == MODE_CLEAR or mode == MODE_REFRESH:
      clear_data()
  
  if mode == MODE_REFRESH or mode == MODE_SEED:
    create_armors()
    create_weapons()
    create_spells()
    create_items()
