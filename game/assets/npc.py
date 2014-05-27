class Npc(object):
  flavor_text = '''He looks vaguely familar, but you can't seem to place him'''

  def __init__(self):
    self.name = __class__.__name__

  def talk(self, **kwargs):
    return '''He mumbles something unintelligble.'''

class Kahn(Npc):
  flavor_text = '''He looks like an angry little man'''

  def talk(self, **kwargs):
    return '''The angry little man stares at you defiantly.'''


class Wizard(Npc):
  flavor_text = '''You see a tall man with a long white beard, a pointy, hat, holding a staff.'''

  def talk(self, **kwargs):
    return '''You must answer three questions to pass.'''
