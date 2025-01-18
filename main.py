import os
import sys
from benchmark import run_full_benchmark
from visualize import main as run_visualizations

# Directory setup
DATASET_DIR = "./dataset/"
PLOTS_DIR = "./plots/"
GIFS_DIR = "./gifs/"


def setup_environment():
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
        print(f"Created dataset directory: {DATASET_DIR}")

    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)
        print(f"Created plots directory: {PLOTS_DIR}")

    if not os.path.exists(GIFS_DIR):
        os.makedirs(GIFS_DIR)
        print(f"Created GIFs directory: {GIFS_DIR}")


def main():
    print("\n========== B-Tree and AVL Tree Benchmark and Visualization ==========")

    setup_environment()

    sys.setrecursionlimit(2_000_000)

    print("\nRunning benchmarks...")
    run_full_benchmark()

    print("\nGenerating GIF visualizations...")
    run_visualizations()

    print("\nAll tasks complete!")
    print(f"Results have been saved to 'benchmark_results.md'.")
    print(f"Plots have been saved to the '{PLOTS_DIR}' directory.")
    print(f"GIFs have been saved to the '{GIFS_DIR}' directory.")


if __name__ == "__main__":
    main()