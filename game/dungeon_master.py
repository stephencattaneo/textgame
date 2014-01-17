import inspect
from random import randint

from assets import *

class ExitGame(BaseException):
  pass

class DungeonMaster(object):
  actions = {}
  rooms = []
  items = {}
  current_room = None
  last_room = None
  inventory = []

  def __init__(self):
    # Cache up the possible actions.
    def append_actions(self, obj):
        for key in obj.command():
          self.actions[key] = obj
    self.cache_asset(action, append_actions)

    # cache the random rooms.
    def append_rooms(self, obj):
      if obj.can_be_random:
          self.rooms.append(obj)
    self.cache_asset(room, append_rooms)

    # cache the items.
    def append_items(self, obj):
      self.items[obj.name] = obj
    self.cache_asset(self, item)

    # enter the lobby to start the game.
    action.EnterRoom().do(self, room=room.Lobby())

  def do_action(self, cmd):
    if not cmd: return

    cmd = cmd.lower().split(' ')
    action = self.actions[cmd[0]]()
    
    if not action:
      print "Unknown command. Type 'help' for a list of available commands."
      return

    action.do(self, cmd)

  def room_change(self, new_room):
    self.last_room = self.current_room
    self.current_room = new_room

  def random_room(self):
    return self.rooms[randint(0, len(self.rooms) - 1)]()

  def exit_game(self):
    raise ExitGame()

  def cache_asset(self, root_class, func):
    for name, obj in inspect.getmembers(root_class):
      if inspect.isclass(obj): func(obj)

if __name__ == '__main__':
  dm = DungeonMaster()
