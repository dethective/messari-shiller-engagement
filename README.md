# Messari API Wrapper Documentation

This project provides a wrapper for the Messari API to analyze crypto-related data and engagement metrics.

## Files Structure

- `messari_wrapper.py` - Main wrapper for Messari API interactions
- `parameters.py` - Configuration file containing API keys and base URLs

## Configuration

The wrapper uses configuration parameters defined in `parameters.py`:
- `MESSARI_PREMIUM_KEY`: Your Messari API key (required for authentication)
- `BASE_URL`: Base URL for the Messari API endpoints

## Usage

To use the wrapper, make sure you have:
1. Set up your Messari API key in `parameters.py`
2. Installed required dependencies

Example usage:
```python
from messari_wrapper import fetch_all_users, fetch_user_engagement, fetch_user_mindshare, get_user_by_id

# Fetch all users
df_users = fetch_all_users(max_users=2000)
print(df_users.head())

# Fetch user engagement
df_engagement = fetch_user_engagement('@Cobratate', start_date='2023-01-01', end_date='2023-12-31')
print(df_engagement.head())

# Fetch user mindshare
df_mindshare = fetch_user_mindshare('@Cobratate', start_date='2023-01-01', end_date='2023-12-31')
print(df_mindshare.head())

# Fetch user by ID
user_data = get_user_by_id('12345')
print(user_data)
```

## Related Files

This project includes visualization outputs:
- `engagement_trends.html` - Interactive visualization of engagement trends

## Data Analysis

The project includes a Jupyter notebook `data_analysis.ipynb` for detailed analysis and visualization of the collected data.

This notebook was used to provide all the charts outlined in the blog post.
