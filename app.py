import pickle
import streamlit as st
from utilities import numerical_rating
from PIL import Image

# Load the model
filename = "saved_models/rf_dep.pkl"
rf_model = pickle.load(open(filename, "rb"))

def main():
    # ---------------- Sidebar Styling ----------------
    st.markdown("""
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #1f8b8d;
    }

    /* Sidebar labels (keep white) */
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 500;
    }

    /* Input fields text */
    [data-testid="stSidebar"] input {
        color: black !important;
        background-color: white !important;
    }

    /* Selectbox text */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        color: black !important;
        background-color: white !important;
    }

    /* Button styling */
    [data-testid="stSidebar"] button {
        background-color: black !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 10px;
        font-weight: bold;
        width: 100%;
    }

    /* Button hover */
    [data-testid="stSidebar"] button:hover {
        background-color: #333 !important;
    }

    /* Number input styling */
    [data-testid="stSidebar"] input[type="number"] {
        color: black !important;
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- Sidebar Inputs ----------------
    st.sidebar.header("Input Features")

    # Function for selectbox in sidebar
    def select_widget_sidebar(label, key):
        return st.sidebar.selectbox(
            label=label,
            key=key,
            options=(
                "Very Poor", "Poor", "Fair", "Below Average", "Average",
                "Cannot Say", "Above Average", "Good", "Very Good", "Excellent", "Very Excellent"
            )
        )

    # Overall Quality
    option_overallQuality = select_widget_sidebar("Overall Build Material Quality", "overallQuality")
    option_overallQuality = numerical_rating(option_overallQuality)

    # Overall Condition
    option_overallCondition = select_widget_sidebar("Overall House Condition", "overallCondition")
    option_overallCondition = numerical_rating(option_overallCondition)

    # Numeric inputs
    livingRoomArea = st.sidebar.number_input("Living Room Area (sq ft)", min_value=334.0, max_value=4650.0, value=1500.0)
    basementArea = st.sidebar.number_input("Basement Area (sq ft)", min_value=0.0, max_value=6100.0, value=500.0)
    firstFloorArea = st.sidebar.number_input("First Floor Area (sq ft)", min_value=334.0, max_value=4690.0, value=1200.0)
    type1FinishedArea = st.sidebar.number_input("First Floor Finished Area (sq ft)", min_value=0.0, max_value=5660.0, value=1000.0)
    secondFloorArea = st.sidebar.number_input("Second Floor Area (sq ft)", min_value=0.0, max_value=2860.0, value=0.0)
    lotArea = st.sidebar.number_input("Total Lot Area (sq ft)", min_value=1300.0, max_value=21500.0, value=7500.0)
    yearBuilt = st.sidebar.number_input("Original Construction Year", min_value=1872, max_value=2010, value=2000)
    bathAboveGrade = st.sidebar.number_input("Bathrooms", min_value=0, max_value=3, value=2)
    yearGarageBuilt = st.sidebar.number_input("Garage Construction Year", min_value=1895, max_value=2010, value=2000)
    porchArea = st.sidebar.number_input("Porch Area (sq ft)", min_value=0.0, max_value=742.0, value=0.0)
    garageArea = st.sidebar.number_input("Garage Area (sq ft)", min_value=0.0, max_value=1448.0, value=400.0)
    garageCarCapacity = st.sidebar.number_input("Garage Car Capacity", min_value=0, max_value=5, value=2)

    # ---------------- Main Page ----------------
    st.title("🏠 Real Estate Price Estimator")
    st.markdown("### Ames Housing Price Prediction")

    # Add a nice description
    st.markdown("""
<p style='text-align: justify;'>This tool predicts the selling price of a house based on various features.
Enter the property details in the sidebar to get an instant estimate.</p>
""", unsafe_allow_html=True)

    image = Image.open("main.png")
    st.image(image, width=500)

    # ---------------- Prediction ----------------
    preds_final = None

    # Remove use_container_width parameter for older Streamlit
    if st.sidebar.button("💰 Predict Price"):
        # Make prediction
        preds = rf_model.predict([[
            option_overallQuality, option_overallCondition, livingRoomArea, basementArea, firstFloorArea,
            type1FinishedArea, secondFloorArea, lotArea, yearBuilt, bathAboveGrade,
            yearGarageBuilt, porchArea, garageArea, garageCarCapacity
        ]])
        preds_final = round(preds[0], 2)

    # ---------------- Output ----------------
    if preds_final is not None:
        st.markdown(f"""
        <div style="
            background-color: #1f8b8d;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-top: 30px;
        ">
            <h2 style="color: white; margin-bottom: 10px;">Estimated Price</h2>
            <h1 style="color: gold; font-size: 48px;">${int(round(preds_final, 2)):,}</h1>
            <p style="color: white;">Based on the features you provided</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- Footer ----------------
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>Note: All areas are in square feet</p>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
