# un job è associato ad un utente (user) ed ha una certa durata (length)
class Job:
    def __init__(self, user, length, id):
        self.user = user
        self.length = length
        self.id = id

    def get_user(self):
        return self.user

    def get_length(self):
        return self.length

    def get_id(self):
        return self.id

    def __str__(self):
        return "(" + self.user + "-" + str(self.length) + ")"
