# LibraryProject
This repository is about analyzing some library-related data, finding explainable factors of late book returns, affording suggestions for libraries to avoid late returns, and visualizing results.

## Background
The libraries in Oregon provide their data to find possible factors of returning books late, defined as books returned after 28 days after checkout. They would like to pay attention to the factors and find a way to monitor returning rate in order to prevent late returns. The data they have is described as follows.

## Data format and attributes
There are 4 files, including checkouts.csv, libraries.csv, books.csv, and customers.csv.
- checkouts.csv has 5 columns: id, patron_id, library_id, date_checkout, and date_returned. 
  There are 3 external keys to connect other files: checkouts.id=books.id, checkouts.patron_id=customers.id, checkouts.library_id=libraries.id.
- libraries.csv has 6 columns: id, name, street_address, city, region, and postal_code.
- books.csv has 8 columns:  id, title, authors, publisher, publishedDate, categories, price, and pages.
- customers.csv has 10 columns: id, name, street_address, city, state, zipcode, birth_date, gender, education, and occupation.

