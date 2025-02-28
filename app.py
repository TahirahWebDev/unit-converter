import streamlit as st
import requests
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Unit Converter",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📏"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 5px;
    }
    .stNumberInput input {
        border-radius: 5px;
    }
    .stMarkdown h1 {
        color: #4CAF50;
    }
    .stMarkdown h2 {
        color: #2E86C1;
    }
    .stMarkdown h3 {
        color: #D35400;
    }
    .footer {
        font-size: 14px;
        text-align: center;
        color: #777;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Description
st.title("✨ Unit Converter")
st.markdown("**Convert between various units effortlessly!**")

# Sidebar for settings
st.sidebar.header("⚙️ Settings")

# Unit categories
unit_categories = {
    "Length": ["meters", "kilometers", "centimeters", "millimeters", "inches", "feet", "yards", "miles"],
    "Weight": ["grams", "kilograms", "milligrams", "pounds", "ounces"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Volume": ["liters", "milliliters", "cubic meters", "cubic centimeters", "cubic feet", "cubic inches", "gallons", "quarts", "pints", "cups"],
    "Speed": ["meters/second", "kilometers/hour", "miles/hour", "feet/second", "knots"],
    "Area": ["square meters", "square kilometers", "square centimeters", "square millimeters", "square feet", "square inches", "square yards", "acres", "hectares"],
    "Time": ["seconds", "minutes", "hours", "days", "weeks", "months", "years"],
    "Pressure": ["pascals", "kilopascals", "bars", "atmospheres", "psi"],
    "Frequency": ["hertz", "kilohertz", "megahertz", "gigahertz"],
    "Energy": ["joules", "kilojoules", "calories", "kilocalories", "kilowatt-hours"],
    "Digital Storage": ["bytes", "kilobytes", "megabytes", "gigabytes", "terabytes"],
    "Data Transfer Rate": ["bits/second", "kilobits/second", "megabits/second", "gigabits/second", "bytes/second"],
    "Currency": [
        "USD", "EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF", "CNY", "NZD",  # Commonly used currencies
        "SGD", "HKD", "KRW", "SEK", "NOK", "DKK", "RUB", "TRY", "ZAR", "MXN",  # Additional currencies
        "BRL", "TWD", "THB", "MYR", "IDR", "PHP", "SAR", "AED", "PLN", "HUF",  # More currencies
        "CZK", "ILS", "ARS", "CLP", "COP", "EGP", "NGN", "PKR", "BDT", "VND"   # Even more currencies
    ],
}

# Conversion factors
conversion_factors = {
    "Length": {
        "meters": 1, "kilometers": 0.001, "centimeters": 100, "millimeters": 1000,
        "inches": 39.3701, "feet": 3.28084, "yards": 1.09361, "miles": 0.000621371,
    },
    "Weight": {
        "grams": 1, "kilograms": 0.001, "milligrams": 1000, "pounds": 0.00220462, "ounces": 0.035274,
    },
    "Temperature": {},  # Handled separately
    "Volume": {
        "liters": 1, "milliliters": 1000, "cubic meters": 0.001, "cubic centimeters": 1000,
        "cubic feet": 35.3147, "cubic inches": 61023.7, "gallons": 0.264172, "quarts": 1.05669,
        "pints": 2.11338, "cups": 4.22675,
    },
    "Speed": {
        "meters/second": 1, "kilometers/hour": 3.6, "miles/hour": 2.23694, "feet/second": 3.28084, "knots": 1.94384,
    },
    "Area": {
        "square meters": 1, "square kilometers": 1e-6, "square centimeters": 10000, "square millimeters": 1e6,
        "square feet": 10.7639, "square inches": 1550.0031, "square yards": 1.19599, "acres": 0.000247105, "hectares": 1e-4,
    },
    "Time": {
        "seconds": 1, "minutes": 1/60, "hours": 1/3600, "days": 1/86400, "weeks": 1/604800, 
        "months": 1/2629746, "years": 1/31556952,
    },
    "Pressure": {
        "pascals": 1, "kilopascals": 0.001, "bars": 1e-5, "atmospheres": 9.8692e-6, "psi": 0.000145038,
    },
    "Frequency": {
        "hertz": 1, "kilohertz": 1e-3, "megahertz": 1e-6, "gigahertz": 1e-9,
    },
    "Energy": {
        "joules": 1, "kilojoules": 0.001, "calories": 0.239006, "kilocalories": 0.000239006, "kilowatt-hours": 2.7778e-7,
    },
    "Digital Storage": {
        "bytes": 1, "kilobytes": 1e-3, "megabytes": 1e-6, "gigabytes": 1e-9, "terabytes": 1e-12,
    },
    "Data Transfer Rate": {
        "bits/second": 1, "kilobits/second": 1e-3, "megabits/second": 1e-6, "gigabits/second": 1e-9, "bytes/second": 1e-3,
    },
    "Currency": {},  # Handled separately
}

# Conversion functions
def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        result = (value * 9/5) + 32
        formula = f"({value} * 9/5) + 32 = {result}"
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        result = value + 273.15
        formula = f"{value} + 273.15 = {result}"
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        result = (value - 32) * 5/9
        formula = f"({value} - 32) * 5/9 = {result}"
    elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
        result = (value - 32) * 5/9 + 273.15
        formula = f"({value} - 32) * 5/9 + 273.15 = {result}"
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        result = value - 273.15
        formula = f"{value} - 273.15 = {result}"
    elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
        result = (value - 273.15) * 9/5 + 32
        formula = f"({value} - 273.15) * 9/5 + 32 = {result}"
    else:
        result = value
        formula = "No conversion needed"
    return result, formula

def convert_currency(value, from_unit, to_unit):
    API_KEY = "87aba4f2f8508fe5e2884253"  # Replace with your API key
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_unit}/{to_unit}/{value}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["result"] == "error":
            st.error(f"API Error: {data['error-type']}")
            return value, "Conversion failed"
        result = data["conversion_result"]
        formula = f"{value} {from_unit} → {result} {to_unit} (using real-time exchange rates)"
        return result, formula
    except Exception as e:
        st.error(f"Error fetching exchange rates: {e}")
        return value, "Conversion failed"

def convert_units(value, from_unit, to_unit, category):
    if category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)
    elif category == "Currency":
        return convert_currency(value, from_unit, to_unit)
    else:
        if from_unit == to_unit:
            return value, "No conversion needed"
        result = value * (conversion_factors[category][to_unit] / conversion_factors[category][from_unit])
        formula = f"({value} * {conversion_factors[category][to_unit]} / {conversion_factors[category][from_unit]}) = {result}"
        return result, formula

# Initialize session state variables
if "category" not in st.session_state:
    st.session_state.category = "Length"

if "value_input" not in st.session_state:
    st.session_state.value_input = 1.0

if "converted_input" not in st.session_state:
    st.session_state.converted_input, st.session_state.formula = convert_units(
        st.session_state.value_input, unit_categories[st.session_state.category][0], unit_categories[st.session_state.category][1], st.session_state.category)

if "history" not in st.session_state:
    st.session_state.history = []

# Callback functions
def update_from_value():
    if st.session_state.category == "Currency":
        st.session_state.converted_input, st.session_state.formula = convert_currency(
            st.session_state.value_input, st.session_state.from_unit, st.session_state.to_unit)
    else:
        st.session_state.converted_input, st.session_state.formula = convert_units(
            st.session_state.value_input, st.session_state.from_unit, st.session_state.to_unit, st.session_state.category)

def update_to_value():
    st.session_state.value_input = st.session_state.converted_input
    update_from_value()

# Layout
col1, col2 = st.columns(2)

# Sidebar to select category
category = st.sidebar.selectbox("Select Category", list(unit_categories.keys()), key="category", index=0)

with col1:
    from_unit = st.selectbox("From", unit_categories[category], key="from_unit", on_change=update_from_value)
    value = st.number_input("Enter Value", value=st.session_state.value_input, key="value_input", on_change=update_from_value)

with col2:
    to_unit = st.selectbox("To", unit_categories[category], key="to_unit", on_change=update_from_value)
    converted_value = st.number_input("Converted Value", value=st.session_state.converted_input, key="converted_input", on_change=update_to_value)

# Formula display
st.markdown(f"**Formula**: `{st.session_state.formula}`")

# Export results
export_data = pd.DataFrame({
    "From Unit": [from_unit],
    "To Unit": [to_unit],
    "Input Value": [value],
    "Converted Value": [converted_value]
})
csv = export_data.to_csv(index=False)
st.download_button(
    label="📥 Export as CSV",
    data=csv,
    file_name="conversion_results.csv",
    mime="text/csv",
)

# Add to history
st.session_state.history.append({
    "Category": category,
    "From Unit": from_unit,
    "To Unit": to_unit,
    "Input Value": value,
    "Converted Value": converted_value,
    "Formula": st.session_state.formula
})

# Display history
st.sidebar.header("📜 Conversion History")
for i, entry in enumerate(st.session_state.history[::-1]):
    st.sidebar.write(f"{i+1}. {entry['Input Value']} {entry['From Unit']} → {entry['Converted Value']} {entry['To Unit']}")
    st.sidebar.write(f"   Formula: {entry['Formula']}")
    st.sidebar.write("---")

# Footer
st.markdown("---")