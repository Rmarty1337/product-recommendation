import streamlit as st
import pandas as pd
import logging
from logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Dataset URL
DATA_URL = "https://raw.githubusercontent.com/fenago/datasets/refs/heads/main/sample-data.csv"

@st.cache_data
def load_data():
    """Load dataset from URL and return DataFrame."""
    try:
        df = pd.read_csv(DATA_URL)
        logger.info(f"Dataset columns: {df.columns.tolist()}")  # Log the columns of the dataset
        logger.info(f"Dataset head: {df.head().to_dict()}")  # Log the first few rows of the dataset
        
        # Ensure 'related' column is correctly formatted
        if 'related' in df.columns:
            df['related'] = df['related'].apply(lambda x: eval(x) if isinstance(x, str) else [])
        else:
            df['related'] = [[]] * len(df)  # Default empty lists if column is missing
        
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        st.error("⚠️ Error loading data. Please check the logs for more details.")
        return pd.DataFrame()

# Load product data
products = load_data()

# Streamlit UI setup
st.title("🛒 Product Recommendation System")

# Display a preview of the dataset
st.write("### Sample Product Data:")
st.dataframe(products.head())  # Show first few rows of the dataset

# Display dataset columns for debugging
st.write("### Dataset Columns:")
st.write(products.columns.tolist())

# Ensure required columns exist
if {'id', 'description', 'related'}.issubset(products.columns):
    if not products.empty:
        try:
            # User selects a product
            product_id = st.selectbox("🔍 Choose a product ID:", products['id'])

            # Get selected product details
            selected_product = products[products['id'] == product_id].iloc[0]
            st.write(f"## Product ID: {selected_product['id']}")
            st.write(f"**Description:** {selected_product['description']}")

            # Display related products
            st.write("### 🏷️ Related Products:")
            for rel_id in selected_product['related']:
                rel_product = products[products['id'] == rel_id]
                if not rel_product.empty:
                    rel_product = rel_product.iloc[0]
                    st.write(f"- **Product ID: {rel_product['id']}**: {rel_product['description']}")
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            st.error("⚠️ Error processing data. Please check the logs for more details.")
    else:
        st.error("⚠️ The dataset is empty. Please check the data source.")
else:
    st.error("⚠️ Dataset does not contain the required columns: 'id', 'description', and 'related'.")
