
class Profile:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.watchlists = []

    def add_watchlist(self, watchlist):
        self.watchlists.append(watchlist)

    def get_watchlists(self):
        return self.watchlists
