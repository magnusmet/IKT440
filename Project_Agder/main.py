from learn_dam import learn_dam, Judge, DamNetwork, Dam, Production

states = 10
time_intervals = 24
judge = Judge()
price = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
prod = Production(price)
dam = Dam(30.0)
#dam2 = Dam()
dams = [dam]  # , dam2]
#inflow = [2.7, 4.1, 4.4, 4.2, 2.0, 4.8, 1.9, 2.3, 2.2, 4.4, 1.4, 4.1, 1.6, 4.9, 4.3, 1.5, 3.2, 2.9, 2.6, 4.8, 4.9,
#          4.8, 4.0, 1.0]
inflow = [5,6,4,2,1,2,1,0,0,2,0,3,0,0,0,0,0,0,0,0,0,0,0,0]
dam_network = DamNetwork(inflow, dams)

iterations = 1000
learning_runs = 100000

highest_profit = learn_dam(judge, iterations, learning_runs, time_intervals, len(dams), dam_network, prod, states)

print 'highest profit', highest_profit[0]
for ad in highest_profit[1]:
    print ad
