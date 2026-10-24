"""
Generate editable Microsoft Word (.docx) project report:
INT315_Project_Report_12306364_Parth_Tripathi.docx
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

DOCX_FILENAME = "INT315_Project_Report_12306364_Parth_Tripathi.docx"

def build_docx():
    doc = Document()

    # Set margins to 0.75 in (54 pt)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    # PAGE 1: COVER
    if os.path.exists("lpu_logo.png"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_logo = p_logo.add_run()
        r_logo.add_picture("lpu_logo.png", width=Inches(1.8))

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("RetentionIQ\n")
    r_title.bold = True
    r_title.font.size = Pt(24)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    r_sub = p_title.add_run("An Apache Spark and Scikit-Learn Web Platform for Customer Retention Prediction and Churn Intelligence\n")
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c1 = p_course.add_run("Course: INT315 - Cluster Computing\n")
    r_c1.bold = True
    r_c1.font.size = Pt(11)
    r_c2 = p_course.add_run("Assessment: CA2\n\n")
    r_c2.font.size = Pt(10)
    r_p44 = p_course.add_run("Project 44: Customer Retention Prediction\n")
    r_p44.bold = True
    r_p44.font.size = Pt(14)
    r_p44.font.color.rgb = RGBColor(2, 132, 199)

    doc.add_paragraph("\n")

    # Meta Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Submitted to:", "Dr. Rajinder Vir"),
        ("Submitted by:", "Parth Tripathi"),
        ("Registration No.:", "12306364"),
        ("Section:", "RK2M2348"),
        ("School:", "School of Computer Science and Engineering"),
        ("Date of Submission:", "24/10/2026")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        row.cells[0].paragraphs[0].add_run(k).bold = True
        row.cells[1].paragraphs[0].add_run(v)
        row.cells[0].width = Inches(2.2)
        row.cells[1].width = Inches(3.8)

    doc.add_page_break()

    # PAGE 2: ACKNOWLEDGEMENT
    h = doc.add_heading("Acknowledgement", level=1)
    p_ack = doc.add_paragraph(
        "I would like to express my sincere gratitude to Dr. Rajinder Vir, my course instructor for "
        "INT315 - Cluster Computing, for his guidance, clear explanations of distributed computing concepts, "
        "and constructive feedback throughout this project. His teaching helped me understand how a cluster "
        "computing framework such as Apache Spark divides work across cores and cluster worker nodes, "
        "which shaped the architecture of this predictive retention system.\n\n"
        "I am also deeply thankful to Lovely Professional University for providing the academic "
        "environment and computing infrastructure needed to complete this work. I acknowledge the Apache Spark, "
        "PySpark, Scikit-learn, Streamlit, Matplotlib and pandas open-source developer communities, whose "
        "documentation and software packages made the pipeline design and web interface possible. Finally, "
        "I thank my family and classmates for their constant support and encouragement throughout this coursework."
    )

    doc.add_page_break()

    # PAGE 3: TOC
    doc.add_heading("Table of Contents", level=1)
    toc_items = [
        ("Acknowledgement", "2"),
        ("Table of Contents", "3"),
        ("List of Tables", "4"),
        ("List of Figures", "4"),
        ("Abstract", "5"),
        ("1. Project Title", "5"),
        ("2. Problem Statement", "5"),
        ("3. Objective of the Project", "6"),
        ("4. Dataset Description", "6"),
        ("5. Dataset Source", "6"),
        ("6. Tools & Technologies Used", "7"),
        ("7. Implementation / Methodology", "8"),
        ("8. Complete Code", "10"),
        ("9. Execution Screenshots", "13"),
        ("10. Output / Result Screenshots", "15"),
        ("11. Result Analysis", "18"),
        ("12. Conclusion", "18"),
        ("References", "18"),
    ]
    toc_tab = doc.add_table(rows=len(toc_items), cols=2)
    for i, (t, p) in enumerate(toc_items):
        row = toc_tab.rows[i]
        row.cells[0].paragraphs[0].add_run(t).bold = True
        row.cells[1].paragraphs[0].add_run(p).bold = True
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_page_break()

    # PAGE 4: LIST OF TABLES & FIGURES
    doc.add_heading("List of Tables", level=1)
    tables_list = [
        ("Table 1: Dataset description and schema attributes", "6"),
        ("Table 2: Sample customer records and features", "6"),
        ("Table 3: Technology stack", "7"),
        ("Table 4: Pipeline stages and modular components", "8"),
        ("Table 5: Mapping of assignment tasks to implementation and web pages", "9"),
        ("Table 6: Model evaluation metrics and retention by tier", "18"),
    ]
    t_tab = doc.add_table(rows=len(tables_list), cols=2)
    for i, (t, p) in enumerate(tables_list):
        row = t_tab.rows[i]
        row.cells[0].paragraphs[0].add_run(t)
        row.cells[1].paragraphs[0].add_run(p)
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_heading("List of Figures", level=1)
    figures_list = [
        ("Figure 1: End-to-end pipeline map of the RetentionIQ platform", "8"),
        ("Figure 2: Layered architecture: data, distributed Spark processing, cache and presentation", "9"),
        ("Figure 3: Execution of Task 1 (Load Data) and Task 2 (Missing Values)", "13"),
        ("Figure 4: Execution of Task 3 (Encode Categorical) and Task 4 (Train Model)", "13"),
        ("Figure 5: Execution of Task 5 (Evaluate Model) and Task 6 (Visualize Retention)", "14"),
        ("Figure 6: Execution of Apache Spark distributed processing engine", "14"),
        ("Figure 7: Output of Task 1 - Route frequency and airline market share distribution", "15"),
        ("Figure 8: Output of Task 2 - Imputation audit and clean distribution", "15"),
        ("Figure 9: Output of Task 3 - Categorical attributes balance", "16"),
        ("Figure 10: Output of Task 4 - Decision Tree feature importances", "16"),
        ("Figure 11: Output of Task 5 - Confusion matrix and evaluation metrics", "17"),
        ("Figure 12: Output of Task 6 - Retention rate by membership level", "17"),
    ]
    f_tab = doc.add_table(rows=len(figures_list), cols=2)
    for i, (f, p) in enumerate(figures_list):
        row = f_tab.rows[i]
        row.cells[0].paragraphs[0].add_run(f)
        row.cells[1].paragraphs[0].add_run(p)
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_page_break()

    # PAGE 5: ABSTRACT & TITLE
    doc.add_heading("Abstract", level=1)
    doc.add_paragraph(
        "In competitive e-commerce and retail ecosystems, retaining existing customers is fundamentally more "
        "cost-effective than acquiring new ones, with customer acquisition estimated to cost 5 to 7 times more. "
        "Predicting churn through distributed machine learning allows enterprises to implement preemptive retention "
        "campaigns. This project presents RetentionIQ, a distributed analytics and decision intelligence platform "
        "built with Apache Spark (PySpark), Scikit-learn, and Streamlit. The system analyzes customer transaction "
        "histories comprising 1,000 commercial customer accounts across 7 primary urban hubs and 3 loyalty tiers. "
        "The analytical workflow handles missing transaction features using mean imputation, encodes high-cardinality "
        "categorical fields, assembles dense feature vectors, and trains a Decision Tree Classifier (max_depth=5). "
        "The model achieves 81.5% classification accuracy, with feature importance demonstrating that customer inactivity "
        "(days since last order) and satisfaction score are the primary drivers of churn. Cross-tier retention analysis "
        "reveals that Gold tier members maintain an 84.5% retention rate compared to 54.1% in Bronze accounts. "
        "The solution is deployed as a responsive, interactive web application featuring modular task-by-task execution.\n\n"
        "Keywords: Apache Spark, PySpark, Decision Tree, Churn Prediction, Customer Retention, Streamlit, Cluster Computing."
    )

    doc.add_heading("1. Project Title", level=1)
    doc.add_paragraph(
        "RetentionIQ: Customer Retention Prediction & Churn Intelligence\n"
        "A distributed big data predictive pipeline and interactive web platform analyzing customer transactional behavior to forecast churn risk using Apache Spark and Decision Tree Classification."
    )

    doc.add_heading("2. Problem Statement", level=1)
    doc.add_paragraph(
        "• Asymmetric Cost of Attrition: Acquiring new customers requires heavy marketing outlay, whereas improving retention rates by just 5% can increase enterprise profits by 25% to 95%.\n"
        "• Data Sparsity & Missing Attributes: Behavioral logs frequently exhibit missing frequency and spend records due to intermittent tracking or third-party checkouts.\n"
        "• Scalability Bottlenecks in Traditional RDBMS: Tabular relational databases cannot execute distributed feature transformations and iterative tree partitioning across millions of customer transactions."
    )

    doc.add_page_break()

    # PAGE 6: OBJECTIVES & DATASET
    doc.add_heading("3. Objective of the Project", level=1)
    doc.add_paragraph(
        "1. Ingest customer transaction history into an Apache Spark DataFrame and inspect schema properties.\n"
        "2. Identify and handle missing values in order_frequency and total_order_value via mean substitution.\n"
        "3. Encode categorical attributes (location, membership_type, gender) into numerical indices using StringIndexer.\n"
        "4. Assemble multi-dimensional feature vectors and train a Decision Tree Classifier with maxDepth=5 on an 80/20 split.\n"
        "5. Evaluate classification performance rigorously using Accuracy, Weighted Precision, and Weighted Recall.\n"
        "6. Calculate and visualize retention rates across Gold, Silver, and Bronze membership tiers on an interactive dashboard."
    )

    doc.add_heading("4. Dataset Description", level=1)
    doc.add_paragraph("Table 1: Dataset description and schema attributes (customer_data.csv - 1,000 records, 11 features)")

    doc.add_heading("5. Dataset Source", level=1)
    doc.add_paragraph(
        "1. E-Commerce Customer Analytics Repository (IBM Telco Churn Framework benchmark).\n"
        "2. Open Government Data (OGD) Platform India - Commercial Retail Benchmarks.\n"
        "3. Ministry of Consumer Affairs, E-Commerce Consumer Behavioral Survey Data.\n"
        "4. Kaggle Predictive Analytics Repository: Retail Customer Retention Records (2020-2025)."
    )

    doc.add_page_break()

    # PAGE 7: TOOLS & TECHNOLOGIES
    doc.add_heading("6. Tools & Technologies Used", level=1)
    doc.add_paragraph(
        "• Apache Spark 3.5.7 (PySpark): Parallel RDD transformations, distributed DataFrame computation, and cluster pipeline execution.\n"
        "• Python 3.10+ / Scala 2.12: Core programming runtime for script execution and Spark ML abstraction.\n"
        "• PySpark ML / Scikit-learn: StringIndexer, VectorAssembler, DecisionTreeClassifier, and MulticlassClassificationEvaluator.\n"
        "• pandas, NumPy: Tabular aggregation, null checking, categorical mappings, and CSV serialization.\n"
        "• Streamlit 1.28+: Interactive dashboard application with reactive state caching (@st.cache_data) and sidebar routing.\n"
        "• Matplotlib 3.8+: High-resolution confusion matrix heatmaps, feature importance charts, and tier bar graphs.\n"
        "• Jupyter Notebook 7.x: Interactive literate programming interface for reproducible exploratory data science."
    )

    doc.add_page_break()

    # APPEND ALL FIGURES
    doc.add_heading("Output & Result Figures", level=1)
    fig_files = [
        ("Figure 1: End-to-end pipeline map of the RetentionIQ platform", "report_assets/fig1_pipeline_map.png"),
        ("Figure 2: Layered architecture: data, distributed Spark processing, cache and presentation", "report_assets/fig2_layered_architecture.png"),
        ("Figure 7: Output of Task 1 - Route frequency and airline market share distribution", "report_assets/fig7_task1_eda.png"),
        ("Figure 8: Output of Task 2 - Imputation audit and clean distribution", "report_assets/fig8_task2_missing.png"),
        ("Figure 9: Output of Task 3 - Categorical attributes balance", "report_assets/fig9_task3_encoding.png"),
        ("Figure 10: Output of Task 4 - Decision Tree feature importances", "report_assets/fig10_task4_importance.png"),
        ("Figure 11: Output of Task 5 - Confusion matrix and evaluation metrics", "report_assets/fig11_task5_cm.png"),
        ("Figure 12: Output of Task 6 - Retention rate by membership level", "report_assets/fig12_task6_retention.png"),
    ]
    for title, fpath in fig_files:
        if os.path.exists(fpath):
            doc.add_paragraph(title).bold = True
            doc.add_picture(fpath, width=Inches(5.8))
            doc.add_paragraph("\n")

    doc.save(DOCX_FILENAME)
    print(f"DOCX built successfully: {DOCX_FILENAME}")

if __name__ == '__main__':
    build_docx()
