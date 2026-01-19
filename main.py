from src.data_reader import DataReader
from src.data_analyzer import DataAnalyzer
from src.data_visualization import DataVisualization
from src.report_generator import ReportGenerator

reader = DataReader('data/sales-data-sample.csv')
df = reader.load_data()
df = reader.preprocess()

analyzer = DataAnalyzer(df)

viz = DataVisualization(analyzer)

viz.generate_all_visuals()

report = ReportGenerator(analyzer)
report.generate_report()
