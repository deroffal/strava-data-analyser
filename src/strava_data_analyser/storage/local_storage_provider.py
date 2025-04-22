import json
from os import walk
from pathlib import Path

class LocalStorageProvider:
    summary_activity_file_path = "../../data/summaries"
    detailed_activity_path = "../../data/details"

    def get_last_activity(self):
        last_file = sorted(self._list_files(self.summary_activity_file_path), key=lambda x: int(Path(x).stem))[-1]
        file_path = Path(f"{self.summary_activity_file_path}/{last_file}")
        return file_path.read_text(encoding='utf-8')

    def upload_summary(self, _name, _data):
        return self._write_to_location(_name, _data, self.summary_activity_file_path)

    def upload_detail(self, _name, _data):
        return self._write_to_location(_name, _data, self.detailed_activity_path)

    # fixme params
    def load_summary_activities(self, year: int = None):
        return self._read_files_in(self.summary_activity_file_path)

    # fixme params
    def load_detailed_activities(self, year: int = None, type: str = None):
        return self._read_files_in(self.detailed_activity_path)

    def _write_to_location(self, name: str, data: str, location: str):
        file_path = Path(f"{location}/{name}")
        file_path.write_text(data, encoding='utf-8')

    def _read_files_in(self, path: str):
        """
        Read json files in a directory
        :param path:
        :return: the content of each file.
        """
        content = []
        files = self._list_files(path)
        for file_name in files:
            txt = Path(f"{path}/{file_name}").read_text(encoding='utf-8')
            content.append(txt)

        return content

    def _list_files(self, directory: str):
        """
        List directory's files name
        :param directory:
        :return: Returns all files name in the directory
        """
        return next(walk(directory), (None, None, []))[2]
