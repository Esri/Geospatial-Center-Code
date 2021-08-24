from pandas.core.frame import DataFrame
from dataFrameToTable import DataFrameToTable
import pytest
import pandas as pd
import os
import arcpy
import logging

arcpy.env.overwriteOutput = True

@pytest.fixture
def emptyDataFrame():
    return pd.DataFrame()

@pytest.fixture
def basicDataFrame():
    df = pd.DataFrame([['djfasdjf', 2, 1.5754], ['dfjaksldjf', 4, 5.353], ['afsdjf', 6, 5.357], ['dlfdsjkafddj', 8, 5.28], ['dfaskldja', 10, 3.5674]], columns=['string', 'int', 'float/double'])
    return df

@pytest.fixture
def basicTextFileReader(tmpdir, basicDataFrame):
    fullPath = os.path.join(tmpdir, 'example.csv')
    basicDataFrame.to_csv(fullPath)
    reader = pd.read_csv(fullPath, chunksize=2)
    return reader

@pytest.fixture
def testFileGDB(tmpdir):
    filename = 'test.gdb'
    arcpy.management.CreateFileGDB(str(tmpdir), filename)
    fullPath = os.path.join(str(tmpdir), filename)
    return fullPath

class TestDataFrameToTable:

    def test_emptyDataFrame(self, emptyDataFrame):
        with pytest.raises(pd.errors.EmptyDataError):
            DataFrameToTable(emptyDataFrame, 'test', '')

    def test_recognizedDataFrame(self, basicDataFrame):
        obj = DataFrameToTable(basicDataFrame, 'test', '')
        assert obj._isIterable == False

    def test_recognizeTextFileReader(self, basicTextFileReader):
        obj = DataFrameToTable(basicTextFileReader, 'test', '')
        assert obj._isIterable == True

    def test_noOutputTableName(self, basicDataFrame):
        with pytest.raises(ValueError):
            DataFrameToTable(basicDataFrame, '', '')

    @pytest.mark.parametrize('inputSource', [
        'jdklafjd;skajs',
        lambda: 542,
        (1, 2, 3, 4),
        {'key': 'value'}
    ])
    def test_incorrectInputDataType(self, inputSource):
        with pytest.raises(TypeError):
            DataFrameToTable(inputSource, 'test', '')

    @pytest.mark.parametrize('paramsAndOutcome', [
        ({'name with spaces': 'object'}, {'name_with_spaces': 'TEXT'}),
        ({'CAPITAL12'})
        ({'na3857329me:,/::---()).. _with characters, and spaces': 'int64'}, {'na3857329me_with_characters_and_spaces': 'LONG'}),
        ({'normalName': 'float64'}, {'normalName': 'DOUBLE'})

    ])
    def test_getArcpyTypesAndConversionFromDf(self, paramsAndOutcome):
        """
        Verifies the efficacy of this conversion function
        
        :param tuple paramsAndOutcome: ({inputColName: inputColType}, {expectedOutColName: expectedOutColType}, {expectedOutColName: inputColName})
        """
        colAndType = paramsAndOutcome[0]
        expectedArcpySafe = paramsAndOutcome[1]
        expectedConversionDict = {list(expectedArcpySafe.keys())[0]: list(colAndType.keys())[0]}


        outArcpySafe, outConversion = DataFrameToTable._getArcpyTypesAndConversionFromDf(colAndType)
        assert expectedArcpySafe == outArcpySafe
        assert expectedConversionDict == outConversion

    @pytest.mark.slow
    @pytest.mark.parametrize('inputSource', [
        pytest.lazy_fixture('basicDataFrame'),
        pytest.lazy_fixture('basicTextFileReader')
    ])
    def test_createTableAndAddFields(self, inputSource, testFileGDB):
        
        obj = DataFrameToTable(inputSource, 'test', testFileGDB)
        try:
            obj.createTableAndAddFields()
        except Exception as e:
            logging.exception(e)
            assert False
        else:
            assert True

    @pytest.mark.slow
    @pytest.mark.parametrize('inputSource', [
        pytest.lazy_fixture('basicDataFrame'),
        pytest.lazy_fixture('basicTextFileReader')
    ])
    def test_populateTable(self, inputSource, testFileGDB):
        obj = DataFrameToTable(inputSource, 'test', testFileGDB)
        conversionDict = obj.createTableAndAddFields()
        try:
            obj.populateTable(conversionDict)
        except Exception as e:
            logging.exception(e)
            assert False
        else:
            assert True