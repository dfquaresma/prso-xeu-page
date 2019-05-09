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

  def access(self, frameId, isWrite):
		for i in range(self.fila.size()):
			(frame, x) = self.fila.get()
      if frame == frameId:
        self.put(frameId, x++)
      else:
        self.put(frameId, x)]

def get_strategy(algorithm):
    if algorithm == "fifo":
        return Fifo(algorithm)
    elif algorithm == "lru":
        return LRU(algorithm)
    else:
        raise Exception(algorithm + " strategy not implemented")
