import streamlit as st
import json
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import csv

# Page configuration
st.set_page_config(
    page_title="IoT Environmental Monitoring Dashboard",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #f5f7fa;
    }
    
    /* Title bar */
    .title-bar {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .title-text {
        color: white !important;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
        letter-spacing: 1px;
    }
    
    .subtitle-text {
        color: #ecf0f1 !important;
        font-size: 1.2rem;
        text-align: center;
        margin-top: 8px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Row indicator */
    .row-indicator {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white !important;
        padding: 15px 30px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.3);
        letter-spacing: 0.5px;
    }
    
    /* Metric cards with enhanced shadows */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 28px;
        box-shadow: 
            0 10px 30px rgba(0,0,0,0.12),
            0 3px 10px rgba(0,0,0,0.08),
            inset 0 1px 2px rgba(255,255,255,0.8);
        border-left: 6px solid;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 
            0 15px 45px rgba(0,0,0,0.15),
            0 5px 20px rgba(0,0,0,0.1),
            inset 0 1px 2px rgba(255,255,255,0.9);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card.normal {
        border-left-color: #27ae60;
    }
    
    .metric-card.warning {
        border-left-color: #f39c12;
    }
    
    .metric-card.danger {
        border-left-color: #e74c3c;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #5a6c7d !important;
        font-weight: 600;
        margin-bottom: 12px;
        display: block;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        color: #1a252f !important;
        line-height: 1.2;
        display: inline-block;
    }
    
    .metric-unit {
        font-size: 1.4rem;
        color: #7f8c8d !important;
        margin-left: 8px;
        font-weight: 600;
    }
    
    .metric-status {
        margin-top: 15px;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.95rem;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-normal {
        background: #d4edda !important;
        color: #155724 !important;
        border: 2px solid #28a745;
    }
    
    .status-warning {
        background: #fff3cd !important;
        color: #856404 !important;
        border: 2px solid #ffc107;
    }
    
    .status-danger {
        background: #f8d7da !important;
        color: #721c24 !important;
        border: 2px solid #dc3545;
    }
    
    /* Graph container with enhanced shadow */
    .graph-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12), 0 2px 10px rgba(0,0,0,0.08);
        margin-top: 20px;
        border: 1px solid rgba(189, 195, 199, 0.3);
        transition: all 0.3s ease;
    }
    
    .graph-container:hover {
        box-shadow: 0 12px 40px rgba(0,0,0,0.15), 0 4px 15px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .graph-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 20px;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Enhanced plotly chart container */
    .js-plotly-plot {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Metric value styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    /* Force all text to be black and visible */
    h1, h2, h3, h4, h5, h6, p, span, div, label, input, button, a {
        color: #000000 !important;
    }
    
    /* Section headers */
    .section-header {
        color: #000000 !important;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    
    .section-subtitle {
        color: #000000 !important;
        font-size: 0.9rem;
    }
    
    /* Streamlit elements */
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: #000000 !important;
    }
    
    [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# State file path
STATE_FILE = 'current_state.json'
CONFIG_FILE = 'config.json'
DATA_FILE = 'data.csv'
TRACKER_FILE = 'row_tracker.txt'

def get_row_info():
    """Get current row number and total rows"""
    try:
        # Get current row index
        current_row = 0
        if os.path.exists(TRACKER_FILE):
            with open(TRACKER_FILE, 'r') as f:
                current_row = int(f.read().strip())
        
        # Get total rows
        total_rows = 0
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                total_rows = len(list(csv.reader(f))) - 1  # Exclude header
        
        return current_row + 1, total_rows  # Return 1-based index
    except Exception:
        return 0, 0

def load_current_data():
    """Load current sensor data from JSON file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        else:
            return {
                'co2': 0,
                'temperature': 0,
                'humidity': 0,
                'status': 'No Data',
                'warnings': [],
                'timestamp': datetime.now().isoformat()
            }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def load_config():
    """Load configuration settings"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        return None

def create_enhanced_visualization(co2, temp, humidity, config):
    """Create beautiful gauge charts with proper scaling for each metric"""
    
    # Get thresholds from config
    temp_threshold = config.get('temperature_limit', 22) if config else 22
    humid_threshold = config.get('humidity_limit', 45) if config else 45
    co2_threshold = 1000  # Standard CO2 threshold
    
    # Define colors based on thresholds
    def get_gauge_color(value, threshold, danger_threshold=None):
        if danger_threshold and value >= danger_threshold:
            return '#e74c3c'  # Red - Danger
        elif value > threshold:
            return '#f39c12'  # Orange - Warning
        else:
            return '#2ecc71'  # Green - Normal
    
    co2_color = get_gauge_color(co2, co2_threshold, co2_threshold * 1.2)
    temp_color = get_gauge_color(temp, temp_threshold, temp_threshold + 3)
    humid_color = get_gauge_color(humidity, humid_threshold, humid_threshold + 10)
    
    # Create 3 gauge charts in subplots (better for different scales)
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('CO₂ Level (ppm)', 'Temperature (°C)', 'Humidity (%)'),
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
        horizontal_spacing=0.1
    )
    
    # CO2 Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=co2,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{co2}</b> ppm", 'font': {'size': 18, 'color': '#000000'}},
        delta={'reference': co2_threshold, 'increasing': {'color': "#e74c3c"}},
        gauge={
            'axis': {'range': [None, 1500], 'tickwidth': 2, 'tickcolor': "#000000"},
            'bar': {'color': co2_color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': "#2c3e50",
            'steps': [
                {'range': [0, co2_threshold], 'color': 'rgba(46, 204, 113, 0.2)'},
                {'range': [co2_threshold, co2_threshold * 1.2], 'color': 'rgba(243, 156, 18, 0.2)'},
                {'range': [co2_threshold * 1.2, 1500], 'color': 'rgba(231, 76, 60, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#f39c12", 'width': 4},
                'thickness': 0.75,
                'value': co2_threshold
            }
        }
    ), row=1, col=1)
    
    # Temperature Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=temp,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{temp}</b> °C", 'font': {'size': 18, 'color': '#000000'}},
        delta={'reference': temp_threshold, 'increasing': {'color': "#e74c3c"}},
        gauge={
            'axis': {'range': [0, 40], 'tickwidth': 2, 'tickcolor': "#000000"},
            'bar': {'color': temp_color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': "#2c3e50",
            'steps': [
                {'range': [0, temp_threshold], 'color': 'rgba(46, 204, 113, 0.2)'},
                {'range': [temp_threshold, temp_threshold + 3], 'color': 'rgba(243, 156, 18, 0.2)'},
                {'range': [temp_threshold + 3, 40], 'color': 'rgba(231, 76, 60, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#f39c12", 'width': 4},
                'thickness': 0.75,
                'value': temp_threshold
            }
        }
    ), row=1, col=2)
    
    # Humidity Gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=humidity,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{humidity}</b> %", 'font': {'size': 18, 'color': '#000000'}},
        delta={'reference': humid_threshold, 'increasing': {'color': "#e74c3c"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "#000000"},
            'bar': {'color': humid_color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': "#2c3e50",
            'steps': [
                {'range': [0, humid_threshold], 'color': 'rgba(46, 204, 113, 0.2)'},
                {'range': [humid_threshold, humid_threshold + 10], 'color': 'rgba(243, 156, 18, 0.2)'},
                {'range': [humid_threshold + 10, 100], 'color': 'rgba(231, 76, 60, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#f39c12", 'width': 4},
                'thickness': 0.75,
                'value': humid_threshold
            }
        }
    ), row=1, col=3)
    
    # Update layout
    fig.update_layout(
        title={
            'text': '🎯 Real-Time Gauge Readings',
            'font': {'size': 24, 'color': '#000000', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=450,
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=20),
        font=dict(family="Arial", size=14, color="#000000")
    )
    
    # Update subplot titles to be black
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=16, color='#000000', family='Arial Bold')
    
    return fig

def create_gauge_chart(value, title, max_value, color, threshold=None):
    """Create a beautiful gauge chart for metrics"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'size': 20, 'color': '#2c3e50'}},
        delta={'reference': threshold if threshold else 0},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, max_value * 0.5], 'color': '#ecf0f1'},
                {'range': [max_value * 0.5, max_value * 0.8], 'color': '#dfe6e9'},
                {'range': [max_value * 0.8, max_value], 'color': '#b2bec3'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold if threshold else max_value
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#2c3e50", 'family': "Arial"}
    )
    
    return fig

def create_comparison_chart(co2, temp, humidity):
    """Create a modern bar chart comparing all metrics"""
    fig = go.Figure(data=[
        go.Bar(
            x=['CO₂', 'Temperature', 'Humidity'],
            y=[co2, temp, humidity],
            marker=dict(
                color=['#e74c3c', '#3498db', '#1abc9c'],
                line=dict(color='rgba(0,0,0,0.3)', width=2)
            ),
            text=[f'{co2} ppm', f'{temp} °C', f'{humidity} %'],
            textposition='outside',
            textfont=dict(size=14, color='white', family='Arial Black')
        )
    ])
    
    fig.update_layout(
        title={
            'text': '📊 Current Readings Comparison',
            'font': {'size': 22, 'color': 'white', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            title='Metrics',
            titlefont=dict(size=16, color='white'),
            tickfont=dict(size=14, color='white', family='Arial Black')
        ),
        yaxis=dict(
            title='Values',
            titlefont=dict(size=16, color='white'),
            tickfont=dict(size=14, color='white'),
            gridcolor='rgba(255,255,255,0.2)'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

# Main app
def main():
    # Professional Title Bar
    st.markdown("""
    <div class="title-bar">
        <h1 class="title-text">🌡️ IoT Environmental Monitoring Dashboard</h1>
        <p class="subtitle-text">Real-Time Air Quality Monitoring System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load configuration
    config = load_config()
    
    # Get row information
    current_row, total_rows = get_row_info()
    
    # Row indicator
    if total_rows > 0:
        st.markdown(f"""
        <div class="row-indicator">
            📍 Now displaying Row {current_row} of {total_rows}
        </div>
        """, unsafe_allow_html=True)
    
    # Auto-refresh control (top right)
    col_left, col_right = st.columns([4, 1])
    with col_right:
        auto_refresh = st.checkbox("Auto-refresh", value=True)
    
    # Load current data
    data = load_current_data()
    
    if data:
        co2 = data.get('co2', 0)
        temp = data.get('temperature', 0)
        humidity = data.get('humidity', 0)
        status = data.get('status', 'No Data')
        warnings = data.get('warnings', [])
        timestamp = data.get('timestamp', '')
        
        # Get thresholds
        temp_threshold = config.get('temperature_limit', 22) if config else 22
        humid_threshold = config.get('humidity_limit', 45) if config else 45
        co2_threshold = 1000
        
        # Determine status for each metric
        def get_status(value, threshold, danger_mult=1.2):
            if value >= threshold * danger_mult:
                return 'danger'
            elif value > threshold:
                return 'warning'
            else:
                return 'normal'
        
        co2_status = get_status(co2, co2_threshold)
        temp_status = get_status(temp, temp_threshold, 1.15)
        humid_status = get_status(humidity, humid_threshold, 1.15)
        
        # Main display section - Two columns
        left_col, right_col = st.columns([1, 1])
        
        with left_col:
            st.markdown("""
            <div style='text-align: center; margin-bottom: 15px;'>
                <h3 style='color: #2c3e50; font-weight: 700; text-shadow: 1px 1px 3px rgba(0,0,0,0.1);'>
                    � Current Sensor Readings
                </h3>
                <p style='color: #7f8c8d; font-size: 0.9rem; margin-top: -10px;'>
                    Live environmental data
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # CO2 Card
            status_label_co2 = "🟢 Normal" if co2_status == 'normal' else ("🟠 Warning" if co2_status == 'warning' else "🔴 Danger")
            st.markdown(f"""
            <div class="metric-card {co2_status}">
                <div class="metric-label">💨 Carbon Dioxide (CO₂)</div>
                <div class="metric-value">{co2}<span class="metric-unit">ppm</span></div>
                <div class="metric-status status-{co2_status}">{status_label_co2}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Temperature Card
            status_label_temp = "🟢 Normal" if temp_status == 'normal' else ("🟠 Warning" if temp_status == 'warning' else "🔴 Danger")
            st.markdown(f"""
            <div class="metric-card {temp_status}">
                <div class="metric-label">🌡️ Temperature</div>
                <div class="metric-value">{temp}<span class="metric-unit">°C</span></div>
                <div class="metric-status status-{temp_status}">{status_label_temp}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Humidity Card
            status_label_humid = "🟢 Normal" if humid_status == 'normal' else ("� Warning" if humid_status == 'warning' else "🔴 Danger")
            st.markdown(f"""
            <div class="metric-card {humid_status}">
                <div class="metric-label">💧 Humidity</div>
                <div class="metric-value">{humidity}<span class="metric-unit">%</span></div>
                <div class="metric-status status-{humid_status}">{status_label_humid}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with right_col:
            st.markdown("""
            <div style='text-align: center; margin-bottom: 15px;'>
                <h3 style='color: #2c3e50; font-weight: 700; text-shadow: 1px 1px 3px rgba(0,0,0,0.1);'>
                    � Live Sensor Visualization
                </h3>
                <p style='color: #7f8c8d; font-size: 0.9rem; margin-top: -10px;'>
                    Real-time readings with threshold indicators
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced visualization with threshold zones
            fig = create_enhanced_visualization(co2, temp, humidity, config)
            
            # Wrap in styled container
            st.markdown('<div class="graph-container">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True, key="main_chart")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Warnings section (if any)
        if warnings:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### ⚠️ Active Alerts")
            for warning in warnings:
                st.error(warning)
        
        # Footer with timestamp and system info
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        footer_col1, footer_col2, footer_col3 = st.columns(3)
        
        with footer_col1:
            if timestamp:
                dt = datetime.fromisoformat(timestamp)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                            padding: 15px; border-radius: 10px; text-align: center;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #90caf9;'>
                    <p style='margin: 0; color: #000000; font-size: 1rem; font-weight: 700;'>
                        🕒 Last Updated: {dt.strftime('%H:%M:%S')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        with footer_col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                        padding: 15px; border-radius: 10px; text-align: center;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #90caf9;'>
                <p style='margin: 0; color: #000000; font-size: 1rem; font-weight: 700;'>
                    ⏱️ Update Interval: {config.get('update_interval', 20)}s
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with footer_col3:
            email_status = "✅ Enabled" if config and config.get('email', {}).get('enabled', False) else "❌ Disabled"
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                        padding: 15px; border-radius: 10px; text-align: center;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #90caf9;'>
                <p style='margin: 0; color: #000000; font-size: 1rem; font-weight: 700;'>
                    📧 Email Alerts: {email_status}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
    else:
        st.error("⚠️ No data available. Please ensure main_csv.py is running.")
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(3)
        st.rerun()

if __name__ == "__main__":
    main()
