from Tsetlin import Production, Tsetlin, Judge, WaterLevel
from time import time







states = 10
judge = Judge()
prod = Production()
wl = WaterLevel()

# automatas = []
# for automata in range(24):
#     automatas.append(Tsetlin(states))

iterations = 1000
learning_runs = 100000

totalIncome = 0.0
income = 0.0
avg_profit = 0.0
highest_profit = [0.0, 0, 0]
t0 = time()
for iteration in range(iterations):
    first_automatas = []
    second_automatas = []
    for automata in range(24):
        first_automatas.append(Tsetlin(states))
        second_automatas.append(Tsetlin(states))
    finished = False
    k = 0
    while not finished:
        first_decisions = []
        second_decisions = []
        income = 0.0

        wl.set_waterlevel()

        for automata in first_automatas:
            first_decisions.append(automata.makeDecision())
        for automata in second_automatas:
            second_decisions.append(automata.makeDecision())

        for t in range(len(first_decisions)):
            if first_decisions[t] == 1:
                income += prod.production(t, wl.get_waterlevel()[0])
                if second_decisions[t] == 1:
                    income += prod.production(t, wl.get_waterlevel()[1])
                    wl.open_or_close(t, True, True)
                else:
                    wl.open_or_close(t, True, False)
            elif second_decisions[t] == 1:
                income += prod.production(t, wl.get_waterlevel()[1])
                wl.open_or_close(t, False, True)
            else:
                wl.open_or_close(t, False, False)

        judge.reward_probability(income)
        for automata in first_automatas:
            automata.reward_or_penalty(judge.reward())
        for automata in second_automatas:
            automata.reward_or_penalty(judge.reward())

        totalIncome += income
        if income > highest_profit[0]:
            highest_profit = [income, k, 1]
            judge.set_max_profit(income)
            print income
            print first_decisions
            print second_decisions
        elif income == highest_profit[0]: highest_profit[2] += 1
        if judge.unchanged_iteration()-1 == learning_runs:
            #print 'break, no progress, {0}/{1}'.format(iteration+1, iterations)
            finished = True
            judge.reset_unchanged_iteration()
        elif k > learning_runs*10:
            print 'max learning runs reached'
            finished = True

        k += 1
    if iteration>0 and iteration % 100 == 0:
        print 'Iteration {0}/{1}'.format(iteration+1, iterations)
    avg_profit += income

t1 = time()

print 'max profit : 150'
print 'profit:', income
print 'avg income', totalIncome/(iterations*learning_runs)
print 'avg final profit', avg_profit/iterations
print 'highest profit', highest_profit
print 'time', t1-t0
#judge = Judge()
#voters = []
#for voter in range(5):
    #voters.append(Tsetlin(states+1))