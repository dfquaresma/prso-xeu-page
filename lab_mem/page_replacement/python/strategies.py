
class Fifo:
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
      super().__init__(algorithm)
      
    def put(self, frameId, bit=0):
      super().put((frameId, bit))

    def evict(self):
      while not super().fila.empty():
        (frameId, bit) = super().evict()
        if bit == 1:
          self.put(frameId)
        else:
          return frameId
      return None

    def access(self, frameId, isWrite):
      for i in range(super().fila.size()):
        (frame, bit) = super().evict()
        if frame == frameId:
          self.put(frameId, 1)
        else:
          self.put(frameId, bit)
      
def get_strategy(algorithm):
    if algorithm == "fifo":
        return Fifo(algorithm)
    elif algorithm == "second-chance":
        return SecondChance(algorithm)
    else:
        raise Exception(algorithm + " strategy not implemented")
