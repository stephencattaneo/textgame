
from pprint import pprint
import re


class Action(object):
  debug_only = False

  def __init__(self, **kwargs):
    self.dm = kwargs['dm']

  @staticmethod
  def command():
    return []

  def do(self, args=None, **kwargs):
    self.dm.out('Why are you trying to call the base action?!?')

  @classmethod
  def help():
    '''  '''

class EnterRoom(Action):
  @staticmethod
  def command():
    return ['north', 'south', 'west', 'east'] #XXX This should be dictated by the current room

  def do(self, args=None, **kwargs):
    if 'room' in kwargs:
      room = kwargs['room']
    elif self.dm.get_current_room().should_use_special_exit():
      room = self.dm.get_current_room().special_exit
    else:
      room = self.dm.random_room()

    self.dm.out('You enter %s.\n' % room.name)

    room.action()
    self.dm.room_change(room)

class Help(Action):
  @staticmethod
  def command():
    return ['help']

  def do(self, args=None, **kwargs):
    cmds = ' '.join(self.dm.actions.keys())
    self.dm.out("available commands: %s" % cmds)

class ListInventory(Action):
  @staticmethod
  def command():
    return ['inventory']

  def do(self, args=None, **kwargs):
    for item in self.dm.inventory:
      self.dm.out(item)

class Talk(Action):
  @staticmethod
  def command():
    return ['talk']

  def do(self, args=None, **kwargs):
    target = args[1] 

    if target == 'me':
      self.dm.out('You talk to yourself.  Crazy Person.')
    else:
      npc = self.dm.get_current_room().get_npc(target)

      if npc:
        npc.talk()
      else:
        '''There is no one by that name'''

class ItemAction(Action):
   def do(self, args=None, **kwargs):
    item_name = args[1]

    item = None
    for inv_item in self.dm.inventory:
      if inv_item.name == item_name:
        item = inv_item
        break

    if not item:
      self.dm.out('no such item')
    else:
      getattr(item, self.action) ()

class UseItem(ItemAction):
  #XXX refactor static method to class method
  # then we can further refactor these classes to 2 lines...
  action = 'use'

  @staticmethod
  def command():
    return ['use']

class ApplyItem(ItemAction):
  action = 'apply'

  @staticmethod
  def command():
    return ['apply']

class PickupItem(ItemAction):
  action = 'pickup'

  @staticmethod
  def command():
    return ['pickup']

class GoTo(Action):
  debug_only = True

  @staticmethod
  def command():
    return ['goto']

  def do(self, args=None, **kwargs):
    room_name = args[1].lower()
    try:
      room = self.dm.all_rooms[room_name]
      EnterRoom(dm=self.dm).do(room=room(dm=self.dm))
    except (KeyError):
      self.dm.out("Unknown room: '%s'." % room_name)
      self.dm.out("Possible rooms:")
      for rm in self.dm.all_rooms.keys():
        self.dm.out("* %s" % rm)

class RoomInfo(Action):
  debug_only = True

  @staticmethod
  def command():
    return ['roominfo']

  def do(self, args=None, **kwargs):
    room = self.dm.get_current_room()
    pprint(room, stream=self.dm.out_stream)
    regex = re.compile('^__*')
    for attr in dir(room):
      if regex.match(attr): continue
      value = getattr(room, attr)
      printed_value = '<function>' if hasattr(value, '__call__') else value
      pprint((attr, printed_value), stream=self.dm.out_stream)


