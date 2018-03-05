import os, csv, sys

#ser variable for input file
folder = 'Resources/'
table = 'budget_data_2.csv'
csvpath = os.path.join(folder, table)

# Set variable for output file
output_file = os.path.join(folder, table[:-4] + '_results.txt')


with open(csvpath, newline='') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')
    results = list(csvreader)

del results[0] #delete headers

TotalMonths = len(results)
TotalRevenue = 0
PreviousMonthRevenue = 0
TotalRevenueChange = []
GreatestRevenueIncrease, GreatestRevenueDecrease = [0, 0], [0, 0]

for row in results:
    TotalRevenue += int(row[1])
    RevenueChange = int(row[1]) - int(PreviousMonthRevenue)
    
    #making sure we don't count increases/decreases for the first record
    if len(TotalRevenueChange) > 0:
        #finding biggest increase in revenue
        if RevenueChange > int(GreatestRevenueIncrease[1]):
            GreatestRevenueIncrease = [row[0], RevenueChange]

        #finding biggest decrease in revenue
        if RevenueChange < int(GreatestRevenueDecrease[1]):
            GreatestRevenueDecrease = [row[0], RevenueChange]

    TotalRevenueChange.append(RevenueChange)
    PreviousMonthRevenue = row[1]

# delete the first record because there is no data for the previous month
# for the first record
del TotalRevenueChange[0] 

with open(output_file, "w") as datafile:
    #record file-descriptor
    oldstdout = sys.stdout

    #change output from console to file
    sys.stdout = datafile

    #print results to the file
    print('Financial Analysis for:', table)
    print('----------------------------')
    print('Total Months:', TotalMonths) 
    print('Total Revenue: ${:,.2f}'.format(TotalRevenue))
    print('Average Revenue Change: ${:,.2f}'.format(sum(TotalRevenueChange)/len(TotalRevenueChange)))
    print('Greatest Increase in Revenue: {} /${:,.2f}/'.format(
        GreatestRevenueIncrease[0], GreatestRevenueIncrease[1])) 
        
    print('Greatest Decrease in Revenue: {} /${:,.2f}/'.format(
        GreatestRevenueDecrease[0], GreatestRevenueDecrease[1]))

    #change output back to console
    sys.stdout = oldstdout

with open(output_file, "r") as datafile:
    #print the file
    print(datafile.read())

    #print where the file was saved
    print('----------------------------')
    print('Data saved to:', datafile.name)

