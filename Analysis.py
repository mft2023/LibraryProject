# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 21:03:31 2024

@author: Meng-Fen Tsai
"""
import numpy as np
import pandas as pd
from datetime import datetime
import pgeocode
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
import matplotlib.pyplot as plt

def clean_date_format(input_date):
    if type(input_date)==str:
        # the dates are separated by special characters, therefore, turn the special characters into '-' if they are not located in the start or end location.
        nums=str();
        for i in range(len(input_date)):
            try:
                if type(int(input_date[i]))==int:
                    nums+=input_date[i];                
            except:
                if i!=0 and i!=len(input_date)-1: # not starting or ending position
                    nums+='-'; #seperator
                else:
                    continue
        try: # MM-DD-YYYY
            ans = datetime.strptime(nums, "%m-%d-%Y");
            return ans
        except:
            try: # DD-MM-YYYY
                ans = datetime.strptime(nums, "%d-%m-%Y");  
                return ans
            except:
                try: # YYYY-MM-DD
                    ans = datetime.strptime(nums, "%Y-%m-%d");  
                    return ans
                except:
                    try: # MMDDYYYY
                        ans = datetime.strptime(nums, "%m%d%Y");  
                        return ans
                    except:
                        try: # DDMMYYYY
                            ans = datetime.strptime(nums, "%d%m%Y");  
                            return ans
                        except:
                            try: # YYYYMMDD
                                ans = datetime.strptime(nums, "%Y%m%d");  
                                return ans
                            except:
                                return ''
    else: # missing value
        return ''
        
def clean_published_year(published_date):
    if type(published_date)==str:
        try: # YYYY-MM-DD
            ans = datetime.strptime(published_date, "%Y-%m-%d");
            return ans
        except:
            try: # YYYY-MM
                ans = datetime.strptime(published_date, "%Y-%m");
                return ans
            except:
                try: # YYYY
                    ans = datetime.strptime(published_date, "%Y");
                    return ans
                except:
                    return ''
    else:
        return ''
    
def clean_txt(txt):
    if type(txt)==str:
        txt=' '.join(txt.split());
        txt=txt.lower();
        return txt
    else:
        return np.nan

def clean_number(number):
    nums=str();
    if type(number)==str:   
        for i in range(len(number)):
            try: 
                if number[i]=='.':
                    nums+=number[i];
                elif type(int(number[i]))==int:
                    nums+=number[i];
            except: # skip any other characters that are not numbers
                continue
        return float(nums)
    else:
        return np.nan
    
def clean_zipcode_format(zipcode):
        nums=str();
        if type(zipcode)==str:
            zipcode=zipcode.split(".")[0]; # remove characters after "."
            for i in range(len(zipcode)):
                try: 
                    int(zipcode[i]);
                    nums+=zipcode[i];    
                except: # skip any other characters that are not numbers
                    continue
            if len(nums)==5: # exact 5 numbers zipcode
                return nums
            else: # cannot identify as correct zipcode format
                return ''
        else:
            return ''

### 1. Load the files and print the percentage of missing values in each file
df_check_out=pd.read_csv('./checkouts.csv');
df_library=pd.read_csv('./libraries.csv');
df_customer=pd.read_csv('./customers.csv');
df_book=pd.read_csv('./books.csv');

print("\n=== Percengate of missing values in each column ===")
print("=== checkouts.csv ===")
missing_values = df_check_out.isnull().sum()
print(round(missing_values/len(df_check_out)*100,2))

print("\n=== libraries.csv ===")
missing_values = df_library.isnull().sum()
print(round(missing_values/len(df_library)*100,2))
    
print("\n=== customers.csv ===")
missing_values = df_customer.isnull().sum()
print(round(missing_values/len(df_customer)*100,2))

print("\n=== book.csv ===")
missing_values = df_book.isnull().sum()
print(round(missing_values/len(df_book)*100,2))


### 2. Find the data with a reasonable timeline
df_check_out.dropna(inplace=True)
df_check_out.reset_index(inplace=True, drop=True)# organize the index to match its length after removing missing values

### 3. Calculate the rates of late returns
dist = pgeocode.GeoDistance('US'); 
print("\n=== Rate of late retruns ===")
total_num_borrow=0;
total_num_late_return=0;
data_continuous=[];
data_categorical=[];
labels=[];
#### 3.1 Go through each checkout and find the checkout and return dates using a for loop.
for i in range(len(df_check_out)):
    library_id=df_check_out['library_id'][i];
    check_out_date = clean_date_format(df_check_out['date_checkout'][i]);
    return_date = clean_date_format(df_check_out['date_returned'][i]);
    #### 3.2 Only a reasonable timeline (check_out_date<return_date) will be analyzed.
    if return_date>check_out_date:
        total_num_borrow+=1;
        #### 4.Data Cleaning for each attribute selected in the analysis reasoning section.
        try:
            ### 4.1 Find the corresponding index in the other files 
            loc_lib=df_library['id'].to_list().index(library_id); 
            loc_cus=df_customer['id'].to_list().index(df_check_out['patron_id'][i]);
            loc_book=df_book['id'].to_list().index(df_check_out['id'][i]);
            
            ### 4.2 Find and calculate the factors: distance, age, gender, education level, occupation, new book, price, and pages.
            # get library zipcode
            zip_lib=df_library['postal_code'][loc_lib];
            zip_lib=clean_zipcode_format(zip_lib);
            # get customer's zipcode
            zip_customer=df_customer['zipcode'][loc_cus];
            zip_customer=clean_zipcode_format(zip_customer);
            # Get distance (in km) between postal codes
            distance=dist.query_postal_code(clean_zipcode_format(zip_lib),clean_zipcode_format(zip_customer));        
            
            # age
            DOB=df_customer['birth_date'][loc_cus];
            DOB=clean_date_format(DOB);
            if DOB!='':
                if check_out_date>DOB: # resonable timeline
                    age=round((check_out_date-DOB).days/365);# age (y/o) when checkout the book
                else:
                    age=np.nan
            else:
                age=np.nan
            
            # gender
            gender=df_customer['gender'][loc_cus];
            gender=clean_txt(gender);
            
            # education
            education=df_customer['education'][loc_cus];
            education=clean_txt(education);
            
            # occupation
            occupation=df_customer['occupation'][loc_cus];
            occupation=clean_txt(occupation);

            # new books
            pub_date=df_book['publishedDate'][loc_book];
            pub_date=clean_published_year(pub_date);
            if pub_date!='':
                if check_out_date>pub_date:# reasonable timeline
                    new_book_days=(check_out_date-pub_date).days;# days after published when checkout
                else:
                    new_book_days=np.nan
            else:
                new_book_days=np.nan
            
            # price
            price=df_book['price'][loc_book];
            price=clean_number(price);

            # pages
            pages=df_book['pages'][loc_book];
            pages=clean_number(pages);
            
            ### 5. Create lists of factors based on their data types
            data_continuous.append([distance, age, new_book_days, price, pages]);
            data_categorical.append([gender, education, occupation]);
            
            #### 6. Create a list of labels
            if (return_date-check_out_date).days>28:# late returns
                total_num_late_return+=1;                        
                labels.append(1)# late returns
            else: 
                labels.append(0)# on-time returns
        except:
            continue
print("Rate of late return: ", round((total_num_late_return/total_num_borrow)*100,2), " %")
ontime_perc=sum(labels)/len(labels);
late_perc=1-ontime_perc;
print("Dataset composition: on-time returns - ",round(ontime_perc*100,2), "%, late returns - ",round(late_perc*100,2),"%") 

### 7. Handle missing values and data preprocessing
# Continuous variables
X_continuous = pd.DataFrame(data_continuous, columns =['distance', 'age', 'new_book_days', 'book_price', 'book_pages']);
for key in X_continuous.keys():
    # replace the missing value with mean
    X_continuous[key].fillna(X_continuous[key].mean(), inplace = True);

scaler = StandardScaler();
X_continuous_scaled = pd.DataFrame(scaler.fit_transform(X_continuous), columns=X_continuous.keys())

# Categorical variables
X_categorical = pd.DataFrame(data_categorical, columns =['gender', 'education', 'occupation']);
for key in X_categorical.keys():
    # replace the missing value with the most frequent category
    X_categorical[key].fillna(X_categorical[key][X_categorical[key].notnull()].mode()[0], inplace = True)
encoder = OneHotEncoder(sparse_output=False);
X_categorical_encoded = pd.DataFrame(encoder.fit_transform(X_categorical), columns=encoder.get_feature_names_out())

# Combine preprocessed data as features
X_processed = pd.concat([X_continuous_scaled, X_categorical_encoded], axis=1)

### 8. Build a logistic regression model
# 8.1 Split features and labels into training (80%) and testing (20%) sets and shuffle data (random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X_processed, labels, test_size=0.2, random_state=42)

# 8.2 Create a logistic regression model and train it
model=LogisticRegression(class_weight={0: late_perc, 1: ontime_perc}) # address to imbalanced classes
model.fit(X_train, y_train)

# 8.3 Generate predictions and print the results of model performance
y_pred=model.predict(X_test);
print("\n=== Results of Logistic Regression Model ===")
f1=f1_score(y_test, y_pred);
precision=precision_score(y_test, y_pred);
recall=recall_score(y_test, y_pred);
accuracy = accuracy_score(y_test, y_pred);
print("Accuracy:", round(accuracy,2));
print("F1-score: ",round(f1,2));
print("precision: ",round(precision,2));
print("recall: ",round(recall,2));

# 8.4 Visualize the magnitudes of the coefficients in the model
weights_factors=pd.DataFrame(model.coef_,columns=X_processed.columns); 
# the top 10 factors are:
print('\n=== Top 10 factors of returning late ===')
rank_factors=abs(weights_factors).rank(axis=1, ascending=False);
for factor in rank_factors.keys():
    if rank_factors[factor][0]<=10:
        print(factor, round(weights_factors[factor][0],2))

plt.figure(1)
plt.barh(weights_factors.columns,weights_factors.loc[0])
plt.subplots_adjust(left=0.35, right=0.9, top=0.9, bottom=0.1)
plt.title('Relationship between Each Factor and Late Return')
plt.xlabel('Magnitude of Logistic Regression Model Coefficients')
plt.xlim([-1,1])
plt.show()
