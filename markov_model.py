from random import randrange


class Dice():
    def __init__(self, p):
        self.batch_started = False
        self.idx = 0
        self.result = []
        self.prob = p
        # find out the precision after the decimal place, such as 0.312 has 3 digits after the decimal place
        prec = 0
        for item in p:
            if len(str(item)) > prec:
                prec = len(str(item)) 
        #print("prec ", prec - 2)
        N = 10**(prec - 2)
        collection = []
        for i in range(6):
            cnt = int(p[i] * N)
            while cnt > 0:
                collection.append(i+1) #dice starts from 1
                cnt -= 1
        #print(collection)
        self.collection = collection
    def copy_an_array(self):
        new_arr = []
        for el in self.collection:
            new_arr.append(el)
        return new_arr
    def get_samples(self, n):
        #print("get_samples", n)
        result = []
        #arr = self.collection
        arr = self.copy_an_array()
        N= len(self.collection)
        for i in range(n):
            idx = randrange(N)
            result.append(arr[idx])
            arr[idx] = arr[N-1]
            N -= 1
            if N == 0:
                #print("iteration ", result)
                #arr = self.collection
                arr = self.copy_an_array()
                N = len(self.collection)
        return result
    def roll(self):  # generator
        if self.batch_started == False:
            self.batch_started = True
            self.result = self.get_samples(len(self.collection))
            self.idx = 1 # next time it should start with idx of 1
            return self.result[0]
        else:
            if self.idx < len(self.collection) - 1:
                idx = self.idx
                self.idx += 1
                return self.result[idx]
            elif self.idx == len(self.collection) - 1:
                self.batch_started = False
                return self.result[self.idx]
        
class Game():
    def __init__(self, p, ladders, snakes):
        
        self.goal = 100
        self.play_times = 5000
        self.p = p
        self.ladders = ladders
        self.snakes = snakes
        self.dice = Dice(p)
    def play(self):
        cnt = 0
        self.pos = 1
        while (cnt < 1000):
            cnt += 1
            value = self.dice.roll()
            #print("pos ", self.pos, "dice value ", value)
            if self.pos + value < self.goal:
                self.pos += value
            
                if self.pos in self.ladders:
                    self.pos = self.ladders[self.pos]
                if self.pos in self.snakes:  # could it be a ladder end lands in a snake start
                    self.pos = self.snakes[self.pos]
            elif self.pos + value == self.goal:
                #print("succeed after ", cnt)
                return cnt
        #print("exit after trying 1000 times")
        return cnt
    def multi_play(self):
        cnts = []
        for i in range(self.play_times):
            cnts.append(self.play())
            
        success = 0
        total = 0
        for c in cnts:
            if c != 1000:
                success += 1
                total += c
        if success != 0:
            ave = total/success
        else:
            ave = -1
        #ave = [total/success: -1 if success != 0]
        return ave

num_of_tests = int(input())
#print("num_of_tests", num_of_tests)
for i in range(num_of_tests):
    p = []
    p_input = input().split(",")
    for j in range(6):
        p.append(float(p_input[j]))
    ls_input = input().split(",")
    lad = int(ls_input[0])
    sna = int(ls_input[1])
    ladders = {}
    ladders_input = input().split(" ")
    for j in range(lad):
        kv_input = ladders_input[j].split(",")
        k = int(kv_input[0])
        v = int(kv_input[1])
        ladders[k] = v
    snakes = {}
    snakes_input = input().split(" ")
    for j in range(sna):
        kv_input = snakes_input[j].split(",")
        k = int(kv_input[0])
        v = int(kv_input[1])
        snakes[k] = v  
    
    #print("done", p, ladders, snakes)
    game1 = Game(p, ladders, snakes)
    print(int(game1.multi_play()))

