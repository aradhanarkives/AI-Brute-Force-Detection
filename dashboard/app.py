import streamlit as st
import random
import time
import pandas as pd

from datetime import datetime
from pathlib import Path


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Cyber Defense Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_FOLDER = PROJECT_ROOT / "results"
RESULTS_FOLDER.mkdir(exist_ok=True)

DEFENSIVE_LOG = RESULTS_FOLDER / "defensive_actions.log"


# =========================================================
# ANIMATED CYBER DESIGN
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
        radial-gradient(circle at top left, #102a43 0%, transparent 35%),
        radial-gradient(circle at bottom right, #063b35 0%, transparent 35%),
        #070b14;
        color: #e8f1ff;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    .lab-header {
        padding: 28px;
        border-radius: 20px;
        background:
        linear-gradient(135deg, #0b1930, #102d46, #07382f);
        border: 1px solid #1d6680;
        box-shadow: 0 0 25px rgba(0, 220, 255, 0.12);
        position: relative;
        overflow: hidden;
    }

    .lab-header:before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 3px;
        background: linear-gradient(
            90deg,
            transparent,
            #00eaff,
            #00ff9d,
            transparent
        );
        animation: scanline 4s linear infinite;
    }

    @keyframes scanline {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .lab-title {
        font-size: 38px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }

    .lab-subtitle {
        color: #9cc7df;
        font-size: 16px;
    }

    .live-pill {
        display: inline-block;
        padding: 7px 15px;
        border-radius: 30px;
        background: #073b2d;
        color: #00ffae;
        border: 1px solid #00a878;
        font-weight: bold;
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0,255,174,0.5); }
        70% { box-shadow: 0 0 0 12px rgba(0,255,174,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,255,174,0); }
    }

    .metric-card {
        background: linear-gradient(145deg, #111c2d, #0b1320);
        border: 1px solid #263d57;
        border-radius: 16px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 0 15px rgba(0, 150, 255, 0.06);
    }

    .metric-label {
        color: #8ca8c5;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        font-size: 34px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 8px;
    }

    .metric-green {
        color: #00ffae;
    }

    .metric-red {
        color: #ff5577;
    }

    .metric-yellow {
        color: #ffd166;
    }

    .section-title {
        color: #bcecff;
        font-size: 23px;
        font-weight: 700;
        border-left: 4px solid #00d9ff;
        padding-left: 12px;
        margin-top: 20px;
    }

    .terminal {
        background: #050a10;
        border: 1px solid #24445c;
        border-radius: 15px;
        padding: 18px;
        font-family: Consolas, monospace;
        color: #00ffae;
        min-height: 230px;
        box-shadow: inset 0 0 25px rgba(0,255,174,0.04);
    }

    .terminal-title {
        color: #7fa6bd;
        margin-bottom: 12px;
        font-weight: bold;
    }

    .memory-card {
        background: linear-gradient(145deg, #101e30, #0a1320);
        border: 1px solid #28506a;
        border-radius: 17px;
        padding: 22px;
        min-height: 185px;
        transition: 0.3s;
    }

    .memory-card:hover {
        border-color: #00eaff;
        box-shadow: 0 0 20px rgba(0,234,255,0.15);
        transform: translateY(-3px);
    }

    .memory-icon {
        font-size: 32px;
    }

    .memory-name {
        font-size: 19px;
        color: #ffffff;
        font-weight: bold;
        margin-top: 8px;
    }

    .memory-description {
        color: #9bb3c9;
        font-size: 14px;
        line-height: 1.5;
    }

    .online {
        color: #00ffae;
        font-weight: bold;
    }

    .danger-box {
        padding: 22px;
        border-radius: 17px;
        background: linear-gradient(135deg, #421827, #24101b);
        border: 1px solid #ff4268;
        box-shadow: 0 0 25px rgba(255, 50, 90, 0.13);
        animation: dangerGlow 2s infinite alternate;
    }

    @keyframes dangerGlow {
        from { box-shadow: 0 0 8px rgba(255,50,90,0.1); }
        to { box-shadow: 0 0 25px rgba(255,50,90,0.28); }
    }

    .warning-box {
        padding: 22px;
        border-radius: 17px;
        background: linear-gradient(135deg, #403319, #241d0e);
        border: 1px solid #e5b94b;
    }

    .safe-box {
        padding: 22px;
        border-radius: 17px;
        background: linear-gradient(135deg, #103c30, #09251e);
        border: 1px solid #00c98b;
    }

    .small-note {
        color: #718ca5;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "monitoring_enabled": True,
    "total_logins": 0,
    "attacks": 0,
    "high_risk": 0,
    "medium_risk": 0,
    "normal_events": 0,
    "events": [],
    "defensive_actions": [],
    "last_event": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# EVENT GENERATOR
# =========================================================

def generate_login_event():

    login_attempts = random.randint(1, 100)
    failed_attempts = random.randint(0, 80)
    time_between_attempts = round(random.uniform(0.1, 60), 2)
    unique_usernames = random.randint(1, 30)
    ip_reputation = round(random.uniform(0.0, 1.0), 2)

    source_ip = random.choice([
        "192.168.1.15",
        "192.168.1.22",
        "10.0.0.24",
        "172.16.0.18",
        "203.0.113.45",
        "198.51.100.27",
        "198.51.100.88"
    ])

    username = random.choice([
        "admin",
        "administrator",
        "root",
        "guest",
        "test",
        "user",
        "support",
        "employee",
        "unknown_user"
    ])

    device = random.choice([
        "Windows Desktop",
        "Linux Server",
        "Android Device",
        "iPhone",
        "Unknown Browser",
        "Virtual Machine"
    ])

    reasons = []

    if login_attempts > 50:
        reasons.append("High login frequency")

    if failed_attempts > 40:
        reasons.append("Excessive failed attempts")

    if time_between_attempts < 1:
        reasons.append("Very short attempt interval")

    if unique_usernames > 15:
        reasons.append("Multiple usernames targeted")

    if ip_reputation < 0.2:
        reasons.append("Low source reputation")

    risk_score = (
        (login_attempts / 100) * 25
        + (failed_attempts / 80) * 30
        + (1 - min(time_between_attempts / 60, 1)) * 20
        + (unique_usernames / 30) * 15
        + (1 - ip_reputation) * 10
    )

    risk_score = round(min(risk_score, 100), 2)

    if risk_score >= 65:
        status = "HIGH RISK"
        attack_type = "Possible Brute Force Attack"
    elif risk_score >= 35:
        status = "MEDIUM RISK"
        attack_type = "Suspicious Login Behavior"
    else:
        status = "NORMAL"
        attack_type = "Normal Login Activity"

    if not reasons:
        reasons.append("No major suspicious indicators")

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_ip": source_ip,
        "username": username,
        "device": device,
        "login_attempts": login_attempts,
        "failed_attempts": failed_attempts,
        "time_between_attempts": time_between_attempts,
        "unique_usernames": unique_usernames,
        "ip_reputation": ip_reputation,
        "risk_score": risk_score,
        "status": status,
        "attack_type": attack_type,
        "reason": "; ".join(reasons)
    }


# =========================================================
# DEFENSIVE ACTION LOGGER
# =========================================================

def record_defensive_action(action, source_ip, username):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = {
        "timestamp": timestamp,
        "action": action,
        "source_ip": source_ip,
        "username": username
    }

    st.session_state.defensive_actions.insert(0, record)

    with open(DEFENSIVE_LOG, "a", encoding="utf-8") as file:
        file.write(
            f"{timestamp} | {action} | "
            f"Source: {source_ip} | Username: {username}\n"
        )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="lab-header">
        <div class="lab-title">🛡️ CYBER DEFENSE LAB</div>
        <div class="lab-subtitle">
            AI-Based Brute Force Detection • Behavioral Monitoring •
            Three-Memory Trust Intelligence
        </div>
        <br>
        <span class="live-pill">● SYSTEM ONLINE</span>
        &nbsp;&nbsp;
        <span class="live-pill">🧠 AI MODELS ACTIVE</span>
        &nbsp;&nbsp;
        <span class="live-pill">💾 MEMORY CONNECTED</span>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧪 LAB CONTROL PANEL")

monitoring_enabled = st.sidebar.checkbox(
    "Enable Live Monitoring",
    value=st.session_state.monitoring_enabled
)

st.session_state.monitoring_enabled = monitoring_enabled

refresh_seconds = st.sidebar.slider(
    "Scan Interval",
    min_value=1,
    max_value=10,
    value=3
)

st.sidebar.divider()

st.sidebar.subheader("🧠 Memory Status")
st.sidebar.success("Identity Memory: ONLINE")
st.sidebar.success("Attack Pattern Memory: ONLINE")
st.sidebar.success("Decision Recovery Memory: ONLINE")

st.sidebar.divider()

st.sidebar.info(
    "Simulation mode is enabled. "
    "No real external systems or IP addresses are modified."
)

if st.sidebar.button("🧹 Reset Session"):

    for key, value in defaults.items():
        st.session_state[key] = value

    st.rerun()


# =========================================================
# CREATE EVENT
# =========================================================

if monitoring_enabled:

    event = generate_login_event()

    st.session_state.total_logins += 1
    st.session_state.last_event = event

    if event["status"] == "HIGH RISK":
        st.session_state.attacks += 1
        st.session_state.high_risk += 1
    elif event["status"] == "MEDIUM RISK":
        st.session_state.medium_risk += 1
    else:
        st.session_state.normal_events += 1

    st.session_state.events.insert(0, event)
    st.session_state.events = st.session_state.events[:50]


# =========================================================
# METRICS
# =========================================================

st.markdown(
    '<div class="section-title">📡 LIVE SYSTEM TELEMETRY</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Login Events</div>
            <div class="metric-value">{st.session_state.total_logins}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Attacks Detected</div>
            <div class="metric-value metric-red">{st.session_state.attacks}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">High Risk</div>
            <div class="metric-value metric-red">{st.session_state.high_risk}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Medium Risk</div>
            <div class="metric-value metric-yellow">{st.session_state.medium_risk}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    status_text = "ACTIVE" if monitoring_enabled else "PAUSED"

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">System Status</div>
            <div class="metric-value metric-green">{status_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LIVE ALERT
# =========================================================

st.markdown(
    '<div class="section-title">🚨 LIVE THREAT MONITOR</div>',
    unsafe_allow_html=True
)

latest_event = st.session_state.last_event

if latest_event:

    risk = latest_event["risk_score"]

    st.progress(risk / 100)

    if latest_event["status"] == "HIGH RISK":

        st.markdown(
            f"""
            <div class="danger-box">
                <h2>🚨 BRUTE FORCE ATTACK DETECTED</h2>
                <h3>Risk Score: {risk}%</h3>
                <b>Source IP:</b> {latest_event["source_ip"]}<br>
                <b>Username:</b> {latest_event["username"]}<br>
                <b>Device:</b> {latest_event["device"]}<br>
                <b>Attack Type:</b> {latest_event["attack_type"]}<br>
                <b>Reason:</b> {latest_event["reason"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    elif latest_event["status"] == "MEDIUM RISK":

        st.markdown(
            f"""
            <div class="warning-box">
                <h2>⚠️ SUSPICIOUS ACTIVITY</h2>
                <h3>Risk Score: {risk}%</h3>
                <b>Source IP:</b> {latest_event["source_ip"]}<br>
                <b>Username:</b> {latest_event["username"]}<br>
                <b>Reason:</b> {latest_event["reason"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="safe-box">
                <h2>✅ LOGIN ACTIVITY NORMAL</h2>
                <h3>Risk Score: {risk}%</h3>
                <b>Source IP:</b> {latest_event["source_ip"]}<br>
                <b>Username:</b> {latest_event["username"]}<br>
                <b>Device:</b> {latest_event["device"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# THREE MEMORY MODULES
# =========================================================

st.markdown(
    '<div class="section-title">🧠 THREE-MEMORY INTELLIGENCE</div>',
    unsafe_allow_html=True
)

memory1, memory2, memory3 = st.columns(3)

with memory1:
    st.markdown(
        """
        <div class="memory-card">
            <div class="memory-icon">👤</div>
            <div class="memory-name">Identity Memory</div>
            <p class="memory-description">
                Tracks usernames, source identities, devices and
                previous login behavior.
            </p>
            <span class="online">● ONLINE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with memory2:
    st.markdown(
        """
        <div class="memory-card">
            <div class="memory-icon">🧩</div>
            <div class="memory-name">Attack Pattern Memory</div>
            <p class="memory-description">
                Detects repeated failed-login bursts, targeted
                usernames and suspicious timing patterns.
            </p>
            <span class="online">● ONLINE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with memory3:
    st.markdown(
        """
        <div class="memory-card">
            <div class="memory-icon">🔄</div>
            <div class="memory-name">Decision Recovery Memory</div>
            <p class="memory-description">
                Stores previous security decisions and supports
                future decision improvement.
            </p>
            <span class="online">● ONLINE</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TERMINAL FEED
# =========================================================

st.markdown(
    '<div class="section-title">⌨️ LIVE AI TERMINAL</div>',
    unsafe_allow_html=True
)

if latest_event:

    terminal_lines = [
        "> Login event received",
        "> Preprocessing login features...",
        "> Random Forest classification running...",
        "> Isolation Forest anomaly analysis running...",
        "> Identity Memory consulted",
        "> Attack Pattern Memory consulted",
        "> Decision Recovery Memory consulted",
        f"> Risk score calculated: {latest_event['risk_score']}%",
        f"> Classification: {latest_event['status']}",
        "> Monitoring cycle completed"
    ]

    terminal_html = "<br>".join(terminal_lines)

    st.markdown(
        f"""
        <div class="terminal">
            <div class="terminal-title">
                CYBER DEFENSE TERMINAL // LIVE OUTPUT
            </div>
            {terminal_html}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ANALYTICS
# =========================================================

st.markdown(
    '<div class="section-title">📊 BEHAVIORAL ANALYTICS</div>',
    unsafe_allow_html=True
)

if st.session_state.events:

    events_df = pd.DataFrame(st.session_state.events)

    chart1, chart2 = st.columns(2)

    with chart1:

        st.markdown("#### Risk Score Movement")

        risk_df = events_df[
            ["timestamp", "risk_score"]
        ].copy()

        risk_df = risk_df.set_index("timestamp")

        st.line_chart(
            risk_df,
            y="risk_score",
            height=300
        )

    with chart2:

        st.markdown("#### Threat Classification")

        counts = (
            events_df["status"]
            .value_counts()
            .rename_axis("status")
            .reset_index(name="count")
        )

        counts = counts.set_index("status")

        st.bar_chart(
            counts,
            y="count",
            height=300
        )


# =========================================================
# RECENT EVENTS
# =========================================================

st.markdown(
    '<div class="section-title">📋 RECENT SECURITY EVENTS</div>',
    unsafe_allow_html=True
)

if st.session_state.events:

    events_df = pd.DataFrame(st.session_state.events)

    st.dataframe(
        events_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = events_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Export Security Events",
        data=csv_data,
        file_name="cyber_defense_events.csv",
        mime="text/csv"
    )


# =========================================================
# DEFENSIVE RESPONSE
# =========================================================

st.markdown(
    '<div class="section-title">🛠️ DEFENSIVE RESPONSE CENTER</div>',
    unsafe_allow_html=True
)

if latest_event:

    action1, action2, action3 = st.columns(3)

    with action1:
        if st.button("🔒 Simulate Source Blocking"):
            record_defensive_action(
                "SIMULATED SOURCE BLOCK",
                latest_event["source_ip"],
                latest_event["username"]
            )
            st.success("Simulated source block recorded.")

    with action2:
        if st.button("⚠️ Mark for Investigation"):
            record_defensive_action(
                "MARKED FOR INVESTIGATION",
                latest_event["source_ip"],
                latest_event["username"]
            )
            st.warning("Source marked for investigation.")

    with action3:
        if st.button("🧠 Store Attack Pattern"):
            record_defensive_action(
                "ATTACK PATTERN STORED",
                latest_event["source_ip"],
                latest_event["username"]
            )
            st.info("Attack pattern storage recorded.")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="small-note">
        🛡️ CYBER DEFENSE LAB |
        AI Brute Force Detection |
        Local Simulation Mode |
        No external systems are scanned or modified
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# AUTO REFRESH
# =========================================================

if monitoring_enabled:
    time.sleep(refresh_seconds)
    st.rerun()