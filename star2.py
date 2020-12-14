#!/usr/bin/env python3

from sys import argv
from collections import defaultdict
import re
import time as tm

class Worker:

    default_step_length = 61
    time_finished = 0
    step = None

    def assign(self, step, start_time):
        self.step = step
        self.time_finished = ord(step) - ord('A') + self.default_step_length + start_time

    def process(self, current_time):
        if self.step and self.time_finished <= current_time:
            step = self.step
            self.step = None
            self.time_finished = 0
            return step

    def __repr__(self):
        return '{}: {}'.format(self.step, self.time_finished) if self.step else 'Free'


regex = re.compile('Step (.) must be finished before step (.) can begin.')
dependency_map = defaultdict(set)
available = set()
finished = list()

newly_available = None

def assign_job(worker, current_time):
    if not pending:
        return
    job = pending[-1]
    worker.assign(job, current_time)
    pending.pop()

def check_progress(worker):
    if worker.step:
        finished_step = worker.process(time)

        if finished_step:
            finished.append(finished_step)

            for dependent_step, dependencies in dependency_map.items():
                if finished_step in dependencies:
                    dependencies.remove(finished_step)
                    if not dependencies:
                        newly_available.append(dependent_step)


start_time = tm.time()

with open("G:\\24daysofcode\\input7.txt", 'r') as f:
    for line in f:
        match = regex.match(line)
        first, second = match.groups()
        
        if first not in available and first not in dependency_map:
            available.add(first)

        if second in available:
            available.remove(second)

        dependency_map[second].add(first)
        
pending = sorted(available, reverse=True)

time = 0
workers = [Worker() for i in range(5)]

while True:
    newly_available = list()
    for worker in workers: 
        check_progress(worker)

    for s in newly_available:
        del dependency_map[s]

    pending.extend(newly_available)
    pending.sort(reverse=True)

    for worker in workers:
        if not worker.step:
            assign_job(worker, time)
    if any(worker.step for worker in workers):
        time = min([w.time_finished for w in workers if w.time_finished])
    else:
        break

print(''.join(finished))
print(time)
print("time taken:", tm.time()-start_time)