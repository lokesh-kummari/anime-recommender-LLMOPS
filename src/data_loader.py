import pandas as pd
from utils.custom_exception import CustomException
from utils.logger import logging
class AnimeDataLoader:
    def __init__(self,original_csv: str, processed_csv: str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv
    
    def load_and_process(self):
        try:
            df = pd.read_csv(self.original_csv, encoding='utf-8', error_bad_lines='False').dropna()
            required_cols = {'Name', 'Genres','sypnopsis'}
            missing = required_cols - set(df.columns)
            if missing:
                raise ValueError(f"Missing required columns: {missing}")
            
            df['combined_info'] = (
            "Title: " + df["Name"] + " Overview: " +df["sypnopsis"] + "Genres : " + df["Genres"]
            )

            df[['combined_info']].to_csv(self.processed_csv , index=False,encoding='utf-8')

            return self.processed_csv
            
        except FileNotFoundError as e:
            raise CustomException(f"File not found: {self.original_csv}", e)   