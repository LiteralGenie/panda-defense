class IdManager:
    _next_id = 1

    @classmethod
    def create(cls):
        result = cls._next_id
        cls._next_id += 1
        return result
