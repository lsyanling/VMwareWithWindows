
set Tasks := { read "tasks.txt" as "<1s>" comment "#" };
set Processors := { read "processors.txt" as "<1s>" comment "#" };
param n := card(Tasks);
set Prioritys := { 1 to n };

set Tasks_X_Processors = Tasks cross Processors;
set Tasks_X_Prioritys = Tasks cross Prioritys;
set Tasks_X_Tasks = Tasks cross Tasks;

# A[i,j]表示第i个任务分配给第j个处理器
var A[Tasks_X_Processors] binary;

# B[i,j]表示第i个任务分配第j个优先级
var B[Tasks_X_Prioritys] binary;

# 一个任务只能分配给一个处理器
subto Constraint_5_2:
	forall <Task_i> in Tasks:
        sum <Processor_j> in C: A[Task_i, Processor_j] == 1;

# 一个任务只能分配一个优先级
subto Constraint_5_3:
	forall <Task_i> in Tasks:
        sum <Priority_j> in C: B[Task_i, Priority_j] == 1;

# 一个优先级只能分配给一个任务
subto Constraint_5_4:
	forall <Priority_j> in Tasks:
        sum <Task_i> in C: B[Task_i, Priority_j] == 1;

# V[i,j]表示第i个任务和第j个任务分配在同一个处理器
var V[Tasks_X_Tasks] binary;

# 
subto Constraint_5_5:
    forall <Task_i> in Tasks:
        forall <Task_j> in Tasks - { Task_i }:
            forall <Task_k> in Tasks - {Task_i, Task_j}:
                V[Task_i, Task_j] >= 1 - (2 - A[Task_i, Task_k] - A[Task_j, Task_k]);

# Q[i,j]表示第i个任务的优先级高于第j个任务
var Q[Tasks_X_Tasks] binary;

# 
subto Constraint_5_6:
	forall <Task_i> in Tasks:
        forall <Task_j> in Tasks - { Task_i }:
            forall <Priority_p> in Prioritys - { n }:
                Q[Task_i, Task_j] <= ((sum <Task_k> in Tasks with Task_k >= Priority_p + 1) + 1 - B[Task_i, Priority_p]);

# 覆盖第i个任务优先级最低的情况
subto Constraint_5_7:
	forall <Task_i> in Tasks:
        forall <Task_j> in Tasks - { Task_i }:
            Q[Task_i, Task_j] <= 1 - B[Task_i, n];

# 第i个任务和第j个任务的优先级有且只有一个更高
subto Constraint_5_8:
	forall <Task_i> in Tasks:
        forall <Task_j> in Tasks - { Task_i }:
            Q[Task_i, Task_j] + Q[Task_j, Task_i] == 1;

param Periods[Tasks] := read "tasks.txt" as "<1s> 2n" comment "#";
param WCET[Tasks] := read "tasks.txt" as "<1s> 3n" comment "#";
param BCET[Tasks] := read "tasks.txt" as "<1s> 4n" comment "#";
var ResponseTime[Tasks];

# 隐式截止期约束
subto Constraint_5_9:
	forall <Task_i> in Tasks:
        ResponseTime[Task_i] <= Periods[Task_i];

var H[Tasks_X_Tasks];

# 根据时间预算分析 TDA 计算响应时间
subto Constraint_5_10:
	forall <Task_i> in Tasks:
        ResponseTime[Task_i] == WCET[Task_i] + sum <Task_j> in Tasks with Task_i != Task_j : H[Task_i][Task_j] * WCET[Task_j];

subto Constraint_5_11_1:
	forall <Task_i> in Tasks:
        forall <Task_j> in Tasks:
            H[Task_i, Task_j] <= ceil(Periods[Task_i] / Periods[Task_j]);

subto Constraint_5_11_2:
	forall <Task_i> in Tasks:
        forall <Task_j> in Tasks:
            H[Task_i, Task_j] >= (-Periods[Task_i] / Periods[Task_j]) * (1 - V[Task_i, Task_j] + Q[Task_i, Task_j]) + ResponseTime[Task_i] / Periods[Task_j];

do print "Load: ", sum <Task_i> in Tasks: WCET[Task_i] / Periods[Task_i];
do print "Cores: ", card(Processors);
do print "Tasks: ", card(Tasks);