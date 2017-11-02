import os
import re
from StringIO import StringIO
import sys
import unittest as u

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dungeon_master import DungeonMaster

import action
import room

class BaseTestCase(u.TestCase):
  def setUp(self):
    self.ostream = StringIO()
    self.dm = DungeonMaster(False, self.ostream)

class GoToAction(BaseTestCase):
  def test_existing_room(self):
    goto = action.GoTo(dm=self.dm)
    goto.do('goto lobby'.split())
    self.assertEqual(self.dm.current_room().__class__.__name__, 'Lobby')

  def test_bad_room(self):
    goto = action.GoTo(dm=self.dm)
    self.dm.all_rooms = {'kittens': None}
    goto.do('goto asdf'.split())
    expected = re.compile('''Unknown room: 'asdf'\.\s+Possible rooms:\s+\* kittens''')
    self.assertTrue(expected.search(self.ostream.getvalue()))

class InventoryAction(BaseTestCase):
  def test_empty_inv(self):
    inv = action.Inventory(dm=self.dm)
    inv.do(['inventory'])
    self.assertEqual(self.ostream.getvalue(), 'You dont have anything\n')

  def test_nonempty_inv(self):
    self.dm.inventory = ['preconsent']
    inv = action.Inventory(dm=self.dm)
    inv.do(['inventory'])
    self.assertEqual(self.ostream.getvalue(), 'Things in your inventory:\n1) preconsent\n')

class MoveAction(BaseTestCase):
  def test_north(self):
    self.dm.all_rooms = {'lobby': room.Lobby}

    north = action.Move(dm=self.dm)
    north.do(['north'])
    self.assertEqual(type(self.dm.current_room), room.Lobby)

  def test_go_back(BaseTestCase):
    self.dm.all_rooms = {'it': room.IT}
    self.dm.start()
    last_room = self.dm.current_room()

    east = action.Move(dm=self.dm)
    east.do(['east'])
    self.assertEqual(type(self.dm.current_room()), room.IT)

    west = action.Move(dm=self.dm)
    west.do(['west'])
    self.assertEqual(self.dm.current_room(), last_room)


if __name__ == '__main__':
  u.main()
