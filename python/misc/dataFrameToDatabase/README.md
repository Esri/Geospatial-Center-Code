## DataFrameToDatabase (in `dataFrameToDatabase.py`)

Author: Jake Lucas

This python class will insert a dataframe (specifically a pandas.DataFrame or pandas.io.parsers.TexFileReader for when a csv is streamed in using chunks) into a database table. Under the hood, this uses the pd.DataFrame.to_sql method, so this class will be compatible with every database that is compatible with the to_sql method (which uses sqlalchemy under the hood).

### Requirements: 
sqlalchemy
pandas
