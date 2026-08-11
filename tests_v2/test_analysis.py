from safeguardshift.analysis import wilson,bootstrap_mean
def test_wilson(): lo,hi=wilson(1,156); assert 0<=lo<hi<=1
def test_bootstrap_deterministic(): assert bootstrap_mean([0,1,1],reps=100)==bootstrap_mean([0,1,1],reps=100)
