import os
import re
from StringIO import StringIO
import sys
import unittest as u

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dungeon_master import DungeonMaster

from action import *

class BaseTestCase(u.TestCase):
  def setUp(self):
    self.ostream = StringIO()
    self.dm = DungeonMaster(False, self.ostream)


class GoToAction(BaseTestCase):
  def test_existing_room(self):
    action = GoTo(dm=self.dm)
    action.do('goto lobby'.split())
    self.assertEqual(self.dm.get_current_room().__class__.__name__, 'Lobby')

  def test_bad_room(self):
    action = GoTo(dm=self.dm)
    self.dm.all_rooms = {'kittens': None}
    action.do('goto asdf'.split())
    expected = re.compile('''Unknown room: 'asdf'\.\s+Possible rooms:\s+\* kittens''')
    self.assertTrue(expected.search(self.ostream.getvalue()))


if __name__ == '__main__':
    u.main()