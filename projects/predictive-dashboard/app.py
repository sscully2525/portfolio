import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Try to import Prophet, fallback to simple forecasting if not available
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Page configuration
st.set_page_config(
    page_title="Predictive Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subheader {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #475569;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #6366f1;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
    }
    .info-box {
        background: #1e293b;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #6366f1;
        margin: 1rem 0;
    }
    .success-box {
        background: #064e3b;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 Predictive Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Upload your time series data and generate forecasts with confidence intervals</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.subheader("Forecast Settings")
    forecast_periods = st.slider("Forecast Periods", 7, 365, 30, 
                                  help="Number of future periods to predict")
    
    confidence_interval = st.slider("Confidence Interval (%)", 80, 99, 95,
                                   help="Prediction interval width")
    
    st.subheader("Model Selection")
    model_type = st.selectbox(
        "Forecasting Model",
        ["Auto (Recommended)", "Prophet", "Linear Regression", "Polynomial", "Moving Average", "Exponential Smoothing"],
        help="Select the forecasting algorithm"
    )
    
    if not PROPHET_AVAILABLE and model_type == "Prophet":
        st.warning("⚠️ Prophet not installed. Install with: `pip install prophet`")
    
    st.markdown("---")
    
    st.subheader("Data Options")
    detect_anomalies = st.checkbox("🔍 Anomaly Detection", value=True)
    show_trends = st.checkbox("📈 Trend Analysis", value=True)
    show_seasonality = st.checkbox("🔄 Seasonality Decomposition", value=True)
    
    st.markdown("---")
    
    st.info("💡 **Supported formats:** CSV, Excel (.xlsx), JSON")

# Helper functions
def generate_sample_data():
    """Generate sample time series data"""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=365, freq='D')
    
    # Create trend
    trend = np.linspace(100, 200, 365)
    
    # Add seasonality
    seasonality = 20 * np.sin(2 * np.pi * np.arange(365) / 365.25)
    
    # Add weekly pattern
    weekly = 10 * np.sin(2 * np.pi * np.arange(365) / 7)
    
    # Add noise
    noise = np.random.normal(0, 10, 365)
    
    # Combine
    values = trend + seasonality + weekly + noise
    
    # Add some anomalies
    anomaly_indices = np.random.choice(365, 5, replace=False)
    values[anomaly_indices] += np.random.choice([-50, 50], 5)
    
    df = pd.DataFrame({
        'date': dates,
        'value': values
    })
    
    return df

def simple_forecast(df, periods, model_type='linear'):
    """Simple forecasting using various methods"""
    df = df.copy()
    df['ds'] = pd.to_datetime(df.iloc[:, 0])
    df['y'] = df.iloc[:, 1]
    
    # Create time features
    df['days'] = (df['ds'] - df['ds'].min()).dt.days
    
    if model_type == 'Linear Regression':
        X = df[['days']].values
        y = df['y'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Forecast
        last_day = df['days'].max()
        future_days = np.arange(last_day + 1, last_day + periods + 1)
        predictions = model.predict(future_days.reshape(-1, 1))
        
        # Confidence intervals (simple)
        residuals = y - model.predict(X)
        std_residuals = np.std(residuals)
        
        return predictions, predictions - 1.96*std_residuals, predictions + 1.96*std_residuals
    
    elif model_type == 'Polynomial':
        X = df[['days']].values
        y = df['y'].values
        
        poly = PolynomialFeatures(degree=3)
        X_poly = poly.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        last_day = df['days'].max()
        future_days = np.arange(last_day + 1, last_day + periods + 1)
        future_poly = poly.transform(future_days.reshape(-1, 1))
        predictions = model.predict(future_poly)
        
        residuals = y - model.predict(X_poly)
        std_residuals = np.std(residuals)
        
        return predictions, predictions - 1.96*std_residuals, predictions + 1.96*std_residuals
    
    elif model_type == 'Moving Average':
        window = min(30, len(df) // 4)
        ma = df['y'].rolling(window=window).mean()
        
        # Extend with last value
        last_values = df['y'].tail(window).values
        predictions = []
        
        for i in range(periods):
            pred = np.mean(last_values)
            predictions.append(pred)
            last_values = np.append(last_values[1:], pred)
        
        predictions = np.array(predictions)
        std_residuals = df['y'].std()
        
        return predictions, predictions - 1.96*std_residuals, predictions + 1.96*std_residuals
    
    elif model_type == 'Exponential Smoothing':
        alpha = 0.3
        values = df['y'].values
        
        # Initialize
        smoothed = [values[0]]
        for i in range(1, len(values)):
            smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[-1])
        
        # Forecast
        predictions = []
        last_smoothed = smoothed[-1]
        
        for i in range(periods):
            predictions.append(last_smoothed)
        
        predictions = np.array(predictions)
        std_residuals = df['y'].std()
        
        return predictions, predictions - 1.96*std_residuals, predictions + 1.96*std_residuals
    
    else:  # Default to moving average
        return simple_forecast(df, periods, 'Moving Average')

def prophet_forecast(df, periods, interval_width=0.95):
    """Forecast using Prophet"""
    if not PROPHET_AVAILABLE:
        return None, None, None
    
    df = df.copy()
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'])
    
    model = Prophet(
        interval_width=interval_width/100,
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    
    model.fit(df)
    
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    # Get only future predictions
    future_forecast = forecast.tail(periods)
    
    return (
        future_forecast['yhat'].values,
        future_forecast['yhat_lower'].values,
        future_forecast['yhat_upper'].values
    )

def detect_anomalies_zscore(df, threshold=3):
    """Detect anomalies using Z-score method"""
    df = df.copy()
    values = df.iloc[:, 1]
    
    z_scores = np.abs((values - values.mean()) / values.std())
    anomalies = z_scores > threshold
    
    return anomalies

def calculate_metrics(actual, predicted):
    """Calculate forecast accuracy metrics"""
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    
    return {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE (%)': mape
    }

# Main content
tab1, tab2, tab3 = st.tabs(["📤 Upload Data", "📈 Forecast", "📊 Insights"])

with tab1:
    st.subheader("Upload Your Time Series Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'json'],
            help="File should have 2 columns: date and value"
        )
    
    with col2:
        st.markdown("### Or use sample data")
        use_sample = st.button("📊 Load Sample Data", use_container_width=True)
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            
            st.session_state['data'] = df
            st.session_state['data_loaded'] = True
            st.success(f"✅ Loaded {len(df)} records from {uploaded_file.name}")
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    
    elif use_sample:
        df = generate_sample_data()
        st.session_state['data'] = df
        st.session_state['data_loaded'] = True
        st.success("✅ Sample data loaded!")
    
    # Display data preview
    if 'data_loaded' in st.session_state and st.session_state['data_loaded']:
        df = st.session_state['data']
        
        st.markdown("### Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Data info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Date Range", f"{(pd.to_datetime(df.iloc[:, 0]).max() - pd.to_datetime(df.iloc[:, 0]).min()).days} days")
        with col3:
            st.metric("Mean Value", f"{df.iloc[:, 1].mean():.2f}")
        with col4:
            st.metric("Std Dev", f"{df.iloc[:, 1].std():.2f}")
        
        # Raw data plot
        st.markdown("### Raw Data Visualization")
        fig = px.line(
            df, 
            x=df.columns[0], 
            y=df.columns[1],
            title="Time Series Data",
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='#1e293b',
            paper_bgcolor='#0f172a',
            font_color='#e2e8f0'
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    if 'data_loaded' not in st.session_state or not st.session_state['data_loaded']:
        st.info("👆 Please upload data or load sample data first")
    else:
        df = st.session_state['data']
        
        st.subheader("🔮 Forecast Generation")
        
        if st.button("🚀 Generate Forecast", use_container_width=True):
            with st.spinner("Training model and generating forecast..."):
                
                # Select model
                if model_type == "Auto (Recommended)":
                    if PROPHET_AVAILABLE:
                        selected_model = "Prophet"
                    else:
                        selected_model = "Polynomial"
                else:
                    selected_model = model_type
                
                # Generate forecast
                if selected_model == "Prophet" and PROPHET_AVAILABLE:
                    yhat, yhat_lower, yhat_upper = prophet_forecast(
                        df, forecast_periods, confidence_interval
                    )
                else:
                    yhat, yhat_lower, yhat_upper = simple_forecast(
                        df, forecast_periods, selected_model
                    )
                
                # Create future dates
                last_date = pd.to_datetime(df.iloc[:, 0]).max()
                future_dates = pd.date_range(
                    start=last_date + timedelta(days=1),
                    periods=forecast_periods,
                    freq='D'
                )
                
                # Store results
                st.session_state['forecast'] = {
                    'dates': future_dates,
                    'predictions': yhat,
                    'lower': yhat_lower,
                    'upper': yhat_upper,
                    'model': selected_model
                }
                
                st.success(f"✅ Forecast generated using {selected_model} model!")
        
        # Display forecast
        if 'forecast' in st.session_state:
            forecast = st.session_state['forecast']
            df = st.session_state['data']
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{forecast['predictions'][-1]:.2f}</div>
                    <div class="metric-label">Final Prediction</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                trend = "📈" if forecast['predictions'][-1] > forecast['predictions'][0] else "📉"
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{trend}</div>
                    <div class="metric-label">Trend Direction</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                uncertainty = np.mean(forecast['upper'] - forecast['lower'])
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">±{uncertainty:.2f}</div>
                    <div class="metric-label">Avg Uncertainty</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col4:
                growth = ((forecast['predictions'][-1] - df.iloc[:, 1].iloc[-1]) / df.iloc[:, 1].iloc[-1] * 100)
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-value">{growth:+.1f}%</div>
                    <div class="metric-label">Projected Growth</div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Forecast plot
            st.subheader("📈 Forecast Visualization")
            
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df.iloc[:, 0]),
                y=df.iloc[:, 1],
                name='Historical',
                line=dict(color='#6366f1', width=2),
                mode='lines'
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast['dates'],
                y=forecast['predictions'],
                name='Forecast',
                line=dict(color='#10b981', width=2, dash='dash'),
                mode='lines'
            ))
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=np.concatenate([forecast['dates'], forecast['dates'][::-1]]),
                y=np.concatenate([forecast['upper'], forecast['lower'][::-1]]),
                fill='toself',
                fillcolor='rgba(16, 185, 129, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name=f'{confidence_interval}% Confidence Interval',
                hoverinfo='skip'
            ))
            
            fig.update_layout(
                title="Time Series Forecast with Confidence Intervals",
                xaxis_title="Date",
                yaxis_title="Value",
                template="plotly_dark",
                plot_bgcolor='#1e293b',
                paper_bgcolor='#0f172a',
                font_color='#e2e8f0',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast table
            with st.expander("📋 View Forecast Data"):
                forecast_df = pd.DataFrame({
                    'Date': forecast['dates'],
                    'Forecast': forecast['predictions'],
                    'Lower Bound': forecast['lower'],
                    'Upper Bound': forecast['upper']
                })
                st.dataframe(forecast_df, use_container_width=True)
                
                # Download button
                csv = forecast_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Forecast (CSV)",
                    data=csv,
                    file_name=f"forecast_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

with tab3:
    if 'data_loaded' not in st.session_state or not st.session_state['data_loaded']:
        st.info("👆 Please upload data first")
    else:
        df = st.session_state['data']
        
        st.subheader("📊 Data Insights & Analysis")
        
        # Anomaly Detection
        if detect_anomalies:
            st.markdown("### 🔍 Anomaly Detection")
            
            anomalies = detect_anomalies_zscore(df)
            anomaly_count = anomalies.sum()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Anomalies Detected", anomaly_count)
            
            with col2:
                if anomaly_count > 0:
                    st.warning(f"⚠️ Found {anomaly_count} anomalous data points")
                else:
                    st.success("✅ No significant anomalies detected")
            
            # Anomaly plot
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df.iloc[:, 0]),
                y=df.iloc[:, 1],
                name='Normal',
                line=dict(color='#6366f1', width=2),
                mode='lines'
            ))
            
            if anomaly_count > 0:
                fig.add_trace(go.Scatter(
                    x=pd.to_datetime(df.iloc[:, 0])[anomalies],
                    y=df.iloc[:, 1][anomalies],
                    name='Anomaly',
                    mode='markers',
                    marker=dict(color='#ef4444', size=10, symbol='x')
                ))
            
            fig.update_layout(
                title="Anomaly Detection (Z-Score Method)",
                template="plotly_dark",
                plot_bgcolor='#1e293b',
                paper_bgcolor='#0f172a'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Trend Analysis
        if show_trends:
            st.markdown("### 📈 Trend Analysis")
            
            # Calculate rolling statistics
            df['rolling_mean_7'] = df.iloc[:, 1].rolling(window=7).mean()
            df['rolling_mean_30'] = df.iloc[:, 1].rolling(window=30).mean()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df.iloc[:, 0]),
                y=df.iloc[:, 1],
                name='Original',
                line=dict(color='#6366f1', width=1),
                opacity=0.6
            ))
            
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df.iloc[:, 0]),
                y=df['rolling_mean_7'],
                name='7-Day MA',
                line=dict(color='#10b981', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df.iloc[:, 0]),
                y=df['rolling_mean_30'],
                name='30-Day MA',
                line=dict(color='#f59e0b', width=2)
            ))
            
            fig.update_layout(
                title="Trend Analysis with Moving Averages",
                template="plotly_dark",
                plot_bgcolor='#1e293b',
                paper_bgcolor='#0f172a'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Seasonality
        if show_seasonality:
            st.markdown("### 🔄 Seasonality Analysis")
            
            df['month'] = pd.to_datetime(df.iloc[:, 0]).dt.month
            df['day_of_week'] = pd.to_datetime(df.iloc[:, 0]).dt.dayofweek
            df['week_of_year'] = pd.to_datetime(df.iloc[:, 0]).dt.isocalendar().week
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Monthly pattern
                monthly_avg = df.groupby('month')[df.columns[1]].mean()
                fig = px.bar(
                    x=monthly_avg.index,
                    y=monthly_avg.values,
                    labels={'x': 'Month', 'y': 'Average Value'},
                    title="Monthly Seasonality",
                    template="plotly_dark"
                )
                fig.update_layout(
                    plot_bgcolor='#1e293b',
                    paper_bgcolor='#0f172a'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Weekly pattern
                daily_avg = df.groupby('day_of_week')[df.columns[1]].mean()
                day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                fig = px.bar(
                    x=[day_names[i] for i in daily_avg.index],
                    y=daily_avg.values,
                    labels={'x': 'Day of Week', 'y': 'Average Value'},
                    title="Weekly Seasonality",
                    template="plotly_dark"
                )
                fig.update_layout(
                    plot_bgcolor='#1e293b',
                    paper_bgcolor='#0f172a'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Statistical Summary
        st.markdown("### 📋 Statistical Summary")
        
        stats_df = pd.DataFrame({
            'Metric': ['Count', 'Mean', 'Std Dev', 'Min', '25%', 'Median', '75%', 'Max'],
            'Value': [
                df.iloc[:, 1].count(),
                df.iloc[:, 1].mean(),
                df.iloc[:, 1].std(),
                df.iloc[:, 1].min(),
                df.iloc[:, 1].quantile(0.25),
                df.iloc[:, 1].median(),
                df.iloc[:, 1].quantile(0.75),
                df.iloc[:, 1].max()
            ]
        })
        
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6b7280;'>Built with ❤️ using Streamlit | Predictive Analytics Dashboard v1.0</p>", unsafe_allow_html=True)
