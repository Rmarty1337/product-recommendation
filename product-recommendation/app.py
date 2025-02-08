import streamlit as st
import pandas as pd
import logging
from logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Dataset URL
DATA_URL = "https://raw.githubusercontent.com/fenago/datasets/refs/heads/main/sample-data.csv"

# Function to load data from a CSV file
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

# Function to find similar products
def find_similar_products(product_name, df, num_results=10):
    df['similarity'] = df['name'].apply(lambda x: product_name.lower() in x.lower())
    similar_products = df[df['similarity']].head(num_results)
    return similar_products[['id', 'name', 'description', 'category']]

# Streamlit UI setup
st.title("🛒 Product Recommendation System")

# Load product data
products = load_data()
st.success("Data loaded successfully!")
st.dataframe(products.head())  # Show the loaded data

# User inputs a product name
product_name = st.text_input("Enter Product Name to Search:", "")
if st.button("Find Similar Products"):
    if product_name:
        results = find_similar_products(product_name, products)
        if not results.empty:
            st.write(f"Top {len(results)} similar products:")
            st.dataframe(results)
        else:
            st.warning("No similar products found.")
    else:
        st.warning("Please enter a product name.")
