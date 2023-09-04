var D[<c,i> in CHAINID] integer >= 0;   # d^+_{i,i+1}
var AGE[S]              integer >= 0;   # DA


subto nonharmonic_delay:       # Eq.(36)
	forall <c> in S:
		forall <i> in {1 to CHAINLEN[c]}:
				D[c,i] == period[CHAINTASKS[c,i]] + RT[CHAINTASKS[c,i]];

subto chain_age:               # Eq.(29)
	forall <c> in S:
		AGE[c] == sum <i> in {1 to CHAINLEN[c]}: RT[CHAINTASKS[c,i]] + sum <i> in {1 to CHAINLEN[c]}: D[c,i];

minimize age:
	# two-objectives: first data age, second response 
	#                 times (to make the RTA tight)
	sum <t> in T: 
		period[t] * sum <c> in S: AGE[c] + sum <t> in T: RT[t];
