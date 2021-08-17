import logging
import time
import pandas as pd
from pandas.errors import EmptyDataError
import sqlalchemy
from typing import Union, List

class DataFrameToDatabase:

    def __init__(self, df:Union[pd.DataFrame, pd.io.parsers.TextFileReader], 
                 dbTableName:str,
                 driver:str, 
                 username:str=None, 
                 password:str=None, 
                 address:str=None, 
                 dbName:str=None, 
                 port:Union[int, str]=None, 
                 query:dict={},
                 dbEcho:bool=True, 
                 if_exists:str='fail', 
                 index:bool=True, 
                 index_label:str=None, 
                 chunksize:int=None,
                 dtype:dict=None,
                 ):

        #private
        self._logger = logging.getLogger('DataFrameToDatabase')
        self._logger.setLevel(logging.INFO)

        #default value updated in self._validateDataFrame
        self._isIterable = False


        #pd.DataFrame.to_sql variables
        self._index = index
        self._index_label = index_label
        self._chunksize = chunksize
        self._dtype = dtype
        self._dbTableName = dbTableName

        if if_exists not in ['fail', 'append', 'replace']:
            raise ValueError('if_exists must be set to "fails", "replace", or "append"')
        elif if_exists == 'replace':
            self._logger.warning(f'Table "{dbTableName}" will be overwritten.')
        self._if_exists = if_exists

        #validating and categorizing it as iterable or not
        self._logger.info('Validating DataFrame...')
        if self._validateDataFrame(df):
            self._df = df
            self._logger.info('Valid DataFrame')
        
        #validating db params
        self._logger.info('Validating database parameters...')
        if self._validateDbParameters(driver, username, password, address, port, dbName, query):
        
            #sqlalchemy.create_engine parameters
            self._dbEcho = dbEcho
            self._driver = driver
            self._username = username
            self._password = password
            self._address = address
            self._port = port
            self._dbName = dbName
            self._query = query
            self._logger.info('Valid database parameters')


        # self._logger.info('Inserting data...')
        # self.insertData()


    def _validateDataFrame(self, df):
        """
        Validates that the df isn't empty and categorizes it as iterable (TextFileReader) or not iterable (DataFrame)
        """
        #if the df is a standard DataFrame
        if type(df) == pd.DataFrame:
            self._logger.info('Using regular dataframe')

            if df.empty:
                self._logger.error('Empty dataframe')
                raise EmptyDataError('DataFrame is empty') 

            self.colsAndTypes = {name: df.dtypes[name] for name in list(df.columns)}
            self._isIterable = False


        #if the df is a large file read in through chunks
        elif type(df) == pd.io.parsers.TextFileReader:
            self._logger.info('Using large dataframe')
            for chunk in df:
                self.colsAndTypes = {name: chunk.dtypes[name] for name in list(chunk.columns)}
                    
                if chunk.empty:
                    self._logger.error('Empty dataframe')
                    raise EmptyDataError('DataFrame is empty') 

                break
            self._isIterable = True

        else:
            raise TypeError(f'Invalid df type. Type "{type(df)}" is not a DataFrame or TextFileReader')

        return True
    
    def _validateDbParameters(self, driver, username, password, address, port, dbName, query):
        """
        Validates database parameters by passing it into create_engine. If it succeeds, the parameters are valid
        """
        try:
            # if driver:
            #     driver = '+' + driver
            # if port:
            #     port = ':' + str(port)
            # if password:
            #     password = ':' + password
            # if address:
            #     address = '@' + address
            
            dbUrl = sqlalchemy.engine.URL.create(drivername=driver,
                                         username=username,
                                         password=password,
                                         host=address,
                                         port=port,
                                         database=dbName,
                                         query=query)
            
            self._engine = sqlalchemy.create_engine(dbUrl, echo=self._dbEcho)
        except Exception as e:
            self._logger.exception(e)
            raise e
        else:
            return True

    def insertData(self):
        """
        Inserts data into the database depending on the type of DataFrame given
        """
        if self._isIterable:
            #boolean tracking if function DataFrame.to_sql has been run for any chunk
            updated = False
            for chunk in self._df:
                start = time.time()
                if not updated:
                    chunk.to_sql(name=self._dbTableName, 
                                con=self._engine, 
                                if_exists=self._if_exists, 
                                index=self._index, 
                                index_label=self._index_label,
                                chunksize=self._chunksize,
                                dtype=self._dtype)     
                    updated = True

                elif updated:
                    chunk.to_sql(name=self._dbTableName, 
                                con=self._engine, 
                                if_exists='append', 
                                index=self._index, 
                                index_label=self._index_label,
                                chunksize=self._chunksize,
                                dtype=self._dtype)     
                end = time.time()
                self._logger.info(f'Chunk inserted in {end-start:.3f} seconds')



        elif not self._isIterable:
            start = time.time()
            self._df.to_sql(name=self._dbTableName, 
                           con=self._engine, 
                           if_exists=self._if_exists, 
                           index=self._index, 
                           index_label=self._index_label,
                           chunksize=self._chunksize,
                           dtype=self._dtype)     
            end = time.time()
            self._logger.info(f'DataFrame inserted in {end-start:.3f} seconds')

    def main(self):
        self._logger.info('Inserting data...')
        self.insertData()



