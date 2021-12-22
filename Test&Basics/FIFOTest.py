import queue

q1 = queue.Queue()

for i in range(4):
    q1.put(i)

while (not(q1.empty())) :
    print(q1.get())

print("----")

q1.put(7)

while (not(q1.empty())) :
    print(q1.get())