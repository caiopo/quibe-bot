import dataset


class Database:
    def __init__(self, url=None):
        self.db = dataset.connect(url)
        self.table = self.db['subscribers']

    def add(self, user):
        user = str(user)
        if user not in self:
            self.table.insert(dict(user_id=user))
            return True
        return False

    def remove(self, user):
        user = str(user)
        if user in self:
            self.table.delete(user_id=user)
            return True
        return False

    def __contains__(self, user):
        user = str(user)
        return self.table.find_one(user_id=user) is not None

    def __iter__(self):
        return iter([user['user_id'] for user in self.table])
