from Queue import Queue
from random import randint

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
    self.frames.append(frame)

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

class NRU(Strategy):
  def __init__(self):
    self.frames = []
    
  def put(self, frameId):
    frame = Frame(frameId)
    frame.referenced = 0
    frame.modified = 0
    self.frames.append(frame)

  def evict(self):
    if not self.frames:
      raise Exception("[NRU] There is no frame to evict")

    c0, c1, c2, c3 = [], [], [], []
    for frame in self.frames:
      if frame.referenced == 0:
        if frame.modified == 0:
          c0.append(frame)
        else:
          c1.append(frame)
      else:
        if frame.modified == 0:
          c2.append(frame)
        else:
          c3.append(frame)
    
    if c0:
      frame = c0.pop(randint(0, len(c0) - 1))
    elif c1:
      frame = c1.pop(randint(0, len(c1) - 1))
    elif c2:
      frame = c2.pop(randint(0, len(c2) - 1))
    else:
      frame = c3.pop(randint(0, len(c3) - 1))
    
    index = self.frames.index(frame)
    self.frames.pop(index)
    return frame.frameId

  def clock(self):
    for frame in self.frames:
      frame.referenced = 0
  
  def access(self, frameId, isWrite):
    for frame in self.frames:
      if frame.frameId == frameId:
        frame.referenced = 1
        if isWrite:
          frame.modified = 1
        break

class Aging(Strategy):
  def __init__(self, nbitsAging):
    self.nbits = nbtisAging
    self.frames = []
    self.counter = 0
    
  def put(self, frameId):
    frame = Frame(frameId)
    frame.counter = self.counter
    self.frames.append(frame)

  def evict(self):
    frameIndex = 0
    minimum = self.frames[frameIndex].counter
    for i in range(len(self.frames)):
      counter = self.frames[i].counter
      if counter < minimum:
        frameIndex = i
        minimum = counter

    frame = self.frames[frameIndex]
    self.frames.pop(frameIndex)
    return frame.frameId    
  
  def access(self, frameId, isWrite):
    for frame in self.frames:
      if frame.frameId == frameId:
        frame.counter |= 1 << (nbits- 1)
        break
 
  def clock(self):
    for frame in self.frames:
      frame.counter >> 1

def get_strategy(algorithm, nbitsAging=None):
    if algorithm == "fifo":
        return Fifo()
    elif algorithm == "second-chance":
        return SecondChance()
    elif algorithm == "lru":
        return LRU()
    elif algorithm == "nru":
        return NRU()
    elif algorithm == "aging":
        return Aging(nbtisAging)
    else:
        raise Exception(algorithm + " strategy not implemented")
