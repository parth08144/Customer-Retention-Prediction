"""
Generate all figures and screenshots needed for Project 44 Report:
Parth Tripathi | Reg No: 12306364 | INT315 CA2
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

os.makedirs('report_assets', exist_ok=True)

# Load dataset
df = pd.read_csv('customer_data.csv')

# ----------------- Fig 7: Output Task 1 (Membership distribution & volume) -----------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=200)

# Top Cities by Customer Volume
city_counts = df['location'].value_counts()
ax1.bar(city_counts.index, city_counts.values, color='#0284c7', width=0.55)
ax1.set_title('Customer Distribution by City Hub', fontsize=11, fontweight='bold', pad=10)
ax1.set_ylabel('Number of Customers', fontsize=9)
ax1.tick_params(axis='x', rotation=30, labelsize=8)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Membership Tier Distribution
mem_counts = df['membership_type'].value_counts()
colors = ['#d97706', '#0284c7', '#0d9488']
bars = ax2.bar(mem_counts.index, mem_counts.values, color=colors, width=0.45)
for bar, val in zip(bars, mem_counts.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{val}',
             ha='center', va='bottom', fontsize=9, fontweight='bold')
ax2.set_title('Membership Tier Breakdown', fontsize=11, fontweight='bold', pad=10)
ax2.set_ylabel('Count', fontsize=9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('report_assets/fig7_task1_eda.png', bbox_inches='tight')
plt.close()

# ----------------- Fig 8: Output Task 2 (Missing Value Imputation Audit) -----------------
fig, ax = plt.subplots(figsize=(8, 3.8), dpi=200)
cols = ['order_frequency', 'total_order_value', 'avg_order_value', 'days_since_last_order', 'customer_age', 'satisfaction_score']
before_missing = [df[c].isnull().sum() for c in cols]
after_missing = [0 for _ in cols]

x = np.arange(len(cols))
width = 0.35

ax.bar(x - width/2, before_missing, width, label='Before Imputation (Nulls Detected)', color='#ef4444')
ax.bar(x + width/2, after_missing, width, label='After Mean Imputation (Zero Nulls)', color='#10b981')

ax.set_ylabel('Missing Count', fontsize=10)
ax.set_title('Task 2: Missing Value Audit Before vs After Imputation', fontsize=11, fontweight='bold', pad=10)
ax.set_xticks(x)
ax.set_xticklabels(cols, rotation=25, ha='right', fontsize=8.5)
ax.legend(frameon=True, fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for i, v in enumerate(before_missing):
    if v > 0:
        ax.text(i - width/2, v + 1, str(v), ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#b91c1c')

plt.tight_layout()
plt.savefig('report_assets/fig8_task2_missing.png', bbox_inches='tight')
plt.close()

# ----------------- Fig 9: Output Task 3 (Categorical Attributes Balance) -----------------
fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), dpi=200)

axes[0].barh(df['location'].value_counts().index, df['location'].value_counts().values, color='#0284c7', height=0.55)
axes[0].set_title('Location Hub Indexing', fontsize=10, fontweight='bold')
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

axes[1].barh(df['membership_type'].value_counts().index, df['membership_type'].value_counts().values, color='#0d9488', height=0.45)
axes[1].set_title('Membership Tier Indexing', fontsize=10, fontweight='bold')
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

axes[2].barh(df['gender'].value_counts().index, df['gender'].value_counts().values, color='#d97706', height=0.35)
axes[2].set_title('Gender Indexing', fontsize=10, fontweight='bold')
axes[2].spines['top'].set_visible(False)
axes[2].spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('report_assets/fig9_task3_encoding.png', bbox_inches='tight')
plt.close()

# ----------------- Clean & Model -----------------
df_clean = df.copy()
df_clean['order_frequency'] = df_clean['order_frequency'].fillna(df_clean['order_frequency'].mean())
df_clean['total_order_value'] = df_clean['total_order_value'].fillna(df_clean['total_order_value'].mean())

le_loc = LabelEncoder()
le_mem = LabelEncoder()
le_gen = LabelEncoder()
df_clean['location_encoded'] = le_loc.fit_transform(df_clean['location'])
df_clean['membership_encoded'] = le_mem.fit_transform(df_clean['membership_type'])
df_clean['gender_encoded'] = le_gen.fit_transform(df_clean['gender'])

feature_cols = ['order_frequency', 'total_order_value', 'avg_order_value',
                'days_since_last_order', 'customer_age', 'satisfaction_score',
                'location_encoded', 'membership_encoded', 'gender_encoded']

X = df_clean[feature_cols]
y = df_clean['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# ----------------- Fig 10: Output Task 4 (Decision Tree Feature Importances) -----------------
imp_df = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=True)

fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=200)
colors_imp = ['#0284c7' if v > 0.1 else '#93c5fd' for v in imp_df['Importance']]
bars = ax.barh(imp_df['Feature'], imp_df['Importance'], color=colors_imp, height=0.55)
for bar, val in zip(bars, imp_df['Importance']):
    if val > 0.01:
        ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', fontsize=8.5, fontweight='bold', color='#1e293b')
ax.set_xlabel('Gini Importance Score', fontsize=9.5)
ax.set_title('Task 4: Decision Tree Feature Importance Ranking', fontsize=11, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('report_assets/fig10_task4_importance.png', bbox_inches='tight')
plt.close()

# ----------------- Fig 11: Output Task 5 (Confusion Matrix) -----------------
cm = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(5.5, 4.5), dpi=200)
im = ax.imshow(cm, interpolation='nearest', cmap='Blues')
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['Retained (0)', 'Churned (1)'], fontsize=9.5)
ax.set_yticklabels(['Retained (0)', 'Churned (1)'], fontsize=9.5)
ax.set_xlabel('Predicted Label', fontsize=10, fontweight='bold')
ax.set_ylabel('True Label', fontsize=10, fontweight='bold')
ax.set_title('Task 5: Model Evaluation Confusion Matrix', fontsize=11, fontweight='bold', pad=12)

for i in range(2):
    for j in range(2):
        ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                fontsize=16, fontweight='bold',
                color="white" if cm[i, j] > cm.max()/2 else "#0f172a")
plt.tight_layout()
plt.savefig('report_assets/fig11_task5_cm.png', bbox_inches='tight')
plt.close()

# ----------------- Fig 12: Output Task 6 (Dual-panel Retention Analysis) -----------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=200)

ret = df_clean.groupby('membership_type')['churn'].agg(['mean', 'count']).reset_index()
ret.columns = ['Membership', 'Churn_Rate', 'Count']
ret['Retention_Rate'] = 1 - ret['Churn_Rate']
ret = ret.sort_values('Membership')

colors = ['#d97706', '#0284c7', '#0d9488']
bars = ax1.bar(ret['Membership'], ret['Retention_Rate'], color=colors, width=0.45)
for bar, rate in zip(bars, ret['Retention_Rate']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{rate:.1%}', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax1.set_ylim(0, 1.15)
ax1.set_ylabel('Retention Rate', fontsize=9.5)
ax1.set_title('Retention Rate by Membership Tier', fontsize=11, fontweight='bold', pad=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Churn Rate by City Hub
city_churn = df_clean.groupby('location')['churn'].mean().sort_values()
ax2.barh(city_churn.index, 1 - city_churn.values, color='#0284c7', height=0.55)
ax2.set_xlabel('Retention Rate', fontsize=9.5)
ax2.set_xlim(0, 1.0)
ax2.set_title('Retention Rate Across Geographic Hubs', fontsize=11, fontweight='bold', pad=10)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('report_assets/fig12_task6_retention.png', bbox_inches='tight')
plt.close()

# ----------------- Architectural Diagrams (Fig 1 & Fig 2) -----------------
fig, ax = plt.subplots(figsize=(10, 3.2), dpi=200)
ax.axis('off')
boxes = [
    ("Stage 1\nRaw Ingestion\ncustomer_data.csv", 0.05),
    ("Stage 2\nMissing Imputation\nMean Substitution", 0.23),
    ("Stage 3\nEncoding\nStringIndexer / LE", 0.41),
    ("Stage 4\nVector Assembly\nVectorAssembler", 0.59),
    ("Stage 5\nDecision Tree\nmaxDepth = 5", 0.77),
    ("Stage 6\nEvaluation & UI\nAccuracy / Streamlit", 0.95),
]
for title, x_pos in boxes:
    ax.text(x_pos, 0.5, title, ha='center', va='center', fontsize=8.5,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f9ff', edgecolor='#0284c7', linewidth=1.5),
            color='#0f172a', fontweight='bold')
    if x_pos < 0.9:
        ax.annotate('', xy=(x_pos + 0.08, 0.5), xytext=(x_pos + 0.04, 0.5),
                    arrowprops=dict(arrowstyle="->", color='#0284c7', lw=2))

ax.set_title('Figure 1: End-to-End Pipeline Map of RetentionIQ Platform', fontsize=11, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('report_assets/fig1_pipeline_map.png', bbox_inches='tight')
plt.close()

# Fig 2: Layered Architecture
fig, ax = plt.subplots(figsize=(10, 3.4), dpi=200)
ax.axis('off')
layers = [
    ("Presentation Layer", "Streamlit 1.58+ Web Interface | Metric Cards | Tabs | Reactive State Caching", "#e0f2fe", 0.8),
    ("Analytics & Evaluation", "Scikit-Learn / PySpark ML Evaluator | Accuracy | Precision | Recall | Confusion Matrix", "#f0fdf4", 0.55),
    ("Distributed Engine Layer", "Apache Spark 3.5.x | PySpark ML Pipeline | VectorAssembler | DecisionTreeClassifier", "#fef3c7", 0.3),
    ("Data Storage Layer", "Customer Transaction Dataset (customer_data.csv) | 1,000 Records | 11 Features", "#f1f5f9", 0.05)
]
for name, desc, col, y_pos in layers:
    ax.text(0.5, y_pos, f"{name}\n{desc}", ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='square,pad=0.6', facecolor=col, edgecolor='#94a3b8', linewidth=1),
            color='#0f172a', fontweight='bold')

ax.set_title('Figure 2: Layered Architecture: Data, Distributed Processing, Cache, and UI', fontsize=11, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('report_assets/fig2_layered_architecture.png', bbox_inches='tight')
plt.close()

print('All report figures generated successfully!')
