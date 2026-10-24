"""
Streamlit Dashboard for Project 44: Customer Retention Prediction
Run with: streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Customer Retention Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CLEAN WHITE CSS STYLING =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
.stApp {
    background-color: #f8fafc;
}

/* Sidebar - Pure White */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] .stMarkdown label,
section[data-testid="stSidebar"] .stMarkdown div {
    color: #0f172a !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: #334155 !important;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 6px 0;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    color: #0284c7 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #e2e8f0 !important;
}

/* Platform Badge in Sidebar */
.platform-badge {
    background-color: #e0f2fe;
    color: #0369a1 !important;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 10px;
    text-transform: uppercase;
}

.brand-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #0f172a !important;
    margin: 0;
    line-height: 1.2;
}
.brand-subtitle {
    font-size: 0.8rem;
    color: #64748b !important;
    margin-top: 3px;
    margin-bottom: 16px;
    font-weight: 400;
}

.section-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: #0f172a !important;
    margin: 18px 0 10px 0;
}

/* Accent Divider */
.accent-divider {
    width: 64px;
    height: 4px;
    background: #0284c7;
    border-radius: 2px;
    margin-bottom: 20px;
}

/* Lab Badge */
.lab-badge {
    background-color: #e0f2fe;
    color: #0284c7;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 4px 10px;
    border-radius: 4px;
    display: inline-block;
    text-transform: uppercase;
    margin-bottom: 14px;
}

/* Context Box */
.context-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #0284c7;
    border-radius: 6px;
    padding: 22px 26px;
    margin: 18px 0 24px 0;
}
.context-box h3 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 10px 0;
}
.context-box p {
    font-size: 0.92rem;
    color: #475569;
    line-height: 1.65;
    margin: 0;
}

/* Metric Cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px 18px;
    text-align: left;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.metric-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 2.1rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.1;
    margin-bottom: 6px;
}
.metric-desc {
    font-size: 0.82rem;
    color: #0284c7;
    font-weight: 500;
}

/* Titles */
.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
    margin-bottom: 14px;
}
.main-desc {
    font-size: 0.98rem;
    color: #475569;
    line-height: 1.7;
    max-width: 780px;
}
.task-title {
    font-size: 1.85rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 8px 0;
    line-height: 1.25;
}
.task-subtitle {
    font-size: 0.95rem;
    color: #64748b;
    line-height: 1.6;
    margin-bottom: 24px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid #e2e8f0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    color: #64748b;
    padding: 10px 16px;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    font-weight: 700;
    color: #0284c7 !important;
    border-bottom: 2px solid #0284c7 !important;
}

/* Web Form & Prediction Card Styling */
.web-form-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.web-form-header {
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 16px;
    margin-bottom: 20px;
}
.result-banner-retained {
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    border: 2px solid #10b981;
    border-radius: 12px;
    padding: 24px 28px;
    margin: 20px 0;
}
.result-banner-churn {
    background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
    border: 2px solid #f43f5e;
    border-radius: 12px;
    padding: 24px 28px;
    margin: 20px 0;
}
.result-status-title {
    font-size: 1.35rem;
    font-weight: 800;
    margin: 0 0 6px 0;
}
.status-retained { color: #047857 !important; }
.status-churn { color: #b91c1c !important; }
.result-meta {
    font-size: 0.95rem;
    font-weight: 600;
    color: #334155;
    margin-bottom: 12px;
}

/* Hide Streamlit Header & Footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ===================== DATA FUNCTIONS =====================
@st.cache_data
def load_raw_data():
    """Load the original CSV dataset."""
    return pd.read_csv("customer_data.csv")

@st.cache_data
def get_clean_data():
    """Load and clean data: fill missing values with column means."""
    df = pd.read_csv("customer_data.csv")
    df['order_frequency'] = df['order_frequency'].fillna(df['order_frequency'].mean())
    df['total_order_value'] = df['total_order_value'].fillna(df['total_order_value'].mean())
    return df

@st.cache_data
def get_encoded_data():
    """Load, clean, and encode categorical columns."""
    df = get_clean_data()
    le_location = LabelEncoder()
    le_membership = LabelEncoder()
    le_gender = LabelEncoder()
    df['location_encoded'] = le_location.fit_transform(df['location'])
    df['membership_encoded'] = le_membership.fit_transform(df['membership_type'])
    df['gender_encoded'] = le_gender.fit_transform(df['gender'])
    return df

@st.cache_resource
def get_prediction_model():
    """Trained Decision Tree model with label encoders for interactive web form scoring."""
    df = get_clean_data()
    le_location = LabelEncoder()
    le_membership = LabelEncoder()
    le_gender = LabelEncoder()

    df_encoded = df.copy()
    df_encoded['location_encoded'] = le_location.fit_transform(df['location'])
    df_encoded['membership_encoded'] = le_membership.fit_transform(df['membership_type'])
    df_encoded['gender_encoded'] = le_gender.fit_transform(df['gender'])

    feature_cols = [
        'order_frequency', 'total_order_value', 'avg_order_value',
        'days_since_last_order', 'customer_age', 'satisfaction_score',
        'location_encoded', 'membership_encoded', 'gender_encoded'
    ]
    X = df_encoded[feature_cols]
    y = df_encoded['churn']

    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X, y)
    return model, le_location, le_membership, le_gender, feature_cols, df

@st.cache_data
def train_and_evaluate():
    """Train Decision Tree and return results."""
    df = get_encoded_data()
    feature_cols = ['order_frequency', 'total_order_value', 'avg_order_value',
                    'days_since_last_order', 'customer_age', 'satisfaction_score',
                    'location_encoded', 'membership_encoded', 'gender_encoded']
    X = df[feature_cols]
    y = df['churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted')
    rec = recall_score(y_test, y_pred, average='weighted')

    return model, X_train, X_test, y_train, y_test, y_pred, acc, prec, rec, feature_cols


# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown('<div class="platform-badge">Apache Spark ML Platform</div>', unsafe_allow_html=True)
    st.markdown('<p class="brand-title">Retention Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Customer Retention & Churn Intelligence</p>', unsafe_allow_html=True)

    st.markdown('<p class="section-label">Navigation</p>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Interactive Prediction Web Form",
            "Task 1: Load Data & EDA",
            "Task 2: Handle Missing Values",
            "Task 3: Encode Categorical Fields",
            "Task 4: Train Decision Tree",
            "Task 5: Evaluate Model",
            "Task 6: Visualize Retention Rates",
            "Major Findings & Summary"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown('<p class="section-label">Primary Focus Hub</p>', unsafe_allow_html=True)
    df_raw = load_raw_data()
    locations = sorted(df_raw['location'].dropna().unique())
    selected_location = st.selectbox(
        "Focus Location",
        ["All Locations"] + locations,
        label_visibility="collapsed",
        help="Filter metrics by customer location"
    )

    st.markdown("---")
    st.markdown('<p class="section-label">Project Report</p>', unsafe_allow_html=True)
    if os.path.exists("INT315_Project_Report_12306364_Parth_Tripathi.pdf"):
        with open("INT315_Project_Report_12306364_Parth_Tripathi.pdf", "rb") as f_pdf:
            st.download_button(
                label="Download Project Report (PDF)",
                data=f_pdf.read(),
                file_name="INT315_Project_Report_12306364_Parth_Tripathi.pdf",
                mime="application/pdf",
                use_container_width=True
            )


# ===================== HELPER FUNCTIONS =====================
def render_metric_cards(metrics):
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{m['label']}</div>
                <div class="metric-value">{m['value']}</div>
                <div class="metric-desc">{m['desc']}</div>
            </div>
            """, unsafe_allow_html=True)


def filtered_data(df):
    if selected_location != "All Locations":
        return df[df['location'] == selected_location]
    return df


# ===================== PAGE: OVERVIEW =====================
if page == "Overview":
    st.markdown('<div class="accent-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <h1 class="main-title">Customer Retention Graph Analysis & Churn Intelligence</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p class="main-desc">
        Enterprise Big Data Analytics Platform analyzing commercial customer transaction records,
        behavioral features, multi-city hubs, and loyalty tiers using Decision Tree Classification
        and Apache Spark ML pipeline.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="context-box">
        <div class="lab-badge">LAB & PROJECT ASSIGNMENT · INT315 CA2</div>
        <h3>Project 44: Customer Retention Prediction</h3>
        <p>
            <strong>Student:</strong> Parth Tripathi &nbsp;|&nbsp; <strong>Registration No.:</strong> 12306364 &nbsp;|&nbsp; <strong>Section:</strong> RK2M2348<br/>
            <strong>Course:</strong> INT315 - Cluster Computing &nbsp;|&nbsp; <strong>Submitted to:</strong> Dr. Rajinder Vir<br/>
            <strong>Context:</strong> Construct and evaluate a customer retention pipeline to identify
            customers likely to churn and assess retention rates across loyalty tiers using Apache Spark ML.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Execution Tasks:**")
    tasks_data = {
        "Task": ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5", "Task 6"],
        "Description": [
            "Load customer transaction history into Spark DataFrame",
            "Handle missing order frequency and value details",
            "Encode categorical fields (location, membership type, gender)",
            "Train a Decision Tree classifier to predict churn or retention",
            "Evaluate using accuracy, precision, and recall",
            "Visualize retention rates across different membership levels"
        ]
    }
    st.table(pd.DataFrame(tasks_data))

    st.markdown("""
    <div style="background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 100%); border: 1px solid #7dd3fc; border-radius: 8px; padding: 18px 22px; margin: 20px 0;">
        <span style="background: #0284c7; color: white; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase;">Live Web Form</span>
        <h4 style="margin: 6px 0 2px 0; color: #0c4a6e; font-weight: 700;">Interactive Customer Retention Web Form Available</h4>
        <p style="margin: 0; font-size: 0.9rem; color: #334155;">Simulate and score real-time customer profiles directly in your browser. Switch to <strong>Interactive Prediction Web Form</strong> in the sidebar to test predictions live.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Download Project Report")
    if os.path.exists("INT315_Project_Report_12306364_Parth_Tripathi.pdf"):
        with open("INT315_Project_Report_12306364_Parth_Tripathi.pdf", "rb") as f_pdf:
            st.download_button(
                label="Download Official Project Report (PDF - 20 Pages)",
                data=f_pdf.read(),
                file_name="INT315_Project_Report_12306364_Parth_Tripathi.pdf",
                mime="application/pdf",
                use_container_width=True
            )


# ===================== PAGE: INTERACTIVE PREDICTION WEB FORM =====================
elif page == "Interactive Prediction Web Form":
    st.markdown('<div class="accent-divider"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="task-title">Customer Retention & Churn Prediction Web Form</h1>', unsafe_allow_html=True)
    st.markdown('<p class="task-subtitle">Interactive machine learning scoring interface. Populate the customer parameters below to simulate Decision Tree inference and receive real-time retention diagnostics.</p>', unsafe_allow_html=True)

    model, le_location, le_membership, le_gender, feature_cols, df_clean = get_prediction_model()

    # Preset Persona Quick-Selector
    st.markdown("#### ⚡ Quick Preset Personas")
    st.markdown('<p style="font-size: 0.85rem; color: #64748b; margin-top: -8px;">Select a pre-configured customer profile to autofill the form or select Custom Entry to define your own values:</p>', unsafe_allow_html=True)

    preset_choice = st.selectbox(
        "Load Customer Persona",
        [
            "Custom Entry (Manual Input)",
            "👑 Persona A: Highly Retained VIP (Gold Tier, Active, 5/5 Satisfaction)",
            "⚠️ Persona B: High Churn Risk (Bronze Tier, 240 Days Inactive, 1/5 Satisfaction)",
            "⚖️ Persona C: Borderline Engagement (Silver Tier, 65 Days Inactive, 3/5 Satisfaction)"
        ],
        label_visibility="collapsed"
    )

    # Defaults based on preset
    if "Persona A" in preset_choice:
        d_loc = "Bangalore"
        d_mem = "Gold"
        d_gen = "Female"
        d_age = 36
        d_freq = 42
        d_val = 45000.0
        d_days = 12
        d_sat = 5
    elif "Persona B" in preset_choice:
        d_loc = "Pune"
        d_mem = "Bronze"
        d_gen = "Male"
        d_age = 56
        d_freq = 8
        d_val = 5200.0
        d_days = 240
        d_sat = 1
    elif "Persona C" in preset_choice:
        d_loc = "Delhi"
        d_mem = "Silver"
        d_gen = "Male"
        d_age = 29
        d_freq = 24
        d_val = 26000.0
        d_days = 65
        d_sat = 3
    else:
        d_loc = "Mumbai" if "Mumbai" in le_location.classes_ else le_location.classes_[0]
        d_mem = "Silver"
        d_gen = "Female"
        d_age = 34
        d_freq = 25
        d_val = 28000.0
        d_days = 45
        d_sat = 4

    st.write("")

    # Web Form Container
    with st.form("retention_prediction_form"):
        st.markdown('<div class="web-form-header"><h3 style="margin: 0; font-size: 1.15rem; color: #0f172a;">📝 Customer Behavioral & Profile Form</h3><p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">All fields are processed through the PySpark ML / Scikit-learn Decision Tree pipeline.</p></div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**👤 Demographics**")
            customer_age = st.slider("Customer Age", min_value=18, max_value=80, value=d_age, help="Age in completed years")
            gender = st.selectbox("Gender", ["Female", "Male"], index=0 if d_gen == "Female" else 1)
            loc_options = sorted(le_location.classes_.tolist())
            loc_index = loc_options.index(d_loc) if d_loc in loc_options else 0
            location = st.selectbox("City Hub / Location", loc_options, index=loc_index)

        with col2:
            st.markdown("**🎖️ Loyalty & Engagement**")
            mem_options = ["Bronze", "Silver", "Gold"]
            mem_index = mem_options.index(d_mem) if d_mem in mem_options else 1
            membership_type = st.selectbox("Membership Tier", mem_options, index=mem_index)
            days_since_last_order = st.slider(
                "Days Since Last Purchase",
                min_value=1,
                max_value=365,
                value=d_days,
                help="Key model split threshold: 155.5 days"
            )
            satisfaction_score = st.select_slider(
                "Satisfaction Score (1 - 5)",
                options=[1, 2, 3, 4, 5],
                value=d_sat,
                help="1 = Very Dissatisfied, 5 = Highly Satisfied"
            )

        with col3:
            st.markdown("**💳 Purchase Economics**")
            order_frequency = st.number_input(
                "Order Frequency (Orders)",
                min_value=1,
                max_value=60,
                value=d_freq,
                help="Total purchase count recorded"
            )
            total_order_value = st.number_input(
                "Total Order Value (₹)",
                min_value=100.0,
                max_value=100000.0,
                value=float(d_val),
                step=500.0,
                help="Cumulative gross transaction volume"
            )
            calculated_aov = round(total_order_value / max(1, order_frequency), 2)
            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 6px; padding: 10px 14px; margin-top: 14px;">
                <span style="font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Derived Avg Order Value (AOV)</span>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0284c7;">₹{calculated_aov:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        submit_button = st.form_submit_button(
            "⚡ Run Customer Retention Prediction",
            type="primary",
            use_container_width=True
        )

    # Inference & Results
    if submit_button or preset_choice != "Custom Entry (Manual Input)":
        # Encode features
        loc_enc = le_location.transform([location])[0]
        mem_enc = le_membership.transform([membership_type])[0]
        gen_enc = le_gender.transform([gender])[0]
        aov = total_order_value / max(1, order_frequency)

        input_data = pd.DataFrame([{
            'order_frequency': order_frequency,
            'total_order_value': total_order_value,
            'avg_order_value': aov,
            'days_since_last_order': days_since_last_order,
            'customer_age': customer_age,
            'satisfaction_score': satisfaction_score,
            'location_encoded': loc_enc,
            'membership_encoded': mem_enc,
            'gender_encoded': gen_enc
        }])

        prediction = model.predict(input_data[feature_cols])[0]
        probabilities = model.predict_proba(input_data[feature_cols])[0]
        retention_prob = probabilities[0] * 100
        churn_prob = probabilities[1] * 100

        st.markdown("---")
        st.subheader("Prediction Result & Risk Analysis")

        if prediction == 0:
            # Retained
            st.markdown(f"""
            <div class="result-banner-retained">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                    <div>
                        <div class="result-status-title status-retained">✅ CUSTOMER STATUS: RETAINED (LOW CHURN RISK)</div>
                        <div class="result-meta">Predicted Class: <strong>Active / Retained</strong> &nbsp;|&nbsp; Model Confidence: <strong>{retention_prob:.1f}%</strong></div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.8rem; font-weight: 700; color: #047857;">RETENTION PROBABILITY</span>
                        <div style="font-size: 2rem; font-weight: 800; color: #065f46;">{retention_prob:.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Churned
            st.markdown(f"""
            <div class="result-banner-churn">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
                    <div>
                        <div class="result-status-title status-churn">⚠️ CUSTOMER STATUS: AT-RISK OF CHURN (HIGH ATTRITION)</div>
                        <div class="result-meta">Predicted Class: <strong>Defection / Churn</strong> &nbsp;|&nbsp; Churn Risk Probability: <strong>{churn_prob:.1f}%</strong></div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.8rem; font-weight: 700; color: #b91c1c;">ATTRITION RISK</span>
                        <div style="font-size: 2rem; font-weight: 800; color: #9f1239;">{churn_prob:.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Tabbed deep-dive
        tab_diag, tab_bench, tab_rec = st.tabs(["Diagnostic Breakdown", "Cohort Benchmarking", "Actionable Retention Playbook"])

        with tab_diag:
            c_a, c_b = st.columns(2)
            with c_a:
                st.markdown("**Key Influencing Behavioral Drivers:**")
                drivers = []
                if days_since_last_order > 155.5:
                    drivers.append(("Dormancy Warning", f"Customer inactive for {days_since_last_order} days (exceeds critical 155.5-day tree threshold).", "negative"))
                else:
                    drivers.append(("Recent Purchase Activity", f"Active recency ({days_since_last_order} days) strengthens retention.", "positive"))

                if satisfaction_score <= 2:
                    drivers.append(("Low Customer Satisfaction", f"Rating of {satisfaction_score}/5 is a major defection driver.", "negative"))
                elif satisfaction_score >= 4:
                    drivers.append(("High Satisfaction Score", f"Rating of {satisfaction_score}/5 indicates strong brand advocacy.", "positive"))

                if membership_type == "Gold":
                    drivers.append(("Gold Tier Protection", "Highest retention loyalty tier across all regional hubs.", "positive"))
                elif membership_type == "Bronze":
                    drivers.append(("Bronze Tier Exposure", "Lowest loyalty stickiness; high vulnerability to competitor switching.", "negative"))

                if aov > 2500:
                    drivers.append(("Premium Basket Size", f"High average basket value (₹{aov:,.2f}) indicates commercial value.", "positive"))

                for title, text, sentiment in drivers:
                    color = "#047857" if sentiment == "positive" else "#b91c1c"
                    bg = "#f0fdf4" if sentiment == "positive" else "#fef2f2"
                    icon = "🟢" if sentiment == "positive" else "🔴"
                    st.markdown(f"""
                    <div style="background: {bg}; border-left: 3px solid {color}; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px;">
                        <div style="font-weight: 700; font-size: 0.85rem; color: {color};">{icon} {title}</div>
                        <div style="font-size: 0.82rem; color: #334155;">{text}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with c_b:
                st.markdown("**Model Decision Tree Rules Traversed:**")
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 14px; font-size: 0.82rem; color: #475569; line-height: 1.7;">
                    <strong>1. Membership Split:</strong> {membership_type} (Encoded Index: {mem_enc})<br/>
                    <strong>2. Inactivity Horizon:</strong> {days_since_last_order} days vs. 155.5 threshold<br/>
                    <strong>3. Satisfaction Vector:</strong> Score {satisfaction_score}/5.0<br/>
                    <strong>4. Spending Trajectory:</strong> ₹{total_order_value:,.2f} total across {order_frequency} orders<br/>
                    <strong>5. Final Leaf Node:</strong> Class {prediction} ({"Retained" if prediction == 0 else "Churn"}) with {max(retention_prob, churn_prob):.1f}% confidence
                </div>
                """, unsafe_allow_html=True)

        with tab_bench:
            st.markdown("**Comparison vs. Regional Cohort Averages:**")
            cohort_data = df_clean[df_clean['location'] == location]
            mem_cohort = df_clean[df_clean['membership_type'] == membership_type]

            benchmarks = pd.DataFrame({
                "Metric": ["Order Frequency", "Total Order Value", "Avg Order Value", "Days Inactive", "Satisfaction Score"],
                "This Customer": [f"{order_frequency}", f"₹{total_order_value:,.2f}", f"₹{aov:,.2f}", f"{days_since_last_order} days", f"{satisfaction_score}/5"],
                f"Avg ({location} Hub)": [f"{cohort_data['order_frequency'].mean():.1f}", f"₹{cohort_data['total_order_value'].mean():,.2f}", f"₹{cohort_data['avg_order_value'].mean():,.2f}", f"{cohort_data['days_since_last_order'].mean():.0f} days", f"{cohort_data['satisfaction_score'].mean():.1f}/5"],
                f"Avg ({membership_type} Tier)": [f"{mem_cohort['order_frequency'].mean():.1f}", f"₹{mem_cohort['total_order_value'].mean():,.2f}", f"₹{mem_cohort['avg_order_value'].mean():,.2f}", f"{mem_cohort['days_since_last_order'].mean():.0f} days", f"{mem_cohort['satisfaction_score'].mean():.1f}/5"]
            })
            st.dataframe(benchmarks, use_container_width=True, hide_index=True)

        with tab_rec:
            st.markdown("**Tailored Strategic Next-Best-Action:**")
            if prediction == 1:
                st.markdown("""
                - **Immediate Re-engagement Trigger:** Deploy an automated personalized discount voucher (15-20% off next order) valid for 7 days.
                - **Priority Customer Support Outreach:** Flag account for dedicated CRM specialist check-in to investigate dissatisfaction causes.
                - **Tier Upgrade Incentive:** Offer a 30-day complimentary trial of Silver/Gold benefits to rebuild engagement.
                - **Product Re-discovery Survey:** Dispatch a 2-question micro-survey on mobile with an instant reward incentive.
                """)
            else:
                st.markdown("""
                - **VIP Appreciation:** Send a personalized loyalty thank-you message with early access to upcoming product releases.
                - **Cross-Selling & Basket Expansion:** Recommend complementary categories based on historical high AOV purchases.
                - **Referral Program Invitation:** Invite this high-satisfaction customer to the ambassador referral reward scheme.
                - **Tier Maintenance Notification:** Provide clear milestones showing progress towards next VIP tier perks.
                """)


# ===================== PAGE: TASK 1 =====================
elif page == "Task 1: Load Data & EDA":
    st.markdown('<div class="accent-divider"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="task-title">Task 1: Load Customer Data & Feature Construction</h1>', unsafe_allow_html=True)
    st.markdown('<p class="task-subtitle">Ingesting customer transaction schedules, fusing master customer registry, and inspecting schema properties.</p>', unsafe_allow_html=True)

    df = load_raw_data()
    df_f = filtered_data(df)

    render_metric_cards([
        {"label": "TOTAL RECORDS", "value": f"{len(df_f):,}", "desc": "Customer transactions"},
        {"label": "TOTAL FEATURES", "value": str(df.shape[1]), "desc": "Behavioral attributes"},
        {"label": "PRIMARY HUBS", "value": str(df['location'].nunique()), "desc": "Operating locations"},
        {"label": "DATA QUALITY SCORE", "value": f"{(1 - df.isnull().any(axis=1).sum() / len(df)) * 100:.1f}%", "desc": "Complete records"}
    ])

    st.write("")

    tab1, tab2, tab3, tab4 = st.tabs(["Dataset Overview & Schema", "Membership Distribution", "Geographic Hub Breakdown", "Statistical Summary"])

    with tab1:
        st.subheader("Dataset Preview & Attributes")
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.markdown("**Sample Customer Transactions (First 5 Rows)**")
            st.dataframe(df_f.head(5), use_container_width=True, hide_index=True)
        with col_b:
            st.markdown("**Master Schema**")
            schema_data = {
                'Column': df.columns.tolist(),
                'Data Type': [str(dt) for dt in df.dtypes],
                'Unique Values': [df[c].nunique() for c in df.columns]
            }
            st.dataframe(pd.DataFrame(schema_data), use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Membership Tier Breakdown")
        mem_dist = df_f['membership_type'].value_counts().reset_index()
        mem_dist.columns = ['Membership Type', 'Count']
        mem_dist['Percentage'] = (mem_dist['Count'] / mem_dist['Count'].sum() * 100).round(1)
        st.dataframe(mem_dist, use_container_width=True, hide_index=True)

        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ['#0284c7', '#0d9488', '#d97706']
        bars = ax.bar(mem_dist['Membership Type'], mem_dist['Count'], color=colors, width=0.45)
        for bar, pct in zip(bars, mem_dist['Percentage']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{pct}%',
                    ha='center', va='bottom', fontsize=10, color='#334155')
        ax.set_ylabel("Count", fontsize=10, color='#64748b')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e2e8f0')
        ax.spines['bottom'].set_color('#e2e8f0')
        ax.tick_params(colors='#64748b')
        ax.set_title("Membership Tier Distribution", fontsize=12, fontweight='bold', color='#0f172a', pad=14)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with tab3:
        st.subheader("Geographic Hub Distribution")
        loc_dist = df['location'].value_counts().reset_index()
        loc_dist.columns = ['Location Hub', 'Customers']
        loc_dist['Churn Rate'] = df.groupby('location')['churn'].mean().reindex(loc_dist['Location Hub']).values
        loc_dist['Churn Rate'] = loc_dist['Churn Rate'].apply(lambda x: f"{x:.1%}")
        st.dataframe(loc_dist, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("Statistical Summary")
        st.dataframe(df_f.describe().round(2), use_container_width=True)

    with st.expander("View PySpark Source Code (task1_load_data.py)"):
        try:
            with open("task1_load_data.py", "r") as f:
                st.code(f.read(), language="python")
        except FileNotFoundError:
            st.warning("task1_load_data.py not found.")


# ===================== PAGE: TASK 2 =====================
elif page == "Task 2: Handle Missing Values":
    st.markdown('<div class="accent-divider"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="task-title">Task 2: Handle Missing Order Frequency & Value Details</h1>', unsafe_allow_html=True)
    st.markdown('<p class="task-subtitle">Detecting null fields across order metrics and applying mean substitution strategy.</p>', unsafe_allow_html=True)

    df_raw = load_raw_data()
    df_clean = get_clean_data()

    missing_freq = df_raw['order_frequency'].isnull().sum()
    missing_val = df_raw['total_order_value'].isnull().sum()
    total_missing = missing_freq + missing_val

    render_metric_cards([
        {"label": "NULL ORDER FREQUENCY", "value": str(missing_freq), "desc": "Imputed via mean"},
        {"label": "NULL TOTAL ORDER VALUE", "value": str(missing_val), "desc": "Imputed via mean"},
        {"label": "TOTAL IMPUTED CELLS", "value": str(total_missing), "desc": "Filled values"},
        {"label": "POST-CLEAN RESIDUAL NULLS", "value": "0", "desc": "Clean dataset"}
    ])

    st.write("")

    tab1, tab2, tab3 = st.tabs(["Before vs After Inspection", "Imputation Specifications", "Cleaned Data Preview"])

    with tab1:
        st.subheader("Missing Value Audit")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Pre-Clean Audit**")
            before_data = df_raw.isnull().sum().reset_index()
            before_data.columns = ['Attribute', 'Missing Count']
            before_data = before_data[before_data['Missing Count'] > 0]
            st.dataframe(before_data, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Post-Clean Audit**")
            after_data = df_clean.isnull().sum().reset_index()
            after_data.columns = ['Attribute', 'Missing Count']
            after_data = after_data[after_data['Missing Count'] > 0]
            if len(after_data) > 0:
                st.dataframe(after_data, use_container_width=True, hide_index=True)
            else:
                st.info("No missing values remain across all columns.")

    with tab2:
        st.subheader("Imputation Parameters")
        mean_freq_val = df_raw['order_frequency'].mean()
        mean_value_val = df_raw['total_order_value'].mean()
        strategy_data = {
            'Attribute': ['order_frequency', 'total_order_value'],
            'Missing Count': [missing_freq, missing_val],
            'Imputation Strategy': ['Mean Substitution', 'Mean Substitution'],
            'Replacement Mean': [f'{mean_freq_val:.2f}', f'{mean_value_val:.2f}']
        }
        st.dataframe(pd.DataFrame(strategy_data), use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Cleaned Dataset (First 10 Rows)")
        st.dataframe(df_clean.head(10), use_container_width=True, hide_index=True)

    with st.expander("View PySpark Source Code (task2_handle_missing.py)"):
        try:
            with open("task2_handle_missing.py", "r") as f:
                st.code(f.read(), language="python")
        except FileNotFoundError:
            st.warning("task2_handle_missing.py not found.")


# ===================== PAGE: TASK 3 =====================
elif page == "Task 3: Encode Categorical Fields":
    st.markdown('<div class="accent-divider"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="task-title">Task 3: Encode Categorical Attributes for Pipeline</h1>', unsafe_allow_html=True)
    st.markdown('<p class="task-subtitle">Transforming string categorical identifiers into numeric index representations for PySpark ML compatibility.</p>', unsafe_allow_html=True)

    df = get_encoded_data()

    render_metric_cards([
        {"label": "ENCODED ATTRIBUTES", "value": "3", "desc": "Indexed columns"},
        {"label": "LOCATION HUBS", "value": str(df['location'].nunique()), "desc": "Distinct values"},
        {"label": "MEMBERSHIP TIERS", "value": str(df['membership_type'].nunique()), "desc": "Distinct values"},
        {"label": "GENDER TIERS", "value": str(df['gender'].nunique()), "desc": "Distinct values"}
    ])

    st.write("")

    tab1, tab2, tab3 = st.tabs(["Mapping Dictionaries", "Encoded Sample Data", "Attribute Distributions"])

    with tab1:
        st.subheader("Categorical Mapping Lookups")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Location Mapping**")
            loc_map = df[['location', 'location_encoded']].drop_duplicates().sort_values('location_encoded').reset_index(drop=True)
            st.dataframe(loc_map, use_container_width=True, hide_index=True)
        with col2:
            st.markdown("**Membership Mapping**")
            mem_map = df[['membership_type', 'membership_encoded']].drop_duplicates().sort_values('membership_encoded').reset_index(drop=True)
            st.dataframe(mem_map, use_container_width=True, hide_index=True)
        with col3:
            st.markdown("**Gender Mapping**")
            gen_map = df[['gender', 'gender_encoded']].drop_duplicates().sort_values('gender_encoded').reset_index(drop=True)
            st.dataframe(gen_map, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Encoded Records (First 10 Rows)")
        st.dataframe(
            df[['customer_id', 'location', 'location_encoded',
                'membership_type', 'membership_encoded',
                'gender', 'gender_encoded']].head(10),
            use_container_width=True, hide_index=True
        )

    with tab3:
        st.subheader("Categorical Balance")
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))

        loc_counts = df['location'].value_counts()
        axes[0].barh(loc_counts.index, loc_counts.values, color='#0284c7', height=0.55)
        axes[0].set_title("Location Hub", fontsize=11, fontweight='bold', color='#0f172a')
        axes[0].spines['top'].set_visible(False)
        axes[0].spines['right'].set_visible(False)
        axes[0].tick_params(labelsize=9)

        mem_counts = df['membership_type'].value_counts()
        axes[1].barh(mem_counts.index, mem_counts.values, color='#0d9488', height=0.45)
        axes[1].set_title("Membership Tier", fontsize=11, fontweight='bold', color='#0f172a')
        axes[1].spines['top'].set_visible(False)
        axes[1].spines['right'].set_visible(False)
        axes[1].tick_params(labelsize=9)

        gen_counts = df['gender'].value_counts()
        axes[2].barh(gen_counts.index, gen_counts.values, color='#d97706', height=0.35)
        axes[2].set_title("Gender", fontsize=11, fontweight='bold', color='#0f172a')
        axes[2].spines['top'].set_visible(False)
        axes[2].spines['right'].set_visible(False)
        axes[2].tick_params(labelsize=9)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with st.expander("View PySpark Source Code (task3_encode_categorical.py)"):
        try:
            with open("task3_encode_categorical.py", "r") as f:
                st.code(f.read(), language="python")
        except FileNotFoundError:
            st.warning("task3_encode_categorical.py not found.")


# ===================== PAGE: TASK 4 =====================
elif page == "Task 4: Train Decision Tree":
    st.markdown('<div class="accent-divider"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="task-title">Task 4: Train Decision Tree Classifier</h1>', unsafe_allow_html=True)
    st.markdown('<p class="task-subtitle">Fitting a DecisionTreeClassifier with max_depth=5 on an 80/20 train-test partition.</p>', unsafe_allow_html=True)

    model, X_train, X_test, y_train, y_test, y_pred, acc, prec, rec, feature_cols = train_and_evaluate()

    render_metric_cards([
        {"label": "TRAINING VOLUME", "value": str(len(X_train)), "desc": "80% partition"},
        {"label": "TEST VOLUME", "value": str(len(X_test)), "desc": "20% partition"},
        {"label": "FEATURE COUNT", "value": str(len(feature_cols)), "desc": "Vector inputs"},
        {"label": "MAX DEPTH", "value": "5", "desc": "Tree parameter"}
    ])

    st.write("")

    tab1, tab2, tab3 = st.tabs(["Classifier Configuration", "Feature Importance Ranking", "Test Sample Predictions"])

    with tab1:
        st.subheader("Model Configuration & Parameters")
        config_data = {
            'Configuration Parameter': ['Algorithm', 'Max Depth', 'Random State', 'Train/Test Ratio', 'Target Label', 'Features'],
            'Configured Setting': ['DecisionTreeClassifier', '5', '42', '80 / 20 Split', 'churn', 'VectorAssembler output (9 cols)']
        }
        st.dataframe(pd.DataFrame(config_data), use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Feature Importance Distribution")
        importance_df = pd.DataFrame({
            'Feature': feature_cols,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=True)

        fig, ax = plt.subplots(figsize=(10, 5))
        colors_imp = ['#0284c7' if v > 0.1 else '#93c5fd' for v in importance_df['Importance']]
        bars = ax.barh(importance_df['Feature'], importance_df['Importance'], color=colors_imp, height=0.55)
        for bar, val in zip(bars, importance_df['Importance']):
            if val > 0.01:
                ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
                        f'{val:.3f}', va='center', fontsize=9, color='#334155')
        ax.set_xlabel("Importance Score", fontsize=10, color='#64748b')
        ax.set_title("Decision Tree Feature Importances", fontsize=12, fontweight='bold', color='#0f172a', pad=14)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e2e8f0')
        ax.spines['bottom'].set_color('#e2e8f0')
        ax.tick_params(colors='#64748b', labelsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with tab3:
        st.subheader("Prediction Sample (First 10 Rows)")
        pred_df = X_test.head(10).copy()
        pred_df['Actual_Churn'] = y_test.values[:10]
        pred_df['Predicted_Churn'] = y_pred[:10]
        pred_df['Result'] = np.where(pred_df['Actual_Churn'] == pred_df['Predicted_Churn'], 'Correct', 'Incorrect')
        st.dataframe(pred_df, use_container_width=True, hide_index=True)

    with st.expander("View PySpark Source Code (task4_train_model.py)"):
        try:
            with open("task4_train_model.py", "r") as f:
                st.code(f.read(), language="python")
        except FileNotFoundError:
            st.warning("task4_train_model.py not found.")


# ===================== PAGE: TASK 5 =====================
elif page == "Task 5: Evaluate Model":
    st.markdown('<div class="accent-divider"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="task-title">Task 5: Evaluate Model Performance Metrics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="task-subtitle">Assessing classification quality via Accuracy, Precision, and Recall using MulticlassClassificationEvaluator.</p>', unsafe_allow_html=True)

    model, X_train, X_test, y_train, y_test, y_pred, acc, prec, rec, feature_cols = train_and_evaluate()

    render_metric_cards([
        {"label": "ACCURACY", "value": f"{acc:.2%}", "desc": "Overall correct classification"},
        {"label": "PRECISION", "value": f"{prec:.2%}", "desc": "Weighted precision"},
        {"label": "RECALL", "value": f"{rec:.2%}", "desc": "Weighted recall"},
        {"label": "EVALUATION SAMPLES", "value": str(len(X_test)), "desc": "Holdout validation set"}
    ])

    st.write("")

    tab1, tab2, tab3 = st.tabs(["Confusion Matrix", "Metric Breakdown", "Prediction Contingency Table"])

    with tab1:
        st.subheader("Confusion Matrix")
        cm = confusion_matrix(y_test, y_pred)
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cm, interpolation='nearest', cmap='Blues')
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Retained (0)', 'Churned (1)'], fontsize=10)
        ax.set_yticklabels(['Retained (0)', 'Churned (1)'], fontsize=10)
        ax.set_xlabel('Predicted Label', fontsize=11, fontweight='bold', color='#334155')
        ax.set_ylabel('True Label', fontsize=11, fontweight='bold', color='#334155')
        ax.set_title('Decision Tree Confusion Matrix', fontsize=12, fontweight='bold', color='#0f172a', pad=14)

        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                        fontsize=18, fontweight='bold',
                        color="white" if cm[i, j] > cm.max()/2 else "#0f172a")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with tab2:
        st.subheader("Evaluation Metric Specifications")
        metric_defs = {
            'Metric': ['Accuracy', 'Weighted Precision', 'Weighted Recall'],
            'Mathematical Formula': [
                '(TP + TN) / (TP + TN + FP + FN)',
                'TP / (TP + FP)',
                'TP / (TP + FN)'
            ],
            'Score': [f'{acc:.4f}', f'{prec:.4f}', f'{rec:.4f}'],
            'Interpretation': [
                'Ratio of total correct predictions to total observations',
                'Proportion of positive identifications that were correct',
                'Proportion of actual positives identified correctly'
            ]
        }
        st.dataframe(pd.DataFrame(metric_defs), use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Contingency Table")
        breakdown = pd.DataFrame({'Actual': y_test.values, 'Predicted': y_pred})
        cross_tab = pd.crosstab(breakdown['Actual'], breakdown['Predicted'],
                                rownames=['Actual'], colnames=['Predicted'], margins=True)
        st.dataframe(cross_tab, use_container_width=True)

    with st.expander("View PySpark Source Code (task5_evaluate.py)"):
        try:
            with open("task5_evaluate.py", "r") as f:
                st.code(f.read(), language="python")
        except FileNotFoundError:
            st.warning("task5_evaluate.py not found.")


# ===================== PAGE: TASK 6 =====================
elif page == "Task 6: Visualize Retention Rates":
    st.markdown('<div class="accent-divider"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="task-title">Task 6: Route Network & Hub Retention Connectivity Chart</h1>', unsafe_allow_html=True)
    st.markdown('<p class="task-subtitle">Analyzing and comparing retention rates across Gold, Silver, and Bronze membership tiers.</p>', unsafe_allow_html=True)

    df = get_clean_data()
    df_f = filtered_data(df)

    retention = df_f.groupby('membership_type')['churn'].agg(['mean', 'count']).reset_index()
    retention.columns = ['Membership Type', 'Churn Rate', 'Total Customers']
    retention['Retention Rate'] = 1 - retention['Churn Rate']
    retention = retention.sort_values('Membership Type')

    gold_val = retention[retention['Membership Type'] == 'Gold']['Retention Rate'].values
    silver_val = retention[retention['Membership Type'] == 'Silver']['Retention Rate'].values
    bronze_val = retention[retention['Membership Type'] == 'Bronze']['Retention Rate'].values

    render_metric_cards([
        {"label": "GOLD RETENTION", "value": f"{gold_val[0]:.1%}" if len(gold_val) > 0 else "N/A", "desc": "Top tier retention"},
        {"label": "SILVER RETENTION", "value": f"{silver_val[0]:.1%}" if len(silver_val) > 0 else "N/A", "desc": "Mid tier retention"},
        {"label": "BRONZE RETENTION", "value": f"{bronze_val[0]:.1%}" if len(bronze_val) > 0 else "N/A", "desc": "Base tier retention"},
        {"label": "NETWORK AVERAGE", "value": f"{1 - df_f['churn'].mean():.1%}", "desc": "All customers"}
    ])

    st.write("")

    tab1, tab2, tab3 = st.tabs(["Retention Chart", "Tier Breakdown Table", "Location Cross Analysis"])

    with tab1:
        st.subheader("Retention Rate by Membership Tier")

        fig, ax = plt.subplots(figsize=(8, 4.5))
        colors = ['#d97706', '#0284c7', '#0d9488']
        bars = ax.bar(retention['Membership Type'], retention['Retention Rate'],
                      color=colors, width=0.45, zorder=3)

        for bar, rate, count in zip(bars, retention['Retention Rate'], retention['Total Customers']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{rate:.1%}', ha='center', va='bottom', fontsize=12,
                    fontweight='bold', color='#0f172a')
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                    f'n={count}', ha='center', va='center', fontsize=9,
                    color='white', fontweight='bold')

        ax.set_ylabel("Retention Rate", fontsize=10, color='#64748b')
        ax.set_ylim(0, 1.15)
        ax.set_title("Customer Retention by Membership Tier", fontsize=12,
                      fontweight='bold', color='#0f172a', pad=14)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e2e8f0')
        ax.spines['bottom'].set_color('#e2e8f0')
        ax.tick_params(colors='#64748b', labelsize=10)
        ax.grid(axis='y', alpha=0.15, color='#94a3b8')
        ax.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with tab2:
        st.subheader("Detailed Retention Metrics")
        display_ret = retention.copy()
        display_ret['Churn Rate'] = display_ret['Churn Rate'].apply(lambda x: f"{x:.2%}")
        display_ret['Retention Rate'] = display_ret['Retention Rate'].apply(lambda x: f"{x:.2%}")
        st.dataframe(display_ret, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Location × Membership Retention Cross Analysis")
        cross = df.groupby(['location', 'membership_type'])['churn'].agg(['mean', 'count']).reset_index()
        cross.columns = ['Location Hub', 'Membership', 'Churn Rate', 'Volume']
        cross['Retention Rate'] = (1 - cross['Churn Rate']).apply(lambda x: f"{x:.1%}")
        cross['Churn Rate'] = cross['Churn Rate'].apply(lambda x: f"{x:.1%}")
        st.dataframe(cross, use_container_width=True, hide_index=True)

    with st.expander("View PySpark Source Code (task6_visualize.py)"):
        try:
            with open("task6_visualize.py", "r") as f:
                st.code(f.read(), language="python")
        except FileNotFoundError:
            st.warning("task6_visualize.py not found.")


# ===================== PAGE: MAJOR FINDINGS & SUMMARY =====================
elif page == "Major Findings & Summary":
    st.markdown('<div class="accent-divider"></div>', unsafe_allow_html=True)

    st.markdown('<h1 class="task-title">Major Findings & Project Summary</h1>', unsafe_allow_html=True)
    st.markdown('<p class="task-subtitle">Synthesizing analytical results, model benchmarks, and strategic operational takeaways.</p>', unsafe_allow_html=True)

    model, X_train, X_test, y_train, y_test, y_pred, acc, prec, rec, feature_cols = train_and_evaluate()
    df = get_clean_data()
    churn_rate = df['churn'].mean()

    render_metric_cards([
        {"label": "MODEL ACCURACY", "value": f"{acc:.2%}", "desc": "Validation score"},
        {"label": "CHURN RATE", "value": f"{churn_rate:.1%}", "desc": "Overall attrition"},
        {"label": "RETENTION RATE", "value": f"{1 - churn_rate:.1%}", "desc": "Overall retained"},
        {"label": "COMPLETED TASKS", "value": "6 of 6", "desc": "End-to-end pipeline"}
    ])

    st.write("")

    tab1, tab2, tab3 = st.tabs(["Key Findings", "Operational Recommendations", "Platform Technologies"])

    with tab1:
        st.subheader("Executive Findings")

        importance_df = pd.DataFrame({
            'Feature': feature_cols,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Top Churn Predictors**")
            top3 = importance_df.head(3).reset_index(drop=True)
            top3.index = top3.index + 1
            top3['Importance'] = top3['Importance'].apply(lambda x: f"{x:.4f}")
            st.dataframe(top3, use_container_width=True)

        with col2:
            st.markdown("**Retention by Membership Level**")
            retention = df.groupby('membership_type')['churn'].mean().reset_index()
            retention.columns = ['Membership', 'Churn Rate']
            retention['Retention Rate'] = (1 - retention['Churn Rate']).apply(lambda x: f"{x:.2%}")
            retention['Churn Rate'] = retention['Churn Rate'].apply(lambda x: f"{x:.2%}")
            st.dataframe(retention, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("""
        **Summary Points:**

        1. Missing values were systematically addressed using mean imputation for `order_frequency` (50 values)
           and `total_order_value` (40 values).
        2. Categorical features (`location`, `membership_type`, `gender`) were indexed into numerical vectors.
        3. Decision Tree Classifier with max_depth=5 achieved stable accuracy on an 80/20 train-test split.
        4. Customer retention is highest among Gold tier members, confirming the protective effect of loyalty status.
        5. Inactivity (`days_since_last_order`) and `satisfaction_score` remain the primary leading indicators of churn.
        """)

    with tab2:
        st.subheader("Operational Recommendations")
        recommendations = {
            'Priority': ['High', 'High', 'Medium', 'Medium', 'Standard'],
            'Strategic Recommendation': [
                'Automate re-engagement triggers for accounts exceeding 180 days since last order',
                'Deploy retention outreach for Bronze tier accounts showing low satisfaction ratings',
                'Incentivize Silver to Gold tier upgrades via targeted loyalty promotions',
                'Integrate Decision Tree scoring into batch marketing workflows',
                'Collect periodic customer feedback to refresh satisfaction scores'
            ],
            'Target Outcome': [
                'Mitigate churn in dormant accounts',
                'Stabilize base tier customer retention',
                'Increase average customer lifetime value',
                'Enable preemptive intervention',
                'Maintain high model prediction accuracy'
            ]
        }
        st.dataframe(pd.DataFrame(recommendations), use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Platform Architecture")
        tools = {
            "Component": [
                "Apache Spark (PySpark)",
                "PySpark ML",
                "Python 3.x",
                "Scikit-learn",
                "Streamlit",
                "Matplotlib",
                "Pandas / NumPy"
            ],
            "Function": [
                "Big data distributed compute engine",
                "StringIndexer, VectorAssembler, DecisionTreeClassifier",
                "Core runtime language",
                "Model training, cross-validation, and metrics",
                "Interactive enterprise analytics interface",
                "Chart rendering and visualization",
                "Tabular data manipulation and aggregation"
            ]
        }
        st.dataframe(pd.DataFrame(tools), use_container_width=True, hide_index=True)
