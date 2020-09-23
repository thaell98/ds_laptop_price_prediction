# Data Science Laptop Price Estimator: Project Overview
* Created a tool that estimates price of a laptop in two popular shops.
* Scraped over 1000 laptop offers.
* Optimized Linear, Lasso and Random Forest Regressors using GridSearchCV to reach the best model.
* Build API using flask

## Code and Resources Used
**Python Version:** 3.7.6
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, flask, json, pickle  
**For Web  Framework Requirements:** ```pip install -r requirements.txt```  
**Scraping tool:** https://www.octoparse.com/  
**Data source:**: https://www.euro.com.pl/, https://www.mediaexpert.pl/  
**Flask Productionization:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2

## Web Scraping
Used octoparse scraping tool to scrape over 1000 laptop offerss, each one of them got the following:
* Title
* Screen
* Processor
* RAM
* Disk
* Graphic Card
* Operating system
* Price/Discounted Price
* Brand
* Price

## Data Cleaning
Ater scraping the data, i needed to clean it up so it was usable for our model. I made the following changes:
* Parsed screen inches, resoulution out of screen column
* Simplifed processor and graphic card columns 
* Split disc column by type of disc
* Simplified operating system column
* Parsed numeric data out of price
* Added column indicating if the price is discounted

## EDA

## Model Building
First, i transformed the categorical values into dummy variables and split the data into train and test sets.

I chose Mean Absolute Error to eavaluate my models:
* Multiple Linear Regression 
* Lasso Regression
* Random Forest

## Model Performance
The Random Forest model far outperformed the other approaches.
* Random Forest: MAE = 792.20
* Linear Regression: MAE = 895.09
* Lasso Regression: MAE = 899.12

## Productionization
