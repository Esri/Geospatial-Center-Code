from fileDownloader import FileDownloader
from zipfile import ZipFile

def main():
    fileUrl = r'https://www.stats.govt.nz/assets/Uploads/Business-financial-data/Business-financial-data-March-2021-quarter/Download-data/business-financial-data-march-2021-quarter-csv.zip'
    downloader = FileDownloader(fileUrl)
    path = downloader.download()
    assert ZipFile(path).testzip() is None
    # print(path)

if __name__=='__main__':
    main()