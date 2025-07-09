# - [362. Design Hit Counter](https://leetcode.com/problems/design-hit-counter/)
"""
Design a hit counter which counts the number of hits received in the past 5 minutes (300 seconds).

Implement the following methods:
void hit(int timestamp) Record a hit at the given timestamp (in seconds).

int getHits(int timestamp) Return the number of hits in the past 5 minutes from the given timestamp.

You may assume timestamp is increasing with each call.


🔍 Time/Space:
Time: O(1) for hit(), O(300) for getHits()

Space: O(300)
"""
class HitCounter:
    def __init__(self):
        self.time = [0] * 300
        self.hits = [0] * 300
    
    def hit(self, timestamp):
        idx = timestamp % 300
        if self.time[idx] != timestamp:
            self.time[idx] = timestamp
            self.hits[idx] = 1
        else:
            self.hits[idx] += 1
    
    def getHits(self, timestamp):
        total = 0
        for i in range(300):
            if timestamp - self.times[i] < 300:
                total += self.hits[i]
        return total