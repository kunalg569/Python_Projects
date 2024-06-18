<h1><center>Purpose</center></h1>

To Analyze the total compensation(salaries) based on `Company, Gender, Race, Education and Years of Experience` for STEM salaries

<h1><center>Goal</center></h1>

Perform EDA and build a regression model that can predict salaries, parameters for which will be decided during analysis phase

## Questions that will be addressed

1. Is there a relation between salary and education?
1. What is the yearly compensation based on Job title
1. IS there a relationship between exeprience and salary?
1. Is there a salary disparity due to Race?
1. Is there a salary disparity due to Gender?
1. Which are the top locations for employment?
1. How much do the FAANG companies pay on an average ?
1. Which is the hottest job title with respect to number of employees ?

## The EDA process is divided in the following phases:
* Discovery: Familiarizing with data
* Cleaning: Removing NaN, mispellings, outliers and duplicates
* Validating: Verifying if the data is consistent 
* Analysis: Performing in depth analysis for seeking relationships or trends

## Modelling is divided in the following phases:

1. Structuring the cleaned data set
1. Label Encoding
1. Splitting the dataset into training set and test set
1. Scaling our feature and target variables wrt to their interquartile ranges using Robust Scaler
1. Using regression model to fit the data and making predictions

# Executive Summary:
* There is no salary disparity with respect to Race or Gender. 
* Specifically, companies are ready to pay large salaries for Managerial positions. 
* Also, Software Engineer is the hottest job in 2023. 
* Surprising enough, level of education is not indicative of the salary of an employee but the years of experience and the job title is.

# Future Work:

The study can be expanded with more data points as +60K data points is relatively a small data set. This will enable us to build more accurate models as a sample would be more representative of the population. Predictive madelling can be carried out using other paramters like Location, Level of the Employee in the company and number of years at the company.
