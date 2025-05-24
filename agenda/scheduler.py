def schedule_tasks(tasks):
    return interval_schedule(tasks)

def interval_schedule(tasks):
    sorted_tasks = sorted(tasks, key=lambda x: x.end_time)
    result = []
    last_end = None
    for task in sorted_tasks:
        if last_end is None or task.start_time >= last_end:
            result.append(task)
            last_end = task.end_time
    return result
