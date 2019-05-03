
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

def get_strategy(algorithm):
    if algorithm == "fifo":
        return Fifo(algorithm)
    else:
        raise Exception(algorithm + " strategy not implemented")
