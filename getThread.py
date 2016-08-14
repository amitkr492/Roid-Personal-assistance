 import threading
import Queue
from bestanswer import get_score
from summarise import *
que = Queue.Queue()
def dosomething(param):
	#print param
	content=getFirstAns(param)
	print(param)
	score=get_score(content)
	return [content,score]
def getMyAns(lst):
	que.queue.clear()
	for i in range(len(lst)):
		thr = threading.Thread(target = lambda q, arg : q.put(dosomething(arg)), args = (que, lst[i]))
		thr.start()
		thr.join()
#while not que.empty():
#print(que.get())

if __name__ == "__main__":
	a1="https://en.wikipedia.org/wiki/Instagram"
	a2="https://en.wikipedia.org/wiki/Kevin_Systrom"
	lst=[a1,a2]
	getMyAns(lst)
	print(que)