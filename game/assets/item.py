class Item(object):
  name = 'thing'
  attributes = {}

  def __init__(self, **kwargs):
    self.dm = kwargs['dm']

  def __str__(self):
    self.dm.out(self.__class__.__name__.lower())
  
  def noop(self):
    self.dm.out("that doesn't seem to do anything")
  
  def apply(self, **kwargs):
    self.noop()    

  def use(self, **kwargs):
    self.noop()

  def eat(self, **kwargs):
    self.noop()

class Stick(Item):
  pass

class Rope(Item):
  pass

class Edible(Item):
  def __init__(self, **kwargs):
    super(Edible, self).__init__(**kwargs)
    self.attributes['edible'] = True

class Apple(Edible):
  pass