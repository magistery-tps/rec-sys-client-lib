import pickle


class Picket:
    @staticmethod
    def save(path, obj):
        with open(f'{path}.pickle', 'wb') as handle:
            pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(path):            
        with open(f'{path}.pickle', 'rb') as handle:
            return pickle.load(handle)