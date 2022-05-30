from scheduler import TaskScheduler

tasks = [
    Task(1, 'Visit Gyeongbokgung Palace', 80, []), 
    Task(1.1, 'Rent Hanbok + buy tickets', 10, [2.1, 2.2, 2.3, 3.1, 3.2, 3.3], multi_tasking = True, multi_tasking_with = [3.1, 3.2, 4.1, 4.3, 5.2, 5.3]), 
    Task(1.2, 'Take photos in traditional Hanbok', 30, [1.1, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3], multi_tasking = True, multi_tasking_with = [1.3]), 
    Task(1.3, 'Walk around the palace', 40, [1.1, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3], multi_tasking = True, multi_tasking_with = [1.2]), 
    Task(2, 'Take CS456 class', 150, []), 
    Task(2.1, 'Skip textbook + watch Khan Academy', 20, []), 
    Task(2.2, 'Do pre-class work', 40 , [2.1]), 
    Task(2.3, 'Participate in class', 90, [2.1, 2.2], starting_time = 540),
    Task(3, 'Eat Gamjatang', 90, []),
    Task(3.1, 'Find restaurants in Itaewon', 20, [2.1, 2.2, 2.3], multi_tasking = True, multi_tasking_with = [3.2, 1.1]),
    Task(3.2, 'Go through menu + order in Korean', 10, [3.1, 2.1, 2.2, 2.3], multi_tasking = True, multi_tasking_with = [3.1, 1.1]),
    Task(3.3, 'Enjoy food and company', 60, [3.1, 3.2, 2.1, 2.2, 2.3], starting_time = 750),
    Task(4, 'Neighborhood chill', 105, []),
    Task(4.1, 'Walk around Haebanchon neighborhood', 30, [2.1, 2.2, 2.3, 3.1, 3.2, 3.3], multi_tasking = True, multi_tasking_with = [4.3]),
    Task(4.2, 'Work at a small boutique cafe', 60, [2.1, 2.2, 2.3, 3.1, 3.2, 3.3]),
    Task(4.3, 'Buy groceries to make Kimchi', 15, [2.1, 2.2, 2.3, 3.1, 3.2, 3.3], multi_tasking = True, multi_tasking_with = [4.1]),
    Task(5, 'Han River chill', 110, []),
    Task(5.1, 'Bike around Han River', 30, [2.1, 2.2, 2.3, 3.1, 3.2, 3.3]),
    Task(5.2, 'Eat Fried chicken + drink Soju', 20, [5.1, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3], multi_tasking = True, multi_tasking_with = [5.3]),
    Task(5.3, 'Hangout with friends', 60, [5.1, 5.2, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3], multi_tasking = True, multi_tasking_with = [5.2]),
]

task_scheduler = TaskScheduler(tasks, MaxHeap(), MaxHeap())
task_scheduler.run_task_scheduler() 
