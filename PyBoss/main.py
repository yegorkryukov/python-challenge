import os, csv, operator, datetime

# Set US State conversion dictionary
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

def read_data(path_to_file, headers=False):
    """ Returns list of lines from a CSV file
        pass 'headers' as True to return the first line from the file
    """
    with open(path_to_file, newline='') as csvfile:

        csvreader = csv.reader(csvfile, delimiter=',')
        
        if headers:
            return list(csvreader)
        else:
            return list(csvreader)[1:]

# Set variable for input file
folder = 'Resources/'
table1 = 'employee_data1.csv'
table2 = 'employee_data2.csv'

# Set variable for output file
output_file = os.path.join(folder, 'employee_results.csv')

# Read and combine files
rawdata = read_data(os.path.join(folder, table1))
rawdata += read_data(os.path.join(folder, table2))

# Set output list
results = [['Emp ID', 'First Name', 'Last Name', 'DOB', 'SSN', 'State']]

# Convert the data
for row in rawdata:

    results.append([row[0], row[1].split(' ')[0],
        row[1].split(' ')[1],
        datetime.datetime.strptime(row[2], '%Y-%m-%d').strftime('%m/%d/%Y'),
        '***-**-' + row[3][-4:],
        us_state_abbrev[row[4]]
        ])

#save results to a file
with open(output_file, "w", newline='') as datafile:
    wr = csv.writer(datafile, quoting=csv.QUOTE_ALL)
    wr.writerows(results)
    
    #print to console where the file was saved
    print('Data saved to:', datafile.name)