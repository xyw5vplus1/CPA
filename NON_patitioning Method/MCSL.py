from castle.metrics import MetricsDAG
from castle.algorithms import MCSL
import numpy as np
import time
from data import simulate_parameter, simulate_linear_sem_hz

num_iters = 1
tot_metrics = {}
for seed in range(num_iters):
    np.random.seed(seed)
    file = r'alarm.txt'
    with open(file,encoding = 'utf-8') as f:
        B_true = np.loadtxt(f)
    W_true = simulate_parameter(B_true)
    dataset = simulate_linear_sem_hz(B=W_true, n=100, noise_type="uniform")

    st = time.time()
    # structure learning
    alg = MCSL(model_type='nn',
          iter_step=100,
          rho_thresh=1e20,
          init_rho=1e-5,
          rho_multiply=10,
          graph_thresh=0.5,
          l1_graph_penalty=2e-3)
    alg.learn(dataset)

    # calculate accuracy
    met = MetricsDAG(alg.causal_matrix, B_true)
    print(met.metrics)
    metrics = met.metrics.copy()
    ed = time.time()
    metrics['time'] = ed-st
    for key in metrics.keys():
        if key not in tot_metrics.keys():
            tot_metrics[key] = 0
        tot_metrics[key] += metrics[key]

for key in tot_metrics.keys():
    tot_metrics[key] /= num_iters
print(tot_metrics)