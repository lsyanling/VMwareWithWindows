# 说明
delta xinbin 与 delta xinbin nooffset 与 delta xinbin nooffset nobcet 结果相同，后两者完全相同
zhu 的三组完全相同


## schlatow source assign
schlatow 原代码，优化处理器分配，优化offset
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc2                                       1 	(obj:0)
A$taskC$Proc2                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc2                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc1                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc1                                       1 	(obj:0)
PI$taskA#3                                          1 	(obj:0)
PI$taskB#7                                          1 	(obj:0)
PI$taskC#9                                          1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#5                                          1 	(obj:0)
PI$taskG#4                                          1 	(obj:0)
PI$taskH#11                                         1 	(obj:0)
PI$taskI#6                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#8                                          1 	(obj:0)
PI$taskL#10                                         1 	(obj:0)
AGE#1                                           11885 	(obj:2260800)
AGE#2                                           12323 	(obj:2260800)
### Pycpa
TODO


## schlatow source noassign
schlatow 原代码，不优化处理器分配，优化offset
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#11                                         1 	(obj:0)
PI$taskB#9                                          1 	(obj:0)
PI$taskC#10                                         1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#7                                          1 	(obj:0)
PI$taskG#5                                          1 	(obj:0)
PI$taskH#8                                          1 	(obj:0)
PI$taskI#6                                          1 	(obj:0)
PI$taskJ#4                                          1 	(obj:0)
PI$taskK#3                                          1 	(obj:0)
PI$taskL#12                                         1 	(obj:0)
AGE#1                                           72655 	(obj:2260800)
AGE#2                                           73093 	(obj:2260800)
### Pycpa
TODO


## schlatow nooffset assign
schlatow offset和jitter为0，优化处理器分配
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc2                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc1                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc1                                       1 	(obj:0)
A$taskL$Proc1                                       1 	(obj:0)
PI$taskA#8                                          1 	(obj:0)
PI$taskB#12                                         1 	(obj:0)
PI$taskC#5                                          1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#3                                          1 	(obj:0)
PI$taskG#4                                          1 	(obj:0)
PI$taskH#6                                          1 	(obj:0)
PI$taskI#7                                          1 	(obj:0)
PI$taskJ#11                                         1 	(obj:0)
PI$taskK#10                                         1 	(obj:0)
PI$taskL#9                                          1 	(obj:0)
AGE#1                                           74635 	(obj:2260800)
AGE#2                                           85033 	(obj:2260800)
### Pycpa
chain1 data age: 64635
chain2 data age: 75033



## schlatow nooffset noassign
schlatow offset和jitter为0，优化处理器分配
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#11                                         1 	(obj:0)
PI$taskB#6                                          1 	(obj:0)
PI$taskC#7                                          1 	(obj:0)
PI$taskD#4                                          1 	(obj:0)
PI$ISR#3                                            1 	(obj:0)
PI$taskE#5                                          1 	(obj:0)
PI$taskG#1                                          1 	(obj:0)
PI$taskH#2                                          1 	(obj:0)
PI$taskI#8                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#10                                         1 	(obj:0)
PI$taskL#9                                          1 	(obj:0)
AGE#1                                           95675 	(obj:2260800)
AGE#2                                          106073 	(obj:2260800)
### Pycpa
chain1 data age: 45675
chain2 data age: 46073



## schlatow nooffset nobcet assign
schlatow offset和jitter为0，bcet=wcet，优化处理器分配
### SCIP
A$taskA$Proc2                                       1 	(obj:0)
A$taskB$Proc2                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc2                                       1 	(obj:0)
A$ISR$Proc2                                         1 	(obj:0)
A$taskE$Proc2                                       1 	(obj:0)
A$taskG$Proc1                                       1 	(obj:0)
A$taskH$Proc1                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc1                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#6                                          1 	(obj:0)
PI$taskB#9                                          1 	(obj:0)
PI$taskC#8                                          1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#3                                          1 	(obj:0)
PI$taskG#4                                          1 	(obj:0)
PI$taskH#11                                         1 	(obj:0)
PI$taskI#5                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#10                                         1 	(obj:0)
PI$taskL#7                                          1 	(obj:0)
AGE#1                                           70870 	(obj:2260800)
AGE#2                                           80870 	(obj:2260800)
Solving Time (sec) : 2584
### Pycpa
chain1 data age: 60870
chain2 data age: 70870



## schlatow nooffset nobcet noassign
schlatow offset和jitter为0，bcet=wcet，不优化处理器分配
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#11                                         1 	(obj:0)
PI$taskB#7                                          1 	(obj:0)
PI$taskC#10                                         1 	(obj:0)
PI$taskD#3                                          1 	(obj:0)
PI$ISR#2                                            1 	(obj:0)
PI$taskE#6                                          1 	(obj:0)
PI$taskG#1                                          1 	(obj:0)
PI$taskH#4                                          1 	(obj:0)
PI$taskI#5                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#9                                          1 	(obj:0)
PI$taskL#8                                          1 	(obj:0)
AGE#1                                           91910 	(obj:2260800)
AGE#2                                          101910 	(obj:2260800)
Solving Time (sec) : 1.47
### Pycpa
chain1 data age: 41910
chain2 data age: 41910



## delta xinbin assign
xinbin 的代码，OFF使用了param而不是var，jitter没改
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc2                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc2                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc1                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc1                                       1 	(obj:0)
A$taskL$Proc1                                       1 	(obj:0)
PI$taskA#9                                          1 	(obj:0)
PI$taskB#11                                         1 	(obj:0)
PI$taskC#7                                          1 	(obj:0)
PI$taskD#3                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#2                                          1 	(obj:0)
PI$taskG#4                                          1 	(obj:0)
PI$taskH#6                                          1 	(obj:0)
PI$taskI#5                                          1 	(obj:0)
PI$taskJ#8                                          1 	(obj:0)
PI$taskK#12                                         1 	(obj:0)
PI$taskL#10                                         1 	(obj:0)
AGE#1                                           73440 	(obj:2260800)
AGE#2                                           84390 	(obj:2260800)
Solving Time (sec) : 36.13
Solving Nodes      : 4172
### Pycpa
TODO



## delta xinbin noassign
xinbin 的代码，OFF使用了param而不是var，jitter没改
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#12                                         1 	(obj:0)
PI$taskB#4                                          1 	(obj:0)
PI$taskC#5                                          1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#3                                          1 	(obj:0)
PI$taskG#6                                          1 	(obj:0)
PI$taskH#7                                          1 	(obj:0)
PI$taskI#8                                          1 	(obj:0)
PI$taskJ#11                                         1 	(obj:0)
PI$taskK#10                                         1 	(obj:0)
PI$taskL#9                                          1 	(obj:0)
AGE#1                                           89390 	(obj:2260800)
AGE#2                                           97890 	(obj:2260800)
Solving Time (sec) : 2.26
Solving Nodes      : 18
### Pycpa
TODO



## delta xinbin nooffset assign
改自xinbin的代码，OFF改为var，jitter改为0
### SCIP
A$taskA$Proc2                                       1 	(obj:0)
A$taskB$Proc2                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc2                                       1 	(obj:0)
A$ISR$Proc2                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc1                                       1 	(obj:0)
A$taskH$Proc1                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc1                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#6                                          1 	(obj:0)
PI$taskB#10                                         1 	(obj:0)
PI$taskC#11                                         1 	(obj:0)
PI$taskD#4                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#2                                          1 	(obj:0)
PI$taskG#3                                          1 	(obj:0)
PI$taskH#8                                          1 	(obj:0)
PI$taskI#5                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#9                                          1 	(obj:0)
PI$taskL#7                                          1 	(obj:0)
AGE#1                                           73440 	(obj:2260800)
AGE#2                                           84390 	(obj:2260800)
Solving Time (sec) : 47.21
Solving Nodes      : 7877
### Pycpa
chain1 data age: 18335
chain2 data age: 20233



## delta xinbin nooffset noassign
改自xinbin的代码，OFF改为var，jitter改为0
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#8                                          1 	(obj:0)
PI$taskB#4                                          1 	(obj:0)
PI$taskC#5                                          1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#3                                          1 	(obj:0)
PI$taskG#6                                          1 	(obj:0)
PI$taskH#7                                          1 	(obj:0)
PI$taskI#9                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#11                                         1 	(obj:0)
PI$taskL#10                                         1 	(obj:0)
AGE#1                                           89390 	(obj:2260800)
AGE#2                                           97890 	(obj:2260800)
Solving Time (sec) : 3.40
Solving Nodes      : 71
### Pycpa
chain1 data age: 45675
chain2 data age: 46073



## delta xinbin nooffset nobcet assign
改自xinbin的代码，OFF改为var，jitter改为0
### SCIP
A$taskA$Proc2                                       1 	(obj:0)
A$taskB$Proc2                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc2                                       1 	(obj:0)
A$ISR$Proc2                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc1                                       1 	(obj:0)
A$taskH$Proc1                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc1                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#6                                          1 	(obj:0)
PI$taskB#10                                         1 	(obj:0)
PI$taskC#11                                         1 	(obj:0)
PI$taskD#4                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#2                                          1 	(obj:0)
PI$taskG#3                                          1 	(obj:0)
PI$taskH#8                                          1 	(obj:0)
PI$taskI#5                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#9                                          1 	(obj:0)
PI$taskL#7                                          1 	(obj:0)
AGE#1                                           73440 	(obj:2260800)
AGE#2                                           84390 	(obj:2260800)
Solving Time (sec) : 47.21
Solving Nodes      : 7877
### Pycpa
chain1 data age: 14570
chain2 data age: 16070



## delta xinbin nooffset nobcet noassign
改自xinbin的代码，OFF改为var，jitter改为0
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#8                                          1 	(obj:0)
PI$taskB#4                                          1 	(obj:0)
PI$taskC#5                                          1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#3                                          1 	(obj:0)
PI$taskG#6                                          1 	(obj:0)
PI$taskH#7                                          1 	(obj:0)
PI$taskI#9                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#11                                         1 	(obj:0)
PI$taskL#10                                         1 	(obj:0)
AGE#1                                           89390 	(obj:2260800)
AGE#2                                           97890 	(obj:2260800)
Solving Time (sec) : 3.40
Solving Nodes      : 71
### Pycpa
chain1 data age: 41910
chain2 data age: 41910



## zhu xinbin assign
xinbin 的代码，OFF使用了param而不是var，jitter没改
### SCIP
A$taskA$Proc2                                       1 	(obj:0)
A$taskB$Proc2                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc2                                       1 	(obj:0)
A$ISR$Proc2                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc1                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc1                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#8                                          1 	(obj:0)
PI$taskB#11                                         1 	(obj:0)
PI$taskC#2                                          1 	(obj:0)
PI$taskD#5                                          1 	(obj:0)
PI$ISR#3                                            1 	(obj:0)
PI$taskE#1                                          1 	(obj:0)
PI$taskG#6                                          1 	(obj:0)
PI$taskH#4                                          1 	(obj:0)
PI$taskI#7                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#10                                         1 	(obj:0)
PI$taskL#9                                          1 	(obj:0)
AGE#1                                          133090 	(obj:2260800)
AGE#2                                          144530 	(obj:2260800)
Solving Time (sec) : 70.26
Solving Nodes      : 1869 (total of 9049 nodes in 2 runs)
### Pycpa
TODO



## zhu xinbin noassign
xinbin 的代码，OFF使用了param而不是var，jitter没改
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#8                                          1 	(obj:0)
PI$taskB#4                                          1 	(obj:0)
PI$taskC#7                                          1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(改自xinbin的代码，OFF改为var，jitter改为0obj:0)
PI$taskE#3                                          1 	(obj:0)
PI$taskG#5                                          1 	(obj:0)
PI$taskH#6                                          1 	(obj:0)
PI$taskI#9                                          1 	(obj:0)
PI$taskJ#12                                         1 	(obj:0)
PI$taskK#11                                         1 	(obj:0)
PI$taskL#10                                         1 	(obj:0)
AGE#1                                          155330 	(obj:2260800)
AGE#2                                          165730 	(obj:2260800)
Solving Time (sec) : 2.19
Solving Nodes      : 19 (total of 20 nodes in 2 runs)
### Pycpa
TODO



## zhu nooffset assign
改自xinbin的代码，OFF改为var，jitter改为0
### SCIP
A$taskA$Proc2                                       1 	(obj:0)
A$taskB$Proc2                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc2                                       1 	(obj:0)
A$ISR$Proc2                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc1                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc1                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#9                                          1 	(obj:0)
PI$taskB#12                                         1 	(obj:0)
PI$taskC#6                                          1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#5                                          1 	(obj:0)
PI$taskG#3                                          1 	(obj:0)
PI$taskH#7                                          1 	(obj:0)
PI$taskI#4                                          1 	(obj:0)
PI$taskJ#8                                          1 	(obj:0)
PI$taskK#11                                         1 	(obj:0)
PI$taskL#10                                         1 	(obj:0)
AGE#1                                          133090 	(obj:2260800)
AGE#2                                          144530 	(obj:2260800)
Solving Time (sec) : 50.35
Solving Nodes      : 8713 (total of 10028 nodes in 2 runs)
### Pycpa
chain1 data age: 65135
chain2 data age: 76573



## zhu nooffset noassign
改自xinbin的代码，OFF改为var，jitter改为0
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#12                                         1 	(obj:0)
PI$taskB#10                                         1 	(obj:0)
PI$taskC#11                                         1 	(obj:0)
PI$taskD#5                                          1 	(obj:0)
PI$ISR#4                                            1 	(obj:0)
PI$taskE#8                                          1 	(obj:0)
PI$taskG#1                                          1 	(obj:0)
PI$taskH#2                                          1 	(obj:0)
PI$taskI#3                                          1 	(obj:0)
PI$taskJ#9                                          1 	(obj:0)
PI$taskK#7                                          1 	(obj:0)
PI$taskL#6                                          1 	(obj:0)
AGE#1                                          155330 	(obj:2260800)
AGE#2                                          165730 	(obj:2260800)
Solving Time (sec) : 2.65
Solving Nodes      : 97
### Pycpa
chain1 data age: 45675
chain2 data age: 46073



## zhu nooffset nobcet assign
改自xinbin的代码，OFF改为var，jitter改为0，bcet=wcet
### SCIP
A$taskA$Proc2                                       1 	(obj:0)
A$taskB$Proc2                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc2                                       1 	(obj:0)
A$ISR$Proc2                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc1                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc1                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#9                                          1 	(obj:0)
PI$taskB#12                                         1 	(obj:0)
PI$taskC#6                                          1 	(obj:0)
PI$taskD#2                                          1 	(obj:0)
PI$ISR#1                                            1 	(obj:0)
PI$taskE#5                                          1 	(obj:0)
PI$taskG#3                                          1 	(obj:0)
PI$taskH#7                                          1 	(obj:0)
PI$taskI#4                                          1 	(obj:0)
PI$taskJ#8                                          1 	(obj:0)
PI$taskK#11                                         1 	(obj:0)
PI$taskL#10                                         1 	(obj:0)
AGE#1                                          133090 	(obj:2260800)
AGE#2                                          144530 	(obj:2260800)
Solving Time (sec) : 50.19
Solving Nodes      : 8713 (total of 10028 nodes in 2 runs)
### Pycpa
chain1 data age: 61370
chain2 data age: 72410



## zhu nooffset nobcet noassign
改自xinbin的代码，OFF改为var，jitter改为0，bcet=wcet
### SCIP
A$taskA$Proc1                                       1 	(obj:0)
A$taskB$Proc1                                       1 	(obj:0)
A$taskC$Proc1                                       1 	(obj:0)
A$taskD$Proc1                                       1 	(obj:0)
A$ISR$Proc1                                         1 	(obj:0)
A$taskE$Proc1                                       1 	(obj:0)
A$taskG$Proc2                                       1 	(obj:0)
A$taskH$Proc2                                       1 	(obj:0)
A$taskI$Proc2                                       1 	(obj:0)
A$taskJ$Proc2                                       1 	(obj:0)
A$taskK$Proc2                                       1 	(obj:0)
A$taskL$Proc2                                       1 	(obj:0)
PI$taskA#12                                         1 	(obj:0)
PI$taskB#10                                         1 	(obj:0)
PI$taskC#11                                         1 	(obj:0)
PI$taskD#5                                          1 	(obj:0)
PI$ISR#4                                            1 	(obj:0)
PI$taskE#8                                          1 	(obj:0)
PI$taskG#1                                          1 	(obj:0)
PI$taskH#2                                          1 	(obj:0)
PI$taskI#3                                          1 	(obj:0)
PI$taskJ#9                                          1 	(obj:0)
PI$taskK#7                                          1 	(obj:0)
PI$taskL#6                                          1 	(obj:0)
AGE#1                                          155330 	(obj:2260800)
AGE#2                                          165730 	(obj:2260800)
Solving Time (sec) : 2.62
Solving Nodes      : 97
### Pycpa
chain1 data age: 41910
chain2 data age: 41910
