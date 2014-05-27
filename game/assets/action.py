from pprint import pprint
import re

class Action(object):
  debug_only = False

  @staticmethod
  def command():
    return []

  def do(self, dm, args=None, **kwargs):
    dm.out('Why are you trying to call the base action?!?')

  @classmethod
  def help():
    '''  '''

class EnterRoom(Action):
  @staticmethod
  def command():
    return ['north', 'south', 'west', 'east'] #XXX This should be dictated by the current room

  def do(self, dm, args=None, **kwargs):
    if 'room' in kwargs:
      room = kwargs['room']
    elif dm.get_current_room().should_use_special_exit():
      room = dm.get_current_room().special_exit
    else:
      room = dm.random_room()

    dm.out('You enter %s.\n' % room.name)

    room.action(dm)
    dm.room_change(room)

class Help(Action):
  @staticmethod
  def command():
    return ['help']

  def do(self, dm, args=None, **kwargs):
    cmds = ' '.join(dm.actions.keys())
    dm.out("available commands: %s" % cmds)

class ListInventory(Action):
  @staticmethod
  def command():
    return ['inventory']

  def do(self, dm, args=None, **kwargs):
    for item in dm.inventory:
      dm.out(item)

class Talk(Action):
  @staticmethod
  def command():
    return ['talk']

  def do(self, dm, args=None, **kwargs):
    target = args[1] 

    if target == 'me':
      dm.out('You talk to yourself.  Crazy Person.')
    else:
      npc = dm.get_current_room().get_npc(target)

      if npc:
        npc.talk()
      else:
        '''There is no one by that name'''

class ItemAction(Action):
   def do(self, dm, args=None, **kwargs):
    item_name = args[1]

    item = None
    for inv_item in dm.inventory:
      if inv_item.name == item_name:
        item = inv_item
        break

    if not item:
      dm.out('no such item')
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

  def do(self, dm, args=None, **kwargs):
    room_name = args[1].lower()
    try:
      room = dm.all_rooms[room_name]
      EnterRoom().do(dm, room=room())
    except (KeyError):
      dm.out("Unknown room: '%s'." % room_name)
      dm.out("Possible rooms:")
      for rm in dm.all_rooms.keys():
        dm.out("* %s" % rm)

class RoomInfo(Action):
  debug_only = True

  @staticmethod
  def command():
    return ['roominfo']

  def do(self, dm, args=None, **kwargs):
    room = dm.get_current_room()
    pprint(room, stream=dm.out_stream)
    regex = re.compile('^__*')
    for attr in dir(room):
      if regex.match(attr): continue
      value = getattr(room, attr)
      printed_value = '<function>' if hasattr(value, '__call__') else value
      pprint((attr, printed_value), stream=dm.out_stream)


