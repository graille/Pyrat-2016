def create():
    return []


# Tests if the queue is empty
def isEmpty(queue):
    return queue == []


# Appends an element to the queue
def push(element, queue):
    queue.append(element)


# Extracts an element from the queue
def pop(queue):
    return queue.pop()

q = create()

visited = []
prev = {}

push((0,0), q)
prev[(0,0)] = None

while not isEmpty(q):
    n = pop(q)
    if n not in visited:
        visited.append(n)
    for k in mazeMap[n].keys():
        if k not in visited:
            push(k, q)
            prev[k] = n
