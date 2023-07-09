import pickle


class Picket:
    @staticmethod
    def save(path, obj):
        with open(f'{path}', 'wb') as handle:
            pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(path):
        with open(f'{path}', 'rb') as handle:
            return pickle.load(handle)