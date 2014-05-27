class Room(object):
  inventory = []
  can_be_random = True
  special_exit = None
  name = 'the same old room'
  flavor_text = 'just another room'
  npcs = []

  def action(self, dm):
    dm.out(self.flavor_text)

  def get_npc(self, npc_name):
    for npc in self.npcs:
      if npc.name == npc_name:
        return npc

    return None

  def should_use_special_exit(self):
    return False

class Lobby(Room):
  name = 'the lobby'
  flavor_text = 'Welcome.'
  can_be_random = False

class Exit(Room):
  name = 'the dungeon exit'
  flavor_text = 'light at the end of the tunnel ... you walk towards the light.'

  def action(self, dm):
    super(Exit, self).action(dm)
    dm.exit_game()

class IT(Room):
  name = 'The IT cube.'
  flavor_text = 'hell.'
  exit_count_down = 3

  def __init__(self):
    self.special_exit = self

  def action(self, dm):
    self.exit_count_down -= 1
    super(IT, self).action(dm)

  def should_use_special_exit(self):
    return self.exit_count_down > 0
