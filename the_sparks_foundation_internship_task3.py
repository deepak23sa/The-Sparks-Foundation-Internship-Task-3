# -*- coding: utf-8 -*-
"""The_Sparks_Foundation_Internship_Task3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nVmsa6WtcB0dVpa2qyeJgz_5rjZkUlLY

**Name: Deepak Sagar**                                                          

**Objective:**

**1. Perform ‘Exploratory Data Analysis’ on dataset ‘SampleSuperstore**

**2.Try to find out the weak areas where you can work to make more profit**

**3. What all business problems you can derive by exploring the data?**

**Data Preperation**
"""

# Commented out IPython magic to ensure Python compatibility.
# Import neccessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *
# %matplotlib inline

# Load the CSV file
Superstore = pd.read_csv("https://raw.githubusercontent.com/deepak23sa/The-Sparks-Foundation-Internship-Task-3/main/SampleSuperstore.csv")
Superstore.head()

# Checking number of rows and column in dataframe
Superstore.shape

Superstore.info()

Superstore.describe()

# Checking the duplication in data
Superstore.duplicated().sum()

Superstore.drop_duplicates(inplace=True)

Superstore.head()

# Count the nummber of unique elements in each column
Superstore.nunique()

# Deleting the variable
sample = Superstore.drop(['Postal Code'],axis=1)

sample.head()

# Correlation between variables
sample.corr()

#Covariance between variable
sample.cov()

"""

**Exploratory Analysis and Visualization**
"""

plt.figure(figsize=(10,5))
plt.bar('Sub-Category','Category',facecolor='green',data=sample)
plt.title('Category vs Sub Category')
plt.xlabel('Sub-Catgory')
plt.ylabel('Category')
plt.xticks(rotation=45)
plt.show()

# Frequency distribution of Sales, Quantity, Discount and Profit
sample.hist(bins=50 ,figsize=(20,15))
plt.show();

# Count the total repeatable states
sample['State'].value_counts()

plt.figure(figsize=(16,8))
sns.countplot(x=sample['State'])
plt.xticks(rotation=90)
plt.title("STATE")
plt.show()

# Visualise the profit and loss off different sub-categories
Profit_plot = (ggplot(sample, aes(x='Sub-Category', y='Profit', fill='Sub-Category')) + geom_col() + coord_flip()
              + scale_fill_brewer(type='div', palette='Spectral') + theme_classic())

display(Profit_plot)

"""Here from the above graph we can visualize that "binders" sub-category has suffered the highest amount of loss and also profit amongst all other sub-Categories (For now we can't say that what is the reason it may be because of discounts given on binders subcategory).

Next,"Copiers" Sub-category has gain highest amount of profit with no loss.There are other sub-categories too who are not faced any kind of losses but their profit margins are also low.

Next,Suffering from highest loss is machines.
"""

ggplot(sample, aes(x='Ship Mode', fill = 'Category')) + geom_bar(stat = 'count')

figsize=(10,7)
sns.pairplot(sample,hue='Sub-Category')
plt.show

"""**Let's explore more about these outliers by using boxplots.**

**First we'll check Sales from Every Segments of Whole Data**
"""

flip_xlabels = theme(axis_text_x = element_text(angle=90, hjust=1),figure_size=(8,4), axis_ticks_length_major=10,axis_ticks_length_minor=5)
(ggplot(sample, aes(x='Sub-Category', fill='Sales')) + geom_bar() + facet_wrap(['Segment']) 
+ flip_xlabels +theme(axis_text_x = element_text(size=12))+ggtitle("Sales From Every Segment Of United States of Whole Data"))

"""From above Graph we can say that "Home Office" segment has less purchased Sub-Categories and in that "Copiers" has the lowest Sales. "Consumer" has purchased more sub-categories as compared to other segments."""

flip_xlabels = theme(axis_text_x = element_text(angle=90, hjust=10),figure_size=(8,4), axis_ticks_length_major=30,axis_ticks_length_minor=30)
(ggplot(sample, aes(x='Category', fill='Sales')) + geom_bar() + theme(axis_text_x = element_text(size=10)) + facet_wrap(['Region']) + 
 flip_xlabels+ ggtitle("Sales From Every Region Of United States of Whole Data"))

# Relation between Profit and Discount given on items
plt.figure(figsize=(10,4))
sns.lineplot('Discount','Profit', data=sample , color='r',label='Discount')
plt.legend()
plt.show()

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

state_code = {'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE',
                'Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY',
                'Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO',
                'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY',
                'North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Rhode Island': 'RI',
                'South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virginia': 'VA',
                'District of Columbia': 'WA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}
sample['state_code'] = sample.State.apply(lambda x: state_code[x])

state_data = sample[['Sales', 'Profit', 'state_code']].groupby(['state_code']).sum()

fig = go.Figure(data=go.Choropleth(locations=state_data.index, z = state_data.Sales, locationmode = 'USA-states', colorscale = 'blues',
                                   colorbar_title = 'Sales in USD'))

fig.update_layout(title_text = 'Total State-Wise Sales',geo_scope='usa',height=600)

fig.show()

"""Now, let us analyze the sales of a few random states from each profit bracket (high profit, medium profit, low profit, low loss and high loss) and try to observe some crucial trends which might help us in increasing the sales."""

def state_data_viewer(states):
  product_data = sample.groupby(['State'])
  for state in states:
    data = product_data.get_group(state).groupby(['Category'])
    fig, ax = plt.subplots(1, 3, figsize = (28,5))
    fig.suptitle(state, fontsize=10)        
    ax_index = 0
    for category in ['Furniture', 'Office Supplies', 'Technology']:
      category_data = data.get_group(category).groupby(['Sub-Category']).sum()
      sns.barplot(x = category_data.Profit, y = category_data.index, ax = ax[ax_index])
      ax[ax_index].set_ylabel(category)
      ax_index +=1
    fig.show()

states = ['California', 'Washington', 'Mississippi', 'Arizona', 'Texas']
state_data_viewer(states)

x = sample.iloc[:, [9, 10, 11]].values

from sklearn.cluster import KMeans
wcss = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0).fit(x)
    wcss.append(kmeans.inertia_)

sns.set_style("whitegrid") 
sns.FacetGrid(sample, hue ="Sub-Category",height = 6).map(plt.scatter,'Sales','Quantity')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,1], 
            s = 100, c = 'yellow', label = 'Centroids')

plt.legend()
plt.show()

sns.set_style("whitegrid") 
sns.FacetGrid(sample, hue ="Sub-Category",height = 6).map(plt.scatter,'Sales','Profit')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:,1], 
            s = 100, c = 'yellow', label = 'Centroids')

plt.legend()
plt.show()

fig, ax = plt.subplots(figsize = (10 , 6))
ax.scatter(sample["Sales"] , sample["Profit"])
ax.set_xlabel('Sales')
ax.set_ylabel('Profit')
ax.set_title('Sales vs Profit')
plt.show()

"""**Conclusion:**

From the Above data Visualization and Clustering we can see that in Which states and in which Category Sales and profits are High or less,We can improve in that States By Providing Discounts in prefered Range so that Company and cosumer both will be in profit.So For Deciding that Range we have to do some Technical Analysis.One can Do it through Factor Analysis,or also can Do it throgh neural networks.

One thing to be noted is that while the superstore is incurring losses due to giving discounts on its products, they can't stop giving discounts of their products. Most of the heavy discounts are during festivals, end-of-season and clearance sales which are necessary so that the store can make space in their warehouses for fresh stock. Also, by incurring small losses, the company gains in the future by attracting more long term customers. Therefore, the small losses from discounts are an essential part of company's business
"""