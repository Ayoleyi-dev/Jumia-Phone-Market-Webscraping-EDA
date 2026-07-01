# Jumia Nigeria: Phone Market Web Scraping & EDA

![Dashboard Screenshot](Jumia_Dashboard_Screenshot.png)

## Overview
This project involves the automated extraction of real-time mobile phone product data from Jumia Nigeria. The objective was to scrape raw e-commerce data, clean and format it using Python, and perform Exploratory Data Analysis (EDA) to uncover market trends, pricing strategies, and brand distribution.

## Dataset Source
All data was extracted directly from the [Jumia Nigeria Android Phones Category](https://www.jumia.com.ng/android-phones/).
The resulting dataset (`jumia_phones_final.csv`) includes:
* Phone Name & Brand
* Current Price & Old Price
* Calculated Discount Percentage
* Customer Rating & Review Count
* Store Type (Official vs. Third-Party)

## Technical Stack
* **Language:** Python
* **Web Scraping:** BeautifulSoup4, Requests
* **Data Manipulation:** Pandas
* **Data Visualization:** Matplotlib, Seaborn

## Key Insights
1. **Price & Brand Dominance:** Samsung dominates the listing volume, but premium brands like Xiaomi and Oppo command higher average sales prices compared to budget brands like FreeYond and Itel.
2. **Discount Strategies:** The highest average discounts are consistently offered on lesser-known or older models (e.g., FreeYond at ~46%, Agm at ~44%).
3. **Inventory Share:** Across all top brands, third-party sellers heavily outweigh official Jumia store listings, indicating a highly decentralized seller market.
