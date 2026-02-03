
class Palete:
    def __init__(self):
        self.all_clear()
        self.max_field = 4
    def all_clear(self):
        self.places = {
            1:0,
            2:0,
            3:0,
            "defect":0
        }
    def clear(self, name):
        self.name

    def isempty(self, name):
        if name == "defect":
            return 0
        if self.places[name] >= self.max_field:
            return False
        return self.places[name] + 1
    
    def put(self, name):
        if name == "defect":
            return True
        self.places[name] += 1
        return True
    
    def show(self):
        return {
            "columns": ["Кол-во"],
            "matrix": map(lambda x: [x], self.places.values()),
            "indexes": ["Объект 1", ],
        }
