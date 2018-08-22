from multiprocessing import Process, Manager, Pool, Array, Queue
import time
import asyncio

def func1(q):
    i = 0
    while i<=10:
        time.sleep(3)
        q.put("A"+str(i))
        i+=1

async def func2(q):
    i = 0
    while i<20:
        await asyncio.sleep(1)
        q.put("B"+str(i))
        i+=1

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

def func(q):
   loop = asyncio.get_event_loop()
   loop.run_until_complete(func2(q))

if __name__ =='__main__':

    #loop = asyncio.get_event_loop()
    #loop1 = asyncio.new_event_loop()
    q = Queue()
    num_processes = 2
    pool = Pool(processes=num_processes)
    processes = []
   # tasks=[func1(), func2()]

    #for i in range(num_processes):

    #process_name = 'P%'

        # Create the process, and connect it to the worker function
    new_process1 = Process(target=func, args=(q,))
    new_process1.start()
    #new_process1.daemon = True
        # Add new process to the list of processes
    processes.append(new_process1)

    new_process2 = Process(target=func1, args=(q,))
    new_process2.start()

    processes.append(new_process2)

        # Start the process

    while True:
        try:
            print(q.get())
        except:
            break