import inspect
from random import randint
import sys

from assets import *
from assets import base

class ExitGame(BaseException):
  pass

class DungeonMaster(object):
  actions = {}
  possible_rooms = []
  all_rooms = {}
  items = {}
  craftable_items = {}
  total_item_weight = 0
  room_grid = [[]]
  inventory = []

  def __init__(self, debug_mode=False, out_stream=sys.stdout):
    self.debug = debug_mode
    self.out_stream = out_stream

    # Cache up the possible actions.
    def append_actions(self, obj):
      if obj.debug_only and not self.debug: return

      for key in obj.command():
        self.actions[key] = obj
    self.cache_asset(action, append_actions)

    # cache the random rooms.
    def append_rooms(self, obj):
      if obj.can_be_random:
        self.possible_rooms.append(obj)
      self.all_rooms[obj.__name__.lower()] = obj
    self.cache_asset(room, append_rooms)

    # cache the items.
    def append_items(self, obj):
      obj_name = obj.__name__.lower()
      self.items[obj_name] = obj
      if isinstance(obj, base.Crafted):
        self.craftable_items[obj_name] = obj
      self.total_item_weight = self.total_item_weight + obj.spawn_weight
    self.cache_asset(item, append_items)



  def start(self):
    # enter the lobby to start the game.
    action.Move(dm=self).do(room=room.Lobby(dm=self), pos=[0,0])


  def do_action(self, cmd):
    if not cmd: return
    try:
      cmd = cmd.lower().split(' ')
      action = self.actions[cmd[0]](dm=self)

    except (KeyError):
      self.out("Unknown command. Type 'help' for a list of available commands.")
      return

    action.do(cmd)


  def room_change(self, new_room, pos):
    self.visited_rooms.append(new_room)


  def current_room(self):
    return self._current_room

  def room_at_position(self, pos):
    return self.visited_rooms[pos[0]][pos[1]]

  def random_room(self):
    return self.possible_rooms[randint(0, len(self.possible_rooms) - 1)](dm=self)


  def exit_game(self):
    raise ExitGame()


  def cache_asset(self, root_class, func):
    for name, obj in inspect.getmembers(root_class):
      if inspect.isclass(obj): func(self, obj)


  def out(self, msg):
    self.out_stream.write(msg + '\n')


  def log(self, msg):
    if self.debug: self.out(msg)
