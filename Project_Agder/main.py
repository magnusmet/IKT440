from Tsetlin import Production, Tsetlin, Judge, WaterLevel







states = 10
judge = Judge()
prod = Production()
automatas = []
wl = WaterLevel()

for automata in range(24):
    automatas.append(Tsetlin(states))

totalIncome = 0.0

for k in range(100000):
    decisions = []
    income = 0.0

    wl.setWaterlevel()

    for automata in automatas:
        decisions.append(automata.makeDecision())

    for t in range(len(decisions)):
        if decisions[t] == 1:
            income += prod.production(t,wl.getWaterlevel())
            wl.openOrClose(t,True)

        else:
            wl.openOrClose(t,False)

    judge.reward_probability(income)
    for i in automatas:
        i.reward_or_penalty(judge.reward())



    totalIncome+=income
print 'max profit : 150'
print 'profit:', income
print 'avg income', totalIncome/100000
#judge = Judge()
#voters = []
#for voter in range(5):
    #voters.append(Tsetlin(states+1))