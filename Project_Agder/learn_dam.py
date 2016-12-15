from Tsetlin import Tsetlin, Judge
from production import Production
from damnetwork import DamNetwork, Dam


def learn_dam(judge, iterations, learning_runs, time_intervals, nr_of_dams, network, prod, states=10):
    highest_profit = [0.0, []]
    for iteration in range(iterations):
        if iteration % 10 == 0:
            print 'Iteration {0}/{1}'.format(iteration + 1, iterations)
        automata_sets = []
        for i in range(nr_of_dams):
            automatas = []
            for automata in range(time_intervals):
                automatas.append(Tsetlin(states))
            automata_sets.append(automatas)

        for j in range(learning_runs):
            income = 0.0

            for dam in network.get_dams():
                dam.set_water_level()

            automatas_decisions = []
            for automatas in automata_sets:
                automata_decision = []
                for automata in automatas:
                    automata_decision.append(automata.makeDecision())
                automatas_decisions.append(automata_decision)

            for t in range(time_intervals):
                decisions = []
                for automata_decisions in automatas_decisions:
                    decisions.append(automata_decisions[t])
                for i in range(len(decisions)):
                    outflow = network.get_dam(i).get_outflow() * decisions[i]
                    water_level = network.get_dam(i).get_water_level()
                    if outflow>0:
                        income += prod.production(t, water_level, outflow)
                network.run_network(t, decisions)

            judge.reward_probability(income)
            for automatas in automata_sets:
                for automata in automatas:
                    automata.reward_or_penalty(judge.reward())

            if income > highest_profit[0]:
                highest_profit = [income, automatas_decisions]
                judge.set_max_profit(income)
                print income
                for ad in automatas_decisions:
                    print ad
        print 'Finished learning iteration'

    return highest_profit
