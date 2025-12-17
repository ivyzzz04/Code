## Shortest Job First
# 'REFERENCE' - refer to section 6 'References' in documentation for citation 
#****************************************************************************************************************

# Initialising empty lists to append various values later within the program
process_number=[]
burst_time=[]
final=[]

waiting_time=[]
turnaround_time=[]

# Initializing variables to assign sum of waiting and turnaround time to; initially assigning 0 to each
sum_waiting_time=0
sum_turnaround_time=0

# Prompting user to enter number of process they require
number=int(input(f"\nEnter the number of processes: "))

# Using for loop to prompt for each process' burst time and creating process numbers (P1,P2....Pn), appending to their respective list
for i in range(number):
    process_burst=int(input(f"Enter the burst time for process P{i+1}: "))
    burst_time.append(process_burst)

for i in range(1,number+1):
    x=f"P{i}"
    process_number.append(x)

# REFERENCE [2]
final_burst,final_process=zip(*sorted(zip(burst_time,process_number)))          # Sorting one list in similiar assortment of the other 
final_burst=list(final_burst)                                                   # Separating the lists
final_process=list(final_process)
# REFERENCE END

# REFERENCE [1]
# Calculating waiting time, turnaround time and the total sum of each using for loop and appending the values to their respective lists or variables
for i in range(len(final_process)):
    waiting_time_curr=sum(final_burst[:i])
    waiting_time.append(waiting_time_curr)
    turnaround_time_curr=waiting_time_curr+final_burst[i]
    turnaround_time.append(turnaround_time_curr)

    sum_waiting_time+=waiting_time_curr
    sum_turnaround_time+=turnaround_time_curr
# REFERENCE END


# Printing final statements to display process number, burst time, waiting time and turnaround time in a tabular manner
print(f"\n{'Process Number':>15}{'Burst Time':>15}{'Waiting Time':>15}{'Turnaround Time':>18}")
for a,b,c,d in zip(final_process,final_burst,waiting_time,turnaround_time):
    print(f"{a:>15}{b:>15}{c:>15}{d:>18}")


# Calculating the average waiting and turn around time and displaying each
print(f"\nAverage Waiting Time: {sum_waiting_time/len(final_process):.2f}")
print(f"Average Turnaround Time: {sum_turnaround_time/len(final_process):.2f}")
print()

#********************************************************************************
# REFERENCE [1] in FCFS.py, SJF.py | Line 47 - 55, Line 61 - 64. Bhojasia, M. SJF Scheduling Program in C. (n.d.). Sanfoundry. https://www.sanfoundry.com/c-program-sjf-scheduling/#:~:text=SJF%20Scheduling%20Algorithm%20in%20C,(Shortest%20Remaining%20Time%20First).
# REFERENCE [2] in SJF.py | Line - Python code to sort two lists according to one list. Yang, D. (2022, July 23). Sorting two lists together according to the order of one list in Python. SysTutorials. https://www.systutorials.com/sorting-two-lists-together-according-to-the-order-of-one-list-in-python/
# REFERENCE [3] in Round_Robin.py | Line 6 - 48. HallowSiddharth. (n.d.). Operating-Systems-Lab/roundrobin.py at main · HallowSiddharth/Operating-Systems-Lab. GitHub. https://github.com/HallowSiddharth/Operating-Systems-Lab/blob/main/roundrobin.py