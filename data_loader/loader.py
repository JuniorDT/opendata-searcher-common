import pandas as pd
import os


class MetaLoader:
    def __init__(self, meta_path, folder_to_save="../data/meta_list"):
        """

        :param meta_path: path to list.csv (for example tomsk.gov.ru/opendata/list.csv)
        :param folder_to_save: (folder for saving meta files)
        """
        self.meta_path = meta_path
        self.folder_to_save = folder_to_save

    def run(self):
        if not os.path.isdir(self.folder_to_save):
            print("Create directory: {}".format(self.folder_to_save))
            os.makedirs(self.folder_to_save)
        meta_list = pd.read_csv(self.meta_path, error_bad_lines=False, warn_bad_lines=False)
        meta_csv_list = meta_list[['property', 'value']][meta_list.format == 'csv']
        j = 0
        for i in meta_csv_list.index.values:
            try:
                new_meta = pd.read_csv(meta_csv_list.loc[i].value)
                name = meta_csv_list.loc[i].property
                name += '.csv'
                new_meta.to_csv(os.path.join(self.folder_to_save, name))
                print(j)
                j += 1
                del new_meta
            except Exception as e:
                print(e)
                continue


class FileLoader:
    """
        Load and save csv-files using meta-info from MetaLoader result files
    """
    def __init__(self, path_to_meta_csv, folder_to_save="../data/files", latest_id=14):
        self.path_to_meta_csv = path_to_meta_csv
        self.folder_to_save = folder_to_save
        self.latest_id = latest_id

    def save_file(self, meta_csv, name):
        """
        Save latest version file
        :param meta_csv: path to meta csv file
        :return:
        """
        meta = pd.read_csv(meta_csv)
        path = meta.loc[self.latest_id].value

        file = pd.read_csv(path)
        file.to_csv(os.path.join(self.folder_to_save, name))

    @property
    def file_list(self):
        """
        :return: iterator for filenames in meta directory
        """
        for f in os.listdir(self.path_to_meta_csv):
            if os.path.isfile(os.path.join(self.path_to_meta_csv, f)):
                yield f

    def save_all(self):
        if not os.path.isdir(self.folder_to_save):
            print("Create directory: {}".format(self.folder_to_save))
            os.makedirs(self.folder_to_save)
        j = 0
        for file in self.file_list:
            try:
                self.save_file(os.path.join(self.path_to_meta_csv, file), file)
                print(j)
                j += 1
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    """
    example for meta loader:
        loader = MetaLoader(meta_path="https://tomsk.gov.ru/opendata/list.csv")
        loader.run()

    example for file loader:
        floader = FileLoader(path_to_meta_csv='../data/meta_list')
        floader.save_all()
    """