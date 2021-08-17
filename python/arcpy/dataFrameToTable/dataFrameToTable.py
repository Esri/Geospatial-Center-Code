import pandas as pd
from typing import Union, List
from pandas.errors import EmptyDataError
import re
import arcpy
import os
import logging
import pprint
import time

class DataFrameToTable:

    def __init__(self, Df:Union[pd.DataFrame, pd.io.parsers.TextFileReader], outTableName:str, outGDB:str=arcpy.env.workspace, dtype={}, logger=None):
        """
        Converts a pd.DataFrame into an table hosted in a file geodatabase within ArcGIS

        :param DataFrame or TextFileReader Df: df or object containing df chunks 
        :param str outTable: the name of the output table
        :param str outGDB: the location of the file geodatabase that the output table will be stored in
        :param dict dtype: NotImplemented
        :raises pd.errors.EmptyDataError: if the datatframe is empty
        :raises ValueError: if an empty output table name was provided
        :raises TypeError: if the data provided is not a DataFrame or TextFileReader
        """
        self._logger = logger if logger is not None else logging.getLogger('DataFrameToTable')
        # self._logger.setLevel(logging.INFO)


        #attribute assignment
        if self._validateDataFrame(Df):
            self.Df = Df

        #if an empty output table name is assigned
        if outTableName == '':
            raise ValueError('Output table name is required.')
        self.outTableName = outTableName
        self.outGDB = outGDB
        arcpy.env.workspace = self.outGDB
        # pprint.pprint(self.colsAfterAndBefore)

    def _validateDataFrame(self, Df):
        #if the df is a standard DataFrame
        if type(Df) == pd.DataFrame:
            self._logger.info('Using regular dataframe')

            if Df.empty:
                self._logger.error('Empty dataframe')
                raise EmptyDataError('DataFrame is empty') 

            self.colsAndTypes = {name: Df.dtypes[name] for name in list(Df.columns)}
            self._isIterable = False


        #if the df is a large file read in through chunks
        elif type(Df) == pd.io.parsers.TextFileReader:
            self._logger.info('Using large dataframe')
            for chunk in Df:
                self.colsAndTypes = {name: chunk.dtypes[name] for name in list(chunk.columns)}
                    
                if chunk.empty:
                    self._logger.error('Empty dataframe')
                    raise EmptyDataError('DataFrame is empty') 

                break
            self._isIterable = True

        else:
            raise TypeError(f'Invalid Df type. Type "{type(Df)}" is not a DataFrame or TextFileReader')

        return True

    def createTableAndAddFields(self) -> dict:
        #converting any non-arcpy-safe column names and datatypes into arcpy-safe ones 
        arcpySafeColsAndTypes, colsAfterAndBefore = self._getArcpyTypesAndConversionFromDf(self.colsAndTypes)

        #populating the field description with the names, dtypes, and aliases (from the dataframe)
        fieldDescription = [[name, value, colsAfterAndBefore[name]] for name, value in arcpySafeColsAndTypes.items()]

        #creating the table and adding the correct fields and datatypes
        arcpy.management.CreateTable(self.outGDB, self.outTableName)
        self._logger.info(f'Created table: {self.outTableName}')
        arcpy.management.AddFields(self.outTableName, fieldDescription)
        self._logger.info(f'Added fields to table: {self.outTableName}')

        return colsAfterAndBefore

    @staticmethod
    def _getArcpyTypesAndConversionFromDf(colsAndTypesDict:dict):

        if len(colsAndTypesDict) < 1:
            raise EmptyDataError('No columns or types in this DataFrame')

        textTypeList = ['object']
        intTypeList = ['int64']
        floatTypeList = ['float64']

        arcpySafeColsAndTypes = {}
        colsAfterAndBefore = {}
        for key, value in colsAndTypesDict.items():
            
            #converting pandas datatype to arcpy datatype
            if value in textTypeList:
                colType = 'TEXT'
            elif value in intTypeList:
                colType = 'LONG'
            elif value in floatTypeList:
                colType = 'DOUBLE'
            else:
                colType = 'TEXT'

            #renaming the key so that there are no spaces in it
            key = key.strip()
            # print(f'Stripped: {key}')
            # underscoredName = re.sub(r'[:,]', '', key)
            underscoredName = re.sub(r'[\s/\-:,\(\)\.]', '_', key)
            # print(f'First Pass: {underscoredName}')
            #replacing a group of underscores with only one
            underscoredName = re.sub(r'_+', '_', underscoredName)
            # print(f'Second Pass: {underscoredName}')
            #removing trailing underscores from columns
            if underscoredName.endswith('_'):
                underscoredName = underscoredName[:-1]

            if len(underscoredName) > 64:
                underscoredName = underscoredName[:64]

            # underscoredName = re.sub(r'_')
            #adding arcpy safe names and types to another dict
            arcpySafeColsAndTypes.update({underscoredName: colType})

            colsAfterAndBefore.update({underscoredName: key})
            
        return arcpySafeColsAndTypes, colsAfterAndBefore

    def populateTable(self, colsAfterAndBefore:dict):
        insertFields = list(colsAfterAndBefore.keys())
        insertCursor = arcpy.da.InsertCursor(self.outTableName, insertFields)

        if self._isIterable:
            for chunk in self.Df:
                start = time.time()
                self._insertRows(chunk, insertFields, colsAfterAndBefore, insertCursor)
                end = time.time()
                self._logger.info(f'Chunk inserted in {end-start: .2f} seconds')
        elif not self._isIterable:
            start = time.time()
            self._insertRows(self.Df, insertFields, colsAfterAndBefore, insertCursor)
            end = time.time()
            self._logger.info(f'DataFrame inserted in {end-start: .2f} seconds')

    def _insertRows(self, Df:pd.DataFrame, insertFields:List[str], colsAfterAndBefore:dict, insertCursor:arcpy.da.InsertCursor):
        for index, row in Df.iterrows():
            inputRow = [row[colsAfterAndBefore[name]] for name in insertFields]
            insertCursor.insertRow(inputRow)

    def main(self):
        #creating ArcGIS table from the df names and dtypes
        self.colsAfterAndBefore = self.createTableAndAddFields()
        self.populateTable(self.colsAfterAndBefore)

        

        