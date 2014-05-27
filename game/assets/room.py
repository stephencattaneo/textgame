
class Room(object):
  items = []
  can_be_random = True
  special_exit = None
  name = 'the same old room'
  flavor_text = 'just another room'
  npcs = []
  can_have_items = True

  def __init__(self, **kwargs):
    self.dm = kwargs['dm']

  def action(self):
    self.dm.out(self.flavor_text)

    self.generate_items()
    for item in self.items:
      self.dm.out('You see a %s.' % item)

  def generate_items(self):
    if not self.can_have_items: return

    '''
    From http://gamedev.stackexchange.com/questions/6043/algorithm-for-determining-random-events
    
    It sounds like you're asking for a more flexible way of specifying the probability of each event. 
    For that, you can use a simple weighing algorithm: simply decide how common each event should be 
    and assign it a weight that is appropriate compared to the other weights. 
    For example, if you have events A, B and C, with probabilities 70%, 25% and 5%, 
    you could give them the weights 70, 25 and 5 (or 14, 5, and 1 - the important 
    thing is the relative difference).

    Once you have that, you can use the following algorithm to select an event:

    Given a list L of items (I,W), where I is the item and W is the weight:

    Add all of the weights together. Call this sum S.
    Generate a random number between 0 and S (excluding S, but including 0). Call this value R.
    Initialize a variable to 0 to keep track of the running total. We'll call this T.
    For each item (I,W) in L:
    T=T+W
    If T > R, return I.
    It's up to you if you want to first select between the different groups of events, 
    or if you want a single table with all of the events (where each "group" has an 
    appropriate sum compared to the others).
    '''

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
  can_have_items = False

  def action(self):
    super(Exit, self).action()
    self.dm.exit_game()

class IT(Room):
  name = 'The IT cube.'
  flavor_text = 'hell.'
  exit_count_down = 3

  def __init__(self, **kwargs):
    super(IT, self).__init__(**kwargs)
    self.special_exit = self

  def action(self):
    self.exit_count_down -= 1
    super(IT, self).action()

  def should_use_special_exit(self):
    return self.exit_count_down > 0
