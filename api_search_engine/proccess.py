from multiprocessing import Process, Queue

def f(q):
    q.put(34)


if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    q.put(22)
    print(q.get())    # prints "[42, None, 'hello']"
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()