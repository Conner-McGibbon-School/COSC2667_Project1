from time import time, sleep
import queue
import random

# Job class to represent a job
class Job:
    def __init__(self, job_number, burst_time, file_path):
        self.job_number = job_number
        self.burst_time = burst_time
        self.time_left = burst_time
        self.start_time = None
        self.turnaround_time = None
        self.wait_start = None
        self.response_time = None
        self.wait_time = 0
        self.file_path = file_path
    
    # record the start time of the job and the time it started waiting
    def start(self):
        self.start_time = time()
        self.wait_start = self.start_time
    
    # record the new start time for waiting
    def start_waiting(self):
        self.wait_start = time()
    
    # record the time the job stopped waiting and add the time waited to the total wait time
    # if the job has not been run yet, record the response time
    def stop_waiting(self):
        self.wait_time += time() - self.wait_start
        if self.response_time is None:
            self.response_time = self.wait_time
    
    # record turnaround time and append the job to the output file
    def end(self):
        self.turnaround_time = time() - self.start_time
        self.append_to_file()
    
    # append the job to the output file
    def append_to_file(self):
        with open(self.file_path, "a") as f:
            f.write(f"{self.job_number}, {self.burst_time}, {self.turnaround_time}, {self.response_time}, {self.wait_time}\n")

# ReadyJobs class to represent a queue of jobs
class ReadyJobs:
    def __init__(self):
        self.jobs = queue.Queue()

    def put(self, job):
        self.jobs.put(job)

    def get(self):
        return self.jobs.get()
    
    def empty(self):
        return self.jobs.empty()


# First Come First Serve scheduler
def Scheduler1(queue):
    while True:
        job = queue.get()
        # if the queue is empty and there are no more jobs to run, break the loop
        if job is None and queue.empty():
            break
        # if the queue is empty but there are more jobs to run, put None back in the queue
        elif job is None:
            queue.put(None)
        else:
            job.stop_waiting()
            print(f"Running job {job.job_number}")
            sleep(job.burst_time)
            job.end()
            

# Round Robin scheduler
def Scheduler2(queue, quantum):
    while True:
        job = queue.get()
        # if the queue is empty and there are no more jobs to run, break the loop
        if job is None and queue.empty():
            break
        # if the queue is empty but there are more jobs to run, put None back in the queue
        elif job is None:
            queue.put(None)
        else:
            job.stop_waiting()
            print(f"Running job {job.job_number}")
            # if the job has time left, run it for the quantum time
            if job.time_left > quantum:
                sleep(quantum)
                job.time_left -= quantum
                job.start_waiting()
                queue.put(job)
            # if the job has less time left than the quantum time, run it for the remaining time
            else:
                sleep(job.time_left)
                job.end()


# Producer function to generate jobs
def Producer(queue, file_path, amount=-1):
    job_number = 1
    while amount != 0:
        print(f"Producing job {job_number}")
        burst_time = random.randint(4, 15) / 1000
        job = Job(job_number, burst_time, file_path)
        job.start()
        queue.put(job)
        job_number += 1
        amount -= 1
        sleep(random.randint(5, 20) / 1000)
    queue.put(None)

