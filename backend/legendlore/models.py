from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Armor(models.Model):
  # Choice Definitions
  class ArmorCategory(models.TextChoices):
    LIGHT =  "LIT", _("Light")
    MEDIUM = "MED", _("Medium")
    HEAVY =  "HEV", _("Heavy")
    SHIELD = "SHL", _("Shield")

  # Class Attributes
  name = models.CharField(max_length=120, unique=True)
  price = models.IntegerField()
  category = models.CharField(
    max_length = 3,
    choices = ArmorCategory,
    default = ArmorCategory.LIGHT
  )
  
  def __str__(self):
    suffix = ""
    if self.category!='SHL' and self.name!='Breastplate' and 'Chain' not in self.name and 'Mail' not in self.name:
      suffix = " Armor" 
    return f"{self.name}{suffix}"
  def __repr__(self):
    return f"{self.name}"

  def is_light(self):
    return self.category == self.ArmorCategory.LIGHT

  def is_medium(self):
    return self.category == self.ArmorCategory.MEDIUM

  def is_heavy(self):
    return self.category == self.ArmorCategory.HEAVY

class Weapon(models.Model):
  # Choice Definitions
  class WeaponDamage(models.TextChoices):
    BLUDGEONING = "BLG", _("Bludgeoning")
    PIERCING =    "PRC", _("Piercing")
    SLASHING =    "SLA", _("Slashing")
  class WeaponClass(models.TextChoices):
    AXE =       "AXE", _("Axe")
    BLOWGUN =   "BLG", _("Blowgun")
    BLUNT =     "BLN", _("Blunt")
    BOOMERANG = "BMG", _("Boomerang")
    BOW =       "BOW", _("Bow")
    CROSSBOW =  "CSB", _("Crossbow")
    DAGGER =    "DGR", _("Dagger")
    DART =      "DRT", _("Dart")
    FIREARM =   "FRM", _("Firearm")
    LANCE =     "LAN", _("Lance")
    PICK =      "PIC", _("Pick")
    POLEARM =   "PLM", _("Polearm")
    SICKLE =    "SKL", _("Sickle")
    SLING =     "SLN", _("Sling")
    SPEAR =     "SPR", _("Spear")
    SWORD =     "SWD", _("Sword")
    WHIP =      "WHP", _("Whip")
  class WeaponMastery(models.TextChoices):
    CLEAVE = "CLV", _("Cleave")
    GRAZE =  "GRZ", _("Graze")
    NICK =   "NIC", _("Nick")
    PUSH =   "PSH", _("Push")
    SAP =    "SAP", _("Sap")
    SLOW =   "SLW", _("Slow")
    TOPPLE = "TPL", _("Topple")
    VEX =    "VEX", _("Vex")

  # Class Attributes
  name = models.CharField(max_length=120, unique=True)
  price = models.IntegerField()
  damage_type = models.CharField(
    max_length = 3,
    choices = WeaponDamage,
    default = WeaponDamage.BLUDGEONING
  )
  weapon_class = models.CharField(
    max_length = 3,
    choices = WeaponClass,
    default = WeaponDamage.BLUDGEONING
  )
  martial = models.BooleanField(default=False)
  ranged = models.BooleanField(default=False)
  mastery = models.CharField(
    max_length = 3,
    choices = WeaponMastery,
    default = WeaponMastery.CLEAVE
  )
  # Weapon Properties
  ammunition = models.BooleanField(default=False)
  finesse = models.BooleanField(default=False)
  heavy = models.BooleanField(default=False)
  light = models.BooleanField(default=False)
  loading = models.BooleanField(default=False)
  reach = models.BooleanField(default=False)
  thrown = models.BooleanField(default=False)
  two_handed = models.BooleanField(default=False)
  versatile = models.BooleanField(default=False)
  
  def __str__(self):
    return f"{self.name} ({'Martial' if self.martial else 'Simple'} {'Ranged' if self.ranged else 'Melee'} Weapon)"
  def __repr__(self):
    return f"{self.name}"
  
  def get_properties(self):
    properties = []
    if self.ammunition:
      properties.append("Ammunition")
    if self.finesse:
      properties.append("Finesse")
    if self.heavy:
      properties.append("Heavy")
    if self.light:
      properties.append("Light")
    if self.loading:
      properties.append("Loading")
    if self.reach:
      properties.append("Reach")
    if self.thrown:
      properties.append("Thrown")
    if self.two_handed:
      properties.append("Two Handed")
    if self.versatile:
      properties.append("Versatile")
    return properties
  
class Spell(models.Model):
  # Choice Definitions
  class SpellLevel(models.IntegerChoices):
    CANTRIP = 0, _("Cantrip")
    FIRST =   1, _("1st")
    SECOND =  2, _("2nd")
    THIRD =   3, _("3rd")
    FOURTH =  4, _("4th")
    FIFTH =   5, _("5th")
    SIXTH =   6, _("6th")
    SEVENTH = 7, _("7th")
    EIGHTH =  8, _("8th")
    NINTH =   9, _("9th")
  class SpellSchool(models.TextChoices):
    ABJURATION =    "ABJ", _("Abjuration")
    CONJURATION =   "CON", _("Conjuration")
    DIVINATION =    "DIV", _("Divination")
    ENCHANTMENT =   "ENC", _("Enchantment")
    EVOCATION =     "EVO", _("Evocation")
    ILLUSION =      "ILL", _("Illusion")
    NECROMANCY =    "NEC", _("Necromancy")
    TRANSMUTATION = "TRA", _("Transmutation")

  # Class Attributes
  name = models.CharField(max_length=120, unique=True)
  level = models.IntegerField(
    choices = SpellLevel,
    default = SpellLevel.CANTRIP
  )
  school = models.CharField(
    max_length = 3,
    choices = SpellSchool,
    default = SpellSchool.EVOCATION
  )

  def __str__(self):
    string = ""
    if self.level > 0:
      string = f"{self.name} ({self.get_level_display()} level {self.get_school_display()})"
    else:
      string = f"{self.name} ({self.get_school_display()} {self.get_level_display()})"
    return string
  def __repr__(self):
    return self.name

class Item(models.Model):
  # Choice Definitions
  class ItemRarity(models.TextChoices):
    MUNDANE =   "M", _("Mundane")
    COMMON =    "C", _("Common")
    UNCOMMON =  "U", _("Uncommon")
    RARE =      "R", _("Rare")
    VERY_RARE = "V", _("Very Rare")
    LEGENDARY = "L", _("Legendary")
    ARTIFACT =  "A", _("Artifact")
  class ItemCategory(models.TextChoices):
    WONDROUS_ITEM = "WON", _("Wondrous Item")
    ARMOR =         "ARM", _("Armor")
    AMMUNITION =    "AMM", _("Ammunition")
    CLASS_ITEM =    "CLS", _("Class Item")
    CLOTHING =      "CLO", _("Clothing")
    CONSUMABLE =    "CON", _("Consumable")
    JEWELRY =       "JWL", _("Jewelry")
    SPELL_SCROLL =  "SCR", _("Spell Scroll")
    TATTOO =        "TAT", _("Tattoo")
    WAND_STAFF =    "WND", _("Wand/Staff")
    WEAPON =        "WPN", _("Weapon")

  # Class Attributes
  name = models.CharField(max_length=240, unique=True)
  price = models.IntegerField()
  attunement = models.BooleanField(default=False)
  rarity = models.CharField(
    max_length = 1,
    choices = ItemRarity,
    default = ItemRarity.COMMON
  )
  category = models.CharField(
    max_length = 3,
    choices = ItemCategory,
    default = ItemCategory.WONDROUS_ITEM
  )
  armor_options = models.ManyToManyField(
    Armor,
    related_name="items",
    related_query_name="item",
    blank=True
  )
  weapon_options = models.ManyToManyField(
    Weapon,
    related_name="items",
    related_query_name="item",
    blank=True
  )
  spell_options = models.ManyToManyField(
    Spell,
    related_name="items",
    related_query_name="item",
    blank=True
  )

  def __str__(self):
    string = f"{self.name}"
    if self.attunement: string += " (requires attunement)"
    string += f", {self.get_rarity_display()} {self.get_category_display()}: {self.price} GP"
    return string
  
  def __repr__(self):
    return f"{self.name}"
  
  def __lt__(self, other):
    return self.name < other.name
  
  def has_options(self):
    return self.armor_options.exists() or self.weapon_options.exists() or self.spell_options.exists()

