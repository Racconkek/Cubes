import pickle
import copy
import os


class Saver:
    def __init__(self):
        pass

    @staticmethod
    def save(info, user_name):
        file_path = os.path.join(os.path.dirname(__file__), 'saves', str(user_name + '.cube'))
        with open(file_path, "wb") as file:
            pickle.dump(info, file)

    @staticmethod
    def load(user_name):
        file_path = os.path.join(os.path.dirname(__file__), 'saves', str(user_name + '.cube'))
        try:
            with open(file_path, "rb") as file:
                info = pickle.load(file)
                return info
        except IOError:
            print("No saves")


class SavedInfo:
    def __init__(self, board, points):
        self.board = copy.deepcopy(board)
        self.points = copy.deepcopy(points)
