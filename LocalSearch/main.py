import os

import matplotlib.pyplot as plt
import pandas as pd
import time
from Machine import Machine
from TestMachine import TestMachine


def manual_test(user_n_jobs, min_job_length, max_job_length, first, seed=None):

    m = Machine(user_n_jobs, min_job_length, max_job_length, seed)

    start = time.time()
    if first:
        steps = m.local_search_first_improvement()
    else:
        steps = m.local_search_steepest_descent()
    end = time.time()

    print((end - start), "(s)")


def run_benchmark_test():
    users = ["A", "B"]
    n_jobs = [10, 30, 50, 70, 90]
    lengths = [100]
    for i in range(0, 5):
        t = TestMachine(users, n_jobs, lengths)
        result = t.run_test()
        result[0].to_csv(".\\tests\\fi\\"+str(i)+"-local_search_first_improvement.csv", index=False)
        result[1].to_csv(".\\tests\\sd\\"+str(i)+"-local_search_steepest_descent.csv", index=False)


def plot(column_x, column_y1, column_y2, l1, l2, title):
    lilla = "#c8a2c8"
    blu = "#6495ED"
    nero = "#000000"

    plt.figure(figsize=(8, 5))
    plt.grid(color=nero, linestyle='-', linewidth=0.5, axis="y")

    plt.title(title)
    file_name = "".join(title.lower()).replace(" ", "_")

    plt.xlabel(column_x.name)
    plt.ylabel(column_y1.name)

    plt.xticks(column_x)

    plt.plot(column_x, column_y1, color=lilla, linestyle='-', marker='o', label=l1)
    plt.plot(column_x, column_y2, color=blu, linestyle='-', marker='o', label=l2)

    plt.legend(loc="upper left")
    plt.savefig(".\\plot\\" + file_name, bbox_inches='tight', transparent=True)
    plt.show()


def plot_all():

    directory = ".\\tests\\fi\\"
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        tmp = pd.read_csv(f)
        df = pd.concat([df, tmp])
    df_grouped = df.groupby(["#j-A", "#j-B"]).mean()
    df_grouped.to_csv(".\\plot\\local_search_first_improvement.csv")

    directory = ".\\tests\\sd\\"
    df = pd.DataFrame()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        tmp = pd.read_csv(f)
        df = pd.concat([df, tmp])
    df_grouped = df.groupby(["#j-A", "#j-B"]).mean()
    df_grouped.to_csv(".\\plot\\local_search_steepest_descent.csv")

    df1 = pd.read_csv(".\\plot\\local_search_first_improvement.csv")
    df2 = pd.read_csv(".\\plot\\local_search_steepest_descent.csv")
    plot(df1["#j-A"], df1["#steps"], df2["#steps"], "FI", "SD", "Numero di step al variare del numero di job")
    plot(df1["#j-A"], df1["t(ms)"], df2["t(ms)"], "FI", "SD", "Tempo di esecuzione al variare del numero di job")
    plot(df1["#j-A"], df1["diff_fo"], df2["diff_fo"], "FI", "SD", "Differenza FO finale al variare del numero di job")
    plot(df1["#j-A"], df1["max-diff-E"], df2["max-diff-E"], "FI", "SD", "Differenza FO_NORM al variare del numero di job")




if __name__ == '__main__':

    manual_test({"A": 10, "B": 10}, 5, 20, False, 2)

    #run_benchmark_test()

    #plot_all()

