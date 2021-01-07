import numpy as np

class single_server:
    def __init__(self):

        self.Q =0 ; self.M=0 ; self.Before =0; self.SumQ =0
        self.clk=0

        self.events = np.array([])

    def initialize_routine(self):
        self.Q=0
        self.M=1
        self.Before =0
        self.SumQ =0

        self.events = np.append(self.events, [1, np.random.exponential(5)])
        self.empty = 0


    def event_routine(self, k, time): # 1 = arrival, 2 = load, 3 = unload
        if k == 1:
            self.SumQ += self.Q*(time-self.Before)
            self.Before = time
            self.Q += 1
            print("arrival")

            # generate new event
            if self.empty == 1:
                self.events = np.array([1, time + np.random.exponential(5)]) # arrival
                if self.M > 0:
                    self.events = np.vstack((self.events, np.array([2, time])))  # load
                self.events = self.events[np.argsort(self.events[:, 1])]
            else:
                self.events = np.vstack((self.events, np.array([1, time + np.random.exponential(5)]))) # arrival
                if self.M > 0:
                    self.events = np.vstack((self.events, np.array([2, time]))) # load
                self.events = self.events[np.argsort(self.events[:, 1])]

        elif k == 2:
            self.SumQ += self.Q*(time-self.Before)
            self.Before = time
            self.Q -= 1
            self.M -= 1
            print("load")

            # generate new event
            if self.empty == 1:
                self.events = np.array([3, time + np.random.uniform(4, 6)])
            else:
                self.events = np.vstack((self.events, np.array([3, time + np.random.uniform(4, 6)])))
                self.events = self.events[np.argsort(self.events[:, 1])]

        elif k == 3:
            self.M += 1
            print("unload")

            # generate new event
            if self.Q > 0:
                if self.empty == 1:
                    self.events = np.array([2, time])
                else:
                    self.events = np.vstack((self.events, np.array([2, time])))
                    self.events = self.events[np.argsort(self.events[:, 1])]


    def retrieve_event(self):
        if np.shape(self.events) == (2,):
            k = self.events[0]
            time = self.events[1]
            self.events = 0
            self.empty = 1
        else:
            k = self.events[0, 0]
            time = self.events[0, 1]
            self.events = np.delete(self.events, 0, axis= 0)
            self.empty = 0

        return k, time

    def statistics(self, time):
        self.SumQ += self.Q * (time - self.Before)
        AQL = self.SumQ / time

        return AQL


#### main code ####

m = single_server()
clk = 0
m.initialize_routine()

while clk < 300:
    k, time = m.retrieve_event()
    clk = time

    m.event_routine(k, time)

AQL = m.statistics(clk)

print(AQL)
