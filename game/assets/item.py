from base import Item, Weapon, Edible, Crafted

class Stick(Item):
  spawn_weight = 5

class Rope(Item):
  spawn_weight = 1

class Flint(Item):
  spawn_weight = 5

class Cloth(Item):
  spawn_weight = 2

class SmallShardOfSteel(Item):
  spawn_weight = 5

class Knife(Weapon):
  spawn_weight = 1

class Apple(Edible):
  spawn_weight = 3

class BlockOCheese(Edible):
  spawn_weight = 2

class Picnic(Crafted):
  requires = {BlockOCheese: 1, Apple: 1, Cloth: 2}

class PoleArm(Crafted):
  requires = {Knife: 1, Stick: 1}