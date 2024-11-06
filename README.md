# DTSE Data Engineer (ETL) assignment solution
## Bc. Oleksandr Lypovetskyi

### Introduction
The automated solution of the data preprocessing problem is proposed as complete REST API service working with PostreSQL database system. Service is designed using Python in combination with FastAPI framework and data processing tools like Pandas and NumPy.

### Preprocessing description
All data preprocessing pipeline is done within `preprocessing.py` module in `prepare_data` function. This function uses similar signature in case to be compatibile with original functionality described in `main.py`. This way, designed pipeline can be easily used directly in creating model script `main.py`.

The proposed preprocessing algorithm can be separated into next main steps:

1. Read the provided .csv file that can have form of either opened file object or string containing path to this file (only in case of integration to `main.py` script). Adding a list of value that should be interpretied as np.nan to a `na_values` paramater helping to get off situations when `Null` is recognised as text value in continuous column.
2. Determine the count of dataset columns and if there is lower than 9 which is required to preprocessed it to a model – raise an `MissingMinimumAmountOfColumnsError`. In other case, just set the flag signing that dataset needs to be pruned of unnecessary columns.
3. Delete whitespaces from the column names, make them only in low-case and rename it to the format in which regression model expects (e.g. `Rooms` -> `total_rooms`).
4. Begin iterate through the continuous attributes dictionary. For each column algorithm verifies if provided dataset contains this required column and if not it will raise `MissingMandatoryColumnError` error. In other case continue and get it's decimal precision.
5. Then try to convert it to the numeric type with `coerce` error option – so every non-numeric values can be converting to `numpy.nan`.
6. Compute the mean value for actual continuous column and fill with it's value all occurencies of NaN in order to save the potentially valueable data from removing.
7. Round values in current dataset column to a given decimal precision and if it's precision is 0 then additionaly convert this column to `Int64` Pandas type.
8. After checking all continuous attributes drop the rest of NaN values, because we cannot fill the same way missing categorical values.
9. Then check if dataset contains only `ocean_proximity` columns. The reason of that is because column `agency` isn't used by the model. Raise the similar exception if `ocean_proximity` isn't founded.
10. Convert `ocean_proximity` to a categorical Pandas data type and delete whitespaces from it's values and make them only in low-case in order to eliminate potential errors.
11. Filter the dataset on this column and check if some of its values are not in ones that are accaptable (only values that mentioned in `ocean_proximity_values` are allowed). In case of containing some unknown values raise `CategoricalValueNotAllowed` error with text describing the unknown value and list of allowed ones.
12. In case of dataset with count of columns greater than required prune it from the useless attributes and drop all duplicates with keeping only first occurence of duplicate rows.
13. Remove all rows containing value `OUT OF REACH` for attribute `ocean_proximity` because it is ignored by prediction model.
14. Encode the categorical variables using original `pd.get_dummies` method in order to compatibility.
15. Add all of dummy encoding columns for `ocean_proximity` in order to provide prediction model with all columns it's needed. For example, append `ocean_proximity_<1H OCEAN` filled with zero if provided dataset not contained any of `<1H OCEAN` values.
16. Rearrange dataset columns to order in which regression model expects it.

### Endpoints description
REST API service providing two endpoints – one to preprocess data and another to extract results from database.

#### preprocess-data
**POST** `/v1/preprocess-data` is used for the serving main funcionality of data preprocession. 
It accepts within it's body only a one file with content type `text/csv`.

##### Funcionality
Endpoint passing provided dataset to a described `prepare_data` method to execute preprocess pipeline. Once it have transformed data, it proceeds to a connecting with database. Then it loads provided regression model with original `load_model` function and get prediction results for each dataset row. 

After that it inserts to a database row by row each entry of transformed dataset along with the predicted values.

##### Return codes
1. `200` HTTP code is returned when data was successfully preprocessed and uploaded to a database.
2. `415` HTTP code is returned if client provided file that's not a .csv
3. `400` HTTP code is returned in case of some error occured during preprocessing (e.g. `MissingMandatoryColumnError`).
4. `500` HTTP code is returned in case of error while connecting or inserting to a database.

#### get-prediction
**POST** `/v1/get-prediction` is used to extract prediction results for specified housing entity. It accept within it's body only one entity described in `.json` format.

##### Functionality
This endpoint gets the `housing` object of type `HousingModel` which is created as a result of parsing HTTP body from JSON. This object basically represents a one entity from the housing data.

The handling starting with a connecting to a database and continues with the constructing the correct `SELECT` query containing all the housing values by which the unique entity can be identified.

As a successfull result, this endpoint finds in database required housing entity and returns it predicted value.

##### Return codes

1. `200` HTTP code is returned in successfull endpoint execution along with the predicted value stored in the database.
2. `404` HTTP code is returned in case when provided housing entity wasn't finded in the database.
3. `500` HTTP code is returned in case of error while connecting to a database or executing `SELECT` request.

### Database description
#### Structure
Database is named `dtse-assignment-task-db` and basically consists of one table `housing_data` which contains all of columns required by the regression model along with the `predicted_house_value` column.
#### Migration
Initialization and migration of database is done in `db_connection.py` in the `init_db` method. This method achieves it by the connecting to a database root database named `postgres` and executing requests of deleting `dtse-assignment-task-db` if it was previously existing and creating a new one.

Then it reconnecting to a PostgreSQL server, to a `dtse-assignment-task-db`, opens a file `db_backup.sql` which contains SQL-script for backuping database. Next, it reads all it's contents and executing this script to recreate database structure.

After that, server application can work well with the prepared database. In case of some errors while migrating, FastAPI process will terminate with respectively log information.

### Installation
Application is packed into Docker Compose image, so you can run it in a few steps:

1. In terminal opened in project directory run `docker-compose up --build`, this command always builds Docker compose image from `docker-compose.yml` and based on `Dockerfile` for REST API service.
2. Once you builded this image, it will be automatically started executing and you can use application.

### Optional Tasks
1. Logging is done by using the standard Python `logging` module which is also used in original script in `main.py`. Every exception case is logged by the `exception` method of this module.
2. Testing can be done through the standard auto-generated FastAPI docs page which can be accessed from web browser on address http://127.0.0.1:8000/docs. Then you can test the solution using `preprocess-data` endpoint to transform data and upload it to a database and then `get-prediction` to extract prediction result for current data. For example you can provide `get-prediction` with JSON body like
```
{
  "longitude": -122.64,
  "latitude": 38.01,
  "housing_median_age": 36.0,
  "total_rooms": 1336.0,
  "total_bedrooms": 258.0,
  "population": 678.0,
  "households": 249.0,
  "median_income": 5.5789,
  "ocean_proximity": "NEAR OCEAN"
}
```
but you should **pay attention** to fit your data to a JSON format, e.g. using only " instead of '.

3. Exception handling is done by sending user dedicated HTTP error codes based on the raising self-maded exception objects of types like `MissingMandatoryColumnError` which are defined in `errors.py` file.

4. API is provided by the FastAPI tools as described before in this documentation
