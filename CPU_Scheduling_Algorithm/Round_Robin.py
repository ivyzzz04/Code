## Round Robin
# 'REFERENCE' - refer to section 6 'References' in documentation for citation 
#********************************************************************************

# Initialising empty list and dictionary to append various values later within the program
process_lists = []
burst_times_list={}

# Initializing variables to assign sum of waiting and turnaround time to; initially assigning 0 to each
sum_waiting_time=0
sum_turnaround_time=0


# Prompting user to enter number of process they require
number = int(input(f"\nEnter number of processes: "))

# Using for loop to prompt for each process' burst time(bt) and and arrival time(at); appending process number, bt and at to list
for i in range(number):
    burst_time = int(input(f"\nEnter burst time for process P{i + 1}: "))
    arrival_time = int(input(f"Enter arrival time for process P{i + 1}: "))
    process_lists.append([f'P{i+1}',arrival_time,burst_time])

# Prompting user to enter time quantum they require
time_quantum = int(input("\nEnter time quantum: "))

# Sorting list in ascending order by arrival time
sorted_process_lists=sorted(process_lists,key=lambda x:x[1])

# _____________________________________________________________________________________________________________________________________ REFERENCE [3]
# Initialising burst times dictionary; process number-key : bt-value
for i in process_lists:
    burst_times_list[i[0]]=i[2]

time=0
gantt_chart=[]
finished_process_list={}

# Using for loop to continue execution of processes till list is empty i.e., all are executed completely
while len(sorted_process_lists)!=0:
    ready_queue=[]                                             

# Process appended to queue if arrival time <= current time
    for i in sorted_process_lists:
        if i[1]<=time:
            ready_queue.append(i)

# No processes ready - appends the current time to list 'gantt_chart' and states it was idle
    if not ready_queue:
        gantt_chart.append(['Idle',time])                                                                                   
        time+=1
        continue

# First process from ready queue is removed from list after assigning to variable 'process'
    else:
        process=ready_queue[0]
        sorted_process_lists.remove(process)
        remaining_burst=burst_times_list[process[0]]              # Remaining burst time of the proceess in execution is calculated  
        gantt_chart.append([process[0],time])                     # Appends process and current time to list 'gantt_chart'

# If remaining burst time is less than time quantum, the value is added to current time - signifies complete execution of process
        if remaining_burst<=time_quantum:
            time+=remaining_burst

    # Calculating completion time, turnaround time and waiting time, appending all to dictionary with key -> process number           
            completion_time = time
            arrival_time = process[1]
            burst_time=process[2]
            turnaround_time = completion_time - arrival_time
            waiting_time = turnaround_time - burst_time
            finished_process_list[process[0]] = [arrival_time,burst_time,completion_time,waiting_time,turnaround_time]
            continue

# If process has not completed execution, it is added back to list 
        else: 
            time+=time_quantum
            burst_times_list[process[0]]-= time_quantum             # Subtraction of time quantum from burst time
            sorted_process_lists.append(process)

gantt_chart.append([process[0],time])                                                                                        
# ________________________________________________________________________________________________________________________________ END REFERENCE [3]

# Printing final statements to display process number, arrival time, burst time, completion time, waiting time and turnaround time in a tabular manner
print(f"\n{'Process Number':>15}{'Arrival Time':>15}{'Burst Time':>15}{'Completion Time':>20}{'Waiting Time':>15}{'Turnaround Time':>18}")
for key,value in finished_process_list.items():
    print(f"{key:>15}{value[0]:>15}{value[1]:>15}{value[2]:>20}{value[3]:>15}{value[4]:>18}") 

# Calculating the average waiting and turn around time
    sum_waiting_time+=value[3]
    sum_turnaround_time+=value[4]

# Printing Gantt chart to display order of execution of process
print("\nGantt Chart:")
for i in gantt_chart:
    print(f"{i[0]} ({i[1]}) |",end="  ")


avg_waiting_time=sum_waiting_time/number
avg_turnaround_time=sum_turnaround_time/number

# Displaying the average waiting and turn around time 
print()
print(f"\nAverage Waiting Time: {avg_waiting_time:.2f}")
print(f"Average Turn Around Time: {avg_turnaround_time:.2f}")

#********************************************************************************
# REFERENCE [1] in FCFS.py, SJF.py | Line 47 - 55, Line 61 - 64. Bhojasia, M. SJF Scheduling Program in C. (n.d.). Sanfoundry. https://www.sanfoundry.com/c-program-sjf-scheduling/#:~:text=SJF%20Scheduling%20Algorithm%20in%20C,(Shortest%20Remaining%20Time%20First).
# REFERENCE [2] in SJF.py | Line - Python code to sort two lists according to one list. Yang, D. (2022, July 23). Sorting two lists together according to the order of one list in Python. SysTutorials. https://www.systutorials.com/sorting-two-lists-together-according-to-the-order-of-one-list-in-python/
# REFERENCE [3] in Round_Robin.py | Line 6 - 48. HallowSiddharth. (n.d.). Operating-Systems-Lab/roundrobin.py at main · HallowSiddharth/Operating-Systems-Lab. GitHub. https://github.com/HallowSiddharth/Operating-Systems-Lab/blob/main/roundrobin.py