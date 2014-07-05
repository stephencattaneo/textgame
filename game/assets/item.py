from base import Item

class Stick(Item):
  spawn_weight = 5

class Rope(Item):
  spawn_weight = 1


class Edible(Item):
  def __init__(self, **kwargs):
    super(Edible, self).__init__(**kwargs)
    self.attributes['edible'] = True

  def eat(self, **kwargs):
    self.dm.out('You eat the %s. Mmmmmmmmmm sooo good.' % self.__class__.__name__)

class Apple(Edible):
  spawn_weight = 3

class BlockOCheese(Edible):
  spawn_weight = 2