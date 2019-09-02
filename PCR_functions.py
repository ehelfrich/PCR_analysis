# Author: Eric Helfrich
# Based off of the original code of Abrar Al-Shaer
# This file includes the the functions originally created by Abrar and updated to python 3
# and changed to meet updated requirements needed by the Smith Lab and UNC

# Imports
import pandas as pd
from scipy import stats
import os


def csv_init(file_PCR):
    print("---------Initiation of CSV file & Filteration---------")
    columns = []  # flag = columns
    from_csv = pd.read_csv(file_PCR, sep=None, header=0, engine='python')  # reading in the CSV file
    columns = from_csv[
        ['Target', 'Content', 'Sample', 'Biological Set Name', 'Cq', 'Cq Mean', 'Cq Std. Dev']]  # reads header columns
    # filteration step
    # blank Cq rows (or NTC) were removed in excel via F5 command
    # df = dataframe
    df = columns[columns.Cq != 0]  # removes zeroes if there is a zero in the Cq column
    df = df.drop_duplicates('Content', keep='first')  # removing duplicates based on content column value
    print(df)  # print first 5 lines of dataframe
    return df  # function returns dataframe as output


def rows_init_store(dataframe):
    print("---------Defining and Storing Rows From Dataframe---------")
    # Initializing blank lists
    Cq = []
    CqDev = []
    CqAvg = []
    content = []
    target = []
    sample = []
    set_name = []
    # loop through all the rows in the dataframe and add each elemenof each row to the proper column list
    for index, row in dataframe.iterrows():
        print(row[1], row[0], row[5], row[6])  # print content variable, target, mean, and standard deviation
        target.append(row[0])  # append = add to list
        content.append(row[1])
        Cq.append(row[4])
        CqAvg.append(row[5])
        CqDev.append(row[6])
        sample.append(row[2])
        set_name.append(row[3])
    return target, content, CqAvg, CqDev, sample, set_name  # function returns lists as output


def Ct_calculations(target, content, CqAvg, CqDev, sample, set_name, reference, one_target):
    print("--------------Ct Calculation Inputs---------------")
    CqAvgAll = []
    CqDevAll = []
    sampleAll = []
    set_nameAll = []
    reference_flag = 0
    target_flag = 0
    if reference in target[0]:
        reference_flag = 1
    if one_target in target[0]:
        target_flag = 1
    print("Reference FLAG:", reference_flag)
    print("Target FLAG:", target_flag)
    for i in range(0, len(content), 2):
        if reference_flag == 1:
            print(sample[i], target[i + 1], "-", target[i], "Means:", CqAvg[i + 1], "-", CqAvg[i],
                  "Standard Dev:", CqDev[i + 1], "&", CqDev[i])
            sampleAll.append(sample[i])
            set_nameAll.append(set_name[i])
            CqAvgAll.append(float(CqAvg[i + 1]) - float(CqAvg[i]))  # Cq calculation wither averages
            CqDevAll.append(
                (float(CqDev[i + 1]) ** 2.0 + float(CqDev[i]) ** 2.0) ** 0.5)  # Cq calculation with standard deviations
        if target_flag == 1:
            print(sample[i], target[i], "-", target[i + 1], "Means:", CqAvg[i], "-", CqAvg[i + 1],
                  "Standard Dev:", CqDev[i], "&", CqDev[i + 1])
            sampleAll.append(sample[i])
            set_nameAll.append(set_name[i])
            CqAvgAll.append(float(CqAvg[i]) - float(CqAvg[i + 1]))  # Cq calculation wither averages
            CqDevAll.append(
                (float(CqDev[i]) ** 2.0 + float(CqDev[i + 1]) ** 2.0) ** 0.5)  # Cq calculation with standard deviations
    return sampleAll, set_nameAll, CqAvgAll, CqDevAll


def Ct_calculations_print(sampleAll, set_nameAll, CqAvgAll, CqDevAll, fileNum, header):
    print("------------Ct Calculation Results-----------------")
    for i in range(0, len(CqAvgAll)):  # loop through and print all the contents of the lists
        print(sampleAll[i], set_nameAll[i], CqAvgAll[i], CqDevAll[i])
    # Ct Calculations DataFrame
    print("\n********Ct Calc File*************\n")
    df_Ct = pd.DataFrame({'Sample IDs': sampleAll, 'Biological Sets': set_nameAll, 'Cq Averages': CqAvgAll,
                          'Cq Standard Deviations': CqDevAll})  # creates a dataframe
    print(df_Ct)  # print all rows of dataframe
    print("\n********Ct Calc File SORTED*************\n")
    df_sort = df_Ct.sort_values('Biological Sets')
    print(df_sort)
    #  make a CSV file out of the DataFrame unique to the file number (fileNum)
    file_name = header + "_NUM_" + fileNum + "_Cq_calculations_" + '.csv'
    df_Ct.to_csv(os.path.join("output", file_name))  # print CSV contents to a file
    return df_sort


def Ct_calculations_merge(df_sorted):  # , df_sort2 add funcion as file no increase
    means = []
    set_names_merge = []

    for df in df_sorted:
        set_nameAll = df['Biological Sets'].tolist()
        CqAvgAll = df['Cq Averages'].tolist()


    print("CALC MERGE DATAFRAME 1\n")
    print(df_sort1)
    set_nameAll_1 = df_sort1['Biological Sets'].tolist()
    CqAvgAll_1 = df_sort1['Cq Averages'].tolist()
    print("SET NAME ALL 1:\n", set_nameAll_1)
    # print "CALC MERGE DATAFRAME 2\n"
    # print df_sort2
    # set_nameAll_2 = df_sort2['Biological Sets'].tolist()
    # CqAvgAll_2 = df_sort2['Cq Averages'].tolist()
    # print set_nameAll_2

    # print "CALC MERGE DATAFRAME 3\n"
    # print df_sort3
    # set_nameAll_3 = df_sort3['Biological Sets'].tolist()
    # CqAvgAll_3 = df_sort3['Cq Averages'].tolist()
    # print set_nameAll_3

    for i in range(0, len(set_nameAll_1)):  # loop through all biological sets
        set_names_merge.append(set_nameAll_1[i])
        means.append((CqAvgAll_1[i]) / 1.0)  # +CqAvgAll_2[i]/2 dividing by 6 because there are 6 replicates - we are getting the average of the Ct calculations across all the files
        print(set_nameAll_1[i])  # set_nameAll_2[i]    # add  set_nameAll_2[i] with each file
    # print results
    for j in range(0, len(set_names_merge)):  # loop and print results
        print(set_names_merge[j], means[j])
    return set_names_merge, means


def sem_calculation(set_names_merge, means):
    # Initialize the list of biological sets
    sets = ['IS-0', 'IS-5', 'ID-0', 'ID-5', 'IX-0', 'IX-5']  # MAKE SURE CALIBRATOR IS FIRST VALUE IN THE LIST
    IS_0 = []
    IS_5 = []
    ID_0 = []
    ID_5 = []
    IX_0 = []
    IX_5 = []
    SEMs = []
    set_averages = []
    for i in range(0, len(set_names_merge)):  # loop through and add to each set it's corresponding values
        if set_names_merge[i] == 'IS-0':
            IS_0.append(means[i])
        if set_names_merge[i] == 'IS-5':
            IS_5.append(means[i])
        if set_names_merge[i] == 'ID-0':
            ID_0.append(means[i])
        if set_names_merge[i] == 'ID-5':
            ID_5.append(means[i])
        if set_names_merge[i] == 'IX-0':
            IX_0.append(means[i])
        if set_names_merge[i] == 'IX-5':
            IX_5.append(means[i])
    # taking the mean of each set
    IS_0_avg = sum(IS_0) / len(IS_0)
    IS_5_avg = sum(IS_5) / len(IS_5)
    ID_0_avg = sum(ID_0) / len(ID_0)
    ID_5_avg = sum(ID_5) / len(ID_5)
    IX_0_avg = sum(IX_0) / len(IX_0)
    IX_5_avg = sum(IX_5) / len(IX_5)
    # averages combined into list
    set_averages.append(IS_0_avg)
    set_averages.append(IS_5_avg)
    set_averages.append(ID_0_avg)
    set_averages.append(ID_5_avg)
    set_averages.append(IX_0_avg)
    set_averages.append(IX_5_avg)
    # SEMs calculated and appended to list
    SEMs.append(stats.sem(IS_0))
    SEMs.append(stats.sem(IS_5))
    SEMs.append(stats.sem(ID_0))
    SEMs.append(stats.sem(ID_5))
    SEMs.append(stats.sem(IX_0))
    SEMs.append(stats.sem(IX_5))
    for j in range(0, len(set_averages)):
        print("Biological Set:", sets[j], "Average:", set_averages[j], "SEM:", SEMs[j])
    return sets, set_averages, SEMs


def delta_delta_Ct(sets, set_averages):
    calibrator_sample = set_averages[0]  # corresponds to IS_0 since it's the first value in the list [index 0]
    dCt_calc = []
    dCt_sets = []
    for i in range(0, len(sets)):
        dCt_sets.append(sets[i])
        dCt_calc.append(set_averages[i] - calibrator_sample)
        print(sets[i], set_averages[i] - calibrator_sample)
    return dCt_sets, dCt_calc


def fold_change(dCt_sets, dCt_calc, SEMs):
    FC = []
    FC_range_1 = []
    FC_range_2 = []
    FC_sets = dCt_sets
    for i in range(0, len(dCt_calc)):
        print("Biological Set:", FC_sets[i], "Fold Change:", 2 ** (dCt_calc[i] * -1), "FC Range:",
              2 ** ((dCt_calc[i] + SEMs[i]) * -1), "&", 2 ** ((dCt_calc[i] - SEMs[i]) * -1))
        FC.append(2 ** (dCt_calc[i] * -1))  # fold change calculation
        FC_range_1.append(2 ** ((dCt_calc[i] + SEMs[i]) * -1))  # fold change range 1
        FC_range_2.append(2 ** ((dCt_calc[i] - SEMs[i]) * -1))  # fold change range 2
    return FC_sets, FC, FC_range_1, FC_range_2


def yes_no(question):
    response = input(question + "(y/n): ").lower().strip()
    print("")
    while not (response == "y" or response == "yes" or response == "n" or response == "no"):
        print("Input yes or no")
        response = input(question + "(y/n):").lower().strip()
        print("")
    if response[0:] == "y" or response[0:] == "yes":
        return True
    else:
        return False

