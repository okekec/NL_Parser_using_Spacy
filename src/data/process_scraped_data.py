import unicodedata
import sys
import os
import pandas as pd

def load_data(dir_path, test_data_filepath):
    """
        Load testing data from the csv.
    Args:
        dir_path: directory of the test data
        test_data_filepath: the path of the test_data.csv file which is used for testing
    Returns:
        df (DataFrame): Dataframe containing annonated data
    """
    #load data
    if not os.path.isfile(os.path.join(dir_path, test_data_filepath)):
        raise FileNotFoundError("This file doesn't exist")
    else:
        df = pd.read_csv(os.path.join(dir_path,test_data_filepath))
        return df

def convert_vulgar_to_mixed_fraction(df):
    """
        Converts unicode vulgar fraction to mixed fraction
    Args:
        df: df that needs to be cleaned
    Returns:
        df (DataFrame): Dataframe containing clean data
    """
    if 'ingredient' not in df.columns:
        raise ValueError("The dataframe should have 3 columns - url, name, ingredient. Found {0}".format(df.columns))
    #convert vulgar fractions
    for ix, row in df.iterrows():
        for char in row['ingredient']:#.decode('utf-8').strip():
            if unicodedata.name(char).startswith('VULGAR FRACTION'):
                normalized = unicodedata.normalize('NFKC', char)
                df.iloc[ix, 2] = df.iloc[ix, 2].replace(char, normalized)
    return(df)

def save_data(df, filepath):
    """
    Takes clean dataframe from `convert_vulgar_to_mixed_fraction` and saves it in csv
    Args:
        df: df that needs to be cleaned
        filepath: filepath of the location where the test_data is to be saved
    Returns:
        None: Does not return anything but saves the csv file
    """
    
    df.to_csv(filepath, index = False, header = True)

def main():
    if len(sys.argv) == 3:

        data_path, final_filename = sys.argv[1:]

        raw_data_path = os.path.join(data_path, 'raw')
        proc_data_path = os.path.join(data_path, 'processed')

        print('Loading data...\n    RAW DATA: {}'
              .format(raw_data_path))
        test_df = load_data(raw_data_path, 'test_data.csv')

        print('Cleaning data...')
        test_df = convert_vulgar_to_mixed_fraction(test_df)

        print('Saving final test data...\n    CSV: {}'
            .format(os.path.join(proc_data_path, final_filename )))
        save_data(test_df, os.path.join(proc_data_path, final_filename + '.csv' )  )

    else:
        print('Please provide the directory path of data folder'\
              ' as well as the filename for cleaned and transformed data'\
              '\n\nExample: python process_data.py '\
              'data/ clean_train final_train')

if __name__ == '__main__':
    main()
