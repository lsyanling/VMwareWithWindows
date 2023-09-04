set T:={ read "tasks.txt" as "<1s>" comment "#" };
set C:={ read "processors.txt" as "<1s>" comment "#" };
set P:={ 1 to card(T)};
param period[T]:=read "tasks.txt" as "<1s> 2n" comment "#";
param jitter[T]:=read "tasks.txt" as "<1s> 5n" comment "#";
param wcet[T]:=read "tasks.txt" as "<1s> 3n" comment "#";
param bcet[T]:=read "tasks.txt" as "<1s> 4n" comment "#";
set M :=T cross C;
set N :=T cross P;
set TT:=T cross T;
var A[M] binary;
var PI[N] binary;
var V[TT] binary;
var X[TT] binary;
var RT[T] integer >= 0;
var OFF[T] integer >= 0;
var H[<i,x> in TT] integer >=0 <=ceil(period[i]/period[x]);
var I[T] integer >= 0;

subto map:          # Eq.(15)
	forall <i> in T: sum <k> in C: A[i,k] == 1;

subto assign1:      # Eq.(16)
	forall <i> in T: sum <p> in P: PI[i,p] == 1;

subto assign2:      # Eq.(17)
	forall <p> in P: sum <i> in T: PI[i,p] <= 1;


subto sameproc:     # Eq.(18)
	forall <x> in T: 
		forall <i> in T - {x}:
			forall <k> in C:
				V[x,i] >= 1 - (2 - A[i,k] - A[x,k]);

subto prio1:        # Eq.(19)
	forall <x> in T:
		forall <i> in T - {x}:
			forall <p> in P - { card(T) }:
				X[i,x] <= sum <j> in { p+1 to card(T) }:
					PI[x,j] + (1 - PI[i,p]);

subto prio2:        # Eq.(20)
	forall <x> in T:
		forall <i> in T - {x}:
            X[i,x] <= 1 - PI[i,card(T)];

subto prio3:        # Eq.(21)
	forall <x> in T:
		forall <i> in T - {x}:
			X[i,x] + X[x,i] == 1;

subto responsetime: # Eq.(22)
	forall <i> in T:
		RT[i] == wcet[i] + I[i];
subto interf1:      # Eq.(22)
	forall <i> in T:
		I[i] == sum <x> in T - { i }: H[i,x] * wcet[x];

subto interf2:      # Eq.(23)
	forall <i> in T:
		forall <x> in T - {i}:
			if period[x] > period[i] 
				or period[i] mod period[x] != 0 then

				H[i,x] >= (RT[i] + jitter[x]) / period[x] 
					- ceil(period[i]/period[x]) * (1 - V[i,x] + X[i,x])
			else
				H[i,x] >= (RT[i] + OFF[i] - OFF[x]) / period[x] 
     - ceil(period[i]/period[x]) * (1 - V[i,x] + X[i,x])
			end;

subto deadline:     # Eq.(24)
	forall <i> in T:
		RT[i] + OFF[i] + jitter[i] <= period[i];
				
do print "Load: ", sum <t> in T: wcet[t] / period[t];
do print "Cores: ", card(C);
do print "Tasks: ", card(T);
