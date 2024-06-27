# Amazon Image Scraper using ScraperAPI

This Python script fetches product image data from Amazon using ScraperAPI, based on predefined product queries. It saves the fetched images locally by a product category.

## Requirements

- Python 3.10
- `requests` library (install via `pip install requests`)

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ajishpradeep/Utills.git
   cd amazon-image-scraper
   ```

2. **Install Dependencies:**
   ```bash
   pip install requests
   ```

3. **API Key Setup:**
   - Sign up for an account on [ScraperAPI](https://www.scraperapi.com/) and obtain an API key.
   - Replace `api_key = `(Expired temporary key used as a placeholder) in the code with your ScraperAPI key.

## Usage

### 1. Running the Script

- Run the script:
  ```bash
  python amazon_image_scraper.py
  ```

### 2. Script Workflow

1. **Fetch Results**: Queries defined product categories (e.g., Groceries, Snacks) and retrieves image URLs using Scrapperapi.
2. **Save Images**: Downloads and saves images locally in the 'images' directory, organized by category and product title.
3. **Output**: Generates a `results.json` file containing metadata (category, title, image URL) of fetched products.
4. **Results Count**: Prints the number of results fetched per category.

### 3. Directory Structure

The script will create the following directory structure:
```
- /images
  - [Category]_[ProductTitle].jpg
- results.json
```

## 4. Configuration

- Adjust `product_queries` list to customize product categories to search.
- Modify `max_results` in `fetch_results_for_query()` function to limit the number of results fetched per category.

## Notes

- **Rate Limiting:** The script includes delays (`time.sleep()`) to respect API rate limits and avoid overloading the server.
- **Error Handling:** If any errors occur during image fetching or saving, error messages are printed to the console.

## Acknowledgments

- Thanks to [Scrapperapi](https://www.scraperapi.com/) for providing the API service used in this project.
