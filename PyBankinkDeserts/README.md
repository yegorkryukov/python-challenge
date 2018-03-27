
# Banking Deserts
---
The below script uncovers the well-known phenomenon of [Banking Deserts](https://en.wikipedia.org/wiki/Banking_desert). The concept is simple: many neighborhoods with predominantly low-income and elderly populations tend to have inadequate coverage of banking services. This leads such communities to be  vulnerable to predatory loan and pricey check casher providers.

In this script, we retrieved and plotted data from the 2013 US Census and Google Places API to show the relationship between various socioeconomic parameters and bank count across 700 randomly selected zip codes. We used Pandas, Numpy, Matplotlib, Requests, Census API, and Google API to accomplish our task.


```python
# Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import time
from pprint import pprint
# Google Places API Key from config
from config import gkey
```

## Data Retrieval


```python
# Import the census data into a pandas DataFrame
census_df = pd.read_csv('Census_Data.csv')

# Preview the data
census_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zipcode</th>
      <th>Address</th>
      <th>Population</th>
      <th>Median Age</th>
      <th>Household Income</th>
      <th>Per Capita Income</th>
      <th>Poverty Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>15081</td>
      <td>South Heights, PA 15081, USA</td>
      <td>342</td>
      <td>50.2</td>
      <td>31500.0</td>
      <td>22177</td>
      <td>20.760234</td>
    </tr>
    <tr>
      <th>1</th>
      <td>20615</td>
      <td>Broomes Island, MD 20615, USA</td>
      <td>424</td>
      <td>43.4</td>
      <td>114375.0</td>
      <td>43920</td>
      <td>5.188679</td>
    </tr>
    <tr>
      <th>2</th>
      <td>50201</td>
      <td>Nevada, IA 50201, USA</td>
      <td>8139</td>
      <td>40.4</td>
      <td>56619.0</td>
      <td>28908</td>
      <td>7.777368</td>
    </tr>
    <tr>
      <th>3</th>
      <td>84020</td>
      <td>Draper, UT 84020, USA</td>
      <td>42751</td>
      <td>30.4</td>
      <td>89922.0</td>
      <td>33164</td>
      <td>4.392880</td>
    </tr>
    <tr>
      <th>4</th>
      <td>39097</td>
      <td>Louise, MS 39097, USA</td>
      <td>495</td>
      <td>58.0</td>
      <td>26838.0</td>
      <td>17399</td>
      <td>34.949495</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Randomly select 700 zip codes locations that have at least 100 residents
# Hint: `pd.sample()`
# Hint: `pd[pd[astype(int) > 100`]]`

census_df = census_df[census_df['Population'].astype(int) > 100].sample(n=700)

# Visualize the DataFrame
#census_df.count()
```


```python
# Create a DataFrame with only a subset of the zipcodes for testing purposes
# One your code runs successfully, run it on all 700.
census_df = census_df[census_df['Zipcode'].astype(int) > 80000]
census_df.count()
```




    Zipcode              95
    Address              95
    Population           95
    Median Age           95
    Household Income     95
    Per Capita Income    95
    Poverty Rate         95
    dtype: int64




```python
# Create blank columns in DataFrame for lat/lng
census_df['lat'], census_df['lng'] = '',''

# Loop through and grab the lat/lng for each of the selected zips using Google maps
# Inside the loop add the lat/lng to our DataFrame
# Note: Be sure to use try/except to handle cities with missing data

for index, row in census_df.iterrows():
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {
        'address':f'{row["Zipcode"]}',
        "key": gkey
    }
    cities_lat_lng = requests.get(base_url, params=params).json()
    
    census_df.at[index,'lat'] = cities_lat_lng['results'][0]['geometry']['location']['lat']
    census_df.at[index,'lng'] = cities_lat_lng['results'][0]['geometry']['location']['lng']


# Visualize the DataFrame
census_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zipcode</th>
      <th>Address</th>
      <th>Population</th>
      <th>Median Age</th>
      <th>Household Income</th>
      <th>Per Capita Income</th>
      <th>Poverty Rate</th>
      <th>lat</th>
      <th>lng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>287</th>
      <td>98362</td>
      <td>Port Angeles, WA 98362, USA</td>
      <td>22052</td>
      <td>47.5</td>
      <td>43827.0</td>
      <td>25914</td>
      <td>14.388718</td>
      <td>48.0962</td>
      <td>-123.301</td>
    </tr>
    <tr>
      <th>77</th>
      <td>89316</td>
      <td>Eureka, NV 89316, USA</td>
      <td>1513</td>
      <td>38.7</td>
      <td>63603.0</td>
      <td>26280</td>
      <td>14.871117</td>
      <td>39.5649</td>
      <td>-115.994</td>
    </tr>
    <tr>
      <th>239</th>
      <td>92252</td>
      <td>Joshua Tree, CA 92252, USA</td>
      <td>10047</td>
      <td>45.0</td>
      <td>42338.0</td>
      <td>22951</td>
      <td>18.771773</td>
      <td>34.1938</td>
      <td>-116.254</td>
    </tr>
    <tr>
      <th>380</th>
      <td>83841</td>
      <td>Laclede, ID 83841, USA</td>
      <td>171</td>
      <td>60.8</td>
      <td>26618.0</td>
      <td>23912</td>
      <td>0.000000</td>
      <td>48.1659</td>
      <td>-116.758</td>
    </tr>
    <tr>
      <th>344</th>
      <td>90210</td>
      <td>Beverly Hills, CA 90210, USA</td>
      <td>21548</td>
      <td>46.4</td>
      <td>132254.0</td>
      <td>111364</td>
      <td>7.420642</td>
      <td>34.103</td>
      <td>-118.41</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Create an empty column for bank count
census_df['bank_count'] = ''

# Re-loop through the DataFrame and run a Google Places search to get all banks in 5 mile radius (8000 meters)
# Inside the loop add the bank count to our DataFrame

# Set up params
params = {
    "radius": 8000, 
    "type": "bank",
    "key": gkey
}

#set up base_url
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'

#set up placehorder of urls for debugging
urls = []

def requester(base_url, params, next_page_token=None):
    """
    Returns the 'results' list of google places API request
    including multipage responses (up to 60 results).
    base_url: Google Places API Nearby Search request as HTTP URL 
    params: dictionary. Required keys: key, location, radius and (keyword|name|type)
    """
    #add next page key to params if next page token exists
    if next_page_token:
        params['pagetoken'] = next_page_token
    
    #get request
    r = requests.get(base_url, params=params)
    
    #uncomment line below to print request urls to console
    #print(f'Just got the response from: {r.url}')
    urls.append(r.url)
    
    #read as json
    response = r.json()
    
    #check response status
    if response['status'] == 'ZERO_RESULTS':
        #print('Zero results')
        #if no results fount return an empty list (length of 0)
        return []
    elif response['status'] == 'INVALID_REQUEST':
        raise Exception('INVALID_REQUEST: operation stopped') 
    elif response['status'] == 'OK':
        #if response if OK save results list to a variable
        results = response['results'] 

        #check for next page token in response
        if 'next_page_token' in response:
            #uncomment line below to print the token to the console
            #print(f'Next token found : {response["next_page_token"]}')

            #google won't return next page if the request is made in less 
            #than 2 seconds so we wait for 2.1
            time.sleep(2.1)

            #make a recursive call to the same 'requester' function
            #this call will continue to happen until there is a next page 
            #token in the response
            next_page = requester(base_url, params, response['next_page_token'])

            #since 'requester' returns a list we just add the returning list 
            #to existing list of results
            results = results + next_page
         
        #return list of places as a list
        return results
    
  
#variable to limit number of requests
k = 1

for index, row in census_df.iterrows():
    
    # update params with zipcode each loop
    params['location'] = f"{row['lat']},{row['lng']}"
    
    #uncomment to see the requests flow
    #print(f'Running request for row #:{k}')
    
    #assign resulting list to a variable 'results'
    results = requester(base_url, params)
    
    #add number of banks to the DF
    #we don't need to check for errors because error handling
    #is done inside 'requester' function
    census_df.at[index,'bank_count'] = len(results)
    
    #increase k 
    k += 1 
    
    #uncomment and change k to number of runs you need
    if k == 10:
        break

# Visualize the DataFrame
census_df.head()
```

    Zero results





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Zipcode</th>
      <th>Address</th>
      <th>Population</th>
      <th>Median Age</th>
      <th>Household Income</th>
      <th>Per Capita Income</th>
      <th>Poverty Rate</th>
      <th>lat</th>
      <th>lng</th>
      <th>bank_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>380</th>
      <td>83841</td>
      <td>Laclede, ID 83841, USA</td>
      <td>171</td>
      <td>60.8</td>
      <td>26618.0</td>
      <td>23912</td>
      <td>0.000000</td>
      <td>48.1659</td>
      <td>-116.758</td>
      <td>0</td>
    </tr>
    <tr>
      <th>344</th>
      <td>90210</td>
      <td>Beverly Hills, CA 90210, USA</td>
      <td>21548</td>
      <td>46.4</td>
      <td>132254.0</td>
      <td>111364</td>
      <td>7.420642</td>
      <td>34.103</td>
      <td>-118.41</td>
      <td>60</td>
    </tr>
    <tr>
      <th>669</th>
      <td>85553</td>
      <td>Tonto Basin, AZ 85553, USA</td>
      <td>1441</td>
      <td>64.6</td>
      <td>36442.0</td>
      <td>28245</td>
      <td>16.932686</td>
      <td>33.8103</td>
      <td>-111.237</td>
      <td>20</td>
    </tr>
    <tr>
      <th>481</th>
      <td>95051</td>
      <td>Santa Clara, CA 95051, USA</td>
      <td>53152</td>
      <td>36.1</td>
      <td>100504.0</td>
      <td>43487</td>
      <td>6.865217</td>
      <td>37.3598</td>
      <td>-121.981</td>
      <td>20</td>
    </tr>
    <tr>
      <th>561</th>
      <td>97366</td>
      <td>Newport, OR 97366, USA</td>
      <td>1301</td>
      <td>58.8</td>
      <td>53135.0</td>
      <td>36010</td>
      <td>4.996157</td>
      <td>44.5772</td>
      <td>-124.054</td>
      <td>20</td>
    </tr>
  </tbody>
</table>
</div>



## Save to a CSV


```python
# Save the DataFrame as a csv

```

## Plot & Save Graphs


```python
# Build a scatter plot for each data type 

```


```python
# Build a scatter plot for each data type
plt.scatter(selected_zips["Bank Count"], 
            selected_zips["Median Age"],
            edgecolor="black", linewidths=1, marker="o", 
            alpha=0.8, label="Zip Codes")

# Incorporate the other graph properties
plt.title("Median Age vs. Bank Count by Zip Code")
plt.ylabel("Median Age")
plt.xlabel("Bank Count")
plt.grid(True)
plt.xlim([-2.5, 202])

# Save the figure
plt.savefig("output_analysis/Age_BankCount.png")

# Show plot
plt.show()
```


```python
# Build a scatter plot for each data type
plt.scatter(selected_zips["Bank Count"], 
            selected_zips["Household Income"],
            edgecolor="black", linewidths=1, marker="o", 
            alpha=0.8, label="Zip Codes")

# Incorporate the other graph properties
plt.title("Household Income vs. Bank Count by Zip Code")
plt.ylabel("Household Income ($)")
plt.xlabel("Bank Count")
plt.grid(True)
plt.xlim([-2.5, 202])
plt.ylim([-2.5, 230000])

# Save the figure
plt.savefig("output_analysis/HouseholdIncome_BankCount.png")

# Show plot
plt.show()
```


```python
# Build a scatter plot for each data type
plt.scatter(selected_zips["Bank Count"], 
            selected_zips["Per Capita Income"],
            edgecolor="black", linewidths=1, marker="o", 
            alpha=0.8, label="Zip Codes")

# Incorporate the other graph properties
plt.title("Per Capita Income vs. Bank Count by Zip Code")
plt.ylabel("Per Capita Income (%)")
plt.xlabel("Bank Count")
plt.grid(True)
plt.xlim([-2.5, 202])
plt.ylim([0, 165000])

# Save the figure
plt.savefig("output_analysis/PerCapitaIncome_BankCount.png")

# Show plot
plt.show()
```


```python
# Build a scatter plot for each data type
plt.scatter(selected_zips["Bank Count"], 
            selected_zips["Poverty Rate"],
            edgecolor="black", linewidths=1, marker="o", 
            alpha=0.8, label="Zip Codes")

# Incorporate the other graph properties
plt.title("Poverty Rate vs. Bank Count by Zip Code")
plt.ylabel("Poverty Rate (%)")
plt.xlabel("Bank Count")
plt.grid(True)
plt.xlim([-2.5, 202])
plt.ylim([-2.5, 102])

# Save the figure
plt.savefig("output_analysis/PovertyRate_BankCount.png")

# Show plot
plt.show()
```
