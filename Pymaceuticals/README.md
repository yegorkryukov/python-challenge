
## Option 2: Pymaceuticals Inc

![Laboratory](images/Laboratory.jpg)

While your data companions rushed off to jobs in finance and government, you remained adamant that science was the way for you. Staying true to your mission, you've since joined Pymaceuticals Inc., a burgeoning pharmaceutical company based out of San Diego, CA. Pymaceuticals specializes in drug-based, anti-cancer pharmaceuticals. In their most recent efforts, they've since begun screening for potential treatments to squamous cell carcinoma (SCC), a commonly occurring form of skin cancer.

As their Chief Data Analyst, you've been given access to the complete data from their most recent animal study. In this study, 250 mice were treated through a variety of drug regimes over the course of 45 days. Their physiological responses were then monitored over the course of that time. Your objective is to analyze the data to show how four treatments (**Capomulin, Infubinol, Ketapril, and Placebo**) compare.


```python
#dependencies 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

#load files
trial_df = pd.read_csv('raw_data/clinicaltrial_data.csv')
drug_df = pd.read_csv('raw_data/mouse_drug_data.csv')
```


```python
#check if mice dictionaries are identical in both df
np.array_equal(np.sort(trial_df['Mouse ID'].unique()), np.sort(drug_df['Mouse ID'].unique()))
```




    True




```python
#there are duplicates in drug)df
drug_df[drug_df.duplicated(subset='Mouse ID', keep=False).values]
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
      <th>Mouse ID</th>
      <th>Drug</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>7</th>
      <td>g989</td>
      <td>Stelasyn</td>
    </tr>
    <tr>
      <th>173</th>
      <td>g989</td>
      <td>Propriva</td>
    </tr>
  </tbody>
</table>
</div>




```python
#drop duplicates
drug_df = drug_df.drop_duplicates(subset='Mouse ID')
```


```python
#leave only Capomulin, Infubinol, Ketapril, and Placebo for analysis
#create df with list of drugs to keep
drugs_list = pd.DataFrame(data={'Drug':['Capomulin', 'Infubinol', 'Ketapril', 'Placebo']})

#merge with provided df to keep the only needed drugs
drug_df = pd.merge(drugs_list, drug_df, on='Drug')
drug_df.head()
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
      <th>Drug</th>
      <th>Mouse ID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Capomulin</td>
      <td>b128</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Capomulin</td>
      <td>r944</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Capomulin</td>
      <td>s185</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Capomulin</td>
      <td>w914</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Capomulin</td>
      <td>l897</td>
    </tr>
  </tbody>
</table>
</div>




```python
#combine data over city name
data_df = pd.merge(trial_df, drug_df, on='Mouse ID')
```


```python
data_df = data_df.set_index('Drug')
```


```python
data_df.head()
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
      <th>Mouse ID</th>
      <th>Timepoint</th>
      <th>Tumor Volume (mm3)</th>
      <th>Metastatic Sites</th>
    </tr>
    <tr>
      <th>Drug</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Capomulin</th>
      <td>b128</td>
      <td>0</td>
      <td>45.000000</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Capomulin</th>
      <td>b128</td>
      <td>5</td>
      <td>45.651331</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Capomulin</th>
      <td>b128</td>
      <td>10</td>
      <td>43.270852</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Capomulin</th>
      <td>b128</td>
      <td>15</td>
      <td>43.784893</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Capomulin</th>
      <td>b128</td>
      <td>20</td>
      <td>42.731552</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



# Creating a scatter plot that shows how the tumor volume changes over time for each treatment.


```python
#calculate standard errors
tumor_error = data_df.groupby(['Drug', 'Timepoint']).sem()['Tumor Volume (mm3)'].unstack(level=0)
met_error = data_df.groupby(['Drug', 'Timepoint']).sem()['Metastatic Sites'].unstack(level=0)



tumor_error
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
      <th>Drug</th>
      <th>Capomulin</th>
      <th>Infubinol</th>
      <th>Ketapril</th>
      <th>Placebo</th>
    </tr>
    <tr>
      <th>Timepoint</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.448593</td>
      <td>0.235102</td>
      <td>0.264819</td>
      <td>0.218091</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.702684</td>
      <td>0.282346</td>
      <td>0.357421</td>
      <td>0.402064</td>
    </tr>
    <tr>
      <th>15</th>
      <td>0.838617</td>
      <td>0.357705</td>
      <td>0.580268</td>
      <td>0.614461</td>
    </tr>
    <tr>
      <th>20</th>
      <td>0.909731</td>
      <td>0.476210</td>
      <td>0.726484</td>
      <td>0.839609</td>
    </tr>
    <tr>
      <th>25</th>
      <td>0.881642</td>
      <td>0.550315</td>
      <td>0.755413</td>
      <td>1.034872</td>
    </tr>
    <tr>
      <th>30</th>
      <td>0.934460</td>
      <td>0.631061</td>
      <td>0.934121</td>
      <td>1.218231</td>
    </tr>
    <tr>
      <th>35</th>
      <td>1.052241</td>
      <td>0.984155</td>
      <td>1.127867</td>
      <td>1.287481</td>
    </tr>
    <tr>
      <th>40</th>
      <td>1.223608</td>
      <td>1.055220</td>
      <td>1.158449</td>
      <td>1.370634</td>
    </tr>
    <tr>
      <th>45</th>
      <td>1.223977</td>
      <td>1.144427</td>
      <td>1.453186</td>
      <td>1.351726</td>
    </tr>
  </tbody>
</table>
</div>




```python
#pivot by drug and timepoint and tumor volume
by_drug = data_df.pivot_table(index='Timepoint', columns='Drug', values='Tumor Volume (mm3)')
by_drug.head(3)
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
      <th>Drug</th>
      <th>Capomulin</th>
      <th>Infubinol</th>
      <th>Ketapril</th>
      <th>Placebo</th>
    </tr>
    <tr>
      <th>Timepoint</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>45.000000</td>
      <td>45.000000</td>
      <td>45.000000</td>
      <td>45.000000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>44.266086</td>
      <td>47.062001</td>
      <td>47.389175</td>
      <td>47.125589</td>
    </tr>
    <tr>
      <th>10</th>
      <td>43.084291</td>
      <td>49.403909</td>
      <td>49.582269</td>
      <td>49.423329</td>
    </tr>
  </tbody>
</table>
</div>




```python
#set fivethirtyeight styles
mpl.style.use('fivethirtyeight')

#initialize figure 
f, ax = plt.subplots(figsize=(13,10))

#plot df
g = by_drug.plot(ax=ax, style='--', yerr=tumor_error)
g.tick_params(axis = 'both', which = 'both', labelsize = 18)

# create valid markers from mpl.markers
valid_markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'x', 'D', 'd', 'P', 'X']
markers = np.random.choice(valid_markers, by_drug.shape[1], replace=False)

for i, line in enumerate(ax.get_lines()):
    line.set_marker(markers[i])
    line.set_markersize(15)
#add legend
ax.legend(ax.get_lines(), by_drug.columns, loc='best', title='Drug')

#set titles
f.suptitle('Tumor response to treatment', y=0.85, fontsize = 26, weight = 'bold', alpha = .75)
plt.xlabel('Time (days)')
plt.ylabel('Tumor volume (mm3)')
plt.axis([-1, 46, 30, 75])

plt.show()
```


![png](output_12_0.png)


# Creating a scatter plot that shows how the number of [metastatic](https://en.wikipedia.org/wiki/Metastasis) (cancer spreading) sites changes over time for each treatment.


```python
#pivot by drug and timepoint and metastatic sites
met = data_df.pivot_table(index='Timepoint', columns='Drug', values='Metastatic Sites')
met.head(3)
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
      <th>Drug</th>
      <th>Capomulin</th>
      <th>Infubinol</th>
      <th>Ketapril</th>
      <th>Placebo</th>
    </tr>
    <tr>
      <th>Timepoint</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.00</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.16</td>
      <td>0.280000</td>
      <td>0.304348</td>
      <td>0.375000</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.32</td>
      <td>0.666667</td>
      <td>0.590909</td>
      <td>0.833333</td>
    </tr>
  </tbody>
</table>
</div>




```python
#set fivethirtyeight styles
mpl.style.use('fivethirtyeight')

#initialize figure 
f, ax = plt.subplots(figsize=(13,10))

#plot df
g = met.plot(ax=ax, style='--', yerr=met_error)
g.tick_params(axis = 'both', which = 'both', labelsize = 18)
#g.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)

# create valid markers from mpl.markers
valid_markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'x', 'D', 'd', 'P', 'X']
markers = np.random.choice(valid_markers, by_drug.shape[1], replace=False)

for i, line in enumerate(ax.get_lines()):
    line.set_marker(markers[i])
    line.set_markersize(15)
#add legend
ax.legend(ax.get_lines(), by_drug.columns, loc='best', title='Drug')


#set titles
f.suptitle('Metastasic spread during treatment', y=0.85, fontsize = 26, weight = 'bold', alpha = .75)
plt.xlabel('Time (days)')
plt.ylabel('Metastasic sites')
#plt.axis([-1, 46, 30, 75])

plt.show()
```


![png](output_15_0.png)


# Creating a scatter plot that shows the number of mice still alive through the course of treatment (Survival Rate)


```python
#pivot by drug and timepoint and mice count
mice = data_df.pivot_table(index='Timepoint', columns='Drug', values='Mouse ID',aggfunc= 'count')

mice.head(3)
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
      <th>Drug</th>
      <th>Capomulin</th>
      <th>Infubinol</th>
      <th>Ketapril</th>
      <th>Placebo</th>
    </tr>
    <tr>
      <th>Timepoint</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
    </tr>
    <tr>
      <th>5</th>
      <td>25</td>
      <td>25</td>
      <td>23</td>
      <td>24</td>
    </tr>
    <tr>
      <th>10</th>
      <td>25</td>
      <td>21</td>
      <td>22</td>
      <td>24</td>
    </tr>
  </tbody>
</table>
</div>




```python
#set fivethirtyeight styles
mpl.style.use('fivethirtyeight')

#initialize figure 
f, ax = plt.subplots(figsize=(13,10))

#plot df
g = mice.plot(ax=ax, style='--')
g.tick_params(axis = 'both', which = 'both', labelsize = 18)
#g.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)

# create valid markers from mpl.markers
valid_markers = ['o', 'v', '^', '<', '>', 's', 'p', '*', 'h', 'H', 'x', 'D', 'd', 'P', 'X']
markers = np.random.choice(valid_markers, by_drug.shape[1], replace=False)

for i, line in enumerate(ax.get_lines()):
    line.set_marker(markers[i])
    line.set_markersize(15)
#add legend
ax.legend(ax.get_lines(), by_drug.columns, loc='best', title='Drug')


#set titles
f.suptitle('Survival during treatment', y=0.85, fontsize = 26, weight = 'bold', alpha = .75)
plt.xlabel('Time (days)')
plt.ylabel('Metastasic sites')
plt.axis([-1, 46, 0, 29])

vals = ax.get_yticks()
ax.set_yticklabels(['{:3.2f}%'.format(x*4) for x in vals])

plt.show()
```


![png](output_18_0.png)


# Creating a bar graph that compares the total % tumor volume change for each drug across the full 45 days.


```python
#pivot for plot
summary = data_df.pivot_table( \
    index=['Drug','Timepoint'], \
    values='Tumor Volume (mm3)', \
    aggfunc= 'mean' \
    ).reset_index('Timepoint')

#create df for plot
totals = pd.DataFrame()
totals['Drug'], totals['Tumor'] = '',''

#store only latest data for plot
for index, row in summary.iterrows():
    #print(row)
    if row['Timepoint'] == 45:
        totals = totals.append({'Tumor': row['Tumor Volume (mm3)'],'Drug': index}, ignore_index=True)

#calculate percentage change
totals['Tumor'] = (totals['Tumor']-45)/45*100

totals.set_index('Drug')
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
      <th>Tumor</th>
    </tr>
    <tr>
      <th>Drug</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Capomulin</th>
      <td>-19.475303</td>
    </tr>
    <tr>
      <th>Infubinol</th>
      <td>46.123472</td>
    </tr>
    <tr>
      <th>Ketapril</th>
      <td>57.028795</td>
    </tr>
    <tr>
      <th>Placebo</th>
      <td>51.297960</td>
    </tr>
  </tbody>
</table>
</div>




```python
#set fivethirtyeight styles
mpl.style.use('fivethirtyeight')

#initialize figure 
f, ax = plt.subplots(figsize=(13,10))

#calculate colors for plot
mask = totals['Tumor'] < 0
colors = np.array(['r']*len(totals))
colors[mask.values] = 'g'

#plot df
g = plt.bar(totals.index,totals['Tumor'],color=colors,width=0.8)

def autolabel(rects, ax):
    # Get y-axis height to calculate label position from.
    (y_bottom, y_top) = ax.get_ylim()
    y_height = y_top - y_bottom

    for rect in rects:
        height = rect.get_height()

        # Fraction of axis height taken up by this rectangle
        p_height = (height / y_height)

        # If we can fit the label above the column, do that;
        # otherwise, put it inside the column.
        if p_height > 0.95: # arbitrary; 95% looked good to me.
            label_position = height - (y_height * 0.05)
        else:
            label_position = height + (y_height * 0.01)

        ax.text(rect.get_x() + rect.get_width()/2., label_position,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(g, ax)

#set titles
f.suptitle('Tumor change over 45 days treatment', y=0.91, fontsize = 26, weight = 'bold', alpha = .75)
plt.xlabel('Drug')
plt.ylabel('% Tumor volume change')
plt.xticks(np.arange(4),totals['Drug'].tolist(),rotation=0)

vals = ax.get_yticks()
ax.set_yticklabels(['{:3.2f}%'.format(x) for x in vals])

plt.show()
```


![png](output_21_0.png)


# Observations
* Capomuline is the only drugs that reduced tumors
* The metastasic sites were also minimal for it
* Over 90% of mice were still alive after the treatment by Capomulin comparing to less than 60% for other drugs 
* Other drugs have no influence on the tumor just like Placebo
