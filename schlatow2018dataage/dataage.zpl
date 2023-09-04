var Wp[<t> in T]        integer >= 0;   # w^+(0)
var Wm[<t> in T]        integer >= 0;   # w^-(0)
var Rp[<t> in T]        integer >= 0;   # r^+(0)
var Rm[<t> in T]        integer >= 0;   # r^-(0)
var D[<c,i> in CHAINID] integer >= 0;   # d^+_{i,i+1}
var AGE[S]              integer >= 0;   # DA
param RTm[<t> in T] := bcet[t];         # RT^-

# helper functions
defnumb add_period(c, i, n) := n * period[CHAINTASKS[c,i]];
defnumb taskperiod(c,i) := period[CHAINTASKS[c,i]];

# boolean helper functions
defbool oversampling(c,i,j)  := 
	 period[CHAINTASKS[c,j]] < period[CHAINTASKS[c,i]];
defbool undersampling(c,i,j) := 
	 period[CHAINTASKS[c,j]] > period[CHAINTASKS[c,i]];
defbool harmonic(c,i,j)      :=
	 period[CHAINTASKS[c,j]] mod period[CHAINTASKS[c,i]] == 0;

param Pmax := max <t> in T :  period[t];
param Pmin := min <t> in T :  period[t];
param nmax := ceil(Pmax / Pmin);

var MASKO[CHAINID*{0 to nmax}] binary;   # O
var MASKU[CHAINID] binary;               # U

subto lastdelay:
	forall <c> in S:
		D[c,CHAINLEN[c]] == 0;

subto rmin:     # Eq.(25)
	forall <i> in T:
		Rm[i] == OFF[i] - jitter[i];

subto rplus:    # Eq.(26)
	forall <i> in T:
		Rp[i] == Wp[i] - RTm[i];

subto wmin:     # Eq.(27)
	forall <i> in T:
		Wm[i] == OFF[i] - jitter[i] + RTm[i];

subto wplus:    # Eq.(28)
	forall <i> in T:
		Wp[i] == OFF[i] + jitter[i] + RT[i];

subto oversampling_decisions:  # Eq.(30)
	forall <c> in S:
		forall <i> in {1 to CHAINLEN[c]-1}:
			if oversampling(c,i,i+1) and harmonic(c,i+1,i) then 
				forall <n> in 
						{0 to ceil(taskperiod(c,i)/taskperiod(c,i+1)) - 1}:
					taskperiod(c,i)*(1-MASKO[c,i,n]) >= 
						Wp[CHAINTASKS[c,i]] - Rm[CHAINTASKS[c,i+1]] 
						- add_period(c, i+1, n)
			end;

subto oversampling_delay1:     # Eq.(31)
	forall <c> in S:
		forall <i> in {1 to CHAINLEN[c]-1}:
			if oversampling(c,i,i+1) and harmonic(c,i+1,i) then 
				forall <n> in 
						{0 to ceil(taskperiod(c,i)/taskperiod(c,i+1)) - 1}:
					D[c,i] >= Rp[CHAINTASKS[c,i+1]] 
															+ add_period(c,i+1,n) - Wm[CHAINTASKS[c,i]]
			end;

subto oversampling_delay2:     # Eq.(32)
	forall <c> in S:
		forall <i> in {1 to CHAINLEN[c]-1}:
			if oversampling(c,i,i+1) and harmonic(c,i+1,i) then 
				forall <n> in 
						{0 to ceil(taskperiod(c,i)/taskperiod(c,i+1)) - 1}:
					D[c,i] >= Rp[CHAINTASKS[c,i+1]] + add_period(c,i+1,n) 
															- Wm[CHAINTASKS[c,i]] - add_period(c, i, -1)
															- 2*MASKO[c,i,n]*taskperiod(c,i)
			end;

subto undersampling_decisions: # Eq.(33)
	forall <c> in S:
		forall <i> in {1 to CHAINLEN[c]-1}:
			if not oversampling(c,i,i+1) and harmonic(c,i,i+1) then 
				taskperiod(c,i+1)*(1-MASKU[c,i]) >= 
					Wp[CHAINTASKS[c,i]] - Rm[CHAINTASKS[c,i+1]]
			end;

subto undersampling_delay1:    # Eq.(34)
	forall <c> in S:
		forall <i> in {1 to CHAINLEN[c]-1}:
			if not oversampling(c,i,i+1) and harmonic(c,i,i+1) then 
				forall <n> in 
						{0 to ceil(taskperiod(c,i+1)/taskperiod(c,i)) - 1}:
					D[c,i] >= Rp[CHAINTASKS[c,i+1]] - Wm[CHAINTASKS[c,i]] 
															- add_period(c, i, n)
			end;

subto undersampling_delay2:    # Eq.(35)
	forall <c> in S:
		forall <i> in {1 to CHAINLEN[c]-1}:
			if not oversampling(c,i,i+1) and harmonic(c,i,i+1) then 
				D[c,i] >= Rp[CHAINTASKS[c,i+1]] - Wm[CHAINTASKS[c,i]] 
														- add_period(c, i, -1) 
														- 2*MASKU[c,i]*taskperiod(c,i+1)
			end;

subto nonharmonic_delay:       # Eq.(36)
	forall <c> in S:
		forall <i> in {1 to CHAINLEN[c]-1}:
			if not oversampling(c,i,i+1) and not harmonic(c,i,i+1)
				or oversampling(c,i,i+1) and not harmonic(c,i+1,i) then
				D[c,i] >= period[CHAINTASKS[c,i]] 
														+ RT[CHAINTASKS[c,i]] - bcet[CHAINTASKS[c,i]]
			end;

subto chain_age:               # Eq.(29)
	forall <c> in S:
		AGE[c] == OFF[CHAINTASKS[c,1]] + jitter[CHAINTASKS[c,1]] + sum <i> in {1 to CHAINLEN[c]}: RT[CHAINTASKS[c,i]] + sum <i> in {1 to CHAINLEN[c]}: D[c,i];

minimize age:
	# two-objectives: first data age, second response 
	#                 times (to make the RTA tight)
	sum <t> in T: 
		period[t] * sum <c> in S: AGE[c] + sum <t> in T: RT[t];
