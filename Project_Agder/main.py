from learn_dam import learn_dam, learn_dam2, Judge, DamNetwork, Dam, Production
from time import time
import plotly
import plotly.graph_objs as go


states = 10
time_intervals = 24
judge = Judge()
price = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
#price = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
#price = [3, 6, 9, 12, 15, 18, 21, 24]
prod = Production(price)
dam = Dam(30.0, 50.0, 4.0)
#dam2 = Dam(0.0, 25.0, 4.0)
# dam3 = Dam(0.0, 25.0, 6.0)
dams = [dam]  # , dam2]  # , dam3]
#inflow = [2.7, 4.1, 4.4, 4.2, 2.0, 4.8, 1.9, 2.3, 2.2, 4.4, 1.4, 4.1, 1.6, 4.9, 4.3, 1.5, 3.2, 2.9, 2.6, 4.8, 4.9,
#          4.8, 4.0, 1.0]
inflow = [5,6,4,2,1,2,1,0,0,2,0,3,0,0,0,0,0,0,0,0,0,0,0,0]
#inflow = [11, 6, 3, 1, 2, 3, 0, 0, 0, 0, 0, 0]
#inflow = [15, 5, 1, 5, 0, 0, 0, 0]

dam_network = DamNetwork(inflow, dams)

iterations = 10
learning_runs = 10000
max_profit = 516.64  # 516.64  # 896.16  # 1196.64

t0 = time()
avg_its = 0
for i in range(100):
    avg_its += learn_dam(judge, iterations, learning_runs, time_intervals, len(dams), dam_network, prod, states, max_profit)

#r = learn_dam2(judge, iterations, learning_runs, time_intervals, len(dams), dam_network, prod, states, max_profit)


print 'avg time:', (time() - t0) / 100.0
print 'avg its:', avg_its / 100.0

# trace0 = go.Scatter(
#     x=results[1],
#     y=results[0],
#     mode='markers',
#     name='Profit'
# )
# trace1 = go.Scatter(
#     x=results[1],
#     y=[max_profit]*len(results[1]),
#     mode='lines',
#     name='Max profit'
# )
# data = [trace0, trace1]
# plotly.offline.plot(data, filename='results.html')

# print 'highest profit', highest_profit[0]
# for ad in highest_profit[1]:
#     print ad
