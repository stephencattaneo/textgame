import unittest as u
import subprocess
import os

from dungeon_master import ExitGame, DungeonMaster

PYLINT = '/usr/local/bin/pylint'

class DoesItBuild(u.TestCase):
  def runTest(self):
    dm = DungeonMaster()

class Lint(u.TestCase):
  def runTest(self):
    # pylint --rcfile=./pylint.rcfile game
    directory = os.path.dirname(os.path.realpath(__file__))
    args = [PYLINT, '--rcfile=%s/pylint.rcfile' % directory, 'game']

    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret = proc.wait()
    (stdout, stderr) = proc.communicate()
    if stderr:
      print "STDERR: %s \n--------" % stderr
    elif ret:
      fd = open('/tmp/lint.out', 'w')
      fd.write(stdout)
      fd.close()
      print('\n****** YOU CAN CHECK /tmp/lint.out FOR LINTER DETAILS. ******')

    self.assertFalse(ret)
