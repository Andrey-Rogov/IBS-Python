from abc import ABC, abstractmethod
from io import StringIO
from random import randint, uniform
import json
import os
import csv
import yaml


class BaseWriter(ABC):
    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        pass


class JSONWriter(BaseWriter):
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
         Writes given data to string object of file StringIO
         :param data: Data to write
         :return: StringIO object with data from 'data'
         """
        json_data = json.dumps(data)
        string_io = StringIO()
        string_io.write(json_data)
        string_io.seek(0)
        return string_io


class CSVWriter(BaseWriter):
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
         Writes given data to string object of file StringIO
         :param data: Data to write
         :return: StringIO object with data from 'data'
         """
        csv_string_io = StringIO()
        csv_writer = csv.writer(csv_string_io)
        csv_writer.writerows(data)
        return csv_string_io


class YAMLWriter(BaseWriter):
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
         Writes given data to string object of file StringIO
         :param data: Data to write
         :return: StringIO object with data from 'data'
         """
        yaml_data = yaml.dump(data)
        string_io = StringIO()
        string_io.write(yaml_data)
        string_io.seek(0)
        return string_io


class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data

    def generate(self) -> None:
        data = [[randint(0, 100),
                 str(randint(10_000, 99_999)),
                 round(uniform(0, 10), 5)] for _ in range(4)]
        self.data = data

    def to_file(self, path: str, writer: BaseWriter) -> None:
        """
         Method for writing data after its generation
         :param path: Path where to save file
         :param writer: One of the BaseWriter child
         """
        if not self.data:
            raise Exception("No data to write")

        extension = {JSONWriter: '.json', CSVWriter: '.csv', YAMLWriter: '.yaml'}
        file_name = os.path.join(path, 'generated' + extension[type(writer)])

        data_to_write = writer.write(self.data).getvalue()
        with open(file_name, 'w') as file:
            file.write(data_to_write)


# el = DataGenerator()
# el.generate()
# el.to_file(os.getcwd(), YAMLWriter())
