import pandas as pd
import pymorphy2
import os


class SyncParser:

    def __init__(self, saver):
        """

        :param saver: its function for saving result (for example - save to json file or database)
        """
        self._morph = pymorphy2.MorphAnalyzer()
        self._saver = saver

        self.current_df = None
        self.current_text = ""

    def parse(self, path):
        try:
            self.current_df = pd.read_csv(path)
            self._drop_numeric_columns()
            columns = list(self.current_df)
            for i in range(self.current_df.shape[0]):
                for column in columns:
                    for word in str(self.current_df.loc[i][column]).split():
                        p = self._morph.parse(word)[0]
                        if 'NUMB' not in p.tag:
                            print(word)
                            self.current_text += word + " "
        except OSError as e:
            raise e
        except Exception as e:
            raise e

    def _drop_numeric_columns(self):
        columns = list(self.current_df)
        types = list(self.current_df.dtypes)
        numeric_types = ['int', 'float', 'complex', 'uint']
        drop_list = []

        for i in range(self.current_df.shape[1]):
            if types[i] in numeric_types:
                drop_list.append(columns[i])
        self.current_df.drop(columns=drop_list, inplace=True)


if __name__ == "__main__":
    """
    example:
        data_path = "../data/files"
        df = pd.read_csv(os.path.join(data_path, '7017069388-taxi.csv'))
        parser = SyncParser('asd')
        parser.parse(os.path.join(data_path, '7017069388-taxi.csv'))
        print(len(parser.current_text))
    """