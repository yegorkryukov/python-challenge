
## Option 2: Academy of Py Analysis:

* Charter schools have better scores (doesn't mean they teach better)
* Worst performing shools spend more money per student
* Math and reading scores are pretty consistent between grades
* Average math score is worst in bigger schools


```python
# Dependencies
import pandas as pd
import numpy as np

# Create a reference the CSV file desired
path_schools = "Resources/schools_complete.csv"
path_students = "Resources/students_complete.csv"

# Read files into a Pandas DataFrame
schools_df = pd.read_csv(path_schools)
students_df = pd.read_csv(path_students)
```


```python
#rename school column for further merge
schools_df = schools_df.rename(columns={'name':'school'})
```


```python
#merge two df
summary_df = pd.merge(schools_df, students_df, how='inner', on = 'school')

#remove excess columns
summary_df = summary_df.drop(columns=['size','budget'])
summary_df = summary_df.set_index('Student ID')
```

**District Summary**

* Create a high level snapshot (in table form) of the district's key metrics, including:
  * Total Schools
  * Total Students
  * Total Budget
  * Average Math Score
  * Average Reading Score
  * % Passing Math
  * % Passing Reading
  * Overall Passing Rate (Average of the above two)
  

  # **Passing grade set to `70` (change if need to)**


```python
#set passing grade
passing_grade = 70
```


```python
#setup df
all_summary = schools_df \
                   .groupby('type') \
                   .aggregate( \
                              {'school':pd.Series.nunique, \
                               'size': np.sum, \
                               'budget':np.sum \
                              }
                             )

#rename columns
all_summary.columns = ['Total Schools','Total Students','Total Budget']

#calculate values using groupby
all_summary[['Average Math Score','% Passing Math','Average Reading Score','% Passing Reading']] = \
                  summary_df.groupby('type').agg \
                    ( \
                     {'math_score': \
                      ['mean', lambda x: sum(x > passing_grade) / x.count() * 100], \
                      'reading_score': \
                      ['mean', lambda x: sum(x > passing_grade) / x.count() * 100], \
                     })

#calculate overal passing grade
all_summary['Overall Passing Rate'] = (all_summary['% Passing Math'] + all_summary['% Passing Reading']) / 2

'''
removed format until figure out how not to change underlying values

#format values
all_summary['Total Budget'] = all_summary['Total Budget'].map('${:,.2f}'.format)
all_summary['Total Students'] = all_summary['Total Students'].map('{:,}'.format)
all_summary['Average Math Score'] = all_summary['Average Math Score'].map('{:.2f}'.format)
all_summary['Average Reading Score'] = all_summary['Average Reading Score'].map('{:.2f}'.format)
all_summary['% Passing Math'] = all_summary['% Passing Math'].map('{:.2f}%'.format)
all_summary['% Passing Reading'] = all_summary['% Passing Reading'].map('{:.2f}%'.format)
all_summary['Overall Passing Rate'] = all_summary['Overall Passing Rate'].map('{:.2f}%'.format)
'''

all_summary
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
      <th>Total Schools</th>
      <th>Total Students</th>
      <th>Total Budget</th>
      <th>Average Math Score</th>
      <th>% Passing Math</th>
      <th>Average Reading Score</th>
      <th>% Passing Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>type</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Charter</th>
      <td>8</td>
      <td>12194</td>
      <td>7301505</td>
      <td>83.406183</td>
      <td>90.282106</td>
      <td>83.902821</td>
      <td>93.152370</td>
      <td>91.717238</td>
    </tr>
    <tr>
      <th>District</th>
      <td>7</td>
      <td>26976</td>
      <td>17347923</td>
      <td>76.987026</td>
      <td>64.305308</td>
      <td>80.962485</td>
      <td>78.369662</td>
      <td>71.337485</td>
    </tr>
  </tbody>
</table>
</div>



**School Summary**

* Create an overview table that summarizes key metrics about each school, including:
  * School Name
  * School Type
  * Total Students
  * Total School Budget
  * Per Student Budget
  * Average Math Score
  * Average Reading Score
  * % Passing Math
  * % Passing Reading
  * Overall Passing Rate (Average of the above two)


```python
#setup df
school_summary = schools_df \
                   .groupby(['school','type']) \
                   .agg( \
                              {'size': 'sum' , \
                               'budget': 'sum'\
                              }
                             )

#make 'type' index to column
school_summary = school_summary.reset_index('type')

#drop index name
school_summary.index.name = ''

#rename columns
school_summary.columns = ['School Type','Total Students','Total School Budget']

#calculate columns
school_summary['Per Student Budget'] = school_summary['Total School Budget'] / school_summary['Total Students']
school_summary[['Average Math Score','% Passing Math','Average Reading Score','% Passing Reading']] = \
    summary_df.groupby('school').agg \
                    ( \
                     {'math_score': \
                      ['mean', lambda x: sum(x > passing_grade) / x.count()], \
                      'reading_score': \
                      ['mean', lambda x: sum(x > passing_grade) / x.count()], \
                     })
school_summary['Overall Passing Rate'] = (school_summary['% Passing Math'] + school_summary['% Passing Reading'])/2

'''
removed format until figure out how not to change underlying values

#format values
school_summary['Total School Budget'] = school_summary['Total School Budget'].map('${:,.2f}'.format)
school_summary['Per Student Budget'] = school_summary['Per Student Budget'].map('{:,.2f}'.format)
school_summary['Total Students'] = school_summary['Total Students'].map('{:,}'.format)
school_summary['Average Math Score'] = school_summary['Average Math Score'].map('{:.2f}'.format)
school_summary['Average Reading Score'] = school_summary['Average Reading Score'].map('{:.2f}'.format)
school_summary['% Passing Math'] = school_summary['% Passing Math'].map('{:.2%}'.format)
school_summary['% Passing Reading'] = school_summary['% Passing Reading'].map('{:.2%}'.format)
school_summary['Overall Passing Rate'] = school_summary['Overall Passing Rate'].map('{:.2%}'.format)
'''
school_summary
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
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Math Score</th>
      <th>% Passing Math</th>
      <th>Average Reading Score</th>
      <th>% Passing Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Bailey High School</th>
      <td>District</td>
      <td>4976</td>
      <td>3124928</td>
      <td>628.0</td>
      <td>77.048432</td>
      <td>0.646302</td>
      <td>81.033963</td>
      <td>0.793006</td>
      <td>0.719654</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1858</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>83.061895</td>
      <td>0.895587</td>
      <td>83.975780</td>
      <td>0.938644</td>
      <td>0.917115</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>2949</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>76.711767</td>
      <td>0.637504</td>
      <td>81.158020</td>
      <td>0.784334</td>
      <td>0.710919</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>District</td>
      <td>2739</td>
      <td>1763916</td>
      <td>644.0</td>
      <td>77.102592</td>
      <td>0.657539</td>
      <td>80.746258</td>
      <td>0.775100</td>
      <td>0.716320</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>Charter</td>
      <td>1468</td>
      <td>917500</td>
      <td>625.0</td>
      <td>83.351499</td>
      <td>0.897139</td>
      <td>83.816757</td>
      <td>0.933924</td>
      <td>0.915531</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>District</td>
      <td>4635</td>
      <td>3022020</td>
      <td>652.0</td>
      <td>77.289752</td>
      <td>0.647465</td>
      <td>80.934412</td>
      <td>0.781877</td>
      <td>0.714671</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>427</td>
      <td>248087</td>
      <td>581.0</td>
      <td>83.803279</td>
      <td>0.906323</td>
      <td>83.814988</td>
      <td>0.927400</td>
      <td>0.916862</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>76.629414</td>
      <td>0.633185</td>
      <td>81.182722</td>
      <td>0.788138</td>
      <td>0.710662</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>4761</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>77.072464</td>
      <td>0.638521</td>
      <td>80.966394</td>
      <td>0.782819</td>
      <td>0.710670</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>962</td>
      <td>585858</td>
      <td>609.0</td>
      <td>83.839917</td>
      <td>0.916840</td>
      <td>84.044699</td>
      <td>0.922037</td>
      <td>0.919439</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>3999</td>
      <td>2547363</td>
      <td>637.0</td>
      <td>76.842711</td>
      <td>0.640660</td>
      <td>80.744686</td>
      <td>0.777444</td>
      <td>0.709052</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>Charter</td>
      <td>1761</td>
      <td>1056600</td>
      <td>600.0</td>
      <td>83.359455</td>
      <td>0.898921</td>
      <td>83.725724</td>
      <td>0.926178</td>
      <td>0.912550</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>Charter</td>
      <td>1635</td>
      <td>1043130</td>
      <td>638.0</td>
      <td>83.418349</td>
      <td>0.902141</td>
      <td>83.848930</td>
      <td>0.929052</td>
      <td>0.915596</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>Charter</td>
      <td>2283</td>
      <td>1319574</td>
      <td>578.0</td>
      <td>83.274201</td>
      <td>0.909330</td>
      <td>83.989488</td>
      <td>0.932545</td>
      <td>0.920937</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>Charter</td>
      <td>1800</td>
      <td>1049400</td>
      <td>583.0</td>
      <td>83.682222</td>
      <td>0.902778</td>
      <td>83.955000</td>
      <td>0.934444</td>
      <td>0.918611</td>
    </tr>
  </tbody>
</table>
</div>



**Top Performing Schools (By Passing Rate)**

* Create a table that highlights the top 5 performing schools based on Overall Passing Rate. Include:
  * School Name
  * School Type
  * Total Students
  * Total School Budget
  * Per Student Budget
  * Average Math Score
  * Average Reading Score
  * % Passing Math
  * % Passing Reading
  * Overall Passing Rate (Average of the above two)


```python
#don't need to convert since didn't format the output on previous step
#convert column to float from object
#school_summary['Overall Passing Rate'] = school_summary['Overall Passing Rate'].str.replace('%', '').astype(float)

#create new df with 5 schools
top_schools = school_summary.nlargest(5, 'Overall Passing Rate')

top_schools
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
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Math Score</th>
      <th>% Passing Math</th>
      <th>Average Reading Score</th>
      <th>% Passing Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Wilson High School</th>
      <td>Charter</td>
      <td>2283</td>
      <td>1319574</td>
      <td>578.0</td>
      <td>83.274201</td>
      <td>0.909330</td>
      <td>83.989488</td>
      <td>0.932545</td>
      <td>0.920937</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>962</td>
      <td>585858</td>
      <td>609.0</td>
      <td>83.839917</td>
      <td>0.916840</td>
      <td>84.044699</td>
      <td>0.922037</td>
      <td>0.919439</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>Charter</td>
      <td>1800</td>
      <td>1049400</td>
      <td>583.0</td>
      <td>83.682222</td>
      <td>0.902778</td>
      <td>83.955000</td>
      <td>0.934444</td>
      <td>0.918611</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1858</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>83.061895</td>
      <td>0.895587</td>
      <td>83.975780</td>
      <td>0.938644</td>
      <td>0.917115</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>427</td>
      <td>248087</td>
      <td>581.0</td>
      <td>83.803279</td>
      <td>0.906323</td>
      <td>83.814988</td>
      <td>0.927400</td>
      <td>0.916862</td>
    </tr>
  </tbody>
</table>
</div>



**Bottom Performing Schools (By Passing Rate)**

* Create a table that highlights the bottom 5 performing schools based on Overall Passing Rate. Include all of the same metrics as above.


```python
#create new df with 5 schools
bottom_schools = school_summary.nsmallest(5, 'Overall Passing Rate')

bottom_schools
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
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Math Score</th>
      <th>% Passing Math</th>
      <th>Average Reading Score</th>
      <th>% Passing Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>3999</td>
      <td>2547363</td>
      <td>637.0</td>
      <td>76.842711</td>
      <td>0.640660</td>
      <td>80.744686</td>
      <td>0.777444</td>
      <td>0.709052</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>76.629414</td>
      <td>0.633185</td>
      <td>81.182722</td>
      <td>0.788138</td>
      <td>0.710662</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>4761</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>77.072464</td>
      <td>0.638521</td>
      <td>80.966394</td>
      <td>0.782819</td>
      <td>0.710670</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>2949</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>76.711767</td>
      <td>0.637504</td>
      <td>81.158020</td>
      <td>0.784334</td>
      <td>0.710919</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>District</td>
      <td>4635</td>
      <td>3022020</td>
      <td>652.0</td>
      <td>77.289752</td>
      <td>0.647465</td>
      <td>80.934412</td>
      <td>0.781877</td>
      <td>0.714671</td>
    </tr>
  </tbody>
</table>
</div>



**Math Scores by Grade**

* Create a table that lists the average Math Score for students of each grade level (9th, 10th, 11th, 12th) at each school.


```python
#group by school and grade calculating mean
math_by_grade = summary_df \
                   .groupby(['school','grade']) \
                   .agg( \
                              {'math_score': 'mean'\
                              }\
                             )
        
#convert level 2 index to columns (pivot)
math_by_grade = math_by_grade.unstack()

#sort column labels alphabetically
math_by_grade = math_by_grade.reindex(sorted(math_by_grade.columns, reverse=True), axis=1)

math_by_grade
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="4" halign="left">math_score</th>
    </tr>
    <tr>
      <th>grade</th>
      <th>9th</th>
      <th>12th</th>
      <th>11th</th>
      <th>10th</th>
    </tr>
    <tr>
      <th>school</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Bailey High School</th>
      <td>77.083676</td>
      <td>76.492218</td>
      <td>77.515588</td>
      <td>76.996772</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>83.094697</td>
      <td>83.277487</td>
      <td>82.765560</td>
      <td>83.154506</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>76.403037</td>
      <td>77.151369</td>
      <td>76.884344</td>
      <td>76.539974</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>77.361345</td>
      <td>76.179963</td>
      <td>76.918058</td>
      <td>77.672316</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>82.044010</td>
      <td>83.356164</td>
      <td>83.842105</td>
      <td>84.229064</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>77.438495</td>
      <td>77.186567</td>
      <td>77.136029</td>
      <td>77.337408</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>83.787402</td>
      <td>82.855422</td>
      <td>85.000000</td>
      <td>83.429825</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>77.027251</td>
      <td>77.225641</td>
      <td>76.446602</td>
      <td>75.908735</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>77.187857</td>
      <td>76.863248</td>
      <td>77.491653</td>
      <td>76.691117</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>83.625455</td>
      <td>84.121547</td>
      <td>84.328125</td>
      <td>83.372000</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>76.859966</td>
      <td>77.690748</td>
      <td>76.395626</td>
      <td>76.612500</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>83.420755</td>
      <td>83.778976</td>
      <td>83.383495</td>
      <td>82.917411</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>83.590022</td>
      <td>83.497041</td>
      <td>83.498795</td>
      <td>83.087886</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>83.085578</td>
      <td>83.035794</td>
      <td>83.195326</td>
      <td>83.724422</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>83.264706</td>
      <td>83.644986</td>
      <td>83.836782</td>
      <td>84.010288</td>
    </tr>
  </tbody>
</table>
</div>



**Reading Scores by Grade**

* Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.


```python
#group by school and grade calculating mean
reading_by_grade = summary_df \
                   .groupby(['school','grade']) \
                   .agg( \
                              {'reading_score': 'mean'\
                              }\
                             )
        
#convert level 2 index to columns (pivot)
reading_by_grade = reading_by_grade.unstack()

#sort column labels alphabetically
reading_by_grade = reading_by_grade.reindex(sorted(reading_by_grade.columns, reverse=True), axis=1)

reading_by_grade
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead tr th {
        text-align: left;
    }

    .dataframe thead tr:last-of-type th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="4" halign="left">reading_score</th>
    </tr>
    <tr>
      <th>grade</th>
      <th>9th</th>
      <th>12th</th>
      <th>11th</th>
      <th>10th</th>
    </tr>
    <tr>
      <th>school</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Bailey High School</th>
      <td>81.303155</td>
      <td>80.912451</td>
      <td>80.945643</td>
      <td>80.907183</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>83.676136</td>
      <td>84.287958</td>
      <td>83.788382</td>
      <td>84.253219</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>81.198598</td>
      <td>81.384863</td>
      <td>80.640339</td>
      <td>81.408912</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>80.632653</td>
      <td>80.662338</td>
      <td>80.403642</td>
      <td>81.262712</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>83.369193</td>
      <td>84.013699</td>
      <td>84.288089</td>
      <td>83.706897</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>80.866860</td>
      <td>80.857143</td>
      <td>81.396140</td>
      <td>80.660147</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>83.677165</td>
      <td>84.698795</td>
      <td>83.815534</td>
      <td>83.324561</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>81.290284</td>
      <td>80.305983</td>
      <td>81.417476</td>
      <td>81.512386</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>81.260714</td>
      <td>81.227564</td>
      <td>80.616027</td>
      <td>80.773431</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>83.807273</td>
      <td>84.591160</td>
      <td>84.335938</td>
      <td>83.612000</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>80.993127</td>
      <td>80.376426</td>
      <td>80.864811</td>
      <td>80.629808</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>84.122642</td>
      <td>82.781671</td>
      <td>84.373786</td>
      <td>83.441964</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>83.728850</td>
      <td>83.831361</td>
      <td>83.585542</td>
      <td>84.254157</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>83.939778</td>
      <td>84.317673</td>
      <td>83.764608</td>
      <td>84.021452</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>83.833333</td>
      <td>84.073171</td>
      <td>84.156322</td>
      <td>83.812757</td>
    </tr>
  </tbody>
</table>
</div>



**Scores by School Spending**

* Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
  * Average Math Score
  * Average Reading Score
  * % Passing Math
  * % Passing Reading
  * Overall Passing Rate (Average of the above two)


```python
#no need to convert since cancelled formatting earlier
#convert column to float from object
#school_bins_df['Per Student Budget'] = school_bins_df['Per Student Budget'].str.replace('$', '').astype(float)

#define empty DF with 1 column
school_bins_summary = pd.DataFrame({'Overall Passing Rate' : []})

#assign bins
bins = [0,580,620,640,700]
bins_names = ['<$580','$580-600','$600-620','$>640']

#add Spending Range to new df
school_summary['Spending Ranges (Per Student)'] = pd.cut(school_summary['Per Student Budget'], bins, labels=bins_names)

#calculate results
school_bins_summary[['Average Math Score','% Passing Math','Average Reading Score','% Passing Reading']] = \
    school_summary.groupby('Spending Ranges (Per Student)') \
        .agg( \
             {'Average Math Score': \
                  ['mean', lambda x: sum(x > passing_grade) / x.count()], \
              'Average Reading Score': \
                  ['mean', lambda x: sum(x > passing_grade) / x.count()] \
             })
   
school_bins_summary['Overall Passing Rate'] = \
    (school_bins_summary['% Passing Math'] + school_bins_summary['% Passing Reading'])/2

#rearrange columns
school_bins_summary = school_bins_summary.reindex(columns = ['Average Math Score','Average Reading Score', \
                                              '% Passing Math','% Passing Reading','Overall Passing Rate'])

school_bins_summary
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
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>Spending Ranges (Per Student)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;$580</th>
      <td>83.274201</td>
      <td>83.989488</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>$580-600</th>
      <td>83.549353</td>
      <td>83.903238</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>$600-620</th>
      <td>79.474551</td>
      <td>82.120471</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>$&gt;640</th>
      <td>77.023555</td>
      <td>80.957446</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>



**Scores by School Size**

* Repeat the above breakdown, but this time group schools based on a reasonable approximation of school size (Small, Medium, Large).


```python
#define empty DF with 1 column
school_size_summary = pd.DataFrame({'Overall Passing Rate' : []})

#assign bins
bins_size = [0,1000,3000,5000]
bins_size_names = ['Small(<1000)','Medium(1000-3000)','Large(>3000)']

#add School Size to new df
school_summary['School Size'] = pd.cut(school_summary['Total Students'], bins_size, labels=bins_size_names)

school_size_summary[['Average Math Score','% Passing Math','Average Reading Score','% Passing Reading']] = \
    school_summary.groupby('School Size') \
        .agg( \
             {'Average Math Score': \
                  ['mean', lambda x: sum(x > passing_grade) / x.count()], \
              'Average Reading Score': \
                  ['mean', lambda x: sum(x > passing_grade) / x.count()] \
             })

school_size_summary['Overall Passing Rate'] = \
       (school_size_summary['% Passing Math'] + school_size_summary['% Passing Reading'])/2

#rearrange columns
school_size_summary = school_size_summary.reindex(columns = ['Average Math Score','Average Reading Score', \
                                              '% Passing Math','% Passing Reading','Overall Passing Rate'])

school_size_summary.head()
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
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Size</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Small(&lt;1000)</th>
      <td>83.821598</td>
      <td>83.929843</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>Medium(1000-3000)</th>
      <td>81.176821</td>
      <td>82.933187</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>Large(&gt;3000)</th>
      <td>77.063340</td>
      <td>80.919864</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>



**Scores by School Type**

* Repeat the above breakdown, but this time group schools based on school type (Charter vs. District).


```python
type_summary = pd.DataFrame({'Overall Passing Rate' : []})

type_summary[['Average Math Score','% Passing Math','Average Reading Score','% Passing Reading']] = \
    school_summary.groupby('School Type') \
        .agg( \
             {'Average Math Score': \
                  ['mean', lambda x: sum(x > passing_grade) / x.count()], \
              'Average Reading Score': \
                  ['mean', lambda x: sum(x > passing_grade) / x.count()] \
             })
        
type_summary['Overall Passing Rate'] = \
       (type_summary['% Passing Math'] + type_summary['% Passing Reading'])/2

#rearrange columns
type_summary = type_summary.reindex(columns = ['Average Math Score','Average Reading Score', \
                                              '% Passing Math','% Passing Reading','Overall Passing Rate'])
        
type_summary
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
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Type</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Charter</th>
      <td>83.473852</td>
      <td>83.896421</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>District</th>
      <td>76.956733</td>
      <td>80.966636</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>


