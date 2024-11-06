import pandas as pd
import numpy as np
import logging
from errors import MissingMinimumAmountOfColumnsError, MissingMandatoryColumnError, CategoricalValueNotAllowed

continuous = {'longitude': 2, 'latitude': 2, 'housing_median_age': 0, 'total_rooms': 0, 'total_bedrooms': 0, 'population': 0, 'households': 0, 'median_income': 4}
#categorical = {'ocean_proximity': ['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'OUT OF REACH', 'ISLAND'], 'agency': ['yes', 'no']}
ocean_proximity_values = ['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'OUT OF REACH', 'ISLAND']

def prepare_data(input_data):

    logging.info('Starting preprocessing data. Reading from provided .cvs file...')
    df = pd.read_csv(input_data, na_values=['NA', 'NaN', 'Null', 'NULL', 'null', 'na', ''])
    
    columns_count = len(df.columns)
    need_to_strip_dataset = False

    logging.info('Preprocessing data...')

    if columns_count < 9:
        # If count of dataset columns is lower than 9, then there is missing minumum of required columns
        raise MissingMinimumAmountOfColumnsError(columns_count)
    elif columns_count > 9:
        # In this case we need to prune the dataset by non-required columns so we can work only with required one
        need_to_strip_dataset = True

    # Delete whitespaces from the column names and make them only in low-case
    df.columns = df.columns.str.strip().str.lower()

    # Rename the columns to the format in which regression model expects
    df.rename(columns = {'lat': 'latitude', 'median_age': 'housing_median_age', 'rooms': 'total_rooms', 'bedrooms': 'total_bedrooms', 'pop': 'population'}, inplace = True)
	
    # Cycle for checking if provided dataset contains all required (or mandatory) continuous columns
    for column in continuous.keys():
        if column not in df.columns:
            raise MissingMandatoryColumnError(column)
        
        # Extracting decimal precision from dictionary of continuous attributes
        decimal_precision = continuous[column]
        # Continuous attributes considered to be numeric and should be treated as it, all values of non-numeric types will be replaced by NaN
        df[column] = pd.to_numeric(df[column], errors = 'coerce')
        # Fill all missing values in current dataset column with it's mean value
        df[column].fillna(df[column].mean(), inplace = True)
        # Round values in current dataset column to a given decimal precision
        df[column] = df[column].round(decimal_precision)

        if decimal_precision == 0:
            # In this case convert all values to integer type to eliminate useless decimal part
            df[column] = df[column].astype('Int64')
    
    # Remove all rows containing NA values from begining and after converting to numeric
    df = df.dropna()
    
    # Verifying if provided dataset contains all required (or mandatory) categorical columns (first version was a cycle which was verifying all categorical columns)
    column = 'ocean_proximity'
    if column not in df.columns:
        raise MissingMandatoryColumnError(column)
        
    # Categorical attributes considered to be strings and should be treated as it
    df[column] = df[column].astype('category')
    df[column] = df[column].convert_dtypes()

    # Delete whitespaces from the categorical values and make them only in low-case
    df[column] = df[column].apply(lambda x: x.strip().upper())

    # Filter the dataset on current column and check if some of its values are not in ones that are accaptable
    test_df = df.loc[~df[column].isin(ocean_proximity_values), column]
    if not test_df.empty:
        # Extract first occurency of forbidden value in column as a example
        forbidden_value = test_df.iloc[0]
        raise CategoricalValueNotAllowed(column, forbidden_value, ocean_proximity_values)

    # In case of dataset with count of columns greater than required we need to prune it from the useless attributes
    if need_to_strip_dataset:
        selected_features = list(continuous.keys())
        selected_features.append('ocean_proximity')
        df = df[selected_features]

    # Drop the duplicates in whole dataset with keeping only first occurence of duplicate rows
    df.drop_duplicates(keep = 'first', inplace = True)
    
    # Remove all rows containing this value for attribute 'ocean_proximity' because it is ignored by prediction model
    df.drop(index = df[df['ocean_proximity'] == 'OUT OF REACH'].index, inplace = True)

    # encode the categorical variables
    df = pd.get_dummies(df)

    ocean_proximity_dummies = ['ocean_proximity_<1H OCEAN', 'ocean_proximity_INLAND', 'ocean_proximity_ISLAND', 'ocean_proximity_NEAR BAY', 'ocean_proximity_NEAR OCEAN']

    # Cycle for adding all of dummy encoding columns for ocean_proximity in order to provide prediction model with all needed columns
    for column in ocean_proximity_dummies:
        if column not in df.columns.values:
            # Adding dummy column with default value
            df[column] = 0

    # Rearranging dataset columns to order in which regression model expects it
    df = df.reindex(columns = [*list(continuous.keys()), *ocean_proximity_dummies])

    logging.info('Data was preprocessed')

    return df

if __name__ == '__main__':

    prepare_data('housing.csv')


