import sys
from markov import identify_speaker
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)

    # open files & read text
    with open(filenameA, "r") as f1:
        text1 = f1.read()

    with open(filenameB, "r") as f2:
        text2 = f2.read()

    with open(filenameC, "r") as f3:
        text3 = f3.read()

    # run performance tests as outlined in README.md
    record = []
    for k in range(1, max_k + 1):
        for run in range(1, runs + 1):
            # Record hashtable running time for each run.
            start_hash = time.perf_counter()
            result_hash = identify_speaker(text1, text2, text3, k, True)
            elapsed_hash = time.perf_counter() - start_hash
            record.append(("Hashtable", k, run, elapsed_hash))
            # Record dict running time for each run.
            start_dict = time.perf_counter()
            result_dict = identify_speaker(text1, text2, text3, k, False)
            elapsed_dict = time.perf_counter() - start_dict
            record.append(("dict", k, run, elapsed_dict))

    # Store record to a dateframe.
    df = pd.DataFrame(data=record, columns=["Data Structure", "K", "Run",
                                            "Time"])
    # Here I referred to https://stackoverflow.com/questions/31569549/how-to-groupby-a-dataframe-in-pandas-and-keep-columns
    # for the use of as_index=False parameter to maintain df structure
    # Group by Implementation then K and get average time.
    df = df.groupby(["Data Structure", "K"], as_index=False)["Time"].mean()

    print(df)

    # Create pointplot graph.
    sns.set_theme()
    graph = sns.pointplot(data=df, x="K", y="Time",
                          hue="Data Structure", linestyles='-', markers='o')
    # Modify graph lable, title and legent title.
    plt.xlabel("K")
    plt.ylabel(f"Average Time (Runs = {runs})")
    plt.title("Hashtable vs Python dict")
    plt.legend(title="Lines")
    # Write execution_graph.png
    plt.savefig("execution_graph.png")
