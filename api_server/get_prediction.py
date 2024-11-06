from fastapi import APIRouter, HTTPException
from api_server.db_connection import create_db_connection
from api_server.pydantic_model import HousingModel
import logging

router = APIRouter()

@router.post('/v1/get-prediction')
def get_prediction(housing: HousingModel):

    logging.info('Starting handling get_prediction request...')

    # Open a connection with database and create a cursor instance for reading data
    try:
        conn = create_db_connection()
    except Exception:
        logging.exception('Error while connecting to a database. Responding with 500 HTTP Error...')
        raise HTTPException(500, 'Internal Server Error while connecting to a database')
    curs = conn.cursor()

    # Constructing name of column ocean_proximity we needed 
    housing.ocean_proximity = "ocean_proximity_" + housing.ocean_proximity.upper()
    try:
        curs.execute(f'''
            SELECT predicted_house_value FROM housing_data
            WHERE (longitude = %s) AND (latitude = %s) AND (housing_median_age = %s) AND (total_rooms = %s) AND (total_bedrooms = %s) AND (population = %s) AND (households = %s) AND (median_income = %s) 
            AND ("{housing.ocean_proximity}" = 1);      
        ''', (housing.longitude, housing.latitude, housing.housing_median_age, housing.total_rooms, housing.total_bedrooms, housing.population, housing.households, housing.median_income))
    except Exception:
        # In case of error terminate the connection and response with HTTP code 500
        logging.exception(f'Error while executing SELECT query. Responding with 500 HTTP Error...')
        curs.close()
        conn.close()
        raise HTTPException(500, f'Internal Server Error while extracting prediction result from a database')

    # Extracting only one row in results
    row = curs.fetchone()
    
    # Close cursor and terminate connection
    curs.close()
    conn.close()

    # In case if query didn't find any occurence of sended housing information raise 404 HTTP Exception
    if row is None:
        logging.exception('Housing data was not founded in database. Responding with 400 HTTP Error...')
        raise HTTPException(404, 'Housing data was not founded in database')
    # In successfull case extract predicted value
    predicted_house_value = row[0]

    return f'Predicted house value is {predicted_house_value}'