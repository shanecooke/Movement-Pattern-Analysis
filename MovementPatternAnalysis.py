#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd #imports pandas as pd.
import matplotlib.pyplot as plot #imports matplotlib as plot.
from pylab import rcParams #imports rcParams from pylab.

ire_csv = pd.read_csv('ireland.csv') #Reads the ireland csv into the variable ire_csv.
ire_csv_smooth = pd.read_csv('ireland.csv') #Reads the ireland csv into the variable ire_csv_smooth.
ire_csv_resampled = pd.read_csv("ireland.csv", parse_dates =["date"], index_col ="date") #Reads the ireland csv into the variable ire_csv_resampled and sets a Date/Time index.
sum_column = ire_csv['retail_and_recreation_percent_change_from_baseline'] + ire_csv['grocery_and_pharmacy_percent_change_from_baseline'] + ire_csv['parks_percent_change_from_baseline'] + ire_csv['transit_stations_percent_change_from_baseline'] + ire_csv['workplaces_percent_change_from_baseline'] + ire_csv['residential_percent_change_from_baseline'] #Sums all of the columns for the totals column.
sum_column_resampled = ire_csv_resampled['retail_and_recreation_percent_change_from_baseline'] + ire_csv_resampled['grocery_and_pharmacy_percent_change_from_baseline'] + ire_csv_resampled['parks_percent_change_from_baseline'] + ire_csv_resampled['transit_stations_percent_change_from_baseline'] + ire_csv_resampled['workplaces_percent_change_from_baseline'] + ire_csv_resampled['residential_percent_change_from_baseline'] #Sums all of the resampled columns for the resampled totals column.
ire_csv["total"] = sum_column #Creates a new column of totals in the original dataframe.
ire_csv["total"] = ire_csv["total"].div(6) #Divides these totals by 6 to get the average total.
ire_csv_smooth["total"] = sum_column
ire_csv_smooth["total"] = ire_csv_smooth["total"].div(6)
ire_csv_resampled["total"] = sum_column_resampled
ire_csv_resampled["total"] = ire_csv_resampled["total"].div(6)
ire_csv_resampled = ire_csv_resampled.resample('W').mean() #Resamples the dataframe, 'W' represents weeks.
lastindex = ire_csv.last_valid_index() #Variable to contain the last index in the csv file.

#print(ire_csv)
#print(ire_csv_smooth)
#print(ire_csv_resampled) #Prints each of the dataframes.

column_list = ['retail_and_recreation_percent_change_from_baseline','grocery_and_pharmacy_percent_change_from_baseline','parks_percent_change_from_baseline','transit_stations_percent_change_from_baseline','workplaces_percent_change_from_baseline','residential_percent_change_from_baseline', 'total'] #A list of the column names.
label_list = ['Retail and Recreation','Grocery and Pharmacy','Parks','Transit Stations','Workplaces','Residential'] #A list of the label names.
colour_list = ['blue','green','red','orange','purple','black'] #A list of colours.

def smoothen_df_ire(): #function to smoothen the data within the dataframe.
    for i in range(len(column_list)):
        ire_csv_smooth[column_list[i]] = ire_csv[column_list[i]].rolling(10).mean() #Function .rolling smoothens the data.
        
smoothen_df_ire() #Calls the function that smooths the data.
ire_csv_smooth.fillna(0, inplace=True) #Fills the NA's in the smoothened dataframe with 0's.

def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) #Function allowing me to print to the console in red.

def get_all_correlations_ire(): #Function to print all of the correlations between each sector in Ireland.
    print('Correlations between sectors in Ireland:')
    for i in range(len(column_list) - 1):
        print('')
        prRed('{}:'.format(label_list[i])) #Calling function that prints to the console in red.
        for x in range(len(column_list) - 1):
            if(x != i):
                print('- {} : {}'.format(label_list[x], ire_csv[column_list[i]].corr(ire_csv[column_list[x]])))
            
get_all_correlations_ire() #Calls function to get all correlations for Ireland.

def print_graphs_ire(): #Function to graph each individual column from the ireland csv.
    for i in range(len(column_list) - 1):
        ire_csv.plot(x='date', y=column_list[i], label=label_list[i], color=colour_list[i], title=label_list[i] + ' : % change from baseline, in Ireland.')
        plot.xlim(0, lastindex) #Sets the limits of the x-axis between 0 and lastindex.
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
        
def print_smooth_graphs_ire(): #Function to graph each individual smoothened column from the ireland csv.
    for i in range(len(column_list) - 1):
        ire_csv_smooth.plot(x='date', y=column_list[i], label=label_list[i], color=colour_list[i], title=label_list[i] + ' : % change from baseline, in Ireland. (Smoothened)')
        plot.xlim(0, lastindex)
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
        
def print_resampled_graphs_ire(): #Function to graph each individual resampled column from the ireland csv.
    for i in range(len(column_list) - 1):
        ire_csv_resampled.plot(y=column_list[i], label=label_list[i], color=colour_list[i], title=label_list[i] + ' : % change from baseline, in Ireland. (Resampled)')        
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
    
rcParams['figure.figsize'] = 15, 8 #Sets the parameters for the plots.
#print_graphs_ire()
#print_smooth_graphs_ire()
#print_resampled_graphs_ire() #Calling each function to print the individual graphs for each column of the csv.

def print_comparison_ire(): #Function to print the comparison graph which contains 6 lines from the ireland csv.
    ax = ire_csv.plot(x='date', y=column_list[0], color=colour_list[0], label=label_list[0], title='Comparison : % change from baseline, in Ireland.')
    plot.xlim(0, lastindex)
    plot.axhline(y=0, color='black', linestyle='--', alpha=0.8) #Plots a dotted line in the graph at y=0.
    for i in range(len(column_list) - 1):
        if(i>0):
            ire_csv.plot(ax=ax, x='date', y=column_list[i], color=colour_list[i], label=label_list[i])

def print_comparison_ire_smooth(): #Function to print the comparison graph which contains 6 smoothened lines from the ireland csv.
    ax = ire_csv_smooth.plot(x='date', y=column_list[0], color=colour_list[0], label=label_list[0], title='Comparison : % change from baseline, in Ireland. (Smoothened))')
    plot.xlim(0, lastindex)
    plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
    for i in range(len(column_list) - 1):
        if(i>0):
            ire_csv_smooth.plot(ax=ax, x='date', y=column_list[i], color=colour_list[i], label=label_list[i])
            
def print_comparison_ire_resampled(): #Function to print the comparison graph which contains 6 resampled lines from the ireland csv.
    ax = ire_csv_resampled.plot(y=column_list[0], color=colour_list[0], label=label_list[0], title='Comparison : % change from baseline, in Ireland. (Resampled))')
    for i in range(len(column_list) - 1):
        if(i>0):
            ire_csv_resampled.plot(ax=ax, y=column_list[i], color=colour_list[i], label=label_list[i])

print_comparison_ire()
print_comparison_ire_smooth()            
print_comparison_ire_resampled() #Calls the functions that print the comparison graphs.

ire_csv.plot(x='date', y='total', color='green', label='Total', title='Total % change from baseline, in Ireland.') #Plots the total movement patterns within Ireland.
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8) #Plots a dotted line in the graph at y=0.
plot.xlim(0, lastindex)

ire_csv_smooth.plot(x='date', y='total', color='green', label='Total', title='Total % change from baseline, in Ireland. (Smoothened)') #Plots the smoothened total movement patterns within Ireland.
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
plot.xlim(0, lastindex)

ire_csv_resampled.plot(y='total', color='green', label='Total', title='Total % change from baseline, in Ireland. (Resampled)') #Plots the resampled total movement patterns within Ireland.
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)


# In[ ]:


it_csv = pd.read_csv('italy.csv') #Reads the italy csv into the variable it_csv.
it_csv_smooth = pd.read_csv('italy.csv') #Reads the italy csv into the variable it_csv_smooth.
it_csv_resampled = pd.read_csv("italy.csv", parse_dates =["date"], index_col ="date") #Reads the italy csv into the variable it_csv_resampled and sets a Date/Time index.
sum_column2 = it_csv['retail_and_recreation_percent_change_from_baseline'] + it_csv['grocery_and_pharmacy_percent_change_from_baseline'] + it_csv['parks_percent_change_from_baseline'] + it_csv['transit_stations_percent_change_from_baseline'] + it_csv['workplaces_percent_change_from_baseline'] + it_csv['residential_percent_change_from_baseline'] #Sums all of the columns for the totals column.
sum_column_resampled2 = it_csv_resampled['retail_and_recreation_percent_change_from_baseline'] + it_csv_resampled['grocery_and_pharmacy_percent_change_from_baseline'] + it_csv_resampled['parks_percent_change_from_baseline'] + it_csv_resampled['transit_stations_percent_change_from_baseline'] + it_csv_resampled['workplaces_percent_change_from_baseline'] + it_csv_resampled['residential_percent_change_from_baseline'] #Sums all of the resampled columns for the resampled totals column.
it_csv["total"] = sum_column2 #Creates a new column of totals in the original dataframe.
it_csv["total"] = it_csv["total"].div(6) #Divides these totals by 6 to get the average total.
it_csv_smooth["total"] = sum_column2
it_csv_smooth["total"] = it_csv_smooth["total"].div(6)
it_csv_resampled["total"] = sum_column_resampled2
it_csv_resampled["total"] = it_csv_resampled["total"].div(6)
it_csv_resampled = it_csv_resampled.resample('W').mean() #Resamples the dataframe, 'W' represents weeks.

#print(it_csv)
#print(it_csv_smooth)
#print(it_csv_resampled) #Prints each of the dataframes.

column_list = ['retail_and_recreation_percent_change_from_baseline','grocery_and_pharmacy_percent_change_from_baseline','parks_percent_change_from_baseline','transit_stations_percent_change_from_baseline','workplaces_percent_change_from_baseline','residential_percent_change_from_baseline','total'] #A list of the column names.
label_list = ['Retail and Recreation','Grocery and Pharmacy','Parks','Transit Stations','Workplaces','Residential'] #A list of the label names.
colour_list = ['blue','green','red','orange','purple','black'] #A list of colours.

def smoothen_df_it(): #function to smoothen the data within the dataframe.
    for i in range(len(column_list)):
        it_csv_smooth[column_list[i]] = it_csv[column_list[i]].rolling(10).mean() #Function .rolling smoothens the data.
        
smoothen_df_it() #Calls the function that smooths the data.
it_csv_smooth.fillna(0, inplace=True) #Fills the NA's in the smoothened dataframe with 0's.
        
def get_all_correlations_it(): #Function to print all of the correlations between each sector in Italy.
    print('Correlations between sectors in Italy:')
    for i in range(len(column_list) - 1):
        print('')
        prRed('{}:'.format(label_list[i])) #Calling function that prints to the console in red.
        for x in range(len(column_list) - 1):
            if(x != i):
                print('- {} : {}'.format(label_list[x], it_csv[column_list[i]].corr(it_csv[column_list[x]])))
            
get_all_correlations_it() #Calls function to get all correlations for Italy.

def print_graphs_it(): #Function to graph each individual column from the italy csv.
    for i in range(len(column_list) - 1):
        it_csv.plot(x='date', y=column_list[i], label=label_list[i], color=colour_list[i], title=label_list[i] + ' : % change from baseline, in Italy.')
        plot.xlim(0, lastindex) #Sets the limits of the x-axis between 0 and lastindex.
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
    
def print_smooth_graphs_it(): #Function to graph each individual smoothened column from the italy csv.
    for i in range(len(column_list) - 1):
        it_csv_smooth.plot(x='date', y=column_list[i], label=label_list[i], color=colour_list[i], title=label_list[i] + ' : % change from baseline, in Italy. (Smoothened)')
        plot.xlim(0, lastindex)
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
        
def print_resampled_graphs_it(): #Function to graph each individual resampled column from the italy csv.
    for i in range(len(column_list) - 1):
        it_csv_resampled.plot(y=column_list[i], label=label_list[i], color=colour_list[i], title=label_list[i] + ' : % change from baseline, in Italy. (Resampled)')        
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
        
rcParams['figure.figsize'] = 15, 8 #Sets the parameters for the plots.            
#print_graphs_it()
#print_smooth_graphs_it()
#print_resampled_graphs_it() #Calling each function to print the individual graphs for each column of the csv.

def print_comparison_it(): #Function to print the comparison graph which contains 6 lines from the italy csv.
    ax = it_csv.plot(x='date', y=column_list[0], color=colour_list[0], label=label_list[0], title='Comparison : % change from baseline, in Italy.')
    plot.xlim(0, lastindex)
    plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
    for i in range(len(column_list) - 1):
        if(i>0):
            it_csv.plot(ax=ax, x='date', y=column_list[i], color=colour_list[i], label=label_list[i])
            
def print_comparison_it_smooth(): #Function to print the comparison graph which contains 6 smoothened lines from the italy csv.
    ax = it_csv_smooth.plot(x='date', y=column_list[0], color=colour_list[0], label=label_list[0], title='Comparison : % change from baseline, in Italy. (Smoothened)')
    plot.xlim(0, lastindex)
    plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
    for i in range(len(column_list) - 1):
        if(i>0):
            it_csv_smooth.plot(ax=ax, x='date', y=column_list[i], color=colour_list[i], label=label_list[i])
            
def print_comparison_it_resampled(): #Function to print the comparison graph which contains 6 resampled lines from the italy csv.
    ax = it_csv_resampled.plot(y=column_list[0], color=colour_list[0], label=label_list[0], title='Comparison : % change from baseline, in Italy. (Resampled)')
    for i in range(len(column_list) - 1):
        if(i>0):
            it_csv_resampled.plot(ax=ax, y=column_list[i], color=colour_list[i], label=label_list[i])
            
print_comparison_it()
print_comparison_it_smooth()
print_comparison_it_resampled() #Calls the functions that print the comparison graphs.

it_csv.plot(x='date', y='total', color='red', label='Total', title='Total % change from baseline, in Italy.') #Plots the total movement patterns within Italy.
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8) #Plots a dotted line in the graph at y=0.
plot.xlim(0, lastindex)

it_csv_smooth.plot(x='date', y='total', color='red', label='Total', title='Total % change from baseline, in Italy. (Smoothened)') #Plots the smoothened total movement patterns within Italy.
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
plot.xlim(0, lastindex)

it_csv_resampled.plot(y='total', color='red', label='Total', title='Total % change from baseline, in Italy. (Resampled)') #Plots the resampled total movement patterns within Italy.
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)


# In[ ]:


nz_csv = pd.read_csv('new_zealand.csv') #Reads the new zealand csv into the variable nz_csv.
nz_csv_smooth = pd.read_csv('new_zealand.csv') #Reads the new zealand csv into the variable nz_csv_smooth.
nz_csv_resampled = pd.read_csv("new_zealand.csv", parse_dates =["date"], index_col ="date") #Reads the new zealand csv into the variable nz_csv_resampled and sets a Date/Time index.
sum_column3 = nz_csv['retail_and_recreation_percent_change_from_baseline'] + nz_csv['grocery_and_pharmacy_percent_change_from_baseline'] + nz_csv['parks_percent_change_from_baseline'] + nz_csv['transit_stations_percent_change_from_baseline'] + nz_csv['workplaces_percent_change_from_baseline'] + nz_csv['residential_percent_change_from_baseline'] #Sums all of the columns for the totals column.
sum_column_resampled3 = nz_csv_resampled['retail_and_recreation_percent_change_from_baseline'] + nz_csv_resampled['grocery_and_pharmacy_percent_change_from_baseline'] + nz_csv_resampled['parks_percent_change_from_baseline'] + nz_csv_resampled['transit_stations_percent_change_from_baseline'] + nz_csv_resampled['workplaces_percent_change_from_baseline'] + nz_csv_resampled['residential_percent_change_from_baseline'] #Sums all of the resampled columns for the resampled totals column.
nz_csv["total"] = sum_column3 #Creates a new column of totals in the original dataframe.
nz_csv["total"] = nz_csv["total"].div(6) #Divides these totals by 6 to get the average total.
nz_csv_smooth["total"] = sum_column3
nz_csv_smooth["total"] = nz_csv_smooth["total"].div(6)
nz_csv_resampled["total"] = sum_column_resampled3
nz_csv_resampled["total"] = nz_csv_resampled["total"].div(6)
nz_csv_resampled = nz_csv_resampled.resample('W').mean() #Resamples the dataframe, 'W' represents weeks.

#print(nz_csv)
#print(nz_csv_smooth)
#print(nz_csv_resampled) #Prints each of the dataframes.

column_list = ['retail_and_recreation_percent_change_from_baseline','grocery_and_pharmacy_percent_change_from_baseline','parks_percent_change_from_baseline','transit_stations_percent_change_from_baseline','workplaces_percent_change_from_baseline','residential_percent_change_from_baseline', 'total'] #A list of the column names.
label_list = ['Retail and Recreation','Grocery and Pharmacy','Parks','Transit Stations','Workplaces','Residential'] #A list of the label names.
colour_list = ['blue','green','red','orange','purple','black'] #A list of colours.

def smoothen_df_nz(): #function to smoothen the data within the dataframe.
    for i in range(len(column_list)):
        nz_csv_smooth[column_list[i]] = nz_csv[column_list[i]].rolling(10).mean() #Function .rolling smoothens the data.
        
smoothen_df_nz() #Calls the function that smooths the data.
nz_csv_smooth.fillna(0, inplace=True) #Fills the NA's in the smoothened dataframe with 0's.

def get_all_correlations_nz(): #Function to print all of the correlations between each sector in New Zealand.
    print('Correlations between sectors in New Zealand:')
    for i in range(len(column_list) - 1):
        print('')
        prRed('{}:'.format(label_list[i])) #Calling function that prints to the console in red.
        for x in range(len(column_list) - 1):
            if(x != i):
                print('- {} : {}'.format(label_list[x], nz_csv[column_list[i]].corr(nz_csv[column_list[x]])))
            
get_all_correlations_nz() #Calls function to get all correlations for New Zealand.

def print_graphs_nz(): #Function to graph each individual column from the new zealand csv.
    for i in range(len(column_list) - 1):
        nz_csv.plot(x='date', y=column_list[i], label=label_list[i], color=colour_list[i], title=label_list[i] + ' : % change from baseline, in New Zealand.')
        plot.xlim(0, lastindex) #Sets the limits of the x-axis between 0 and lastindex.
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
        
def print_smooth_graphs_nz(): #Function to graph each individual smoothened column from the new zealand csv.
    for i in range(len(column_list) - 1):
        nz_csv_smooth.plot(x='date', y=column_list[i], label=label_list[i], color=colour_list[i], title=label_list[i] + ' : % change from baseline, in New Zealand. (Smoothened)')
        plot.xlim(0, lastindex)
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
        
def print_resampled_graphs_nz(): #Function to graph each individual resampled column from the new zealand csv.
    for i in range(len(column_list) - 1):
        nz_csv_resampled.plot(y=column_list[i], label=label_list[i], color=colour_list[i], title=label_list[i] + ' : % change from baseline, in New Zealand. (Resampled)')            
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
        
rcParams['figure.figsize'] = 15, 8 #Sets the parameters for the plots.        
#print_graphs_nz()
#print_smooth_graphs_nz()
#print_resampled_graphs_nz() #Calling each function to print the individual graphs for each column of the csv.

def print_comparison_nz(): #Function to print the comparison graph which contains 6 lines from the new zealand csv.
    ax = nz_csv.plot(x='date', y=column_list[0], color=colour_list[0], label=label_list[0], title='Comparison : % change from baseline, in New Zealand.')
    plot.xlim(0, lastindex)
    plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
    for i in range(len(column_list) - 1):
        if(i>0):
            nz_csv.plot(ax=ax, x='date', y=column_list[i], color=colour_list[i], label=label_list[i])
            
def print_comparison_nz_smooth(): #Function to print the comparison graph which contains 6 smoothened lines from the new zealand csv.
    ax = nz_csv_smooth.plot(x='date', y=column_list[0], color=colour_list[0], label=label_list[0], title='Comparison : % change from baseline, in New Zealand. (Smoothened)')
    plot.xlim(0, lastindex)
    plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
    for i in range(len(column_list) - 1):
        if(i>0):
            nz_csv_smooth.plot(ax=ax, x='date', y=column_list[i], color=colour_list[i], label=label_list[i])
            
def print_comparison_nz_resampled(): #Function to print the comparison graph which contains 6 resampled lines from the new zealand csv.
    ax = nz_csv_resampled.plot(y=column_list[0], color=colour_list[0], label=label_list[0], title='Comparison : % change from baseline, in New Zealand. (Resampled)')
    for i in range(len(column_list) - 1):
        if(i>0):
            nz_csv_resampled.plot(ax=ax, y=column_list[i], color=colour_list[i], label=label_list[i])
            
print_comparison_nz()
print_comparison_nz_smooth()
print_comparison_nz_resampled() #Calls the functions that print the comparison graphs.

nz_csv.plot(x='date', y='total', color='black', label='Total', title='Total % change from baseline, in New Zealand.') #Plots the total movement patterns within New Zealand.
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8) #Plots a dotted line in the graph at y=0.
plot.xlim(0, lastindex)

nz_csv_smooth.plot(x='date', y='total', color='black', label='Total', title='Total % change from baseline, in New Zealand. (Smoothened)') #Plots the smoothened total movement patterns within New Zealand.
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
plot.xlim(0, lastindex)

nz_csv_resampled.plot(y='total', color='black', label='Total', title='Total % change from baseline, in New Zealand. (Resampled)') #Plots the resampled total movement patterns within New Zealand.
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)


# In[ ]:


def print_comparisons(): #Function to print the comparison graphs for each column, from all 3 countries.
    for i in range(len(column_list) - 1):
        ax = ire_csv.plot(x='date', y=column_list[i], color='green', label='Ireland', title='Comparison between Countries : ' + label_list[i] + ' % change from baseline')
        it_csv.plot(ax=ax, x='date', y=column_list[i], color='red', label='Italy')
        nz_csv.plot(ax=ax, x='date', y=column_list[i], color='black', label='New Zealand')
        plot.xlim(0, lastindex)
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
        
def print_smoothened_comparisons(): #Function to print the smoothened comparison graphs for each column, from all 3 countries.
    for i in range(len(column_list) - 1):
        ax = ire_csv_smooth.plot(x='date', y=column_list[i], color='green', label='Ireland', title='Comparison between Countries : ' + label_list[i] + ' % change from baseline. (Smoothened)')
        it_csv_smooth.plot(ax=ax, x='date', y=column_list[i], color='red', label='Italy')
        nz_csv_smooth.plot(ax=ax, x='date', y=column_list[i], color='black', label='New Zealand')
        plot.xlim(0, lastindex)
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)
        
def print_resampled_comparisons(): #Function to print the resampled comparison graphs for each column, from all 3 countries.
    for i in range(len(column_list) - 1):
        ax = ire_csv_resampled.plot(y=column_list[i], color='green', label='Ireland', title='Comparison between Countries : ' + label_list[i] + ' % change from baseline. (Resampled)')
        it_csv_resampled.plot(ax=ax, y=column_list[i], color='red', label='Italy')
        nz_csv_resampled.plot(ax=ax, y=column_list[i], color='black', label='New Zealand')
        plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)

rcParams['figure.figsize'] = 15, 8 #Sets the parameters for the plots.        
#print_comparisons()        
#print_smoothened_comparisons()
#print_resampled_comparisons() #Calls each of the functions to print the country comparison graphs.

ax=ire_csv.plot(x='date', y='total', color='green', label='Ireland', title='Comparison between Countries : Total % change from baseline.') #Prints a comparison graph for each countries average total.
it_csv.plot(ax=ax, x='date', y='total', color='red', label='Italy')
nz_csv.plot(ax=ax, x='date', y='total', color='black', label='New Zealand')
plot.xlim(0, lastindex)
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)  #Plots a dotted line in the graph at y=0.

ax=ire_csv_smooth.plot(x='date', y='total', color='green', label='Ireland', title='Comparison between Countries : Total % change from baseline (Smoothened).') #Prints a smoothened comparison graph for each countries average total.
it_csv_smooth.plot(ax=ax, x='date', y='total', color='red', label='Italy')
nz_csv_smooth.plot(ax=ax, x='date', y='total', color='black', label='New Zealand')
plot.xlim(0, lastindex)
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)

ax=ire_csv_resampled.plot(y='total', color='green', label='Ireland', title='Comparison between Countries : Total % change from baseline (Resampled).') #Prints a resampled comparison graph for each countries average total.
it_csv_resampled.plot(ax=ax, y='total', color='red', label='Italy')
nz_csv_resampled.plot(ax=ax, y='total', color='black', label='New Zealand')
plot.axhline(y=0, color='black', linestyle='--', alpha=0.8)


# In[ ]:


correlations = [0,0,0,0,0,0] #Creates 3 empty correlation lists.
correlations2 = [0,0,0,0,0,0]
correlations3 = [0,0,0,0,0,0]

def correlations_ire_it(): #Function to fill the correlation list between Ireland and Italy.
    for i in range(len(column_list) - 1):
        correlations[i] = ire_csv[column_list[i]].corr(it_csv[column_list[i]])
        
def correlations_ire_nz(): #Function to fill the correlation list between Ireland and New Zealand.
    for i in range(len(column_list) - 1):
        correlations2[i] = ire_csv[column_list[i]].corr(nz_csv[column_list[i]])
        
def correlations_it_nz():
    for i in range(len(column_list) - 1):
        correlations3[i] = it_csv[column_list[i]].corr(nz_csv[column_list[i]]) #Function to fill the correlation list between Italy and New Zealand.

correlations_ire_it()
correlations_ire_nz()
correlations_it_nz() #Calls each of the correlation functions.

correlations_dataframe = pd.DataFrame() #Creates a new empty datframe.
correlations_dataframe['Sectors'] = label_list #Creates a column with all of the different sectors from the original csv.
correlations_dataframe['Ireland vs Italy'] = correlations #Creates a column for Ireland vs Italy.
correlations_dataframe['Ireland vs New Zealand'] = correlations2 #Creates a column for Ireland vs New Zealand.
correlations_dataframe['Italy vs New Zealand'] = correlations3 #Creates a column for Italy vs New Zealand.

ire_it_total = correlations_dataframe['Ireland vs Italy'].sum() / 6 #sums all of the correlations and gets the average by dividing by 6.
ire_nz_total = correlations_dataframe['Ireland vs New Zealand'].sum() / 6
it_nz_total = correlations_dataframe['Italy vs New Zealand'].sum() / 6

totals_df = pd.DataFrame() #Creats a new empty dataframe.
totals_df['Comparisons'] = ['Ireland vs Italy','Ireland vs New Zealand','Italy vs New Zealand'] #Creates a column called Comparisons.
totals_df['Values'] = [ire_it_total,ire_nz_total,it_nz_total] #Creats a column called Values.
#print(totals_df) #Prints the totals dataframe.

#print(correlations_dataframe) #Prints the correlations dataframe.

rcParams['figure.figsize'] = 6, 8 #Sets the parameters for the graph.
correlations_dataframe.plot.bar(x='Sectors', color=['blue', 'green', 'red'], edgecolor='black', title='Comparison between Countries : Correlations.')
plot.axhline(y=0.428648, color='black', linestyle='--', alpha=0.7) #Plots a dotted line along the minimum point of the graph.
plot.axhline(y=0.805559, color='black', linestyle='--', alpha=0.7) #Plots a dotted line along the maximum point of the graph.

rcParams['figure.figsize'] = 6, 6 
totals_df.plot.bar(x='Comparisons', y='Values', color=['blue', 'green', 'red'], edgecolor='black', title='Comparison between Countries : Total Correlations.')
plot.axhline(y=0.746500, color='blue', linestyle='--', alpha=0.7) #Plots a dotted line at Ireland vs Italy.
plot.axhline(y=0.673447, color='green', linestyle='--', alpha=0.7) #Plots a dotted line at Ireland vs New Zealand.
plot.axhline(y=0.625431, color='red', linestyle='--', alpha=0.7) #Plots a dotted line at Italy vs New Zealand.


# In[ ]:




