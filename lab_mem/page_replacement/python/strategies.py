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
          
class LRU:
  def __init__(self, algorithm):
   from Queue import Queue
	 self.fila = Queue()
	 self.timer = 0
    
  def put(self, frameId, self.timer):
    self.timer = self.timer + 1;
    self.fila.put((frameId, self.timer))

  def evict(self):
    (frame, x) = self.fila.get()
    lruFrame = frame
    lru = x
    self.put((frame, x))
    for i in range(self.fila.size()):
      (frame, x) = self.fila.get()
      if(x < lru):
        lruFrame = frame
        self.put((frame, x))	
	return lruFrame				
  
  def clock(self):
    pass
  
  def access(self, frameId, isWrite):
    for i in range(self.fila.size()):
      (frame, x) = self.fila.get()
      if frame == frameId:
        x = x + 1
        self.put(frameId, x)
      else:
        self.put(frameId, x)

def get_strategy(algorithm):
    if algorithm == "fifo":
        return Fifo(algorithm)
    elif algorithm == "second-chance":
        return SecondChance(algorithm)
    elif algorithm == "lru":
        return LRU(algorithm)
    else:
        raise Exception(algorithm + " strategy not implemented")
