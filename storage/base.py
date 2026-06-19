# storage/base.py

from abc import ABC, abstractmethod

class BaseStorage(ABC):

    @abstractmethod
    def load_temp(self):
        pass

    @abstractmethod
    def save_temp(self, rows):
        pass

    @abstractmethod
    def save_final(self, rows):
        pass