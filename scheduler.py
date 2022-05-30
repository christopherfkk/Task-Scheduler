class MaxHeap:
    
    def __init__(self):
        self.heap = []
        self.heap_size = 0
        
    def left(self, i):
        return 2*i + 1
    
    def right(self, i):
        return 2*i + 2
    
    def parent(self, i):
        return (i-1)//2
    
    def maxkey(self):
        return self.heap[0]
    
    def heappush(self, key):
        
        self.heap.append(-float('inf')) 
        self.increase_key(self.heap_size, key) 
        self.heap_size += 1 
    
    def increase_key(self, i, key):
        
        if key < self.heap[i]:
            raise ValueError('New key is smaller than the current key')
        
        self.heap[i] = key
        
        while i > 0 and self.heap[self.parent(i)] < self.heap[i]:
            j = self.parent(i)
            self.heap[j], self.heap[i] = self.heap[i], self.heap[j] 
            i = j 
            
    def heapify(self, i):
        
        if self.left(i) <= (self.heap_size-1) and self.heap[self.left(i)] > self.heap[i]:
            largest = self.left(i)
            
        else: largest = i
            
        if self.right(i) <= (self.heap_size-1) and self.heap[self.right(i)] > self.heap[largest]:
            largest = self.right(i)
        
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self.heapify(largest) 
            
    def heappop(self):
        
        if self.heap_size < 1:
            raise ValueError("Heap underflow: no keys in the priority queue")
            
        maxkey = self.heap[0] 
        self.heap[0] = self.heap[-1] 
        self.heap.pop() 
        self.heap_size -= 1
        self.heapify(0) 
        
        return maxkey
    
    def heapclean(self):
        
        self.heap.clear()
        self.heap_size = 0
    
    # changed
    def __getitem__(self, val):
        try:
            get = self.heap[val]
        except:
            get = float("-inf") # if the priority queue is empty, then return sentinel
            
        return get
    
class Task:
    
    def __init__(self, task_id, description, duration, dependencies, status = 'N', other_dependencies = None, starting_time = None, multi_tasking = False, multi_tasking_with = None):
        
        self.id = task_id
        self.description = description
        self.duration = duration
        self.dependencies = dependencies
        self.status = status
        self.other_dependencies = other_dependencies 
        self.starting_time = starting_time
        self.multi_tasking = multi_tasking # new attribute
        self.multi_tasking_with = multi_tasking_with # new attribute
        
    def __repr__(self):
        return f"{self.description} - id: {self.id}\n\tDuration:{self.duration}\n\tDepends on: {self.dependencies}\n\tStatus: {self.status}\n\tDepended by: {self.other_dependencies}\n\tStarting time: {self.starting_time}"
    
    # added: so operators can be used to directly compare Task instances
    def __lt__(self, other):
        
        if isinstance(self, Task) and isinstance(other, Task):
            return self.other_dependencies < other.other_dependencies
        
        if isinstance(self, Task) and isinstance(other, (int, float)): # corresponds to sentinels
            return self.other_dependencies < other
    
    # added
    def __le__(self, other):
        
        if isinstance(self, Task) and isinstance(other, Task):
            return self.other_dependencies <= other.other_dependencies
        
        if isinstance(self, Task) and isinstance(other, (int, float)):
            return self.other_dependencies <= other
    
    # added
    def __ge__(self, other):
        
        if isinstance(self, Task) and isinstance(other, Task):
            return self.other_dependencies >= other.other_dependencies
        
        if isinstance(self, Task) and isinstance(other, (int, float)):
            return self.other_dependencies >= other
    
    # added
    def __gt__(self, other):
        
        if isinstance(self, Task) and isinstance(other, Task):
            return self.other_dependencies > other.other_dependencies
        
        if isinstance(self, Task) and isinstance(other, (int, float)):
            return self.other_dependencies > other
        
class TaskScheduler:
    
    NOT_STARTED = 'N'
    IN_PRIORITY_QUEUE = 'I'
    COMPLETED = 'C'
    PARENT = 'P'
    IN_PROGRESS = "IP" # new variable
    IN_MULTI_TASKING_QUEUE = "M" # new variable
    
    def __init__(self, tasks, priority_queue, multi_tasking_queue):
        self.tasks = tasks 
        self.priority_queue = priority_queue
        self.multi_tasking_queue = multi_tasking_queue # new attribute
        
    def print_tasks(self):
        print('Input list of Tasks')
        for t in self.tasks:
            print(t)
            
    def remove_dependency(self, task):
        for t in self.tasks:
            if t.id != task.id and task.id in t.dependencies: 
                t.dependencies.remove(task.id) 
                
    def check_unscheduled_tasks(self):
        for t in tasks:
            if t.status == self.NOT_STARTED:
                return True
        return False
    
    def format_time(self, time):
        return f"{time//60}h{time%60:02d}"
    
    def find_parent_task(self, subtask):
        for t in self.tasks:
            if int(subtask.id) == t.id and t.status == self.PARENT:
                parent = t
                return parent
    
    def count_other_dependencies(self, task):
        appearances = 0
        for t in self.tasks:
            if task.id in t.dependencies:
                appearances += 1
        
        task.other_dependencies = appearances 
        
    def get_earliest_time_constrained_task(self):
        
        earliest_time_constrained_task = Task(
            0, "Dummy", float("inf"), [], starting_time = float("inf"))
        
        for t in self.tasks:
            if (t.starting_time is not None) and (
                t.status != self.COMPLETED) and (
                t.starting_time < earliest_time_constrained_task.starting_time):
                earliest_time_constrained_task = t
                
        return earliest_time_constrained_task
                
    # changed
    def get_tasks_ready(self):
        
        for t in self.tasks:
            
            if t.id % 1 == 0 and t.status != self.PARENT:
                t.status = self.PARENT
            
            self.count_other_dependencies(t)
            
            if t.status != self.COMPLETED and t.status != self.PARENT:
                
                if t.multi_tasking is False:
                    t.status = self.IN_PRIORITY_QUEUE
                    self.priority_queue.heappush(t)
                    
                # if multi_tasking is True, push it to the newly created multi_tasking_queue
                elif t.multi_tasking is True:
                    t.status = self.IN_MULTI_TASKING_QUEUE
                    self.multi_tasking_queue.heappush(t) 
    
    # changed
    def run_task_scheduler(self, starting_time = 480): 
        
        current_time = starting_time
        
        # while there are still unscheduled tasks or the two queues are not empty
        while self.check_unscheduled_tasks() or self.priority_queue.heap or self.multi_tasking_queue.heap: 
            
            self.priority_queue.heapclean()
            self.multi_tasking_queue.heapclean() # clean the new multi_tasking queue too
            self.get_tasks_ready()
                            
            earliest_time_constrained_task = self.get_earliest_time_constrained_task()
            
            # if first task of priority queue has higher priority value than that of multi-tasking queue
            if self.priority_queue and self.priority_queue[0] >= self.multi_tasking_queue[0]:
                
                # if first task of priority queue doesn't exceed the next time constraint
                if (current_time + self.priority_queue[0].duration
                    ) <= earliest_time_constrained_task.starting_time:
                    
                    current_task = self.priority_queue.heappop()
                    current_task.status = self.IN_PROGRESS
                    parent_task = self.find_parent_task(current_task)
                
                    if (current_task.starting_time is not None
                       ) & (current_time != current_task.starting_time):
                        
                        print(f"❌ Time: {self.format_time(current_time)}, {current_task.starting_time - current_time} mins down-time until the next task")
                        current_time = current_task.starting_time
                
                    print(f"⏰ Time: {self.format_time(current_time)}, Task ID: {current_task.id}, Duration: {current_task.duration} mins, Parent ID: {parent_task.id}, Parent: {parent_task.description}")
                    current_time += current_task.duration 
                    print(f"✅ Completed Task {current_task.id} - '{current_task.description}' at time {self.format_time(current_time)}\n")
                    print(f"\tNot Multitaskable, FOCUS!\n")
                
                # else execute the time-constrained task
                else:
                    current_task = earliest_time_constrained_task
                    parent_task = self.find_parent_task(current_task)

                    if current_time != earliest_time_constrained_task.starting_time:
                        print(f"❌ Time: {self.format_time(current_time)}, {current_task.starting_time - current_time} mins down-time until the next task")
                        current_time = current_task.starting_time

                    print(f"⏰ Time: {self.format_time(current_time)}, Task ID: {current_task.id}, Duration: {current_task.duration} mins, Parent ID: {parent_task.id}, Parent: {parent_task.description}")
                    current_time += current_task.duration 
                    print(f"✅ Completed Task {current_task.id} - '{current_task.description}' at time {self.format_time(current_time)}\n")                     
                
            # if first task of priority queue has lower priority value than that of multi-tasking queue  
            
            if self.multi_tasking_queue and self.priority_queue[0] < self.multi_tasking_queue[0]:
                
                # if first task of multi-tasking queue doesn't exceed the next time constraint
                if (current_time + self.multi_tasking_queue[0].duration
                    ) <= earliest_time_constrained_task.starting_time:
                
                    current_task = self.multi_tasking_queue.heappop()
                    parent_task = self.find_parent_task(current_task)
                    
                    print(f"⏰ Time: {self.format_time(current_time)}, Task ID: {current_task.id}, Duration: {current_task.duration} mins, Parent ID: {parent_task.id}, Parent: {parent_task.description}")
                    current_time += current_task.duration 
                    print(f"✅ Completed Task {current_task.id} - '{current_task.description}' at time {self.format_time(current_time)}\n")                     
                    
                    # if the next task in multi-tasking queue is in the list of the first tasks' multi-taskable list
                    if current_task.id in self.multi_tasking_queue[0].multi_tasking_with:
                        
                        # execute the next task too for multi-tasking
                        current_task_2 = self.multi_tasking_queue.heappop()
                        parent_task_2 = self.find_parent_task(current_task_2)
                        
                        current_time -= current_task.duration
                        
                        print(f"\t⏰ Multitask Time: {self.format_time(current_time)}, Task ID: {current_task_2.id}, Duration: {current_task_2.duration} mins")
                        current_time += current_task_2.duration 
                        print(f"\t✅ Completed Multitask {current_task_2.id} - '{current_task_2.description}' at {self.format_time(current_time)}\n")
                    
                        self.remove_dependency(current_task_2)
                        current_task_2.status = self.COMPLETED
                        
                        # current time set until the longer of the two tasks is completed
                        if current_task.duration >= current_task_2.duration:
                              current_time = current_time - current_task_2.duration + current_task.duration
                              
                        else:
                              current_time = current_time
                    
                    # else the first task is multi-taskable but no next is task is scheduled too
                    else:
                        
                        print(f"\tMultitaskable but no suitable task available!\n")
                
                else:
                    
                    current_task = earliest_time_constrained_task
                    parent_task = self.find_parent_task(current_task)

                    if current_time != earliest_time_constrained_task.starting_time:
                        print(f"❌ Time: {self.format_time(current_time)}, {current_task.starting_time - current_time} mins down-time until the next task")
                        current_time = current_task.starting_time

                    print(f"⏰ Time: {self.format_time(current_time)}, Task ID: {current_task.id}, Duration: {current_task.duration} mins, Parent ID: {parent_task.id}, Parent: {parent_task.description}")
                    current_time += current_task.duration 
                    print(f"✅ Completed Task {current_task.id} - '{current_task.description}' at time {self.format_time(current_time)}\n")
                    print(f"\tNot Multitaskable, FOCUS!\n")
            
            self.remove_dependency(current_task)
            current_task.status = self.COMPLETED
                
        total_time = current_time - starting_time
        print(f"🏁 Time: {self.format_time(current_time)} - Completed all planned tasks in {total_time//60}h{total_time%60:02d}min")                
