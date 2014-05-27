class Item(object): 
  name = 'thing'

  def __str__(self):
    print(self.name)
  
  def noop(self):
    print("that doesn't seem to do anything")
  
  def apply(self, **kwargs):
    self.noop()    

  def use(self, **kwargs):
    self.noop()

  def eat(self, **kwargs):
    self.noop()

class Stick(Item):
  name = 'stick'