from base import Room

class Lobby(Room):
  name = 'the lobby'
  flavor_text = 'The secretary does not look up from her computer.'

class Exit(Room):
  name = 'the dungeon exit'
  flavor_text = 'light at the end of the tunnel ... you walk towards the light.'
  can_have_items = False
  can_be_random = False

  def action(self):
    super(Exit, self).action()
    self.dm.exit_game()

class IT(Room):
  name = 'the IT cube.'
  flavor_text = '''You feel as though you've entered some form of purgatory.'''
  exit_count_down = 3

  def __init__(self, dm, **kwargs):
    super(IT, self).__init__(dm, **kwargs)
    self.special_exit = self

  def action(self):
    self.exit_count_down -= 1
    super(IT, self).action()

  def should_use_special_exit(self):
    return self.exit_count_down

class Kitchen(Room):
  name =  'lunch room.'
  flavor_text = 'The smell of stale coffee fills the air.'

class Gym(Room):
  name = 'workout room.'
  flavor_text = 'The room is full of broken work out machines.'

class Server(Room):
  name = 'server room.'
  flavor_text = 'computers and wires everywhere, the sound of whiring fans is deafening.'

class Meeting(Room):
  name = 'a meeting room.'
  flavor_text = 'At the center of the room is a table surround by chairs.'