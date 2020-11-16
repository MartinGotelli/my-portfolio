import pickle
from abc import abstractmethod


class PersistenceManager:
    def persist(self, object):
        with open(self.file_name(), 'wb') as file:
            pickle.dump(object, file)

    def retrieve(self):
        with open(self.file_name(), 'rb') as file:
            return pickle.load(file)

    @abstractmethod
    def file_name(self):
        return ""
