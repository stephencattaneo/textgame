class Item(object):
  attributes = {}
  spawn_weight = 0

  def __init__(self, **kwargs):
    self.dm = kwargs['dm']
    self.name = self.__class__.__name__.lower()

  def __str__(self):
    return self.name

  def noop(self):
    self.dm.out("that doesn't seem to do anything")

  def apply(self, **kwargs):
    self.noop()

  def use(self, **kwargs):
    self.noop()

  def eat(self, **kwargs):
    self.noop()

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