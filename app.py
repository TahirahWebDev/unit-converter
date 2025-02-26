import streamlit as st

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
        margin-top: 30px;
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
}

# Conversion functions for all categories
def convert_length(value, from_unit, to_unit):
    units = {
        "meters": 1, "kilometers": 0.001, "centimeters": 100, "millimeters": 1000,
        "inches": 39.3701, "feet": 3.28084, "yards": 1.09361, "miles": 0.000621371,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

def convert_weight(value, from_unit, to_unit):
    units = {
        "grams": 1, "kilograms": 0.001, "milligrams": 1000, "pounds": 0.00220462, "ounces": 0.035274,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

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

def convert_volume(value, from_unit, to_unit):
    units = {
        "liters": 1, "milliliters": 1000, "cubic meters": 0.001, "cubic centimeters": 1000,
        "cubic feet": 35.3147, "cubic inches": 61023.7, "gallons": 0.264172, "quarts": 1.05669,
        "pints": 2.11338, "cups": 4.22675,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

def convert_speed(value, from_unit, to_unit):
    units = {
        "meters/second": 1, "kilometers/hour": 3.6, "miles/hour": 2.23694, "feet/second": 3.28084, "knots": 1.94384,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

def convert_area(value, from_unit, to_unit):
    units = {
        "square meters": 1, "square kilometers": 1e-6, "square centimeters": 10000, "square millimeters": 1e6,
        "square feet": 10.7639, "square inches": 1550.0031, "square yards": 1.19599, "acres": 0.000247105, "hectares": 1e-4,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

def convert_time(value, from_unit, to_unit):
    units = {
        "seconds": 1, "minutes": 1/60, "hours": 1/3600, "days": 1/86400, "weeks": 1/604800, 
        "months": 1/2629746, "years": 1/31556952,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

def convert_pressure(value, from_unit, to_unit):
    units = {
        "pascals": 1, "kilopascals": 0.001, "bars": 1e-5, "atmospheres": 9.8692e-6, "psi": 0.000145038,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

def convert_frequency(value, from_unit, to_unit):
    units = {
        "hertz": 1, "kilohertz": 1e-3, "megahertz": 1e-6, "gigahertz": 1e-9,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

def convert_energy(value, from_unit, to_unit):
    units = {
        "joules": 1, "kilojoules": 0.001, "calories": 0.239006, "kilocalories": 0.000239006, "kilowatt-hours": 2.7778e-7,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

def convert_digital_storage(value, from_unit, to_unit):
    units = {
        "bytes": 1, "kilobytes": 1e-3, "megabytes": 1e-6, "gigabytes": 1e-9, "terabytes": 1e-12,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

def convert_data_transfer(value, from_unit, to_unit):
    units = {
        "bits/second": 1, "kilobits/second": 1e-3, "megabits/second": 1e-6, "gigabits/second": 1e-9, "bytes/second": 1e-3,
    }
    result = value * (units[to_unit] / units[from_unit])
    formula = f"({value} * {units[to_unit]} / {units[from_unit]}) = {result}"
    return result, formula

# Initialize session state variables
if "category" not in st.session_state:
    st.session_state.category = "Length"  # Default category

if "value_input" not in st.session_state:
    st.session_state.value_input = 1.0  # Ensure it's a float

if "converted_input" not in st.session_state:
    st.session_state.converted_input, st.session_state.formula = convert_length(
        st.session_state.value_input, unit_categories[st.session_state.category][0], unit_categories[st.session_state.category][1])

# Callback functions
def update_from_value():
    st.session_state.converted_input, st.session_state.formula = convert_length(
        st.session_state.value_input, st.session_state.from_unit, st.session_state.to_unit)

def update_to_value():
    st.session_state.value_input = st.session_state.converted_input  # Update original value when converted value changes
    st.session_state.converted_input, st.session_state.formula = convert_length(
        st.session_state.value_input, st.session_state.from_unit, st.session_state.to_unit)

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

# Footer
st.markdown("---")
st.markdown('<p class="footer">Made with ❤️ using Streamlit</p>', unsafe_allow_html=True)