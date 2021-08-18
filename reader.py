import os

from tiled.readers.dataframe import DataFrameAdapter
from tiled.trees.in_memory import Tree
import pandas


def parse_thing(file):
    metadata = {}
    for row in range(2):  # first two lines are metadata
        line = file.readline()
        key, value = line.split(": ", 1)
        metadata[key] = value
    # The rest of the file is a CSV table. Let pandas read it.
    df = pandas.read_csv(file)
    return metadata, df


class ThingDataFrameAdapter(DataFrameAdapter):

    @classmethod
    def from_file(cls, filepath):
        with open(filepath) as file:
            metadata, df = parse_thing(file)
        return cls.from_pandas(df, metadata=metadata, npartitions=1)


def build_reader(filepath):
    "An another approach"
    with open(filepath) as file:
        metadata, df = parse_thing(file)
    return DataFrameAdapter.from_pandas(df, metadata=metadata, npartitions=1)


def is_candidate(filename):
    return True


tree = Tree(
    {
        filename: build_reader(f"files/{filename}")
        for filename in os.listdir("files/")
        if is_candidate(filename)
    }
)
