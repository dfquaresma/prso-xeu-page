class Frame:
  def __init__(self, frameId):
    self.frameId = frameId

class Strategy(object):
  def __init__(self):
    pass

  def put(self, frameId):
    pass

  def evict(self):
    pass

  def clock(self):
    pass

  def access(self, frameId, isWrite):
    pass

class Fifo(Strategy):
  def __init__(self):
    from Queue import Queue
    self.fila = Queue()

  def put(self, frameId):
    self.fila.put(frameId)

  def evict(self):
    return self.fila.get()

class SecondChance(Fifo):
    def __init__(self):
      super(SecondChance, self).__init__()
      
    def put(self, frameId, bit=0):
      frame = Frame(frameId)
      frame.bit = bit
      super(SecondChance, self).put(frame)

    def evict(self):
      while not self.fila.empty():
        frame = super(SecondChance, self).evict()
        if frame.bit == 1:
          self.put(frame.frameId)
        else:
          return frame.frameId

    def access(self, frameId, isWrite):
      for i in range(self.fila.qsize()):
        frame = super(SecondChance, self).evict()
        if frame.frameId == frameId:
          self.put(frameId, 1)
        else:
          self.put(frameId, frame.bit)
          
class LRU(Strategy):
  def __init__(self):
    self.frames = []
    self.timer = 0
    
  def put(self, frameId):
    self.timer += 1
    frame = Frame(frameId)
    frame.timer = self.timer
    self.frames.append(Frame(frameId))

  def evict(self):
    frameIndex = 0
    minimum = self.frames[frameIndex].timer
    for i in range(len(self.frames)):
      timer = self.frames[i].timer
      if timer < minimum:
        frameIndex = i
        minimum = timer

    frame = self.frames[frameIndex]
    self.frames.pop(frameIndex)
    return frame.frameId	
  
  def access(self, frameId, isWrite):
    self.timer += 1
    for frame in self.frames:
      if frame.frameId == frameId:
        frame.timer = self.timer
        break

def get_strategy(algorithm):
    if algorithm == "fifo":
        return Fifo()
    elif algorithm == "second-chance":
        return SecondChance()
    elif algorithm == "lru":
        return LRU()
    else:
        raise Exception(algorithm + " strategy not implemented")
