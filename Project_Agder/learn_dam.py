from Tsetlin import Tsetlin, Judge
from production import Production
from damnetwork import DamNetwork, Dam
from time import time


def learn_dam(judge, iterations, learning_runs, time_intervals, nr_of_dams, network, prod, states=10, max_profit=0):
    highest_profit = [0.0, []]
    for iteration in range(iterations):
        if (iteration + 1) % 10 == 0:
            print 'Iteration {0}/{1}'.format(iteration + 1, iterations)
        automata_sets = []
        for i in range(nr_of_dams):
            automatas = []
            for automata in range(time_intervals):
                automatas.append(Tsetlin(states))
            automata_sets.append(automatas)

        for j in range(learning_runs):
            income = 0.0

            automatas_decisions = []
            nr_of_decisions = 0
            for automatas in automata_sets:
                automata_decision = []
                for automata in automatas:
                    automata_decision.append(automata.makeDecision())
                    nr_of_decisions += 1
                automatas_decisions.append(automata_decision)

            for dam in network.get_dams():
                dam.reset_water_level()

            for t in range(time_intervals):
                decisions = []
                for automata_decisions in automatas_decisions:
                    decisions.append(automata_decisions[t])

                for i in range(len(decisions)):
                    dam = network.get_dam(i)
                    outflow = dam.get_outflow() * decisions[i]
                    water_level = dam.get_water_level()
                    if outflow > 0 and water_level > 0:
                        capacity = dam.get_max_capacity()
                        p = prod.production(t, water_level, capacity, outflow)
                        income += p
                network.run_network(t, decisions)

            bitflip_income = [0.0] * nr_of_decisions
            for a in range(nr_of_decisions):
                for dam in network.get_dams():
                    dam.reset_water_level()

                for t in range(time_intervals):
                    decisions = []
                    for automata_decisions in automatas_decisions:
                        decisions.append(automata_decisions[t])
                    b = a
                    c = 0
                    while not b < time_intervals:
                        b -= time_intervals
                        c += 1
                    if b == t:
                        decisions[c] = not decisions[c]

                    for i in range(len(decisions)):
                        dam = network.get_dam(i)
                        outflow = dam.get_outflow() * decisions[i]
                        water_level = dam.get_water_level()
                        if outflow > 0 and water_level > 0:
                            capacity = dam.get_max_capacity()
                            p = prod.production(t, water_level, capacity, outflow)
                            bitflip_income[a] += p

                    network.run_network(t, decisions)

            # Calculate individual probability
            # if flip gives highest outcome -> 0.2
            # if flip gives lowest -> 0.8
            maks = max(bitflip_income)
            diff = maks - min(bitflip_income)
            probabilities = []
            for profit in bitflip_income:
                p = maks - profit
                p /= diff
                p *= 0.6
                probabilities.append(0.2+p)

            i = 0
            for automatas in automata_sets:
                for automata in automatas:
                    automata.reward_or_penalty(judge.individual_reward(probabilities[i]))
                    i += 1

            if income > highest_profit[0]:
                highest_profit = [income, automatas_decisions]
                judge.set_max_profit(income)
                if max_profit and round(income, 2) == max_profit:
                    return iteration*learning_runs + j
                # print income
                # for ad in automatas_decisions:
                #     print ad

    print 'Full run'
    return iterations*learning_runs


def learn_dam2(judge, iterations, learning_runs, time_intervals, nr_of_dams, network, prod, states=10, max_profit=0):
    results = [[], []]
    highest_profit = [0.0, 0]
    for iteration in range(iterations):
        # if (iteration + 1) % 10 == 0:
        #     print 'Iteration {0}/{1}'.format(iteration + 1, iterations)
        automata_sets = []
        for i in range(nr_of_dams):
            automatas = []
            for automata in range(time_intervals):
                automatas.append(Tsetlin(states))
            automata_sets.append(automatas)

        for j in range(learning_runs):
            income = 0.0

            automatas_decisions = []
            nr_of_decisions = 0
            for automatas in automata_sets:
                automata_decision = []
                for automata in automatas:
                    automata_decision.append(automata.makeDecision())
                    nr_of_decisions += 1
                automatas_decisions.append(automata_decision)

            for dam in network.get_dams():
                dam.reset_water_level()

            for t in range(time_intervals):
                decisions = []
                for automata_decisions in automatas_decisions:
                    decisions.append(automata_decisions[t])

                for i in range(len(decisions)):
                    dam = network.get_dam(i)
                    outflow = dam.get_outflow() * decisions[i]
                    water_level = dam.get_water_level()
                    if outflow > 0 and water_level > 0:
                        capacity = dam.get_max_capacity()
                        p = prod.production(t, water_level, capacity, outflow)
                        income += p
                network.run_network(t, decisions)

            judge.reward_probability(income)
            for automatas in automata_sets:
                for automata in automatas:
                    automata.reward_or_penalty(judge.reward())

            for automatas in automata_sets:
                for automata in automatas:
                    automata.reward_or_penalty(judge.reward())

            if income > highest_profit[0]:
                highest_profit = [income, iteration*learning_runs+j]
                results[0].append(highest_profit[0])
                results[1].append(highest_profit[1])
                judge.set_max_profit(income)
                if max_profit and round(income, 2) == max_profit:
                    return results
                #print income
                #print iteration*learning_runs+j
    print highest_profit
    return results
