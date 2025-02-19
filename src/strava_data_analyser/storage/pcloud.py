import logging
import os

import requests

from strava_data_analyser.utils.oauth2 import OAuth2

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PCloud:

    def __init__(self):
        _oauth2 = OAuth2(
            "https://my.pcloud.com/oauth2/authorize",
            "https://eapi.pcloud.com/oauth2_token",
            os.getenv("STORAGE_CLIENT_ID"),
            os.getenv("STORAGE_CLIENT_SECRET"),
            redirect_url="http://localhost:12185"
        )
        self.baseUrl = "https://eapi.pcloud.com"
        self.access_token = _oauth2.get_access_token()
        operations = Operations(self.baseUrl, self.access_token)
        self.operations = operations
        root_folder = operations.list_folder(os.getenv('STORAGE_ROOT_FOLDER_ID'))
        _folders = root_folder['metadata']['contents']
        _summaries_folder_id = self._get_id(_folders, 'summaries')
        self.summaries_folder_id = _summaries_folder_id
        _details_folder_id = self._get_id(_folders, 'details')
        self.details_folder_id = _details_folder_id
        _segments_folder_id = self._get_id(_folders, 'segments')
        self.segments_folder_id = _segments_folder_id
        _last_activity_date_file_id = self._get_id(_folders, 'synchronization.json')
        self.last_activity_date_file_id = _last_activity_date_file_id

    def _get_id(self, _folders, _name):
        return next((folder for folder in _folders if folder['name'] == _name), None)['id'][1:]

    def get_last_activity(self):
        return self.operations.get_file_content(self.last_activity_date_file_id)

    def update_last_activity(self, _last_activity):
        return self.operations.update_file(self.last_activity_date_file_id, _last_activity)

    def upload_summary(self, _name, _data):
        return self.operations.upload(_name, self.summaries_folder_id, _data)

    def upload_detail(self, _name, _data):
        return self.operations.upload(_name, self.details_folder_id, _data)


class Operations:

    def __init__(self, baseUrl, access_token):
        self.baseUrl = baseUrl
        self.access_token = access_token

    def get_file_content(self, _id):
        _fd = self._file_open(_id)
        if _fd is None:
            return None

        return self._file_read(_fd)

    def update_file(self, _file_id, _last_activity):
        _fd = self._file_open(_file_id)
        self._file_truncate(_fd)
        _fd = self._file_open(_file_id)
        self._file_write(_file_id, _fd, _last_activity)
        close = self._file_close(_file_id, _fd)
        return close

    def upload(self, _name, _location, _content: str):
        _data = str(_content)
        _response = requests.request(
            "PUT",
            f"{self.baseUrl}/uploadfile?folderid={_location}&filename={_name}",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "content-type": "text/plain"
                , "Content-Length": str(len(_data))
            },
            data=_data
        )
        if _response.status_code != 200:
            logger.error(f"Error {_response.status_code} : {_response.text}")
            raise RuntimeError(f"Error {_response.status_code} : {_response.text}")
        return _response.json()

    def list_folder(self, _folder_id):
        _response = requests.request(
            "GET",
            f"{self.baseUrl}/listfolder?folderid={_folder_id}",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        if _response.status_code != 200:
            logger.error(f"Error {_response.status_code} : {_response.text}")
            raise RuntimeError(f"Error {_response.status_code} : {_response.text}")
        return _response.json()

    def _file_open(self, _id):
        _response = requests.request(
            "GET",
            f"{self.baseUrl}/file_open?fileid={_id}&flags=1",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        if _response.status_code != 200:
            logger.error(f"Error {_response.status_code} : {_response.text}")
            raise RuntimeError(f"Error {_response.status_code} : {_response.text}")
        return _response.json()["fd"]

    def _file_read(self, _fd):
        _response = requests.request(
            "GET",
            f"{self.baseUrl}/file_read?fd={_fd}&count=1000",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        if _response.status_code != 200:
            logger.error(f"Error {_response.status_code} : {_response.text}")
            raise RuntimeError(f"Error {_response.status_code} : {_response.text}")
        return _response.text

    def _file_truncate(self, _fd):
        _response = requests.request(
            "GET",
            f"{self.baseUrl}/file_truncate?fd={_fd}&length=0",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        if _response.status_code != 200:
            logger.error(f"Error {_response.status_code} : {_response.text}")
            raise RuntimeError(f"Error {_response.status_code} : {_response.text}")
        return _response.text

    def _file_write(self, _id, _fd, _content: str):
        _data = str(_content)
        _response = requests.request(
            "PUT",
            f"{self.baseUrl}/file_write?fileid={_id}&fd={_fd}",
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "content-type": "text/plain"
                , "Content-Length": str(len(_data))
            },
            data=_data
        )
        if _response.status_code != 200:
            logger.error(f"Error {_response.status_code} : {_response.text}")
            raise RuntimeError(f"Error {_response.status_code} : {_response.text}")
        return _response.text

    def _file_close(self, _id, _fd):
        _response = requests.request(
            "GET",
            f"{self.baseUrl}/file_close?fileid={_id}&fd={_fd}",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        if _response.status_code != 200:
            logger.error(f"Error {_response.status_code} : {_response.text}")
            raise RuntimeError(f"Error {_response.status_code} : {_response.text}")
        return _response.text
