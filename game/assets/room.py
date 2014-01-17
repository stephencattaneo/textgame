class Room(object):
  inventory = []
  can_be_random = True
  special_exit = None
  name = 'the same old room'
  flavor_text = 'just another room'

  def action(self, dm):
    print(flavor_text)

class Lobby(Room):
  name = 'the lobby'
  flavor_text = 'The lobby.'
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
