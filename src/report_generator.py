import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors


class ReportGenerator:
    def __init__(self, analyzer, charts_dir="./images", output_dir="./reports"):
        self.analyzer = analyzer
        self.charts_dir = charts_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        self.file_path = os.path.join(self.output_dir, "Business_Insight_Report.pdf")

        self.styles = getSampleStyleSheet()
        self.styles.add(
            ParagraphStyle(
                name="TitleStyle",
                fontSize=20,
                alignment=TA_CENTER,
                spaceAfter=20,
                textColor=colors.HexColor("#2C3E50"),
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="SectionTitle",
                fontSize=14,
                spaceBefore=16,
                spaceAfter=8,
                textColor=colors.HexColor("#1F77B4"),
                fontName="Helvetica-Bold",
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="NormalText",
                fontSize=10.5,
                leading=14,
                textColor=colors.black,
            )
        )

    # ---------------------- HELPERS ---------------------- #

    def _load_chart(self, filename, width=400, height=250):
        path = os.path.join(self.charts_dir, filename)
        if os.path.exists(path):
            return Image(path, width=width, height=height)
        return None

    # ---------------------- REPORT ---------------------- #

    def generate_report(self):
        doc = SimpleDocTemplate(
            self.file_path,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30,
        )

        story = []

        # ---------------- TITLE ---------------- #
        story.append(Paragraph("📊 Business Performance Report", self.styles["TitleStyle"]))
        story.append(
            Paragraph(
                "This report gives a simple, visual overview of how the business is performing. "
                "You can understand everything at a glance — no technical or business knowledge required.",
                self.styles["NormalText"],
            )
        )
        story.append(Spacer(1, 16))

        # ---------------- KPI SUMMARY ---------------- #
        kpis = self.analyzer.kpi_summary()

        story.append(Paragraph("📌 Key Business Numbers", self.styles["SectionTitle"]))

        kpi_table_data = [["Metric", "Value"]]
        for key, value in kpis.items():
            kpi_table_data.append([key, str(value)])

        kpi_table = Table(kpi_table_data, colWidths=[220, 150])
        kpi_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F77B4")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ]
            )
        )

        story.append(kpi_table)

        story.append(
            Paragraph(
                "<b>How to read this:</b> These numbers show overall sales, profit, discounts, "
                "and delivery performance. Higher sales and profit are good. Lower shipping days are better.",
                self.styles["NormalText"],
            )
        )

        # ---------------- SALES INSIGHTS ---------------- #
        story.append(Paragraph("💰 Sales Insights", self.styles["SectionTitle"]))
        story.append(
            Paragraph(
                "This section explains where the money is coming from and which areas perform best.",
                self.styles["NormalText"],
            )
        )

        chart = self._load_chart("sales_by_category.png")
        if chart:
            story.append(chart)

        chart = self._load_chart("sales_by_region.png")
        if chart:
            story.append(chart)

        story.append(
            Paragraph(
                "👉 Categories and regions with taller bars generate more revenue. "
                "These are the strongest parts of the business.",
                self.styles["NormalText"],
            )
        )

        # ---------------- PROFIT INSIGHTS ---------------- #
        story.append(Paragraph("📈 Profitability Insights", self.styles["SectionTitle"]))

        chart = self._load_chart("profit_by_category.png")
        if chart:
            story.append(chart)

        story.append(
            Paragraph(
                "Profit shows real earnings after costs. "
                "Some categories may sell well but earn less profit — those need attention.",
                self.styles["NormalText"],
            )
        )

        # ---------------- CUSTOMER INSIGHTS ---------------- #
        story.append(Paragraph("👥 Customer Insights", self.styles["SectionTitle"]))

        chart = self._load_chart("top_customers.png")
        if chart:
            story.append(chart)

        story.append(
            Paragraph(
                "Top customers contribute the most to revenue. "
                "Keeping these customers happy is very important.",
                self.styles["NormalText"],
            )
        )

        # ---------------- SHIPPING INSIGHTS ---------------- #
        story.append(Paragraph("🚚 Delivery & Shipping Insights", self.styles["SectionTitle"]))

        chart = self._load_chart("shipping_status_distribution.png")
        if chart:
            story.append(chart)

        chart = self._load_chart("average_shipping_days.png")
        if chart:
            story.append(chart)

        story.append(
            Paragraph(
                "Fast and reliable delivery improves customer satisfaction. "
                "Delays can reduce repeat purchases.",
                self.styles["NormalText"],
            )
        )

        # ---------------- FORECAST ---------------- #
        story.append(Paragraph("🔮 Sales Forecast Accuracy", self.styles["SectionTitle"]))

        chart = self._load_chart("forecast_vs_actual.png")
        if chart:
            story.append(chart)

        story.append(
            Paragraph(
                "This compares predicted sales vs actual sales. "
                "Closer lines mean better planning and forecasting.",
                self.styles["NormalText"],
            )
        )

        # ---------------- FINAL SUMMARY ---------------- #
        story.append(Paragraph("✅ One-Look Business Summary", self.styles["SectionTitle"]))
        story.append(
            Paragraph(
                """
                ✔ The business performance can be understood quickly using this report.<br/>
                ✔ Sales, profit, customers, and delivery are visually explained.<br/>
                ✔ This report helps in making better decisions without technical knowledge.
                """,
                self.styles["NormalText"],
            )
        )

        doc.build(story)

        print(f"📄 Report generated successfully: {self.file_path}")
