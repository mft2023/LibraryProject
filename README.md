# LibraryProject
This repository is about analyzing some library-related data, finding explainable factors of late book returns, affording suggestions for libraries to avoid late returns, and visualizing results.

## Background
The libraries in Oregon provide their data to find possible factors of returning books late, defined as books returned after 28 days of checkout. They would like to pay attention to the factors and find a way to monitor returning rate to prevent late returns. The data they have is described as follows.

## Data format and attributes
There are 4 files, including checkouts.csv, libraries.csv, books.csv, and customers.csv.
- checkouts.csv has 5 columns: id, patron_id, library_id, date_checkout, and date_returned. 
- libraries.csv has 6 columns: id, name, street_address, city, region, and postal_code.
- books.csv has 8 columns:  id, title, authors, publisher, publishedDate, categories, price, and pages.
- customers.csv has 10 columns: id, name, street_address, city, state, zipcode, birth_date, gender, education, and occupation.

## Analysis Reasoning
There are 3 categories of factors: geographical, behavioral, and book-related factors. 
- Geographical factors: distance between home and the library. Customers may not pass by the library on their routine trips if they live away from it and tend to return books late.
- Behavioral factors: age, gender, education level, and occupation.
- Book-related factors: new book, price, and pages. Newly released books may be very popular among customers' family and friends. Other people may borrow books from the customers. More pages in a book may require more time to finish. These are potential factors for returning books late.

## Data Analysis
#### Each step in the analysis is also numbered in the Python script accordingly.
### 1. Load the files and investigate data composition and percentage of missing values in each file to decide what attributes have enough quality for further investigation. 
If the majority of the data is missing, then it's not suitable to consider as a factor since the results may be misleading. Here, I only analyzed the attributes/factors that are missing less than 10% of data.
### 2. Find the data with a reasonable timeline: Remove the data with missing checkout or return dates because we won't be able to judge whether the books are returned on time.
### 3. Calculate the rates of late returns in all libraries (as a group) and in each library.
#### 3.1 Go through each library id and find the checkout and return dates in the checkouts.csv using a for loop. 
#### 3.2 Analyze the data with a reasonable timeline (return_date>check_out_date).
If the return_date is after checkout_date, count the num_borrows for the library and total_num_borrow for all the libraries.
### 4. Data Cleaning for each attribute selected in the analysis reasoning section.
Data cleaning for the correct format of zipcode, date, publish year, and txt are in the functions created. Please kindly refer to the functions for details.
#### 4.1 Find the external keys to connect the check_out.csv with the other files. 
There are 3 external keys to connect other files: checkouts.library_id=libraries.id, checkouts.patron_id=customers.id, and checkouts.id=books.id. 
Use these connections to find the corresponding library_id, customer_id, and book_id for each checkout.
#### 4.2 Find and calculate the factors: distance, age, gender, education level, occupation, new book, price, and pages
- distance: find the zipcodes of the home address of the customer and the library that he/she borrow books from. Calculate the distance between the two zipcodes using [pgeocode library](https://pgeocode.readthedocs.io/en/latest/generated/pgeocode.GeoDistance.html).
- age: find the customer's birth_date(DOB) and checkout_date and see if it makes sense (check_out_date>DOB), otherwise, set age as nan.
- new_book_days: find the date of publication and check if the timeline makes sense (check_out_date>pub_date). If so, calculate the days of publication at the checkout date. If missing data or an unreasonable timeline, then set new_book_days as nan. 
- gender, education level, occupation, price, and pages: find the corresponding location in the data, if any missing data, set the factors as nan.
### 5. Store those data based on its data type: continuous data or categorical data.
### 6. Judge whether the book is returned late and assign the checkout to two labels, 0: on-time return and 1: late return.
If the return date is greater than 28 days after checkout, then it is a late return. Count the num_late_return for each library and total_num_late_return for the overall rate of late returns.
The overall rate of late returns from all the libraries is 15.22 %.
### 7. Handle missing values and data normalization
#### 7.1 Preprocess continuous variables: fill the missing value with mean and normalize each factor using StandardScaler.
#### 7.2 Preprocess categorical variables: fill the missing value with the most frequent category and encode each factor using OneHotEncoder (turn each category into a corresponding number).
#### 7.3 Combine preprocessed data as features
### 8. Logistic regression model training
#### 8.1 Split data into training (80%) and testing (20%) sets and shuffle data (random_state=42)
#### 8.2 Create the model and train it
### 9. Explain results with visualization of the coefficients in the model
The factors with larger weights/coefficients, no matter positive or negative values, are the influential factors of late returns.
If the factor is positive, it represents that under the condition of this factor happening, the chance of late return increases.
If it's negative, then under the condition of the factor, the chance of late return decreases.
Based on the results, the top 10 influential factors with positive (+) and negative (-) relationships to late returns are listed as follows:
- Geographical factor: distance (+). Customers live in a longer distance from the libraries tend to return books late.
- Behavioural factors: 
  -- Education level: college degree (-) and graduate degree(+).
  -- Occupation: business & finance (+), tech (+), admin & support (-) and education & health (-).
- Book-realted factors: book price(+), pages(+), and new book (+).



## Reference
* [https://pgeocode.readthedocs.io/en/latest/generated/pgeocode.GeoDistance.html]











