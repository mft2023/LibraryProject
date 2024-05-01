# Library Project
This repository is about analyzing some library-related data, finding explainable factors of late returns, visualizing results, and giving suggestions to monitor the rate of returns.

## Background
The libraries in Oregon provide their data to find possible factors of returning books late, defined as books returned after 28 days of checkout. They would like to pay attention to the factors and find a way to monitor returning rate to prevent late returns. The data they have is described as follows.

## Data format and attributes
There are four files, including checkouts.csv, libraries.csv, books.csv, and customers.csv. Attributes of each file is listed.
- checkouts.csv: id, patron_id, library_id, date_checkout, and date_returned. 
- libraries.csv: id, name, street_address, city, region, and postal_code.
- books.csv: id, title, authors, publisher, publishedDate, categories, price, and pages.
- customers.csv: id, name, street_address, city, state, zipcode, birth_date, gender, education, and occupation.

## Analysis Reasoning
### Model Selection
In order to increase the explainability of late return factors, I chose a logistic regression model to classify on-time and late returns. 
The coefficients of features/factors in the model represent the probability of late returns.
### Potential factors
There are 3 categories of factors: geographical, behavioral, and book-related factors. 
- Geographical factors: distance between home and the library. Customers may not pass by the library on their routine trips if they live away from it and tend to return books late.
- Behavioral factors: age, gender, education level, and occupation.
- Book-related factors: new book, price, and pages. Newly released books may be very popular among customers' family and friends. Thus, other people may borrow books from the customers. More pages in a book may require more time to finish. These are potential factors for returning books late.

## Install required Python packages
```
pip install -r requirements.txt
```

## Data Cleaning
- Date format: `clean_date_format` function (input: string, output: datetime).
  Dates are written in different formats, the majority are 'YYYY/MM/DD' and 'YYYY-MM-DD'. Thus, this function converts these two formats first.
  If it cannot convert to datetime successfully, then go over each digit in the string and only keep numbers. 
  In order to read the date correctly, it should have 8 digits (YYYY, MM, DD). If 8 digits are available, convert to datetime. Otherwise, return nan.
- Published year format: `clean_published_year` function (input: string, output: datetime).
  The most common format in publish_date is 'year', here, all the dates are converted into the year. This function converts 'YYYY-MM-DD', 'YYYY-MM', and 'YYYY' into years in datetime.
  If the function cannot convert dates into years, return nan.
- Text format: `clean_txt ` function (input: string, output: string).
  This function removes all the extra spaces in the string and makes the string lowercase.
- Number format: `clean_number` function (input: string, output: float).
  This function goes over each character and only keeps '.' and numbers.
- Zipcode format: `clean_zipcode_format` function (input: string, output: string).
  This function removes every special character. If the zipcode is consisted of 5 digits, then it's the correct zipcode format, otherwise, return ''.

## Data Analysis
Each step in the analysis is also numbered in the Python script accordingly.
#### 1. Load the files and investigate data composition and percentage of missing values in each file to decide what attributes have enough quality for further investigation. 
If the majority of the data is missing, then it's not suitable to consider as a factor since the results may be misleading. Here, I only analyzed the attributes/factors that are missing less than 10% of data.

#### 2. Find the data with a reasonable timeline: Remove the data with missing checkout or return dates because we won't be able to judge whether the books are returned on time.
#### 3. Calculate the rates of late returns in all libraries (as a group) and in each library.
##### 3.1 Go through each library id and find the checkout and return dates in the checkouts.csv using a for loop. 
##### 3.2 Analyze the data with a reasonable timeline (return_date>check_out_date).
If the return_date is after checkout_date, count the num_borrows for the library and total_num_borrow for all the libraries.

#### 4. Data Cleaning for each attribute selected in the analysis reasoning section.
Data cleaning for the correct format of zipcode, date, publish year, and txt are in the functions created. Please kindly refer to the functions for details.
##### 4.1 Find the external keys to connect the check_out.csv with the other files. 
There are 3 external keys to connect other files: checkouts.library_id=libraries.id, checkouts.patron_id=customers.id, and checkouts.id=books.id. 
Use these connections to find the corresponding library_id, customer_id, and book_id for each checkout.
##### 4.2 Find and calculate the factors: distance, age, gender, education level, occupation, new book, price, and pages
- distance: find the zipcodes of the home address of the customer and the library that he/she borrow books from. Calculate the distance between the two zipcodes using a Python library: pgeocode*.
- age: find the customer's birth_date(DOB) and checkout_date and see if it makes sense (check_out_date>DOB), otherwise, set age as nan.
- new_book_days: find the date of publication and check if the timeline makes sense (check_out_date>pub_date). If so, calculate the days of publication at the checkout date. If missing data or an unreasonable timeline, then set new_book_days as nan. 
- the other factors: find the corresponding location in the data, if any missing data, set the factors as nan.

#### 5. Store those data based on its data type: continuous data or categorical data.

#### 6. Judge whether the book is returned late and assign the checkout to two labels, 0: on-time return and 1: late return.
If the return date is greater than 28 days after checkout, then it is a late return. Count the num_late_return for each library and total_num_late_return for the overall rate of late returns.
The overall rate of late returns from all the libraries is 15.22 %.

#### 7. Handle missing values and data normalization
##### 7.1 Preprocess continuous variables: fill the missing value with mean and normalize each factor using StandardScaler.
##### 7.2 Preprocess categorical variables: fill the missing value with the most frequent category and encode each factor using OneHotEncoder (turn each category into a corresponding number).
##### 7.3 Combine preprocessed data as features

#### 8. Build a predictive model - logistic regression model training
##### 8.1 Split data into training (80%) and testing (20%) sets and shuffle data (random_state=42)
##### 8.2 Train a binary logistic regression model
The logistic regression model predicts binary outcomes, 0 means on-time return and 1 means late return.
##### 8.3 Predict whether the book will be returned late using the logistic regression model
The logistic model can predict the testing set with the results of 0.81 as accuracy, 0.3 as F1-score, 0.71 as precision, and 0.19 as recall.
The results had high precision and low recall, which meant the model tended to predict as 0, which is the majority of data. There are four ways to improve the model recall.
1. Collect more data on late returns.
2. Add the parameter of class_weights in the model to address late return data. For example, set class_weight="balanced" or customize weights class_weight={0:weight_on_time, 1:weight_late} to help the model identify late returns better.
3. Find more possible features/factors to train the model.
4. Try other classification models, such as a random forest classifier or neural networks.

#### 9. Explain results with visualization of the coefficients in the model
The factors with larger coefficients, no matter positive or negative values, are the influential factors of late returns.
A horizontal barplot is created to visualize the magnitude of the coefficients of each factor.
If the factor is positive, it represents that under the condition of this factor happening, the chance of late return increases.
If it's negative, then under the condition of the factor, the chance of late return decreases.

## Results Explanation
Based on the results, the top 10 influential factors with positive (+) and negative (-) relationships to late returns are listed as follows:
- Geographical factor: distance (+). Customers live in a longer distance from the libraries tend to return books late.
- Behavioural factors:  
  Education level: college degree (-) and graduate degree(+).  
  Occupation: business & finance (+), tech (+), admin & support (-) and education & health (-).  
- Book-realted factors: book price(+), pages(+), and new book (+). Books with a higher price, more pages, and a closer release date tend to be returned late. 
  Maybe customers need more time to finish the book with more pages. Newer books may be very popular that friends or family of the customers also want to read and tend to be returned late.

## Suggestion for the libraries
1. Build an email reminder system to remind the customers of the date of return automatically.
2. Extend the borrowing policy for customers who live away from libraries and those who borrow thick books.
3. Set up book return boxes around the cities to make returning books easier for customers who live away from libraries.
4. Set up a system where customers can submit a request for extending the borrowing period. In this way, the libraries can know whether customers need more time to finish the book or simply forget to return it. If many customers request an extension, the libraries can extend the days in the borrowing policy accordingly.
6. The libraries can set up a reading area that allows customers to read new books and expensive ones on-site only. After a period of time, when these books are not so popular, they can be checked out. In this way, it avoids late returns and many customers can enjoy reading time in the libraries.
7. Use the logistic regression model to find which customers may tend to return books late and make customized reminder calls.

## Reference
* [pgeocode](https://pgeocode.readthedocs.io/en/latest/generated/pgeocode.GeoDistance.html)
* [An example of calculating distance between two zipcodes using geocode](https://stackoverflow.com/questions/67166295/using-pgeocode-in-pandas)











