import sys
import queue


class Link():
    ''' No repeat link '''

    def __init__(self):
        self.map = {}
        self.tail = "head"
        self.map["head"] = {"next": "null"}

    def __contains__(self, key):
        return key in self.map

    def __len__(self):
        return len(self.map) - 1

    def isEmpty(self):
        if self.getHead() == "null":
            return True
        else:
            return False

    def clearLink(self):
        self.map.clear()

    def getTail(self):
        return self.tail

    def getHead(self):
        return self.map["head"]["next"]

    def add(self, string):
        #      self.test_output("OrderedMapQueue")
        # args = string.split('\t')
        if string not in self.map:
            self.map[string] = {"next": "null"}
            self.map[self.tail]["next"] = string
            self.tail = string

    def pop(self):
        if not self.isEmpty():
            head_task = self.map["head"]["next"]
            rt_value = head_task
            self.map["head"]["next"] = self.map[head_task]["next"]
            del self.map[head_task]
            if head_task == self.tail:
                self.tail = "head"
            return rt_value
        return None



class OrderedMapQueue(queue.Queue):
    ''' ordered-map queue '''

    def _init(self, maxsize=0):
        self.queue = Link()

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop()

    def _qsize(self):
        return self.queue.__len__()



