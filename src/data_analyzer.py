import pandas as pd


class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    # ---------------- SALES ANALYSIS ---------------- #

    def total_sales(self) -> float:
        return self.df["Sales"].sum()

    def total_profit(self) -> float:
        return self.df["Profit"].sum()

    def sales_by_category(self) -> pd.DataFrame:
        return (
            self.df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

    def sales_by_region(self) -> pd.DataFrame:
        return (
            self.df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

    # ---------------- PROFITABILITY ---------------- #

    def profit_by_category(self) -> pd.DataFrame:
        return (
            self.df.groupby("Category")["Profit"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

    def unprofitable_orders(self) -> pd.DataFrame:
        return self.df[self.df["Profit"] < 0]

    # ---------------- CUSTOMER ANALYSIS ---------------- #

    def top_customers_by_sales(self, top_n=10) -> pd.DataFrame:
        return (
            self.df.groupby("CustomerName")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
        )

    # ---------------- SHIPPING ANALYSIS ---------------- #

    def average_shipping_delay(self) -> float:
        return self.df["DaystoShipActual"].mean()

    def shipping_status_distribution(self) : 
        df = (
            self.df["ShipStatus"]
            .value_counts()
            .reset_index()
        )
        df.columns = ["ShipStatus", "Count"]
        return df

    # ---------------- FORECAST VS ACTUAL ---------------- #

    def forecast_accuracy(self) -> pd.DataFrame:
        df = self.df.copy()
        df["ForecastError"] = df["Sales"] - df["SalesForecast"]
        return df[["OrderID", "Sales", "SalesForecast", "ForecastError"]]

    # ---------------- KPI SUMMARY ---------------- #

    def kpi_summary(self) -> dict:
        return {
            "Total Sales": round(self.total_sales(), 2),
            "Total Profit": round(self.total_profit(), 2),
            "Avg Profit Ratio": round(self.df["ProfitRatio"].mean(), 2),
            "Avg Discount": round(self.df["Discount"].mean(), 2),
            "Avg Shipping Days": round(self.average_shipping_delay(), 2)
        }
