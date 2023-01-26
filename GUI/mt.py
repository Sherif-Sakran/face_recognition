from threading import Thread
import time
import glob


def sleep(n):
    print(f'sleeping for {n} seconds')
    time.sleep(n)


if __name__ == "__main__":
    stamp1 = time.time()
    sleeps = [1]
    threads = []
    for i in range(len(sleeps)):
        thread = Thread(target=sleep, args=(sleeps[i],))
        threads.append(thread)
        thread.start()

    # for thread in threads:
    for thread in threads:
        thread.join()
    # t1 = Thread(target=sleep, args=(3,))
    # t2 = Thread(target=sleep, args=(3,))
    # t3 = Thread(target=sleep, args=(3,))
    # t1.start()
    # t2.start()
    # t3.start()
    # t1.join()
    # t2.join()
    # t3.join()
    print(f'time = {time.time() - stamp1}')
    print(glob.glob("D:/Courses/9- Summer 2022/Internship/Library_internship-main/Environment/images/faces/training_set/*"))