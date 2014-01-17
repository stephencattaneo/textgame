#!/usr/bin/env python

import readline
from game import *



class Game(object):
  DEBUG_MODE = True

  def run(self):
    gm = dungeon_master.DungeonMaster()

    print('Welcome.')

    while (True):
      try:
        cmd = raw_input('> ')
        print('\n')
        if self.DEBUG_MODE and cmd == 'quit': 
          print('Goodbye. (debug quit)')
          break

        gm.do_action(cmd)
      
      except (EOFError, KeyboardInterrupt):
        print('nope. >:D ')

      except dungeon_master.ExitGame:
        print 'exit game!'
        break


 # if __name__ == '__main__':
 #   g = Game()
 #   g.run()