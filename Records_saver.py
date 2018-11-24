from collections import namedtuple

UserRecord = namedtuple("UserRecord", ["name", "points"])

class RecordsSaver:
    def __init__(self, file_name):
        self.records = []
        self.file_name = file_name
        with open(file_name, 'r') as file:
            for line in file:
                name = line.split(' ')[0]
                points = line.split(' ')[1]
                if points[len(points) - 1] == '\n':
                    points = points[:-1]
                points = int(points)
                user = UserRecord(name, points)
                self.records.append(user)

    def get_records(self):
        s = ""
        for i in range(len(self.records)):
            s+= str(i + 1) + ') ' + self.records[i].name + ' ' +\
                str(self.records[i].points) + '\n'
        print(s)

    def add_records(self, points, name):
        print('{0}, your score {1}'.format(name, points))
        self.records.append(UserRecord(name, points))
        self.records.sort(key=lambda score: score.points, reverse=True)
        if len(self.records) > 5:
            self.records.pop()
        with open(self.file_name, "w") as file:
            for user in self.records:
                s = user.name + ' ' + str(user.points) + '\n'
                file.write(s)
        self.get_records()