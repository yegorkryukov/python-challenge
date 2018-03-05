import os, csv, sys, operator

#ser variable for input file
folder = 'Resources/'
table = 'election_data_2.csv'
csvpath = os.path.join(folder, table)

# Set variable for output file
output_file = os.path.join(folder, table[:-4] + '_results.txt')


with open(csvpath, newline='') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')
    rawdata = list(csvreader)

results = {}
TotalVotes = 0

#start with second element '[1:]' to avoid counting headers
for row in rawdata[1:]:
    #count total number of votes
    TotalVotes += 1
    
    # add vote count of the 'row' record if a candidate is in the results
    if row[2] in results:
        results[row[2]] += 1
    # else add candidate to the results  
    else:
        results[row[2]] = 1

#save results to a file
with open(output_file, "w", newline='') as datafile:
    datafile.write('Election Results\n')
    datafile.write('-------------------------\n')
    datafile.write('Total Votes: {:,d} \n'.format(TotalVotes))
    datafile.write('-------------------------\n')

    #save individual candidate result to the file
    for line in results:
        percent = results[line]/TotalVotes
        datafile.write(line + ': {:.1%}'.format(percent) + 
            ' ({:,d})\n'.format(results[line]))
    
    datafile.write('-------------------------\n')
    # save the winner
    datafile.write('Winner: ' + 
        max(results.items(), key=operator.itemgetter(1))[0] + '\n')
    datafile.write('-------------------------\n')

with open(output_file, "r") as datafile:
    #print the file to the console
    print(datafile.read())

    #print where the file was saved
    print('Data saved to:', datafile.name)
