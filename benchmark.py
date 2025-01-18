import os
import random
import time
import memory_profiler
import matplotlib.pyplot as plt
from avl_tree import AVLTree
from b_tree import BTree
import sys
import json

DATASET_DIR = "./dataset/"
PLOTS_DIR = "./plots/"
RESULTS_FILE = "benchmark_results.md"


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def generate_or_load_dataset(size):
    """
    Generate a random dataset of the given size or load it if already saved.
    """
    ensure_directory_exists(DATASET_DIR)
    dataset_path = os.path.join(DATASET_DIR, f"dataset_{size}.txt")

    if os.path.exists(dataset_path):
        with open(dataset_path, "r") as f:
            data = list(map(int, f.read().strip().split()))
        print(f"Loaded dataset of size {size} from {dataset_path}")
    else:
        data = [random.randint(0, 10_000_000) for _ in range(size)]
        with open(dataset_path, "w") as f:
            f.write(" ".join(map(str, data)))
        print(f"Generated new dataset of size {size} and saved to {dataset_path}")
    return data


def measure_time_and_memory(func, *args, **kwargs):
    """
    Measure the execution time and memory usage of a function call.
    Returns:
      - time_elapsed: float (in seconds)
      - mem_diff: float (in MB)
    """
    mem_before = memory_profiler.memory_usage()[0]
    start_time = time.perf_counter()

    result = func(*args, **kwargs)

    end_time = time.perf_counter()
    mem_after = memory_profiler.memory_usage()[0]

    time_elapsed = end_time - start_time
    mem_diff = mem_after - mem_before

    return time_elapsed, mem_diff, result


def run_benchmark_for_size(n):
    """
    Run insert, search, and delete for both AVL and B-Tree for dataset of size n.
    Returns a dictionary with timing and memory usage metrics.
    """
    data = generate_or_load_dataset(n)

    avl = AVLTree()
    btree = BTree(t=3)

    def avl_insert_all():
        for value in data:
            avl.insert_key(value)

    avl_insert_time, avl_insert_mem, _ = measure_time_and_memory(avl_insert_all)

    def btree_insert_all():
        for value in data:
            btree.insert_key(value)

    btree_insert_time, btree_insert_mem, _ = measure_time_and_memory(btree_insert_all)

    search_samples = random.sample(data, min(n, 100))

    def avl_search_all():
        for val in search_samples:
            avl.search_key(val)

    avl_search_time, avl_search_mem, _ = measure_time_and_memory(avl_search_all)

    def btree_search_all():
        for val in search_samples:
            btree.search_key(val)

    btree_search_time, btree_search_mem, _ = measure_time_and_memory(btree_search_all)

    delete_samples = random.sample(data, min(n, 100))

    def avl_delete_all():
        for val in delete_samples:
            avl.delete_key(val)

    avl_delete_time, avl_delete_mem, _ = measure_time_and_memory(avl_delete_all)

    def btree_delete_all():
        for val in delete_samples:
            btree.delete_key(val)

    btree_delete_time, btree_delete_mem, _ = measure_time_and_memory(btree_delete_all)

    return {
        "size": n,
        "avl_insert_time": avl_insert_time,
        "avl_insert_mem": avl_insert_mem,
        "avl_search_time": avl_search_time,
        "avl_search_mem": avl_search_mem,
        "avl_delete_time": avl_delete_time,
        "avl_delete_mem": avl_delete_mem,

        "btree_insert_time": btree_insert_time,
        "btree_insert_mem": btree_insert_mem,
        "btree_search_time": btree_search_time,
        "btree_search_mem": btree_search_mem,
        "btree_delete_time": btree_delete_time,
        "btree_delete_mem": btree_delete_mem,
    }


def generate_plots(results):
    """
    Generate plots for time and memory complexity.
    """
    ensure_directory_exists(PLOTS_DIR)

    sizes = [res["size"] for res in results]

    # Time plots
    plt.figure()
    plt.plot(sizes, [res["avl_insert_time"] for res in results], label="AVL Insert")
    plt.plot(sizes, [res["btree_insert_time"] for res in results], label="B-Tree Insert")
    plt.plot(sizes, [res["avl_search_time"] for res in results], label="AVL Search")
    plt.plot(sizes, [res["btree_search_time"] for res in results], label="B-Tree Search")
    plt.plot(sizes, [res["avl_delete_time"] for res in results], label="AVL Delete")
    plt.plot(sizes, [res["btree_delete_time"] for res in results], label="B-Tree Delete")
    plt.xlabel("Dataset Size")
    plt.ylabel("Time (seconds)")
    plt.title("Time Complexity")
    plt.legend()
    plt.savefig(os.path.join(PLOTS_DIR, "time_complexity.png"))

    # Memory plots
    plt.figure()
    plt.plot(sizes, [res["avl_insert_mem"] for res in results], label="AVL Insert")
    plt.plot(sizes, [res["btree_insert_mem"] for res in results], label="B-Tree Insert")
    plt.plot(sizes, [res["avl_search_mem"] for res in results], label="AVL Search")
    plt.plot(sizes, [res["btree_search_mem"] for res in results], label="B-Tree Search")
    plt.plot(sizes, [res["avl_delete_mem"] for res in results], label="AVL Delete")
    plt.plot(sizes, [res["btree_delete_mem"] for res in results], label="B-Tree Delete")
    plt.xlabel("Dataset Size")
    plt.ylabel("Memory (MB)")
    plt.title("Memory Complexity")
    plt.legend()
    plt.savefig(os.path.join(PLOTS_DIR, "memory_complexity.png"))


def save_results_to_markdown(results):
    """
    Save benchmark results to a markdown file, including memory usage data.
    """
    with open(RESULTS_FILE, "w") as f:
        f.write("# Benchmark Results\n\n")
        f.write(
            "This document contains the results of benchmarking AVL and B-Tree operations, including time and memory usage.\n\n")

        f.write("## Summary Table\n")
        f.write(
            "| Size | AVL Insert (s) | AVL Insert (MB) | AVL Search (s) | AVL Search (MB) | AVL Delete (s) | AVL Delete (MB) | ")
        f.write(
            "B-Tree Insert (s) | B-Tree Insert (MB) | B-Tree Search (s) | B-Tree Search (MB) | B-Tree Delete (s) | B-Tree Delete (MB) |\n")
        f.write(
            "|------|----------------|-----------------|----------------|-----------------|----------------|-----------------|")
        f.write(
            "------------------|------------------|------------------|------------------|------------------|------------------|\n")

        for res in results:
            f.write(
                f"| {res['size']} | "
                f"{res['avl_insert_time']:.4f} | {res['avl_insert_mem']:.4f} | "
                f"{res['avl_search_time']:.4f} | {res['avl_search_mem']:.4f} | "
                f"{res['avl_delete_time']:.4f} | {res['avl_delete_mem']:.4f} | "
                f"{res['btree_insert_time']:.4f} | {res['btree_insert_mem']:.4f} | "
                f"{res['btree_search_time']:.4f} | {res['btree_search_mem']:.4f} | "
                f"{res['btree_delete_time']:.4f} | {res['btree_delete_mem']:.4f} |\n"
            )

        f.write("\n")
        f.write("## Key Metrics\n")
        f.write("- **Time** is measured in seconds.\n")
        f.write("- **Memory** is measured in megabytes (MB).\n")
        f.write("\n")
        f.write("## Visualization\n")
        f.write("Refer to the generated plots in the `/plots` folder for a visual comparison of the results.\n")


def run_full_benchmark():
    """
    Run benchmarks for multiple dataset sizes, save results, and generate plots.
    """
    dataset_sizes = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000]

    results = []
    for size in dataset_sizes:
        stats = run_benchmark_for_size(size)
        results.append(stats)

    save_results_to_markdown(results)
    generate_plots(results)


if __name__ == "__main__":
    sys.setrecursionlimit(2_000_000)
    run_full_benchmark()