import copy
import pandas as pd
import time

from Machine import Machine


def extract_info(steps, start, end, user_n_jobs, length):
    fo_start = steps[0][1]
    fo_end = steps[-1][1]
    fo_norm_start = steps[0][2]
    fo_norm_end = steps[-1][2]

    user_n_jobs = {"#j-" + k: v for k, v in user_n_jobs.items()}
    fo_start = {"fo-S-" + k: v for k, v in fo_start.items()}
    fo_end = {"fo-E-" + k: v for k, v in fo_end.items()}
    fo_norm_start = {"foN-S-" + k: v for k, v in fo_norm_start.items()}
    fo_norm_end = {"foN-E-" + k: v for k, v in fo_norm_end.items()}

    user_n_jobs.update({"len": length, "#steps": len(steps), "t(ms)": round((end - start) / 1000000)})
    user_n_jobs.update(fo_start)
    user_n_jobs.update(fo_end)
    sum_start = sum(fo_start.values())
    sum_end = sum(fo_end.values())
    user_n_jobs.update({"sum-S": sum_start, "sum-E": sum_end, "diff_fo": sum_end - sum_start})
    user_n_jobs.update(fo_norm_start)
    user_n_jobs.update(fo_norm_end)
    start_max_fo_norm = max(fo_norm_start.values())
    start_min_fo_norm = min(fo_norm_start.values())
    end_max_fo_norm = max(fo_norm_end.values())
    end_min_fo_norm = min(fo_norm_end.values())
    diff_S = start_max_fo_norm - start_min_fo_norm
    diff_E = end_max_fo_norm - end_min_fo_norm
    user_n_jobs.update({"max-diff-S": diff_S, "max-diff-E": diff_E, "diff_fo_norm": diff_S - diff_E})

    return user_n_jobs


class TestMachine:

    def __init__(self, users, n_jobs, lengths):
        self.users = users
        self.n_jobs = n_jobs
        self.lengths = lengths

    def run_test(self):

        data1 = []
        data2 = []
        for length in self.lengths:
            # for list_n_jobs in list(combinations_with_replacement(self.n_jobs, len(self.users))):
            #    user_n_jobs = {self.users[i]: list_n_jobs[i] for i in range(len(list_n_jobs))}
            for n in self.n_jobs:
                user_n_jobs = {self.users[i]: n for i in range(len(self.users))}

                print(f"Durata ({length}) - User-nJobs({user_n_jobs})\n")

                m = Machine(user_n_jobs, 1, length, None)

                x = m.get_sequence()

                print("local_search_first_improvement")
                start = time.time_ns()
                steps = m.local_search_first_improvement()
                end = time.time_ns()
                tmp_dict = copy.deepcopy(user_n_jobs)
                data1.append(extract_info(steps, start, end, tmp_dict, length))

                m.set_sequence(x)

                print("local_search_steepest_descent")
                start = time.time_ns()
                steps = m.local_search_steepest_descent()
                end = time.time_ns()
                tmp_dict = copy.deepcopy(user_n_jobs)
                data2.append(extract_info(steps, start, end, tmp_dict, length))

        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        return df1, df2
