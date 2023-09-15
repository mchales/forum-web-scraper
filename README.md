# Breast Cancer Forum Web Scraper

This project uses [Scrapy](https://scrapy.org/) to extract forum posts and responses from [BreastCancer.org's Discussion Forum](https://community.breastcancer.org/en/categories/hormonal-therapy---before-during-and-after). The created dataset was used in the paper "Assessing the Performance of Large Language Models in Identifying Hormonal Therapy Medication Consumption from Online Discussions" published in the AMIA 2024 Informatics Summit.

## Key Figures

- **Original Post Count:** Initially scraped approximately 7,000 posts.
- **Relevant Post Count:** After filtering for mentions of specific breast cancer medications, about 4,000 posts were retained.

## Objective

The primary goal was to gather data for testing ChatGPT's capabilities in Named Entity Recognition (NER), especially for recognizing breast cancer symptoms and medicines.

## How It Works

1. **Scraping Tool:** Used [Scrapy](https://scrapy.org/) for navigating the forum threads and extracting relevant data.
2. **Data Filtering:** Processed the posts to retain only those mentioning specific breast cancer medications.
3. **Application:** Utilized the curated data to test ChatGPT on its NER performance (not in this repository)
