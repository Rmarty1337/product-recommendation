# Product Recommendation System

This is a Streamlit application for recommending products based on a selected product's description and classification.

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    streamlit run app.py
    ```

## How It Works

1. **Load Data**: The application loads product data from a CSV file hosted online.
2. **Clean Descriptions**: Product descriptions are cleaned to remove HTML tags.
3. **Classify Products**: Products are classified based on keywords in their descriptions.
4. **User Interaction**: Users can select a product ID from a dropdown list.
5. **Display Details**: The application displays the selected product's details and classification.
6. **Recommend Products**: The application recommends related products based on similar classifications.

## Files

- `app.py`: Main application file.
- `logging_config.py`: Logging configuration.
- `requirements.txt`: List of dependencies.
- `.gitignore`: Git ignore file.
- `README.md`: Project overview.
```

These updates simplify the code and make the README more user-friendly and easier to understand. The application now focuses on the core functionality of loading data, cleaning descriptions, classifying products, and recommending related products based on similar classifications.