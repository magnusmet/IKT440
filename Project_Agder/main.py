from Tsetlin import Judge, Tsetlin


states = 10

judge = Judge()
voters = []
for voter in range(5):
    voters.append(Tsetlin(states+1))