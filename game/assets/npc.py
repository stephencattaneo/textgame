class Npc(object):
  flavor_text = '''He looks vaguely faimilar, but you can't seem to place him'''

  def __init__(self):
    self.name = __class__.__name__

  def talk(self, **kwargs):
    return '''He mumbles something unintelligible.'''

class Khaaaan(Npc):
  flavor_text = '''He looks like a distinguished angry little man'''

  def talk(self, **kwargs):
    return '''The angry little man stares at you defiantly and then looks back at his laptop.'''

class Wizard(Npc):
  flavor_text = '''You see a tall man with a long white beard, a pointy hat, holding a staff.'''

  def talk(self, **kwargs):
    return '''You must answer three questions to pass.'''

class Cobald(Npc):
  flavor_text = 'an upright reptile that is reminiscent of a dead language.'
