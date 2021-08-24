# from ntpath import join
import requests
import logging
import os
import shutil
import time
from customErrors import DirectoryNotFoundError

# logging.basicConfig(level=logging.INFO)

class FileDownloader:

    def __init__(self, url:str, saveDir:str=os.getcwd(), params:dict=None):
        """
        Downloads a file from a given link to a given directory

        :param str url: the url containing the file to be downloaded
        :param str saveDir: the directory where the file will be downloaded to. Defaults to current directory
        :param (optional) dict params: NotImplemented
        :raises requests.exceptions.MissingSchema if the url is an invalid url
        :raises requests.exceptions.HttpError if the url doesn't return a 2xx status code
        :raises DirectoryNotFoundError if the directory passed doesn't exist
        """
        self._validateUrl(url)
        self.url = url
        self.fileName = url.split('/')[-1] 

        # if saveDir != os.path.abspath(os.path.dirname(__file__)):
        #     saveDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), saveDir)
        if saveDir != os.getcwd():
            saveDir = os.path.join(os.getcwd(), saveDir)
            saveDir = os.path.normpath(saveDir)
            # saveDir = os.path.normcase(saveDir)
        self._validatesaveDir(saveDir)
        self.saveDir = saveDir

        self.fullPath = os.path.join(self.saveDir, self.fileName)
        self._logger = logging.getLogger('FileDownloader')
        self._logger.setLevel(logging.INFO)


    def _validateUrl(self, url:str):
        try:
            r = requests.get(url, stream=True)
        except requests.exceptions.MissingSchema:
            raise requests.exceptions.MissingSchema(f'Invalid url: {url}')
        else:
            r.raise_for_status()

    def _validatesaveDir(self, saveDir:str):
        if not os.path.exists(saveDir):
            raise DirectoryNotFoundError(f'Invalid save directory. Path "{saveDir}" does not exist')

    def download(self) -> str:
        """
        Downloads file from link

        :returns str: the path of the downloaded file
        """
        self._logger.info(f'Downloading file: "{self.url}"')
        start = time.time()

        r = requests.get(self.url, stream=True)
        with open(self.fullPath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        end = time.time()
        self._logger.info(f'File downloaded to path: "{self.fullPath}" in {end-start: .2f} seconds')

        return self.fullPath



        