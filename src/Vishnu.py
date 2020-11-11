import pandas as pd
import csv
import locale
import sys
sys.path.append("..")
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
df = pd.read_csv("../input/censustract-00-10.csv")

# select the columns we need
df_select = df[['CBSA09', 'CBSA_T', 'POP00', 'POP10', 'PPCHG']]

#  drop all the row with No Values
df_select = df_select.dropna()
#  Sort the values in the column CBSA_T alphabetically
df_select = df_select.sort_values("CBSA_T")
#  Rest the indices as they are mixed-up at this point
df_select = df_select.reset_index()
#  Remove the duplicate rows in CBSA_T column
values = df_select.drop_duplicates('CBSA_T')

#  Use these Indices values for additions and subtraction in the following steps
indexes = values.index.tolist()
# This is the total number of rows present in the data frame.
size_df=len(df_select.index)

i = 0
#  Output File where the result will be written.
with open('../output/report.csv', 'w', newline='') as file:
    while i < len(indexes):
        j = int(indexes[i])  # Set Base variable value
        k = 0
        #   Condition to ensure value is not going out of bound
        if i == len(indexes) - 1: # J value has reached the last element of the array, so k = i+1 is not possible anymore
            k = size_df
        else:

            k = int(indexes[i + 1])  # Looks for the next value in the array to perform a subtraction
        city_name = df_select.loc[j, 'CBSA_T'] # City Name
        difference = k - j  # This is how many times the city name is repeating.
        val_pop00 = []  # Population 2000
        val_pop10 = []  # Population 2010
        val_avg = []    # Population Change for 2000 and 2010
        total = 0
        total_10 = 0
        total_avg = 0
        cbsa_code = df_select.loc[j, 'CBSA09']  # City Code

        for item in range(j, j + difference):   # Loop the number of times city name is repeating
            val_pop00.append(df_select.loc[item, 'POP00'])
            val_pop10.append(df_select.loc[item, 'POP10'])
            if df_select.loc[item, 'PPCHG'] == '(X)':   # X is null so change it to 0.
                val_avg.append('0.0')
            else:
                val_avg.append(df_select.loc[item, 'PPCHG'])

        for val in range(len(val_pop00)):   # Add all the values appended above
            total = total + locale.atoi(val_pop00[val])
            total_10 = total_10 + locale.atoi(val_pop10[val])
            total_avg = total_avg + locale.atof(val_avg[val])

        total_avg = total_avg / float(difference)   # Population Change AVG
        row_list = [[int(cbsa_code), str(city_name), difference, total, total_10, round(total_avg, 2)]] # This list will be printed to the output file
        writer = csv.writer(file)
        writer.writerows(row_list)  # Write into the output file
        # Clear the arrays
        val_pop00.clear()
        val_pop10.clear()
        i = i + 1






