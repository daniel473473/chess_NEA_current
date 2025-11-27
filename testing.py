class Self_Made_Queue:
    def __init__(self, max_size,):
        self.data = []
        self.max_size = max_size
        self.size = 0
        self.front = -1
        self.rear = -1

    def isFull(self):
        return self.size == self.max_size
    
    def isEmpty(self):
        return self.size == 0
    
    def peak(self):
        return self.data[self.front]
    
    def enQueue(self, n):
        if not self.isFull():
            self.data.append(n)
            self.rear = (self.rear + 1) % self.max_size
            self.size += 1

    def deQueue(self):
        if not self.isEmpty():
            item = self.data[self.front]
            self.front = (self.front + 1) % self.max_size
            self.size -= 1
            return item
        
queue = Self_Made_Queue(5)
queue.enQueue(5)
queue.enQueue(5)
queue.enQueue(5)
queue.enQueue(5)
queue.enQueue(5)
print(queue.isFull())
print(queue.deQueue())
        
        