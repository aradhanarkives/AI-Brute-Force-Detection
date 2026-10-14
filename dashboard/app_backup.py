
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import joblib
import pickle

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Brute Force Detection Tool",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "dataset" / "login_data.csv"
RF_MODEL_PATH = PROJECT_ROOT / "models" / "random_forest.pkl"
IF_MODEL_PATH = PROJECT_ROOT / "models" / "isolation_forest.pkl"
SCALER_PATH = PROJECT_ROOT / "models" / "scaler.pkl"

FEATURES = [
    "login_attempts",
    "failed_attempts",
    "time_between_attempts",
    "unique_usernames",
    "ip_reputation"
]

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1120;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    .tool-card {
        background-color: #172033;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 18px;
        min-height: 145px;
    }

    .tool-title {
        font-size: 18px;
        font-weight: 700;
        color: #f8fafc;
    }

    .tool-description {
        color: #cbd5e1;
        font-size: 14px;
    }

    .status-active {
        color: #22c55e;
        font-weight: bold;
    }

    .status-warning {
        color: #f59e0b;
        font-weight: bold;
    }

    .status-danger {
        color: #ef4444;
        font-weight: bold;
    }

    .section-title {
        color: #e2e8f0;
        font-size: 22px;
        font-weight: 700;
        margin-top: 15px;
    }

    .result-box {
        background-color: #172033;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #475569;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# FILE LOADING FUNCTIONS
# ==========================================================

@st.cache_data
def load_dataset():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    data = pd.read_csv(DATASET_PATH)

    missing_columns = [
        column for column in FEATURES + ["label"]
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing dataset columns: {missing_columns}"
        )

    return data


def load_pickle_file(file_path):
    """
    Try joblib first.
    If it fails, try normal pickle loading.
    """
    try:
        return joblib.load(file_path)
    except Exception as joblib_error:
        try:
            with open(file_path, "rb") as file:
                return pickle.load(file)
        except Exception as pickle_error:
            raise RuntimeError(
                f"Could not load {file_path.name}. "
                f"Joblib error: {joblib_error}. "
                f"Pickle error: {pickle_error}"
            )


@st.cache_resource
def load_models():
    if not RF_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Random Forest model not found: {RF_MODEL_PATH}"
        )

    if not IF_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Isolation Forest model not found: {IF_MODEL_PATH}"
        )

    if not SCALER_PATH.exists():
        raise FileNotFoundError(
            f"Scaler not found: {SCALER_PATH}"
        )

    random_forest = load_pickle_file(RF_MODEL_PATH)
    isolation_forest = load_pickle_file(IF_MODEL_PATH)
    scaler = load_pickle_file(SCALER_PATH)

    return random_forest, isolation_forest, scaler


# ==========================================================
# AI DETECTION FUNCTION
# ==========================================================

def detect_activity(input_data, random_forest, isolation_forest, scaler):
    """
    Performs detection using both AI models.

    Random Forest:
    0 = Normal
    1 = Attack

    Isolation Forest:
    1 = Normal
    -1 = Anomaly
    """

    feature_data = input_data[FEATURES].copy()

    scaled_data = scaler.transform(feature_data)

    rf_prediction = random_forest.predict(scaled_data)
    if_prediction = isolation_forest.predict(scaled_data)

    rf_result = np.array(rf_prediction).astype(int)

    isolation_result = np.where(
        np.array(if_prediction) == -1,
        1,
        0
    )

    final_result = np.where(
        (rf_result == 1) | (isolation_result == 1),
        1,
        0
    )

    output = input_data.copy()

    output["Random Forest"] = rf_result
    output["Isolation Forest"] = isolation_result
    output["AI Result"] = np.where(
        final_result == 1,
        "Attack",
        "Normal"
    )

    return output


# ==========================================================
# LOAD APPLICATION DATA
# ==========================================================

try:
    dataset = load_dataset()
    random_forest, isolation_forest, scaler = load_models()
    loading_successful = True

except Exception as error:
    loading_successful = False

    st.error("⚠️ Dataset or AI model loading failed")
    st.code(str(error))

    st.info(
        "If the error is related to a .pkl file, retrain and save "
        "the models using joblib.dump()."
    )

    st.stop()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🛡️ Security Tool")

st.sidebar.success("AI Models Loaded")

mode = st.sidebar.radio(
    "Select Detection Mode",
    [
        "Dashboard Overview",
        "Dataset Detection",
        "Manual Login Test",
        "Live Login Simulation"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("Model Information")

st.sidebar.write("Random Forest: Active")
st.sidebar.write("Isolation Forest: Active")
st.sidebar.write("Feature Scaler: Active")

st.sidebar.markdown("---")

if st.sidebar.button("Clear Model Cache"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Cache cleared. Restarting...")
    st.rerun()

# ==========================================================
# HEADER
# ==========================================================

st.title("🛡️ AI-Based Brute Force Attack Detection Tool")

st.write(
    "Adaptive Identity-Aware Brute Force Detection using "
    "Random Forest, Isolation Forest and Three-Memory Trust Intelligence."
)

st.markdown("---")

# ==========================================================
# DATASET STATISTICS
# ==========================================================

total_records = len(dataset)
actual_attacks = int((dataset["label"] == 1).sum())
actual_normal = int((dataset["label"] == 0).sum())

attack_percentage = (
    actual_attacks / total_records * 100
    if total_records > 0
    else 0
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(
        "Total Login Records",
        total_records
    )

with metric2:
    st.metric(
        "Dataset Attacks",
        actual_attacks
    )

with metric3:
    st.metric(
        "Normal Records",
        actual_normal
    )

with metric4:
    st.metric(
        "Attack Percentage",
        f"{attack_percentage:.2f}%"
    )

# ==========================================================
# DASHBOARD OVERVIEW
# ==========================================================

if mode == "Dashboard Overview":

    st.markdown(
        '<div class="section-title">🧠 Three-Memory Trust Intelligence</div>',
        unsafe_allow_html=True
    )

    memory1, memory2, memory3 = st.columns(3)

    with memory1:
        st.markdown(
            """
            <div class="tool-card">
                <div class="tool-title">👤 Identity Memory</div>
                <br>
                <div class="tool-description">
                    Compares current login behavior with normal identity
                    patterns such as login frequency, timing and usernames.
                </div>
                <br>
                <div class="status-active">● Monitoring</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with memory2:
        st.markdown(
            """
            <div class="tool-card">
                <div class="tool-title">⚔️ Attack Pattern Memory</div>
                <br>
                <div class="tool-description">
                    Identifies repeated failures, high login attempts,
                    multiple usernames and suspicious activity patterns.
                </div>
                <br>
                <div class="status-active">● Monitoring</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with memory3:
        st.markdown(
            """
            <div class="tool-card">
                <div class="tool-title">🔄 Decision Recovery Memory</div>
                <br>
                <div class="tool-description">
                    Represents previous security decisions and supports
                    future investigation and recovery decisions.
                </div>
                <br>
                <div class="status-warning">● Interface Connected</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.subheader("📊 Dataset Distribution")

    distribution = pd.DataFrame(
        {
            "Activity": ["Normal", "Attack"],
            "Count": [actual_normal, actual_attacks]
        }
    )

    st.bar_chart(
        distribution.set_index("Activity")
    )

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        dataset.head(10),
        use_container_width=True
    )

# ==========================================================
# DATASET DETECTION
# ==========================================================

elif mode == "Dataset Detection":

    st.subheader("🔍 AI Dataset Detection")

    with st.spinner("Analyzing login records using AI models..."):
        detected_data = detect_activity(
            dataset,
            random_forest,
            isolation_forest,
            scaler
        )

    ai_attacks = int(
        (detected_data["AI Result"] == "Attack").sum()
    )

    ai_normal = int(
        (detected_data["AI Result"] == "Normal").sum()
    )

    result1, result2 = st.columns(2)

    with result1:
        st.metric(
            "AI Detected Attacks",
            ai_attacks
        )

    with result2:
        st.metric(
            "AI Detected Normal Activity",
            ai_normal
        )

    st.markdown("---")

    filter_type = st.selectbox(
        "Filter Detection Results",
        [
            "All Results",
            "Only Attacks",
            "Only Normal"
        ]
    )

    if filter_type == "Only Attacks":
        filtered_data = detected_data[
            detected_data["AI Result"] == "Attack"
        ]

    elif filter_type == "Only Normal":
        filtered_data = detected_data[
            detected_data["AI Result"] == "Normal"
        ]

    else:
        filtered_data = detected_data

    st.dataframe(
        filtered_data,
        use_container_width=True,
        height=450
    )

    st.subheader("📈 AI Detection Distribution")

    chart_data = pd.DataFrame(
        {
            "Activity": ["Normal", "Attack"],
            "Count": [ai_normal, ai_attacks]
        }
    )

    st.bar_chart(
        chart_data.set_index("Activity")
    )

    csv_data = detected_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Export Detection Results",
        data=csv_data,
        file_name="ai_detection_results.csv",
        mime="text/csv"
    )

# ==========================================================
# MANUAL LOGIN TEST
# ==========================================================

elif mode == "Manual Login Test":

    st.subheader("🧪 Manual Login Activity Analyzer")

    st.write(
        "Enter login activity values and test them using the trained AI models."
    )

    left, right = st.columns(2)

    with left:
        login_attempts = st.number_input(
            "Login Attempts",
            min_value=1,
            max_value=1000,
            value=5
        )

        failed_attempts = st.number_input(
            "Failed Attempts",
            min_value=0,
            max_value=1000,
            value=4
        )

        time_between_attempts = st.number_input(
            "Time Between Attempts",
            min_value=0.0,
            max_value=10000.0,
            value=2.0
        )

    with right:
        unique_usernames = st.number_input(
            "Unique Usernames",
            min_value=1,
            max_value=1000,
            value=3
        )

        ip_reputation = st.slider(
            "IP Reputation",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.01
        )

    manual_data = pd.DataFrame(
        [
            {
                "login_attempts": login_attempts,
                "failed_attempts": failed_attempts,
                "time_between_attempts": time_between_attempts,
                "unique_usernames": unique_usernames,
                "ip_reputation": ip_reputation
            }
        ]
    )

    st.markdown("---")

    if st.button("🔎 Analyze Login Activity", type="primary"):

        result = detect_activity(
            manual_data,
            random_forest,
            isolation_forest,
            scaler
        )

        rf_result = int(result["Random Forest"].iloc[0])
        isolation_result = int(result["Isolation Forest"].iloc[0])
        final_result = result["AI Result"].iloc[0]

        st.subheader("🛡️ Security Decision")

        if final_result == "Attack":
            st.error("🚨 Suspicious Login Activity Detected")

            st.markdown(
                """
                <div class="result-box">
                    <h3 class="status-danger">Attack Classification</h3>
                    <p>
                    The AI models detected suspicious login behavior.
                    Further investigation or temporary blocking may be required.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.success("✅ Login Activity Appears Normal")

            st.markdown(
                """
                <div class="result-box">
                    <h3 class="status-active">Normal Classification</h3>
                    <p>
                    The current login activity did not produce a strong
                    attack signal from the AI models.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("Random Forest Prediction:", rf_result)
        st.write("Isolation Forest Prediction:", isolation_result)

        st.subheader("🧠 Memory Analysis")

        if failed_attempts >= 5:
            st.warning(
                "Attack Pattern Memory: High failed-login activity detected."
            )
        else:
            st.info(
                "Identity Memory: Login failure count is within the basic threshold."
            )

        if unique_usernames >= 4:
            st.warning(
                "Attack Pattern Memory: Multiple usernames detected."
            )

        st.info(
            "Decision Recovery Memory: This decision can be recorded "
            "for future investigation."
        )

        st.caption(
            "Analysis time: "
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

# ==========================================================
# LIVE LOGIN SIMULATION
# ==========================================================

elif mode == "Live Login Simulation":

    st.subheader("📡 Live Login Activity Simulation")

    st.write(
        "Generate a test login event and analyze it using the trained models."
    )

    if st.button("Generate and Analyze Login Event", type="primary"):

        simulated_event = pd.DataFrame(
            [
                {
                    "login_attempts": np.random.randint(1, 25),
                    "failed_attempts": np.random.randint(0, 18),
                    "time_between_attempts": np.random.uniform(0.5, 60),
                    "unique_usernames": np.random.randint(1, 8),
                    "ip_reputation": np.random.uniform(0.0, 1.0)
                }
            ]
        )

        result = detect_activity(
            simulated_event,
            random_forest,
            isolation_forest,
            scaler
        )

        st.subheader("Generated Login Event")

        st.dataframe(
            simulated_event,
            use_container_width=True
        )

        final_result = result["AI Result"].iloc[0]

        if final_result == "Attack":
            st.error("🚨 AI Alert: Suspicious Login Event")
        else:
            st.success("✅ AI Result: Normal Login Event")

        st.write(
            "Random Forest Prediction:",
            int(result["Random Forest"].iloc[0])
        )

        st.write(
            "Isolation Forest Prediction:",
            int(result["Isolation Forest"].iloc[0])
        )

        st.caption(
            "Event analyzed at "
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "AI-Based Brute Force Attack Detection Tool | "
    "Random Forest + Isolation Forest + Three-Memory Trust Intelligence"
)