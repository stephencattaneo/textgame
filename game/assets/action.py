from pprint import pprint
import re
from base import Action, ItemAction, DebugAction

class EnterRoom(Action):
  @staticmethod
  def command():
    return ['north', 'south', 'west', 'east'] #XXX This should be dictated by the current room

  def do(self, args=None, **kwargs):
    if 'room' in kwargs:
      room = kwargs['room']
    elif self.dm.current_room().should_use_special_exit():
      room = self.dm.current_room().special_exit
    else:
      room = self.dm.random_room()

    self.dm.out('You enter %s.\n' % room.name)

    room.action()
    self.dm.room_change(room)

class Help(Action):
  @staticmethod
  def command():
    return ['help', '?']

  def do(self, args=None, **kwargs):
    cmds = ' '.join(self.dm.actions.keys())
    self.dm.out("available commands: %s" % cmds)

class Inventory(Action):
  @staticmethod
  def command():
    return ['inventory']

  def do(self, args=None, **kwargs):
    if len(self.dm.inventory):
      self.dm.out("Things in your inventory:")
      for i in range(len(self.dm.inventory)):
        self.dm.out(
          '%d) %s' % (i, str(self.dm.inventory[i]))
        )
    else:
      self.dm.out('You dont have anything')

class Talk(Action):
  @staticmethod
  def command():
    return ['talk']

  def do(self, args=[], **kwargs):
    if len(args) < 2:
      target = 'me'
    else:
      target = args[1]

    if target == 'me':
      self.dm.out('You talk to yourself.  Crazy Person.')
    else:
      npc = self.dm.current_room().get_npc(target)

      if npc:
        npc.talk()
      else:
        self.dm.out('''There is no one by that name''')



class Use(ItemAction):
  #XXX refactor static method to class method
  # then we can further refactor these classes to 2 lines...
  action = 'use'

  @staticmethod
  def command():
    return ['use']

class Apply(ItemAction):
  action = 'apply'

  @staticmethod
  def command():
    return ['apply']

class Pickup(ItemAction):
  action = 'pickup'

  @staticmethod
  def command():
    return ['pickup']

  def do(self, args=None, **kwargs):
    item_name = args[1]

    item = None
    for inv_item in self.dm.current_room().items:
      if inv_item.name == item_name:
        item = inv_item
        break

    if not item:
      self.dm.out('no such item')
    else:
      self.execute(item)

  def execute(self, item):
    items = self.dm.current_room().items
    for i in xrange(len(items)):
      inv_item = items[i]
      if inv_item == item:
        del items[i]
        break
    self.dm.inventory.append(item)
    self.dm.out('You pick up the %s.' % item)

class Eat(ItemAction):
  @staticmethod
  def command():
    return ['eat']

class GoTo(DebugAction):
  @staticmethod
  def command():
    return ['goto']

  def do(self, args=None, **kwargs):
    if len(args) < 2:
      self.help_message()
      return

    room_name = args[1].lower()
    try:
      room = self.dm.all_rooms[room_name]

      room_args = {'dm': self.dm}
      # any additional parts of the input command should become
      # part of kwargs to the room object.
      for i in xrange(0, len(args[2:]), 2):
        room_args[args[2+i]] = args[3+i]

      EnterRoom(dm=self.dm).do(room=room(**room_args))
    except (KeyError):
      self.dm.out("Unknown room: '%s'." % room_name)
      self.help_message()

  def help_message(self):
    self.dm.out("Possible rooms:")
    for rm in self.dm.all_rooms.keys():
      self.dm.out("* %s" % rm)


class RoomInfo(DebugAction):
  @staticmethod
  def command():
    return ['roominfo']

  def do(self, args=None, **kwargs):
    self.debug_obj(self.dm.current_room())

class DMStatus(DebugAction):
  @staticmethod
  def command():
    return ['dmstatus']

  def do(self, args=None, **kwargs):
    self.debug_obj(self.dm)


