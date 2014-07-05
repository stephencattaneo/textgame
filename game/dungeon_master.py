import inspect
from random import randint
import sys

from assets import *

class ExitGame(BaseException):
  pass

class DungeonMaster(object):
  actions = {}
  possible_rooms = []
  all_rooms = {}
  items = {}
  total_item_weight = 0
  visited_rooms = []
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
      self.items[obj.__name__.lower()] = obj
      self.total_item_weight = self.total_item_weight + obj.spawn_weight
    self.cache_asset(item, append_items)


  def start(self):
    # enter the lobby to start the game.
    action.EnterRoom(dm=self).do(room=room.Lobby(dm=self))


  def do_action(self, cmd):
    if not cmd: return
    try:
      cmd = cmd.lower().split(' ')
      action = self.actions[cmd[0]](dm=self)

    except (KeyError):
      self.out("Unknown command. Type 'help' for a list of available commands.")
      return

    action.do(cmd)


  def room_change(self, new_room):
    self.visited_rooms.append(new_room)


  def current_room(self):
    return self.visited_rooms[-1]


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
