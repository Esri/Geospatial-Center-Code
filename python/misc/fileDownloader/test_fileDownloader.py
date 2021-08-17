import pytest
from fileDownloader import FileDownloader
import requests
import os
from customErrors import DirectoryNotFoundError
import logging
from zipfile import ZipFile

class TestFileDownloader:

    def test_validUrl(self, tmpdir):
        with pytest.raises(requests.exceptions.MissingSchema):
            FileDownloader('dakfldfjasfk', str(tmpdir))

    @pytest.mark.webtest
    def test_onlineUrl(self, tmpdir):
        with pytest.raises(requests.exceptions.HTTPError):
            #url is a valid test url that returns a 404
            FileDownloader('https://reqres.in/api/users/23', str(tmpdir))

    def test_validSaveDir(self, tmpdir):
        validUrl = r'https://reqres.in/api/users?page=2'
        invalidDir = os.path.join(str(tmpdir), 'nonExistent')
        with pytest.raises(DirectoryNotFoundError):
            FileDownloader(validUrl, invalidDir)

    @pytest.mark.webtest
    def test_downloadZip(self, tmpdir):
        fileUrl = r'https://www.stats.govt.nz/assets/Uploads/Business-financial-data/Business-financial-data-March-2021-quarter/Download-data/business-financial-data-march-2021-quarter-csv.zip'
        fileName = r'business-financial-data-march-2021-quarter-csv.zip'
        
        downloader = FileDownloader(fileUrl, str(tmpdir))
        try:
            path = downloader.download()

        except Exception as e:
            logging.exception(e)
            assert False
        else:
            assert path == os.path.join(str(tmpdir), fileName)
            #asserting that the zipfile is valid and uncorrupted
            assert ZipFile(path).testzip() is None
        