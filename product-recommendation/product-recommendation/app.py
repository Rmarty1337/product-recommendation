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

# Ensure required columns exist
if {'id', 'name', 'description', 'related', 'category'}.issubset(products.columns):
    try:
        # User selects a category
        category = st.selectbox("🔍 Choose a category:", products['category'].unique())
        
        # Filter products by selected category
        filtered_products = products[products['category'] == category]
        
        # User selects a product from the filtered list
        product_id = st.selectbox("🔍 Choose a product ID:", filtered_products['id'])

        # Get selected product details
        selected_product = filtered_products[filtered_products['id'] == product_id].iloc[0]
        st.write(f"## {selected_product['name']}")
        st.write(f"**Description:** {selected_product['description']}")

        # Display related products
        st.write("### 🏷️ Related Products:")
        for rel_id in selected_product['related']:
            rel_product = products[products['id'] == rel_id]
            if not rel_product.empty:
                rel_product = rel_product.iloc[0]
                st.write(f"- **{rel_product['name']}**: {rel_product['description']}")
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        st.error("⚠️ Error processing data. Please check the logs for more details.")
else:
    st.error("⚠️ Dataset does not contain the required columns: 'id', 'name', 'description', 'related', and 'category'.")
