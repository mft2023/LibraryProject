# LibraryProject
This repository is about analyzing some library-related data, finding explainable factors of late book returns, affording suggestions for libraries to avoid late returns, and visualizing results.

## Background
The libraries in Oregon provide their data to find possible factors of returning books late, defined as books returned after 28 days of checkout. They would like to pay attention to the factors and find a way to monitor returning rate to prevent late returns. The data they have is described as follows.

## Data format and attributes
There are 4 files, including checkouts.csv, libraries.csv, books.csv, and customers.csv.
- checkouts.csv has 5 columns: id, patron_id, library_id, date_checkout, and date_returned. 
  There are 3 external keys to connect other files: checkouts.id=books.id, checkouts.patron_id=customers.id, checkouts.library_id=libraries.id.
- libraries.csv has 6 columns: id, name, street_address, city, region, and postal_code.
- books.csv has 8 columns:  id, title, authors, publisher, publishedDate, categories, price, and pages.
- customers.csv has 10 columns: id, name, street_address, city, state, zipcode, birth_date, gender, education, and occupation.

## Data Analysis
#### Each step in the analysis is also numbered in the Python script accordingly.
### 1. Investigate data composition and percentage of missing values in each file to decide what attributes are useful. 
There are 3 categories of factors: geographical factors, human factors, and book factors. 
- Geographical factors: distance between home and the library. Customers may not pass by the library on their routine trips if they live away from it and tend to return books late.
- Human factors: age, gender, education level, and occupation.
- Book factors: new book, price, and pages. Newly released books may be very popular among customers' family and friends. Other people may borrow books from the customers. More pages in a book may require more time to finish. These are potential factors for returning books late.

If the majority of the data is missing, then it's not suitable to consider as a factor since the results may be misleading. Here, I only analyzed the attributes/factors that are missing less than 10% of data.
### 2. Find the data with a reasonable timeline
#### 2.1 Remove the data with missing checkout or return dates because we won't be able to judge whether the books are returned on time.
```
