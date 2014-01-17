class Action(object):
  @staticmethod
  def command():
    return []

  def do(self, dm, args=None, **kwargs):
    print('Why are you trying to call the base action?!?')

class EnterRoom(Action):
  @staticmethod
  def command():
    return ['north', 'south', 'west', 'east'] #XXX This should be dictated by the current room

  def do(self, dm, args=None, **kwargs):
    room = kwargs['room'] if 'room' in kwargs else dm.random_room()
    print('You enter %s.' % room.name)
    print('')
    print(room.flavor_text)
    dm.room_change(room)

class Help(Action):
  @staticmethod
  def command():
    return ['help']

  def do(self, dm, args=None, **kwargs):
    cmds = ' '.join(dm.actions.keys())
    print "available commands: %s" % cmds

class ListInventory(Action):
  @staticmethod
  def command():
    return ['inventory']

  def do(self, dm, args=None, **kwargs):
    for item in dm.inventory:
      print(item)

class UseItem(Action):
  @staticmethod
  def command():
    return ['use']

    def do(self, dm, args=None, **kwargs):
      item_name = args[1]

      item = None
      for inv_item in dm.inventory:
        if inv_item.name == item_name:
          item = inv_item
          break

      if not item:
        print('no such item')

      item.use()