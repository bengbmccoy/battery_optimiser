'''
Written: Ben McCoy, 201903

This is the first writing of the optimiser script:
1. Take a profile and calculate the list of volume_charges
2. Take a profile and calculate the list of capacity_charges
3. Sum the elemets of each list and call it all_charges
4. Find the index of max(all_charges)
5. Remove from profile[nmax] the battery diff
6. Remove the batter diff from batter_cap

'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def list_volume_charges(new_profile, tariff):
    ''' this function takes an electricity profile as a list and a tariff of
    the same len as the profilie and multiplies each item and places those
    values in a list that is returned'''

    volume_charges = []
    for i in range(len(new_profile)):
        volume_charges.append(new_profile[i] * tariff[i])
    return volume_charges

def list_cpacity_charges(new_profile, capacity_charge):
    ''' this functon currently find the index of the max value in an electricity
    profilie and then returns a list with every value as 0 except o the index
    with the peak profile demand, this element is capacity_charge * max(profile)

    TODO:
    - Rework this function to be able to handle peak times etc.

    '''

    capacity_charges = []
    index_max = max(xrange(len(new_profile)), key=new_profile.__getitem__)

    for i in range(len(new_profile)):
        if i == index_max:
            capacity_charges.append(new_profile[i] * capacity_charge)
        else:
            capacity_charges.append(0)

    return capacity_charges

def list_summed_charges(list_vol_charges, list_cap_charges):
    '''returns a list that is the sum of both the list_vol_charges and
    list_cap_charges at each index'''

    all_charges = []

    for i in range(len(list_vol_charges)):
        all_charges.append(list_vol_charges[i] + list_cap_charges[i])

    return all_charges

def index_peak_charge(list_sum_charges):
    '''returns the index of the max value in a list'''

    index_max = max(xrange(len(list_sum_charges)), key=list_sum_charges.__getitem__)
    return index_max

def optimise_profile(index_peak_charge, battery_diff, new_profile):
    '''subtracts the battery diff from the new_profile element of index n
    and returns the updated list'''

    for i in range(len(new_profile)):
        if i == index_peak_charge:
            new_profile[i] = new_profile[i] - battery_diff

    return  new_profile

def get_data():
    '''gets data from data/energydatayr.csv and returns a pandas dataframe
    with the index as a datetime object'''

    data = pd.read_csv('data/energydatayr.csv')
    data.set_index('DateTime', inplace=True)
    data.index = pd.to_datetime(data.index)

    return data

def get_list_days(data):
    '''gets a list of unique days from the index of the dataframe'''

    days = []
    index_list = data.index.values
    for item in index_list:
        if str(item)[:10] not in days:
            days.append(str(item)[:10])
    return days

def get_days_values_dict(data, days):
    '''initislises a dictionary with the keys as unique days and the values
    as empty lists. Then itereates through the data frame and appends any
    consumption values from that day to the list with the dictionary'''

    days_values_dict = {}
    for day in days:
        days_values_dict[day] = list()

    for index, row in data.iterrows():
        data_day = str(index)[:10]
        days_values_dict[data_day].append(row['Value'])

    return days_values_dict

def main():

    data = get_data()
    # print data

    days = get_list_days(data)
    # print days

    days_values_dict = get_days_values_dict(data, days)
    # print days_values_dict

    opt_profile_dict = {}
    for day in days:
        opt_profile_dict[day] = days_values_dict[day]
    print opt_profile_dict

    for key, value in opt_profile_dict.iteritems():
        print len(value)

    ''' Below this part is the first part of this project that will be piped
    to the second part when it is ready.


    The below code is how to optimise one day at a time and
    the above code is how to sort the data into manageable days


    flag = False

    # profile = [1,2,3,4,5,6,5,4,5,4,5,6,7,8,9,9,8,7,5,4,3,1]
    # new_profile = list(profile)
    # tariff = [1,1,1,1,1,1,1,2,2,2,2,2,2,2,4,4,4,4,4,4,2,2]
    # battery = 50
    # new_battery = int(battery)
    # battery_diff = 0.25
    # cap_cost = 2

    if flag == True:
        while new_battery >= battery_diff:

            list_vol_charges = list_volume_charges(new_profile, tariff)
            list_cap_charges = list_cpacity_charges(new_profile, cap_cost)
            list_sum_charges = list_summed_charges(list_vol_charges, list_cap_charges)
            index_max_charge = index_peak_charge(list_sum_charges)
            new_profile = optimise_profile(index_max_charge, battery_diff, new_profile)
            new_battery = new_battery - battery_diff
            # print list_sum_charges
            print sum(list_sum_charges)


            y1 = new_profile
            plt.plot(y1)
            plt.ylim(0, max(profile))
            plt.draw()
            plt.pause(0.0001)
            plt.clf()


    if flag == True:
        y = profile
        y1 = new_profile

        plt.plot(range(len(y)), y, label='profile')
        plt.plot(range(len(y1)), y1, label='new_profile')
        plt.legend()
        plt.show()

    '''

main()
