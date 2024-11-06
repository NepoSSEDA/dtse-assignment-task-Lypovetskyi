import logging
from fastapi import APIRouter, UploadFile, HTTPException
from preprocessing import prepare_data
from errors import MissingMinimumAmountOfColumnsError, MissingMandatoryColumnError, CategoricalValueNotAllowed
from api_server.db_connection import create_db_connection
from main import load_model, predict

router = APIRouter()

@router.post('/v1/preprocess-data')
def preprocess_rest(file: UploadFile):

    logging.info('Starting handling preprocessing request...')

    if file.content_type != 'text/csv':
        logging.exception('Client provided wrong file type. Responding with 415 HTTP Error...')
        # Return 415 HTTP error if client provided file that's not a .csv
        raise HTTPException(415, 'Unsupported Media Type (only text/csv is allowed)')

    try:
        df = prepare_data(file.file)
    except MissingMinimumAmountOfColumnsError as e:
        logging.exception('Client provided a dataset with lower than minimum amount of columns. Responding with 400 HTTP Error...')
        # Return 400 HTTP error if client provided a dataset with lower than minimum amount of columns
        raise HTTPException(400, repr(e))
    except MissingMandatoryColumnError as e:
        logging.exception('Client provided a dataset that not containing some of mandatory attributes. Responding with 400 HTTP Error...')
        # Return 400 HTTP error if client provided a dataset that not containing some of mandatory attributes
        raise HTTPException(400, repr(e))
    except CategoricalValueNotAllowed as e:
        logging.exception('Client provided a dataset with not-acceptable categorical values. Responding with 400 HTTP Error...')
        # Return 400 HTTP error if client provided a dataset with not-acceptable categorical values
        raise HTTPException(400, repr(e))
    
    # Open a connection with database and create a cursor instance for inserting data
    try:
        conn = create_db_connection()
    except Exception:
        logging.exception('Error while connecting to a database. Responding with 500 HTTP Error...')
        raise HTTPException(500, 'Internal Server Error while connecting to a database')
    curs = conn.cursor()

    # Load model from the provided file and get the prediction results
    logging.info('Loading model and extracting prediction results...')
    model = load_model('model.joblib')
    df['predicted_house_value'] = predict(df, model)

    # Generating string containing all of dataframe columns escaped by "" and separated by , for using SQL INSERT query
    columns_query_list = ", ".join([f'\"{column}\"' for column in df.columns.values])
    # Generating string consists of %s placeholders for values of each dataframe raw also for using it in SQL INSERT query
    placeholders = ", ".join(["%s"] * len(df.columns))

    # Cycle for inserting in database each data element row by row
    for i in range(df.shape[0]):
        logging.info(f'Inserting to a database row number {i}...')
        try:
            # Executing SQL query with generated columns list and placeholders 
            curs.execute(f'''
                INSERT INTO housing_data({columns_query_list}) VALUES({placeholders})
                ON CONFLICT ("longitude", "latitude", "housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income", "ocean_proximity_<1H OCEAN", "ocean_proximity_INLAND", "ocean_proximity_ISLAND", "ocean_proximity_NEAR BAY", "ocean_proximity_NEAR OCEAN") DO NOTHING;
            ''', tuple(df.iloc[i, :]))
        except Exception:
            # In case of error terminate the connection and response with HTTP code 500
            logging.exception(f'Error while inserting row number {i}. Responding with 500 HTTP Error...')
            curs.close()
            conn.close()
            raise HTTPException(500, f'Internal Server Error while inserting row number {i}')

    # Commit insertion to database, close cursor and connection    
    curs.close()
    conn.commit()
    conn.close()

    logging.info('Data was successfully preprocessed and uploaded to a database')
    return "Data was successfully preprocessed and uploaded to a database"
