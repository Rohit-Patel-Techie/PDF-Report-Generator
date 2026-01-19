import pandas as pd

class DataReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def load_data(self) -> pd.DataFrame:
        """Load CSV data"""
        self.df = pd.read_csv(self.file_path)
        return self.df

    def preprocess(self) -> pd.DataFrame:
        """Clean and preprocess dataset"""

        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Convert dates
        self.df["OrderDate"] = pd.to_datetime(self.df["OrderDate"])
        self.df["ShipDate"] = pd.to_datetime(self.df["ShipDate"])

        # Remove duplicates
        self.df.drop_duplicates(inplace=True)

        # Handle missing values
        self.df.fillna({
            "Discount": 0,
            "Profit": 0,
            "SalesForecast": self.df["Sales"].mean()
        }, inplace=True)

        # Create useful derived columns
        self.df["OrderMonth"] = self.df["OrderDate"].dt.month
        self.df["OrderYear"] = self.df["OrderDate"].dt.year

        return self.df

    def get_data(self) -> pd.DataFrame:
        """Return processed dataframe"""
        return self.df
