import copy
from JobSequence import JobSequence


class Machine:

    def __init__(self, user_n_jobs, min_length_job, max_length_job, seed):
        self.x = JobSequence(user_n_jobs, min_length_job, max_length_job, seed)
        self.x.order_jobs_sequence()
        self.users = list(user_n_jobs.keys())

    def get_sequence(self):
        return self.x

    def set_sequence(self, x):
        self.x = x

    # restituisce la lista delle posizioni dei job di un determinato utente (user)
    def get_position_of_jobs_user(self, user):
        return [self.x.get_job_sequence().index(job) for job in self.x.get_job_sequence() if job.get_user() == user]

    def find_previous_number_in_list(self, numbers, n):
        try:
            index = numbers.index(n)
            return numbers[index - 1] if index > 0 else None
        except ValueError:
            return None

    # restituisce le posizioni dei job che permettono di decrementare la fo_normalizzata facendo lo switch
    # con un dato job (position) all'interno della sequenza
    def index_of_jobs_to_decrease_fo(self, position, user):
        position_of_jobs_user = self.get_position_of_jobs_user(user)
        prev = self.find_previous_number_in_list(position_of_jobs_user, position)
        if prev:
            return list(range(prev+1, position))
        else:
            return list(range(0, position))

    # restituisce le posizioni dei job che permettono di incrementare la fo_normalizzata facendo lo switch
    # con un dato job (position) all'interno della sequenza
    def index_of_jobs_to_increase_fo(self, position, user):
        position_of_jobs_user = self.get_position_of_jobs_user(user)
        if position == position_of_jobs_user[-1]:
            return list(range(position + 1, len(self.x.get_job_sequence())))
        else:
            tmp = [pos for pos in position_of_jobs_user if pos > position]
            return list(range(position + 1, tmp[0]))

    # restituisce il vicinato ottenuto scambiando il job in position con i job presenti in index_of_jobs
    def make_neighborhood(self, position, index_of_jobs):
        neighbors = []
        for i in index_of_jobs:
            y = copy.deepcopy(self.x)
            y.switch_two_jobs(position, i)
            if y.check_sequence():
                neighbors.append(y)
        return neighbors

    # restituisce il vicinato della soluzione attuale self.x, tenendo conto dell'utente (user) che ha
    # fo_normalizzata più alta
    def neighborhood(self, user, increase=False):
        list_of_neighbors = []
        for position in self.get_position_of_jobs_user(user):
            if increase:
                index_of_jobs = self.index_of_jobs_to_increase_fo(position,
                                                                  self.x.get_job_sequence()[position].get_user())
            else:
                index_of_jobs = self.index_of_jobs_to_decrease_fo(position,
                                                                  self.x.get_job_sequence()[position].get_user())
            list_of_neighbors.extend(self.make_neighborhood(position, index_of_jobs))
        return list_of_neighbors

    def get_info_sequence(self):
        x = copy.deepcopy(self.x)
        x_fo = {}
        x_fo_norm = {}
        for user in self.users:
            x_fo_norm[user] = self.x.fo_norm(user)
            x_fo[user] = self.x.fo(user)
        return x, x_fo, x_fo_norm

    def local_search_steepest_descent(self):

        steps = 0
        steps_sequence = []
        x, x_fo, x_fo_norm = self.get_info_sequence()
        steps_sequence.append((x, x_fo, x_fo_norm))
        print(f"Step: {steps}\nFunzione obiettivo: {x_fo}={sum(x_fo.values())}\n"
              f"Funzione obiettivo normalizzata{x_fo_norm}={max(x_fo_norm.values()) - min(x_fo_norm.values()):.8f}\n")
        stop = False

        while not stop:

            x, x_fo, x_fo_norm = self.get_info_sequence()
            user_with_max_fo_norm = max(x_fo_norm, key=x_fo_norm.get)

            neighborhood = self.neighborhood(user_with_max_fo_norm)
            neighbors = {}
            for y in neighborhood:
                neighbors[y] = {}
                for user in self.users:
                    neighbors[y][user] = y.fo_norm(user)

            tmp = {k: max(v.values()) for k, v in neighbors.items()}
            y = min(tmp, key=tmp.get)

            stop = True
            if max(neighbors[y].values()) < max(x_fo_norm.values()):
                self.x = y
                steps += 1
                x, x_fo, x_fo_norm = self.get_info_sequence()
                steps_sequence.append((x, x_fo, x_fo_norm))

                print(f"Grandezza vicinato: {len(neighborhood)}\n\n")
                print(f"Step: {steps}\nFunzione obiettivo: {x_fo}={sum(x_fo.values())}\n"
                      f"Funzione obiettivo normalizzata{x_fo_norm}={max(x_fo_norm.values())-min(x_fo_norm.values()):.8f}\n")
                stop = False

        return steps_sequence

    def local_search_first_improvement(self):

        steps = 0
        steps_sequence = []
        x, x_fo, x_fo_norm = self.get_info_sequence()
        steps_sequence.append((x, x_fo, x_fo_norm))
        print(f"Step: {steps}\nFunzione obiettivo: {x_fo}={sum(x_fo.values())}\n"
              f"Funzione obiettivo normalizzata{x_fo_norm}={max(x_fo_norm.values()) - min(x_fo_norm.values()):.8f}\n")
        stop = False

        while not stop:

            x, x_fo, x_fo_norm = self.get_info_sequence()
            user_with_max_fo_norm = max(x_fo_norm, key=x_fo_norm.get)

            stop = True
            index = 0
            neighborhood = self.neighborhood(user_with_max_fo_norm)
            for y in neighborhood:
                index += 1
                y_fo_norm = {}
                for user in self.users:
                    y_fo_norm[user] = y.fo_norm(user)
                if max(y_fo_norm.values()) < max(x_fo_norm.values()):
                    self.x = y
                    steps += 1
                    x, x_fo, x_fo_norm = self.get_info_sequence()
                    steps_sequence.append((x, x_fo, x_fo_norm))

                    print(f"Grandezza vicinato: {len(neighborhood)}\nNumero vicini considerati: {index}\n\n")
                    print(f"Step: {steps}\nFunzione obiettivo: {x_fo}={sum(x_fo.values())}\n"
                          f"Funzione obiettivo normalizzata{x_fo_norm}={max(x_fo_norm.values()) - min(x_fo_norm.values()):.8f}\n")
                    stop = False
                    break

        return steps_sequence

    def __str__(self):
        return str(self.x)
