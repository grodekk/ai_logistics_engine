import pandas as pd


class JSONExtractor:
    def __init__(self, loader):
        self.loader = loader

    def load_json_to_df(self, filepath):
        data = self.loader.load(filepath)
        return pd.DataFrame(data)