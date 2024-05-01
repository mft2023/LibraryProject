# Library Project
This repository is about analyzing some library-related data, finding explainable factors of late returns, visualizing results, and giving suggestions to monitor the rate of returns.

## Background
The libraries in Oregon provide their data to find possible factors of returning books late, defined as books returned after 28 days of checkout. They would like to pay attention to the factors and find a way to monitor returning rate to prevent late returns. The data they have is described as follows.

## Data format and attributes
There are four files, including checkouts.csv, libraries.csv, books.csv, and customers.csv. Attributes of each file are listed.
- checkouts.csv: id, patron_id, library_id, date_checkout, and date_returned. 
- libraries.csv: id, name, street_address, city, region, and postal_code.
- books.csv: id, title, authors, publisher, publishedDate, categories, price, and pages.
- customers.csv: id, name, street_address, city, state, zipcode, birth_date, gender, education, and occupation.

## Analysis Reasoning
### Model Selection
In order to explain the analysis results to the client, I chose an explainable model, a logistic regression model, to classify on-time and late returns. 
The coefficients of features/factors in the model represent the probability of late returns, which can explain the relationship between each factor and late return.
### Potential factors
There are 3 categories of factors: geographical, behavioral, and book-related factors. 
- Geographical factors: distance between home and the library.  
  Customers may not pass by the library on their routine trips if they live away from it and tend to return books late.
- Behavioral factors: age, gender, education level, and occupation.
- Book-related factors: new book, price, and pages.  
  Newly released books may be very popular among customers' family and friends. Thus, other people may borrow books from the customers.
  More pages in a book may require more time to finish. These are potential factors for returning books late.
  
## Install required Python packages and run analysis
```
pip install -r requirements.txt
python Analysis.py
```
  
## Data Cleaning
Several functions are built to organize the output formats of dates, texts, numbers, and zipcodes.  
An input from a Dtaframe is either a string or nan. The functions convert strings only, if the input is a nan, then return nan or an empty string ''. 
The data types of input and output in each function are described.  
- Date format: [`clean_date_format`](https://github.com/mft2023/LibraryProject/blob/b27b4965254068d958ec74700d883622952847ee/Analysis.py#L17) function (input: string, output: datetime or '').  
  This function tries to convert the string into datetime. The majority of formats are 'YYYY/MM/DD' and 'YYYY-MM-DD'. Thus, this function converts these two formats first.  
  If it cannot convert to datetime successfully, then go over each character in the string and only keep numbers.  
  In order to read the date correctly, it should have 8 digits (YYYY, MM, DD). If 8 digits are available, convert to datetime. Otherwise, return an empty string ''.  
- Published year format: [`clean_published_year`](https://github.com/mft2023/LibraryProject/blob/b27b4965254068d958ec74700d883622952847ee/Analysis.py#L45) function (input: string, output: datetime or '').  
  This function tries to convert the string into years in datetime.  
  If the function cannot convert dates into years, return an empty string ''.  
- Text format: [`clean_txt`](https://github.com/mft2023/LibraryProject/blob/b27b4965254068d958ec74700d883622952847ee/Analysis.py#L63) function (input: string, output: string or nan).  
  If the input is a string, it removes all the extra spaces in the string and makes the string lowercase.  
- Number format: [`clean_number`](https://github.com/mft2023/LibraryProject/blob/b27b4965254068d958ec74700d883622952847ee/Analysis.py#L71) function (input: string, output: float or nan).  
  If the input is a string, then go over each character and only keep '.' and numbers.  
- Zipcode format: [`clean_zipcode_format`](https://github.com/mft2023/LibraryProject/blob/b27b4965254068d958ec74700d883622952847ee/Analysis.py#L86) function (input: string, output: string or '').  
  If the input is a string, this function removes every special character in the string. If the output consists of 5 digits, then it's the correct zipcode format, otherwise, return ''.  

## Data Analysis
Each step in the analysis is also numbered in the Python script accordingly.
#### 1. Load the files and print the percentage of missing values in each file
If the majority of the data is missing, then it's not suitable to consider as a factor since the results may be misleading.  
Here, I only analyzed the attributes/factors that are missing less than 10% of the data.  

#### 2. Find the data with both checkout and return dates
Remove the data with missing checkout and return dates in the checkouts.csv because we won't be able to judge whether the books are returned on time.  

#### 3. Calculate the rate of late returns
3.1 Go through each book checkout and find the checkout and return dates using a for-loop  
3.2 Analyze the data with a reasonable timeline  
If the return_date is later than the checkout_date, count the total_num_borrow.

#### 4. Data Cleaning for each factor
Factors are listed in the analysis reasoning section, including distance, age, new_book_days, price, pages, gender, education, and occupation. 
For consistency of the date, text, and zipcode formats, please kindly refer to the [Data Cleaning](https://github.com/mft2023/LibraryProject#data-cleaning) section for details.  

4.1 Find the corresponding index in the other files  
There are 3 external keys to connect other files: checkouts.library_id=libraries.id, checkouts.patron_id=customers.id, and checkouts.id=books.id. 
Use these connections to find the corresponding library_id, customer_id, and book_id for each checkout.

4.2 Find and calculate the factors  
- distance: find the zipcodes of the home address of the customer and the library that he/she borrow books from. Calculate the distance between the two zipcodes using a Python library: pgeocode <sup>1,2<sup>  .
- age: find the customer's birth_date and checkout_date. Then, see if the timeline makes sense (check_out_date>birth_date), otherwise, set age as nan.
- new_book_days: find the date of publication and check if the timeline makes sense (check_out_date>pub_date). If so, calculate the days of publication at the checkout date. If missing data or an unreasonable timeline, then set new_book_days as nan. 
- the other factors: find the corresponding location in the data, if any missing data, set the factors as nan.

#### 5. Create lists of factors based on their data types
`data_continuous`: stores factors of distance, age, new_book_days, price, and pages.  
`data_categorical`: stores factors of gender, education, and occupation.  

#### 6. Create a list of labels
Judge whether the book is returned late and assign the checkout to two labels, 0: on-time return and 1: late return.  
If the return date is greater than 28 days after checkout, then it is a late return. Count the total_num_late_return for late returns.  

#### 7. Handle missing values and data preprocessing
- Continuous variables: fill the missing value with mean and normalize each factor using StandardScaler.
- Categorical variables: fill the missing value with the most frequent category and encode each factor using OneHotEncoder (turn each category into a corresponding number).
Combine preprocessed data as features to feed a logistic regression model.

#### 8. Build a logistic regression model
8.1 Split features and labels into training (80%) and testing (20%) sets and shuffle data (random_state=42).  
8.2 Create a logistic regression model and train it.  
8.3 Visualization of the coefficients in the model   
8.4 Generate predictions and print the results of model performance  
The logistic regression model predicts binary outcomes, 0 means on-time return and 1 means late return.  

## Results
The rate of late returns from all the libraries was 19.38 %.  
### Explanation of factors
The factors with larger coefficients, no matter positive or negative values, are the influential factors of late returns.  
A horizontal barplot is created to visualize the magnitude of the coefficients of each factor.  
If the factor is positive, it represents that under the condition of this factor happening, the chance of late return increases. 
If it's negative, then under the condition of the factor, the chance of late return decreases.  
  
Based on the results, the top 10 influential factors with positive (+) and negative (-) relationships to late returns are listed as follows:
- Geographical factor: distance (+).
Customers live in a longer distance from the libraries tend to return books late.
- Behavioural factors:
  - Gender: male(+), and female (-).  
    Men tend to return books late compared to females.  
  - Education level: college (+).  
    Customers with the highest education level in college tend to return books late.  
  - Occupation: blue collar (+), education & health (-), and others (-).  
    Blue-collar customers tend to return books late.  
    Customers who work in the field of education and health tend to return books on time.
- Book-realted factors: new book (+), book price(+), pages(+).  
    Books with a closer release date, a higher price, and more pages tend to be returned late.  
    Newer or more expensive books may be very popular among customers and tend to be returned late.  
    As for thick books, customers may need more time to finish them.  

### Suggestions for the client
1. Build an email reminder system to remind the customers of the date of return automatically.
2. Extend the borrowing policy for customers who live away from libraries.
3. Set up book return boxes around the cities to make returning books easier for customers who live away from libraries.
4. Set up a system where customers can submit a request for extending the borrowing period.
   In this way, the client can know whether customers need more time to finish the book or simply forget to return it.  
   If many customers request an extension, the client can extend the days in the borrowing policy accordingly.
6. The client can set up a reading area in each library that allows customers to read new books on-site only.
   After a period of time, when these books are not so popular, they can be checked out.  
   In this way, it avoids late returns and many customers can enjoy reading time in the libraries.
8. Use the logistic regression model to find which customers may return books late and make customized reminder calls.

### Explanation of model performance
The logistic model can predict the testing set with the results of 0.80 as accuracy, 0.13 as F1-score, 0.62 as precision, and 0.07 as recall.  
The results had very low F1-score and recall, which meant the model tended to predict as 0, which is the majority of data.  
There are four ways to improve the recall.  
1. Collect more data on late returns.  
2. Add the parameter of class_weights in the model to address late return data. For example, set class_weight="balanced" or customize weights class_weight={0:weight_on_time, 1:weight_late} to help the model learn from the features of late returns better.  
3. Find more features/factors to train the model.  
4. Try other classification models, such as a random forest classifier or neural networks.

## Reference
1. Python library pgeocode: [here](https://pgeocode.readthedocs.io/en/latest/generated/pgeocode.GeoDistance.html)  
2. An example of calculating the distance between two zipcodes using geocode: [here](https://stackoverflow.com/questions/67166295/using-pgeocode-in-pandas)











