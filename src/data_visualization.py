import os
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap


class DataVisualization:
    def __init__(self, analyzer, output_dir="./images"):
        self.analyzer = analyzer
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        plt.rcParams.update({
            "font.size": 10,
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "axes.edgecolor": "#DDDDDD",
            "axes.linewidth": 0.8,
            "grid.color": "#EEEEEE",
            "grid.linestyle": "--",
            "grid.linewidth": 0.6,
        })

    # -------------------- HELPERS -------------------- #

    def _save_plot(self, filename):
        plt.tight_layout()
        plt.savefig(
            os.path.join(self.output_dir, filename),
            dpi=300,
            bbox_inches="tight"
        )
        plt.close()

    def _clean_axes(self):
        ax = plt.gca()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.7)

    def _get_colors(self, n):
        cmap = get_cmap("tab10")
        return [cmap(i) for i in range(n)]

    # -------------------- SALES -------------------- #

    def sales_by_category(self):
        df = self.analyzer.sales_by_category()
        colors = self._get_colors(len(df))

        plt.figure(figsize=(6.5, 4))
        plt.bar(df["Category"], df["Sales"], color=colors)
        plt.title("Sales by Category")
        plt.ylabel("Total Sales")
        self._clean_axes()

        self._save_plot("sales_by_category.png")

    def sales_by_region(self):
        df = self.analyzer.sales_by_region()
        colors = self._get_colors(len(df))

        plt.figure(figsize=(6.5, 4))
        plt.bar(df["Region"], df["Sales"], color=colors)
        plt.title("Sales by Region")
        plt.ylabel("Total Sales")
        self._clean_axes()

        self._save_plot("sales_by_region.png")

    # -------------------- PROFIT -------------------- #

    def profit_by_category(self):
        df = self.analyzer.profit_by_category()
        colors = self._get_colors(len(df))

        plt.figure(figsize=(6.5, 4))
        plt.bar(df["Category"], df["Profit"], color=colors)
        plt.title("Profit by Category")
        plt.ylabel("Total Profit")
        self._clean_axes()

        self._save_plot("profit_by_category.png")

    # -------------------- CUSTOMER -------------------- #

    def top_customers(self, top_n=10):
        df = self.analyzer.top_customers_by_sales(top_n)
        colors = self._get_colors(len(df))

        plt.figure(figsize=(7, 4.5))
        plt.barh(df["CustomerName"], df["Sales"], color=colors)
        plt.title(f"Top {top_n} Customers by Sales")
        plt.xlabel("Sales")
        plt.gca().invert_yaxis()
        self._clean_axes()

        self._save_plot("top_customers.png")

    # -------------------- SHIPPING -------------------- #

    def shipping_status_distribution(self):
        df = self.analyzer.shipping_status_distribution()
        colors = self._get_colors(len(df))

        plt.figure(figsize=(5, 5))
        plt.pie(
            df["Count"],
            labels=df["ShipStatus"],
            autopct="%1.0f%%",
            startangle=90,
            colors=colors,
            wedgeprops={"edgecolor": "white"}
        )
        plt.title("Shipping Status Distribution")

        self._save_plot("shipping_status_distribution.png")

    def average_shipping_days(self):
        avg_days = self.analyzer.average_shipping_delay()

        plt.figure(figsize=(5, 3.5))
        plt.bar(
            ["Average Shipping Days"],
            [avg_days],
            color=self._get_colors(1)
        )
        plt.ylabel("Days")
        plt.title("Average Shipping Duration")
        self._clean_axes()

        self._save_plot("average_shipping_days.png")

    # -------------------- FORECAST VS ACTUAL -------------------- #

    def forecast_vs_actual(self):
        df = self.analyzer.forecast_accuracy().head(40)

        plt.figure(figsize=(7, 4))
        plt.plot(
            df["Sales"].values,
            label="Actual Sales",
            color="#1F77B4",
            linewidth=2
        )
        plt.plot(
            df["SalesForecast"].values,
            label="Forecasted Sales",
            color="#FF7F0E",
            linewidth=2,
            linestyle="--"
        )

        plt.title("Sales Forecast vs Actual")
        plt.xlabel("Orders")
        plt.ylabel("Sales")
        plt.legend(frameon=False)
        self._clean_axes()

        self._save_plot("forecast_vs_actual.png")

    # -------------------- KPI SUMMARY -------------------- #

    def kpi_overview(self):
        kpis = self.analyzer.kpi_summary()

        labels = list(kpis.keys())
        values = list(kpis.values())

        colors = self._get_colors(len(values))

        plt.figure(figsize=(7, 4))
        bars = plt.bar(labels, values, color=colors)

        plt.title("Business KPI Overview")
        plt.xticks(rotation=20)
        self._clean_axes()

        for bar, value in zip(bars, values):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold"
            )
        self._save_plot("kpi_overview.png")

    # -------------------- MASTER -------------------- #

    def generate_all_visuals(self):
        self.sales_by_category()
        self.sales_by_region()
        self.profit_by_category()
        self.top_customers()
        self.shipping_status_distribution()
        self.average_shipping_days()
        self.forecast_vs_actual()
        self.kpi_overview()

        print("✅ Multi-color professional charts generated successfully.")
