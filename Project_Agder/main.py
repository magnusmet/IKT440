from learn_dam import learn_dam, Judge, DamNetwork, Dam, Production

states = 10
time_intervals = 24
judge = Judge()
prod = Production()
dam = Dam(40.0)
dam2 = Dam()
dams = [dam]  # , dam2]
inflow = [2.7, 4.1, 4.4, 4.2, 2.0, 4.8, 1.9, 2.3, 2.2, 4.4, 1.4, 4.1, 1.6, 4.9, 4.3, 1.5, 3.2, 2.9, 2.6, 4.8, 4.9,
          4.8, 4.0, 1.0]
dam_network = DamNetwork(inflow, dams)

iterations = 1000
learning_runs = 100000

highest_profit = learn_dam(judge, iterations, learning_runs, time_intervals, len(dams), dam_network, prod, states)

print 'highest profit', highest_profit[0]
for ad in highest_profit[1]:
    print ad
