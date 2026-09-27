# benchmark.py
# Empirically measures the execution time of the migration algorithms.

from importlib.resources import files
from time import perf_counter
import random
import pandas as pd
from methods import migrateServersBaseline, migrateServersProposed

def generate_test_data(size, max_L):
    """Generates an array of random file sizes."""
    return [random.randint(1, max_L) for _ in range(size)]

def benchmark_algo_multi(algo, test_cases, repeat=1):
    times = []
    for i in test_cases:
        for _ in range(repeat):
            start = perf_counter()
            algo(i)
            end = perf_counter()
            times.append((len(i), end - start))
    return times

def run_benchmarks():
    input_sizes = [10, 50, 100, 500, 1000, 5000, 10000, 20000, 30000, 40000, 50000]
    L = 100
    test_cases = [generate_test_data(size, L) for size in input_sizes]

    baseline_times = benchmark_algo_multi(lambda files: migrateServersBaseline(files, L), test_cases, repeat=5)
    proposed_times = benchmark_algo_multi(lambda files: migrateServersProposed(files, L), test_cases, repeat=5)
    
    df_baseline = pd.DataFrame(baseline_times, columns=['Files', 'Time'])
    df_baseline['Algorithm'] = 'Baseline'
    df_proposed = pd.DataFrame(proposed_times, columns=['Files', 'Time'])
    df_proposed['Algorithm'] = 'Proposed'

    df_all = pd.concat([df_baseline, df_proposed], ignore_index=True)
    df_all.to_csv("empirical_results.csv", index=False)
    print("All Times:")
    print(df_all)

if __name__ == '__main__':
    run_benchmarks()