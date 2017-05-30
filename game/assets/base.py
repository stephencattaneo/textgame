from random import randint
from pprint import pprint
import re

class Base(object):
  def __init__(self, dm, **kwargs):
    self.dm = dm

class Room(Base):
  can_be_random = True
  special_exit = None
  name = 'the same old room'
  flavor_text = 'just another room'
  can_have_items = True
  chance = 3 #  where 1 in chance of items
  visited = False

  def __init__(self, dm, **kwargs):
    super(Room, self).__init__(dm, **kwargs)
    self.chance = int(kwargs['chance']) if 'chance' in kwargs else self.chance
    self.npcs = []
    self.items = []

  def action(self):
    self.dm.out(self.flavor_text)

    if not self.visited:
      self.visited = True
      self.generate_items()

    for item in self.items:
      self.dm.out('You see a %s.' % item)

  def generate_items(self):
    if not self.can_have_items: return

    # 33% chance of anything dropping.
    if randint(1, self.chance) % self.chance != 0: return

    '''
    From http://gamedev.stackexchange.com/questions/6043/algorithm-for-determining-random-events

    It sounds like you're asking for a more flexible way of specifying the probability of each event.
    For that, you can use a simple weighing algorithm: simply decide how common each event should be
    and assign it a weight that is appropriate compared to the other weights.
    For example, if you have events A, B and C, with probabilities 70%, 25% and 5%,
    you could give them the weights 70, 25 and 5 (or 14, 5, and 1 - the important
    thing is the relative difference).

    Once you have that, you can use the following algorithm to select an event:

    Given a list L of items (I,W), where I is the item and W is the weight:

    Add all of the weights together. Call this sum S.
    Generate a random number between 0 and S (excluding S, but including 0). Call this value R.
    Initialize a variable to 0 to keep track of the running total. We'll call this T.
    For each item (I,W) in L:
    T=T+W
    If T > R, return I.
    It's up to you if you want to first select between the different groups of events,
    or if you want a single table with all of the events (where each "group" has an
    appropriate sum compared to the others).
    '''

    for count in range(randint(1, 2)):
      R = randint(0, self.dm.total_item_weight - 1)
      T = 0
      for item_name in self.dm.items:
        I = self.dm.items[item_name]
        if I.spawn_weight == 0: continue
        T = T + I.spawn_weight
        if T > R:
          self.items.append(I(dm=self.dm))
          break

  def get_npc(self, npc_name):
    for npc in self.npcs:
      if npc.name == npc_name:
        return npc

    return None

  def should_use_special_exit(self):
    return False


class Item(Base):
  spawn_weight = 0

  def __init__(self, dm, **kwargs):
    super(Item, self).__init__(dm, **kwargs)
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

class Edible(Item):
  def eat(self, **kwargs):
    self.dm.out('You eat the %s. Mmmmmmmmmm sooo good.' % self.__class__.__name__)

class Crafted(Item):
  pass

class Weapon(Item):
  pass

class Action(Base):
  debug_only = False

  @staticmethod
  def command():
    return []

  def do(self, args=None, **kwargs):
    raise Exception()

  @classmethod
  def help():
    '''  '''

class ItemAction(Action):
  def do(self, args=None, **kwargs):
    if len(args) < 2:
      self.dm.out('no such item.')
      return
    item_name = args[1]

    item = None
    for inv_item in self.dm.inventory:
      if inv_item.name == item_name:
        item = inv_item
        break

    if not item:
      self.dm.out('no such item')
    else:
      self.execute(item)

  def execute(self, item):
    getattr(item, self.__class__.__name__.lower()) ()

class DebugAction(Action):
  debug_only = True

  def debug_obj(self, obj):
    pprint(obj, stream=self.dm.out_stream)
    hidden_regex = re.compile('^__*')
    for attr in dir(obj):
      if hidden_regex.match(attr): continue
      value = getattr(obj, attr)
      printed_value = '<function>' if hasattr(value, '__call__') else value
      pprint((attr, printed_value), stream=self.dm.out_stream)
