
class Page:
  def __init__(self, frameId, bit):
    self.frameId = frameId
    self.bit = bit

class Fifo(object):
  def __init__(self, algorithm):
    from Queue import Queue
    self.fila = Queue()

  def put(self, frameId):
    self.fila.put(frameId)

  def evict(self):
    return self.fila.get()

  def clock(self):
    pass

  def access(self, frameId, isWrite):
    pass

class SecondChance(Fifo):
    def __init__(self, algorithm):
      super(SecondChance, self).__init__(algorithm)
      
    def put(self, frameId, bit=0):
      super(SecondChance, self).put(Page(frameId, bit))

    def evict(self):
      while not self.fila.empty():
        page = super(SecondChance, self).evict()
        if page.bit == 1:
          self.put(page.frameId)
        else:
          return page.frameId

    def access(self, frameId, isWrite):
      for i in range(self.fila.qsize()):
        page = super(SecondChance, self).evict()
        if page.frameId == frameId:
          self.put(frameId, 1)
        else:
          self.put(frameId, page.bit)

def get_strategy(algorithm):
    if algorithm == "fifo":
        return Fifo(algorithm)
    elif algorithm == "second-chance":
        return SecondChance(algorithm)
    else:
        raise Exception(algorithm + " strategy not implemented")
