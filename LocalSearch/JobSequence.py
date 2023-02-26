import random
import copy
from Job import Job


class JobSequence:

    # una sequenza di job (JobSequence) viene inizializzata in modo casuale a partire da un dizionario
    # user_n_jobs={"utente1": numero_job_utente1, "utente2": numero_job_utente2, ...}
    # ogni job della sequenza avrà una durata compresa tra min_length_job e max_length_job
    # self.jobs è una lista di oggetti Job
    def __init__(self, user_n_jobs, min_length_job, max_length_job, seed):

        if seed is not None:
            random.seed(seed)

        self.users = list(user_n_jobs.keys())

        sequence_length = sum(user_n_jobs.values())
        self.jobs = [None] * sequence_length
        job_positions_list = random.sample(range(0, sequence_length), sequence_length)
        for user, n_jobs in user_n_jobs.items():
            for i in range(0, n_jobs):
                job_position = job_positions_list.pop(0)
                job_length = random.randint(min_length_job, max_length_job)
                self.jobs[job_position] = Job(user, job_length, str(user)+str(i))

    def set_job_sequence(self, jobs):
        self.jobs = jobs

    def get_job_sequence(self):
        return self.jobs

    def is_sorted(self, lst):
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                return False
        return True

    def get_list_len_job_user(self, user):
        return [job.get_length() for job in self.jobs if job.get_user() == user]

    def check_sequence(self):
        for user in self.users:
            if not self.is_sorted(self.get_list_len_job_user(user)):
                return False
        return True


    # ordina self.jobs in base alla durata dei job, con reverse=False in ordine crescente di durata
    # mentre con reverse=True in ordine decrescente di durata
    def order_jobs_sequence(self, reverse=False):
        self.jobs.sort(key=lambda x: x.get_length(), reverse=reverse)

    def switch_two_jobs(self, pos1, pos2):
        self.jobs[pos1], self.jobs[pos2] = self.jobs[pos2], self.jobs[pos1]

    # permette di ordinare i job in maniera tale da ottenere la peggior sequenza per l'utente specificato (user)
    # la sequenza peggiore è quella per cui tutti i job di user sono messi alla fine, inoltre,
    # i job sono in ordine descrescente di durata
    def make_worst(self, user):
        self.order_jobs_sequence(reverse=True)
        jobs_of_user = list(filter(lambda x: x.get_user() == user, self.jobs))
        jobs_of_other_user = list(filter(lambda x: x.get_user() != user, self.jobs))
        self.jobs = jobs_of_other_user + jobs_of_user

    # permette di ordinare i job in maniera tale da ottenere la miglior sequenza per l'utente specificato (user)
    # la sequenza migliore è quella per cui tutti i job di user sono messi all'inizio, inoltre,
    # i job sono in ordine crescente di durata
    def make_best(self, user):
        self.order_jobs_sequence()
        jobs_of_user = list(filter(lambda x: x.get_user() == user, self.jobs))
        jobs_of_other_user = list(filter(lambda x: x.get_user() != user, self.jobs))
        self.jobs = jobs_of_user + jobs_of_other_user

    # restituisce il tempo di completamento per un job all'inteno della sequenza (job in posizione pos_job)
    def get_waiting_time(self, pos_job):
        return sum([x.get_length() for x in self.jobs][:pos_job + 1])

    # calcola la funzione obiettivo per un utente
    def fo(self, user):
        return sum([self.get_waiting_time(self.jobs.index(x)) for x in self.jobs if x.get_user() == user])

    # calcola la funzione obiettivo normalizzata per un utente
    def fo_norm(self, user):
        best_sequence = copy.deepcopy(self)
        best_sequence.make_best(user)
        worst_sequence = copy.deepcopy(self)
        worst_sequence.make_worst(user)

        bs = best_sequence.fo(user)
        ws = worst_sequence.fo(user)

        return (self.fo(user) - bs) / (ws - bs)

    def __str__(self):
        return ','.join(map(str, self.jobs))