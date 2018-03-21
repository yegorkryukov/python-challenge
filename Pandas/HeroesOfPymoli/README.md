

```python
# Dependencies
import pandas as pd
import numpy as np

# Create a reference the CSV file desired
json_path = "Resources/purchase_data.json"

# Read the file into a Pandas DataFrame
# 'records' : list like [{column -> value}, ... , {column -> value}]
pymoli_df = pd.read_json(json_path, orient='records')

# Print the first five rows of data to the screen
#pymoli_df.head()
```


```python
#rename SN -> Player
pymoli_df = pymoli_df.rename(columns = {'SN':'Player'})
pymoli_df.head()
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
      <th>Age</th>
      <th>Gender</th>
      <th>Item ID</th>
      <th>Item Name</th>
      <th>Price</th>
      <th>Player</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>38</td>
      <td>Male</td>
      <td>165</td>
      <td>Bone Crushing Silver Skewer</td>
      <td>3.37</td>
      <td>Aelalis34</td>
    </tr>
    <tr>
      <th>1</th>
      <td>21</td>
      <td>Male</td>
      <td>119</td>
      <td>Stormbringer, Dark Blade of Ending Misery</td>
      <td>2.32</td>
      <td>Eolo46</td>
    </tr>
    <tr>
      <th>2</th>
      <td>34</td>
      <td>Male</td>
      <td>174</td>
      <td>Primitive Blade</td>
      <td>2.46</td>
      <td>Assastnya25</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21</td>
      <td>Male</td>
      <td>92</td>
      <td>Final Critic</td>
      <td>1.36</td>
      <td>Pheusrical25</td>
    </tr>
    <tr>
      <th>4</th>
      <td>23</td>
      <td>Male</td>
      <td>63</td>
      <td>Stormfury Mace</td>
      <td>1.27</td>
      <td>Aela59</td>
    </tr>
  </tbody>
</table>
</div>



**Player Count**

* Total Number of Players


```python
#setup result dataframe
results_df = pd.DataFrame(columns = ['Total Players'])

#calculate number of unique players
results_df.loc[1] = pymoli_df['Player'].nunique()

results_df
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
      <th>Total Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>573</td>
    </tr>
  </tbody>
</table>
</div>



**Purchasing Analysis (Total)**

* Number of Unique Items
* Average Purchase Price
* Total Number of Purchases
* Total Revenue


```python
#calculate values
results_df['Number of Unique Items'] = pymoli_df['Item ID'].nunique()
results_df['Average Purchase Price'] = round(pymoli_df['Price'].mean(),2)
results_df['Total Number of Purchases'] = pymoli_df.shape[0]
results_df['Total Revenue'] = pymoli_df['Price'].sum()

#assign formats
results_df['Average Purchase Price'] = results_df['Average Purchase Price'].map('${:,.2f}'.format)
results_df['Total Revenue'] = results_df['Total Revenue'].map('${:,.2f}'.format)
results_df
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
      <th>Total Players</th>
      <th>Number of Unique Items</th>
      <th>Average Purchase Price</th>
      <th>Total Number of Purchases</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>573</td>
      <td>183</td>
      <td>$2.93</td>
      <td>780</td>
      <td>$2,286.33</td>
    </tr>
  </tbody>
</table>
</div>



#  Gender Demographics

* Percentage and Count of Male Players
* Percentage and Count of Female Players
* Percentage and Count of Other / Non-Disclosed


```python
#setup result dataframe and calculate totals
demografics_df = (pymoli_df.groupby('Gender')['Player'].nunique()).to_frame()

#remove index name
demografics_df.index.name = ''

#calculate pecentage
demografics_df['Pecentage of Players'] = ( demografics_df['Player'] / \
                                           demografics_df['Player'].sum() * 100 \
                                           ).map('{0:.2f}%'.format)

#rename columns
demografics_df = demografics_df.rename(columns={'Player':'Total Count'})

#swap columns
demografics_df = demografics_df.reindex(columns = ['Pecentage of Players','Total Count'])

demografics_df
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
      <th>Pecentage of Players</th>
      <th>Total Count</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>17.45%</td>
      <td>100</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>81.15%</td>
      <td>465</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>1.40%</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>



**Purchasing Analysis (Gender)** 

* The below each broken by gender
  * Purchase Count
  * Average Purchase Price
  * Total Purchase Value
  * Normalized Totals
  
# Ask TAs about normalized totals!!!


```python
#setup result dataframe and calculate totals
purchases_df = pymoli_df.groupby('Gender').aggregate({'Item ID':np.count_nonzero, 'Price':np.sum})
                
#remove index name
purchases_df.index.name = ''

#rename columns
purchases_df = purchases_df.rename(columns={'Item ID':'Purchase Count', 'Price':'Total Purchase Value'})

#calculate values
purchases_df['Average Purchase Price'] = (purchases_df['Total Purchase Value']/purchases_df['Purchase Count']) \
                                            .map('${:,.2f}'.format)

purchases_df['Normalized Totals'] = (purchases_df['Total Purchase Value']/demografics_df['Total Count']) \
                                            .map('${:,.2f}'.format)

purchases_df
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
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
      <th>Average Purchase Price</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>136</td>
      <td>382.91</td>
      <td>$2.82</td>
      <td>$3.83</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>632</td>
      <td>1867.68</td>
      <td>$2.96</td>
      <td>$4.02</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>11</td>
      <td>35.74</td>
      <td>$3.25</td>
      <td>$4.47</td>
    </tr>
  </tbody>
</table>
</div>



**Age Demographics**

* The below each broken into bins of 4 years (i.e. &lt;10, 10-14, 15-19, etc.) 
  * Purchase Count
  * Average Purchase Price
  * Total Purchase Value
  * Normalized Totals


```python
#assign bins
bins = [0,10,14,19,24,29,34,39,100]
bins_names = ['<10','10-14','15-19','20-24','25-29','30-34','35-39','40+']

#add 'Age Group' column to original df
pymoli_df['Age Group'] = pd.cut(pymoli_df['Age'], bins, labels=bins_names)

#group players by age
players_age_df = (pymoli_df.groupby('Age Group')['Player'].nunique()).to_frame()

#remove index name
players_age_df.index.name = ''

#rename columns
players_age_df.columns = ['Total Count of Players']

#calculate percentage
players_age_df['Percentage of Players'] = ( players_age_df['Total Count of Players'] / \
                                            players_age_df['Total Count of Players'].sum() * 100 \
                                          ) .map('{0:.2f}%'.format)
                                          

players_age_df
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
      <th>Total Count of Players</th>
      <th>Percentage of Players</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>22</td>
      <td>3.84%</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>20</td>
      <td>3.49%</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>100</td>
      <td>17.45%</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>259</td>
      <td>45.20%</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>87</td>
      <td>15.18%</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>47</td>
      <td>8.20%</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>27</td>
      <td>4.71%</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>11</td>
      <td>1.92%</td>
    </tr>
  </tbody>
</table>
</div>




```python
#calculate purchase totals and counts
age_df = pymoli_df.groupby('Age Group').aggregate({'Item ID':np.count_nonzero, 'Price':np.sum})

#rename columns
age_df = age_df.rename(columns={'Item ID':'Purchase Count', 'Price':'Total Purchase Value'})

#calculate average purchase value
age_df['Average Purchase Value'] = (age_df['Total Purchase Value'] / age_df['Purchase Count']) \
                                    .map('${:,.2f}'.format)

#calculate normalized purchase value
age_df['Normalized Purchase Value'] = (age_df['Total Purchase Value'] / \
                                       players_age_df['Total Count of Players']).map('${:,.2f}'.format)

#calculate percent of all purchases
age_df['Percentage of Purchases'] = (age_df['Total Purchase Value'] / \
                                     age_df['Total Purchase Value'].sum() * 100 \
                                    ).map('{0:.2f}%'.format)

age_df
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
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
      <th>Average Purchase Value</th>
      <th>Normalized Purchase Value</th>
      <th>Percentage of Purchases</th>
    </tr>
    <tr>
      <th>Age Group</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>32</td>
      <td>96.62</td>
      <td>$3.02</td>
      <td>$4.39</td>
      <td>4.23%</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>31</td>
      <td>83.79</td>
      <td>$2.70</td>
      <td>$4.19</td>
      <td>3.66%</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>133</td>
      <td>386.42</td>
      <td>$2.91</td>
      <td>$3.86</td>
      <td>16.90%</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>336</td>
      <td>978.77</td>
      <td>$2.91</td>
      <td>$3.78</td>
      <td>42.81%</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>125</td>
      <td>370.33</td>
      <td>$2.96</td>
      <td>$4.26</td>
      <td>16.20%</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>63</td>
      <td>197.25</td>
      <td>$3.13</td>
      <td>$4.20</td>
      <td>8.63%</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>42</td>
      <td>119.40</td>
      <td>$2.84</td>
      <td>$4.42</td>
      <td>5.22%</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>17</td>
      <td>53.75</td>
      <td>$3.16</td>
      <td>$4.89</td>
      <td>2.35%</td>
    </tr>
  </tbody>
</table>
</div>



**Top Spenders**

* Identify the the top 5 spenders in the game by total purchase value, then list (in a table):
  * SN
  * Purchase Count
  * Average Purchase Price
  * Total Purchase Value


```python
#setup result dataframe and calculate totals
top_df = pymoli_df.groupby('Player').aggregate({'Item ID':np.count_nonzero, 'Price':np.sum})

#leave 5 top spenders only
top_df = top_df.nlargest(5, 'Price')

#calculate averages
top_df['Average Purchase Price'] = top_df['Price'] / top_df['Item ID']

#rename columns 
top_df = top_df.rename(columns={'Item ID':'Purchase Count', 'Price':'Total Purchase Value'})

#swap columns
top_df = top_df.reindex(columns = ['Purchase Count','Average Purchase Price','Total Purchase Value'])

#format values
top_df = top_df.style.format({'Average Purchase Price': "${:,.2f}", 'Total Purchase Value': '${:,.2f}'})


top_df
```




<style  type="text/css" >
</style>  
<table id="T_13195670_2c65_11e8_b16b_8c85901d5a00" > 
<thead>    <tr> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Purchase Count</th> 
        <th class="col_heading level0 col1" >Average Purchase Price</th> 
        <th class="col_heading level0 col2" >Total Purchase Value</th> 
    </tr>    <tr> 
        <th class="index_name level0" >Player</th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_13195670_2c65_11e8_b16b_8c85901d5a00level0_row0" class="row_heading level0 row0" >Undirrala66</th> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row0_col0" class="data row0 col0" >5</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row0_col1" class="data row0 col1" >$3.41</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row0_col2" class="data row0 col2" >$17.06</td> 
    </tr>    <tr> 
        <th id="T_13195670_2c65_11e8_b16b_8c85901d5a00level0_row1" class="row_heading level0 row1" >Saedue76</th> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row1_col0" class="data row1 col0" >4</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row1_col1" class="data row1 col1" >$3.39</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row1_col2" class="data row1 col2" >$13.56</td> 
    </tr>    <tr> 
        <th id="T_13195670_2c65_11e8_b16b_8c85901d5a00level0_row2" class="row_heading level0 row2" >Mindimnya67</th> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row2_col0" class="data row2 col0" >4</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row2_col1" class="data row2 col1" >$3.18</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row2_col2" class="data row2 col2" >$12.74</td> 
    </tr>    <tr> 
        <th id="T_13195670_2c65_11e8_b16b_8c85901d5a00level0_row3" class="row_heading level0 row3" >Haellysu29</th> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row3_col0" class="data row3 col0" >3</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row3_col1" class="data row3 col1" >$4.24</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row3_col2" class="data row3 col2" >$12.73</td> 
    </tr>    <tr> 
        <th id="T_13195670_2c65_11e8_b16b_8c85901d5a00level0_row4" class="row_heading level0 row4" >Eoda93</th> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row4_col0" class="data row4 col0" >3</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row4_col1" class="data row4 col1" >$3.86</td> 
        <td id="T_13195670_2c65_11e8_b16b_8c85901d5a00row4_col2" class="data row4 col2" >$11.58</td> 
    </tr></tbody> 
</table> 



**Most Popular Items**

* Identify the 5 most popular items by purchase count, then list (in a table):
  * Item ID
  * Item Name
  * Purchase Count
  * Item Price
  * Total Purchase Value


```python
#group pymoli_df by 'Item ID' and 'Item name' counting total purchase count
#as count of 'Item ID' and total price as sum of 'Price'
#and leave 5 max values of 'Price' column only
item_top_df = pymoli_df.groupby(['Item ID', 'Item Name', 'Price']) \
              .aggregate({'Item ID':np.count_nonzero, 'Price':np.sum}) \
              .nlargest(5, 'Item ID')
    
#rename columns
item_top_df.columns = ['Purchase Count','Total Purchase Value']

#make 'Price' index - result of groupby - to column
#can do that only after renaming columns since
#aggregate function of groupby has 'Price' name too
item_top_df = item_top_df.reset_index('Price')

#rename Price column
item_top_df = item_top_df.rename(columns={'Price':'Item Price'})

#swap columns
item_top_df = item_top_df.reindex(columns = ['Purchase Count', 'Item Price','Total Purchase Value'])
 
#format values
item_top_df = item_top_df.style.format({'Item Price': '${:,.2f}', 'Total Purchase Value': '${:,.2f}'})

                             
item_top_df
```




<style  type="text/css" >
</style>  
<table id="T_16b541a4_2c65_11e8_8796_8c85901d5a00" > 
<thead>    <tr> 
        <th class="blank" ></th> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Purchase Count</th> 
        <th class="col_heading level0 col1" >Item Price</th> 
        <th class="col_heading level0 col2" >Total Purchase Value</th> 
    </tr>    <tr> 
        <th class="index_name level0" >Item ID</th> 
        <th class="index_name level1" >Item Name</th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level0_row0" class="row_heading level0 row0" >39</th> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level1_row0" class="row_heading level1 row0" >Betrayal, Whisper of Grieving Widows</th> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row0_col0" class="data row0 col0" >11</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row0_col1" class="data row0 col1" >$2.35</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row0_col2" class="data row0 col2" >$25.85</td> 
    </tr>    <tr> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level0_row1" class="row_heading level0 row1" >84</th> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level1_row1" class="row_heading level1 row1" >Arcane Gem</th> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row1_col0" class="data row1 col0" >11</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row1_col1" class="data row1 col1" >$2.23</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row1_col2" class="data row1 col2" >$24.53</td> 
    </tr>    <tr> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level0_row2" class="row_heading level0 row2" >13</th> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level1_row2" class="row_heading level1 row2" >Serenity</th> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row2_col0" class="data row2 col0" >9</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row2_col1" class="data row2 col1" >$1.49</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row2_col2" class="data row2 col2" >$13.41</td> 
    </tr>    <tr> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level0_row3" class="row_heading level0 row3" >31</th> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level1_row3" class="row_heading level1 row3" >Trickster</th> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row3_col0" class="data row3 col0" >9</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row3_col1" class="data row3 col1" >$2.07</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row3_col2" class="data row3 col2" >$18.63</td> 
    </tr>    <tr> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level0_row4" class="row_heading level0 row4" >34</th> 
        <th id="T_16b541a4_2c65_11e8_8796_8c85901d5a00level1_row4" class="row_heading level1 row4" >Retribution Axe</th> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row4_col0" class="data row4 col0" >9</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row4_col1" class="data row4 col1" >$4.14</td> 
        <td id="T_16b541a4_2c65_11e8_8796_8c85901d5a00row4_col2" class="data row4 col2" >$37.26</td> 
    </tr></tbody> 
</table> 



**Most Profitable Items**

* Identify the 5 most profitable items by total purchase value, then list (in a table):
  * Item ID
  * Item Name
  * Purchase Count
  * Item Price
  * Total Purchase Value


```python
#group pymoli_df by 'Item ID' and 'Item name' counting total purchase count
#as count of 'Item ID' and total price as sum of 'Price'
#and leave 5 max values of 'Price' column only
item_top_df = pymoli_df.groupby(['Item ID', 'Item Name', 'Price']) \
              .aggregate({'Item ID':np.count_nonzero, 'Price':np.sum}) \
              .nlargest(5, 'Price')
    
#rename columns
item_top_df.columns = ['Purchase Count','Total Purchase Value']

#make 'Price' index - result of groupby - to column
#can do that only after renaming columns since
#aggregate function of groupby has 'Price' name too
item_top_df = item_top_df.reset_index('Price')

#rename Price column
item_top_df = item_top_df.rename(columns={'Price':'Item Price'})

#swap columns
item_top_df = item_top_df.reindex(columns = ['Purchase Count', 'Item Price','Total Purchase Value'])
 
#calculate total purchases
total_purchases = pymoli_df['Price'].sum()

#calculate percentage of total purcahses per item
item_top_df['Percentage of purchases'] = (item_top_df['Total Purchase Value'] / \
                                          total_purchases * 100 \
                                         ).map('{0:.2f}%'.format)    
    
#format values
item_top_df = item_top_df.style.format({'Item Price': '${:,.2f}', 'Total Purchase Value': '${:,.2f}'})

item_top_df
```




<style  type="text/css" >
</style>  
<table id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00" > 
<thead>    <tr> 
        <th class="blank" ></th> 
        <th class="blank level0" ></th> 
        <th class="col_heading level0 col0" >Purchase Count</th> 
        <th class="col_heading level0 col1" >Item Price</th> 
        <th class="col_heading level0 col2" >Total Purchase Value</th> 
        <th class="col_heading level0 col3" >Percentage of purchases</th> 
    </tr>    <tr> 
        <th class="index_name level0" >Item ID</th> 
        <th class="index_name level1" >Item Name</th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
        <th class="blank" ></th> 
    </tr></thead> 
<tbody>    <tr> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level0_row0" class="row_heading level0 row0" >34</th> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level1_row0" class="row_heading level1 row0" >Retribution Axe</th> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row0_col0" class="data row0 col0" >9</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row0_col1" class="data row0 col1" >$4.14</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row0_col2" class="data row0 col2" >$37.26</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row0_col3" class="data row0 col3" >1.63%</td> 
    </tr>    <tr> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level0_row1" class="row_heading level0 row1" >115</th> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level1_row1" class="row_heading level1 row1" >Spectral Diamond Doomblade</th> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row1_col0" class="data row1 col0" >7</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row1_col1" class="data row1 col1" >$4.25</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row1_col2" class="data row1 col2" >$29.75</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row1_col3" class="data row1 col3" >1.30%</td> 
    </tr>    <tr> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level0_row2" class="row_heading level0 row2" >32</th> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level1_row2" class="row_heading level1 row2" >Orenmir</th> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row2_col0" class="data row2 col0" >6</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row2_col1" class="data row2 col1" >$4.95</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row2_col2" class="data row2 col2" >$29.70</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row2_col3" class="data row2 col3" >1.30%</td> 
    </tr>    <tr> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level0_row3" class="row_heading level0 row3" >103</th> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level1_row3" class="row_heading level1 row3" >Singed Scalpel</th> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row3_col0" class="data row3 col0" >6</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row3_col1" class="data row3 col1" >$4.87</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row3_col2" class="data row3 col2" >$29.22</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row3_col3" class="data row3 col3" >1.28%</td> 
    </tr>    <tr> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level0_row4" class="row_heading level0 row4" >107</th> 
        <th id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00level1_row4" class="row_heading level1 row4" >Splitter, Foe Of Subtlety</th> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row4_col0" class="data row4 col0" >8</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row4_col1" class="data row4 col1" >$3.61</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row4_col2" class="data row4 col2" >$28.88</td> 
        <td id="T_0e14597a_2d57_11e8_9a57_8c85901d5a00row4_col3" class="data row4 col3" >1.26%</td> 
    </tr></tbody> 
</table> 



## Observations:
* 80% of the players are male
* Almost half of the players are between 20-24 yo
* All age groups spend about the same amount of money per player
* Top purchased items are about the same percentage of all purchases
