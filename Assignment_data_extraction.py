# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 13:04:20 2020

@author: Niall
"""

"""
Report into London Housing from 1995 to 2018
Tasks: Data extraction
    The data is in one csv file, this file comprises of monthly and yearly records, within these monthly
    and yearly records the data is comprised of 44 areas taken monthly, and 50 taken yearly. Within the monthly areas there are 
    32 unique areas and 12 groups of areas(The groups are different areas of England aswell as different groupings of London itself),
    and within the yearly records we have 31 unique areas and 18 groups of areas (again different parts of England, the U.K as a whole,
    Britain as an Island, Wales, Scotland, Northern Ireland ect.). 
    The challenge with extracting this data is that I must seperate these areas so that groups do not mix with individual areas and
    yearly does not mix with monthly. 
    Due to the mix of data there is a lot of missing values where certain groups do not have data for said variables, this must also be 
    dealt with.
"""

date = []
area = []
average_price = []
code = []
houses_sold = []
no_of_crimes = []
median_salary = []
life_satisfaction = []
mean_salary = []
recycling_pct = []
population_size = []
number_of_jobs = []
area_size = []
no_of_houses = []
with open("HousinginLondonyearlyandMonthly.csv") as data_file:
    data_file.readline() #Top Line
    for data in data_file:
        daten,arean,average_pricen,coden,houses_soldn,no_of_crimesn,median_salaryn,life_satisfactionn,mean_salaryn,recycling_pctn,population_sizen,number_of_jobsn,area_sizen,no_of_housesn = data.strip().split(",")
        date.append(daten)
        area.append(arean)
        average_price.append(average_pricen)
        code.append(coden)
        houses_sold.append(houses_soldn)
        no_of_crimes.append(no_of_crimesn)
        median_salary.append(median_salaryn)
        life_satisfaction.append(life_satisfactionn)
        mean_salary.append(mean_salaryn)
        recycling_pct.append(recycling_pctn)
        population_size.append(population_sizen)
        number_of_jobs.append(number_of_jobsn)
        area_size.append(area_sizen)
        no_of_houses.append(no_of_housesn)

"""For all the integer/ float lists the strings in them must be converted into ints/floats"""
lists_with_numeric_values = [average_price, houses_sold, no_of_crimes, median_salary, life_satisfaction, mean_salary,recycling_pct,population_size,number_of_jobs,area_size,no_of_houses]
lists_with_numeric_values_names = ["average_price", "houses_sold", "no_of_crimes", "median_salary", "life_satisfaction", "mean_salary","recycling_pct","population_size","number_of_jobs","area_size","no_of_houses"]

count = 0
list_count = 0

list_value_holder = []
index_value_holder = []


"""Find null values which in these lists are represented by empty strings and None values
   replace these with    .    for ease of processing and any actual missing values will be revealed
   giving their list and index. We can save these indexes for further processing"""
   
for each in lists_with_numeric_values:
    count = 0
    for data in each:
        try:
            if data == "" or data == None:
                each[count] = "."
                count+=1
                
            else:
                each[count] = float(each[count])
                count+=1
                
                
        except ValueError:
            #print(f"List {lists_with_numeric_values_names[list_count]} contains a non numeric, non null value at index {count}")
            list_value_holder.append(list_count)
            index_value_holder.append(count)
            count+=1
    list_count+=1

"""We now need to use the lists and index values that were missing to try and correct the data,
    the method I am going with is to get the previous years/months and the following years/months 
    data for that area and average them to find a value that is probably very close to actual"""
    
"""We need to use a for loop to loop back through the data to find the last non null value
    in that area for that variable"""

year_before = []
year_after = []
count = 0


for each in index_value_holder:
    index = each 
    if lists_with_numeric_values[list_value_holder[count]][index] == "-":
        print("Inner/OuterLondon")
        count +=1
    else:
        index = each - 1
        try:
            while area[each] != area[index] or lists_with_numeric_values[list_value_holder[count]][index] == ".":
                index -=1 
            try:
                tmp = float(lists_with_numeric_values[list_value_holder[count]][index])
                year_before.append(tmp)
            except:
                year_before.append(0)
        except IndexError:
            print("Out of range")
            year_after.append(0)
    
count = 0
for each in index_value_holder:
    index = each 
    if lists_with_numeric_values[list_value_holder[count]][index] == "-":
        print("Inner/OuterLondon")
        count +=1
    else:
        index = each + 1
        try:
            while area[each] != area[index] or lists_with_numeric_values[list_value_holder[count]][index] == ".":
                index +=1 
            try:
                tmp = float(lists_with_numeric_values[list_value_holder[count]][index])
                year_after.append(tmp)
            except:
                year_after.append(0)
        except IndexError:
            year_after.append(0)

#Creating averages
count = 0
corrected_values = []
for each in year_before:
    if year_before[count] == 0:
        corrected_values.append(year_after[count])
        count+=1
    elif year_after[count] == 0:
        corrected_values.append(year_before[count])
        count+=1
    else:
        corrected_values.append((year_before[count]+year_after[count])/2)
        count+=1

#Assigning averages
count=0
corrected_count=0
for each in index_value_holder:
    index = each 
    if lists_with_numeric_values[list_value_holder[count]][index] == "-":
        count +=1
    else:
        lists_with_numeric_values[list_value_holder[count]][index] = corrected_values[corrected_count]
        count+=1
        corrected_count+=1

#Find monthly areas of London
#Area code goes from E09000001 - 33 for london areas the other codes begin with E12 or something else

monthly_areas_of_london = []
monthly_areas_of_england = []
yearly_areas_of_England = []
count = 0
yorks = "yorks and the humber" #an awkward area with two similiar names
for each in area:
    if area[count] == yorks:
        area[count] = "yorkshire and the humber" 
    count+=1
count= 0
for each in area:      
    if float(code[count][2]) == 9 and float(code[count][-2:]) < 34 and each not in monthly_areas_of_london:
        monthly_areas_of_london.append(each) 
    elif count < 100 and each not in monthly_areas_of_england and each not in monthly_areas_of_london:
        monthly_areas_of_england.append(each)
    count+=1

#where area names have been slightly different
count=0   
for each in area:
    if float(code[count][2]) == 9 and float(code[count][-2:]) < 34:
        if code[count] == "E090000" + code[count][-2:]:
           area[count] = monthly_areas_of_london[int(code[count][-2:]) -1]
    count+=1

count = 0
for each in area:
    if each not in monthly_areas_of_england and each not in monthly_areas_of_london and each not in yearly_areas_of_England:
        yearly_areas_of_England.append(each)
   
    
#Now that the data is extracted cleaned and seperated we can start to work with it and we can
#start to bring in some interactive statements

#yearly or monthly,# what variable,# London city, england as a whole or the UK
#one area or all areas
#data available for monthly is






    
            

# =============================================================================
# for each in index_value_holder:
#     index = each - 1
#     while area[each] != area[index] or lists_with_numeric_values[list_value_holder[count]][index] == ".":
#         #print(lists_with_numeric_values[list_value_holder[count]][index])
#         index -=1
#     if lists_with_numeric_values[list_value_holder[count]][index] != "-":
#         print(lists_with_numeric_values[list_value_holder[count]][index])
#         tmp = float(lists_with_numeric_values[list_value_holder[count]][index])
#         year_before.append(tmp)
#     
# """We then need to use a for loop to loop forward through the data to find the next non null value
#     in that area for that variable"""
#     
# for each in index_value_holder:
#     index = each + 1
#     try:
#         while area[each] != area[index] or lists_with_numeric_values[list_value_holder[count]][index] == ".":
#             #print(lists_with_numeric_values[list_value_holder[count]][index])
#             index +=1
#         try:
#             tmp = float(lists_with_numeric_values[list_value_holder[count]][index])
#             year_after.append(tmp)   
#         except ValueError:
#             print("No value for year after using year before value instead")
#             year_after.append(year_before[len(year_before) - 1])
#             
#     except IndexError:
#         print("No value for year after using year before value instead")
#         year_after.append(year_before[len(year_before) - 1])
# 
# """We can then average these values and replace whats missing"""
# print(year_after)
# count = 0
# for each in list_value_holder:
#     average = (year_before[count] + year_after[count])/2
#     print(average)
#     lists_with_numeric_values[list_value_holder[count]][index_value_holder[count]] = average
#     count+=1
#         
# 
#     # tmp = lists_with_numeric_values_names[list_value_holder[count]]
#     # print(lists_with_numeric_values[list_value_holder[count]][each])
# =============================================================================
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    