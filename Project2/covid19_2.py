'''This program analyse covid data from 2020 to 2021 from different countries and continents.
Aim of this program is to ouput number of cases, death, number of days/values greater than average of cases and death in 4 lists
if the user input country or continent as the key of the dictonary. If there is anything wrong with the file, terminate the
program and return None and show the error message on display'''

def main(csvfile):
    '''main function that output the sorted data '''
    try:
        countries, continents, requiredHeader = read_file (csvfile)
        if len(requiredHeader) > 5:                          # check iff any duplicate columns, if yes return None. 
            print ("Duplicates found in required columns")   # len != 5 can be used to find both duplicate or missing columns 
            return None                                      # but to get more specific error message, missing columns is determined by IndexError
        country_dic = findSum_lst(countries)
        continent_dic = findSum_lst1(continents)
        return country_dic, continent_dic            # return 2 dic if conditions satisfied,  else try catch errors that may occur
    except IOError:
        print("File wasn't found. Please input the correct filename/enter a string value.")
        return None
    except OSError:                                  # if file cannot be read/no permission (Could be IOError)
        print("File is not readable.")
        return None
    except TypeError:                                # if data type of argument like dic, list etc
        print("Please enter a string value.")
        return None
    except IndexError:                               # if requried columns are missing
        print("Required column/s cannot be found in the file, please check file data.")
        return None
    except:
        print("Unexpected error, please check your file")
        return None

def checkDuplicate(header, requiredCol):
    header2 = []
    for item in header :
        if item in requiredCol:
            header2.append(item)
    return header2
    
def read_file (filename):
    '''process file'''
    file = open(filename, "r")    
    header = next(file).strip().split(',')     # list of header of the file 
    header = [s.lower() for s in header]       # convert all headers to lower case
    requiredCol = ["continent", "location", "date", "new_cases", "new_deaths"] # required column for data analysis
    header2 = checkDuplicate(header, requiredCol)    
    headerInd = findcol(header, requiredCol)   # index of the required headers in the header column
    countries={}
    continents={}
    for line in file:                                 # read file from second line
        continent, country, case, death, month, day, date = parseLine(line, headerInd)
        if sortDate(date):                            # if date has right format == true
            countries = checkkey(country, countries, month, day, case, death)
            continents = checkkey(continent, continents, month, day, case, death)
        else:  
            continue              
    file.close()
    
    return countries, continents, header2

# change the case and death data to int, empty data and non-numeric data set to 0.
def case_lst(lst):
    case = []
    for item in lst:
        if item and item.isdigit():
            case.append(int(item))
        if item == False or item.isdigit() == False:
            case.append(0)
    return case

def count_day(lst2, avg):  # count days/values greater than the average.
    count = 0
    for item in lst2:
        if item > avg:
            count+=1
    return count
    
def countDay1(avg, lst):  # count values greater than average for continent
    lst2 = case_lst(lst) 
    count = count_day(lst2, avg)
    return count

def countDay(lst):          # count days for country 
    lst2 = case_lst(lst)
    avg = sum(lst2)/(len(lst2) or 1)
    count = count_day(lst2, avg)
    return count

def findSum_lst1(dic): # continent dic
    dic2 = {}
    days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for key in dic.keys():
        for i in range (12):
            sumcase, sumdeath = findSum(dic.get(key)[i].get('case')), findSum(dic.get(key)[i].get('death'))
            avgCase, avgDeath = sumcase/days[i], sumdeath/days[i]
            if key in dic2:
                dic2[key][0].append(sumcase)
                dic2[key][1].append(sumdeath)
                dic2[key][2].append(countDay1(avgCase, dic.get(key)[i].get('case')))
                dic2[key][3].append(countDay1(avgDeath, dic.get(key)[i].get('death')))
                
            else:
                dic2[key]=[[] for i in range (4)]
                dic2[key][0].append(sumcase)
                dic2[key][1].append(sumdeath)
                dic2[key][2].append(countDay1(avgCase, dic.get(key)[i].get('case')))
                dic2[key][3].append(countDay1(avgDeath, dic.get(key)[i].get('death')))
    return dic2

def findSum_lst(dic):   # country dic 
    dic2 = {}
    for key in dic.keys():
        for i in range (12):
            if key in dic2:
                dic2[key][0].append(findSum(dic.get(key)[i].get('case')))
                dic2[key][1].append(findSum(dic.get(key)[i].get('death')))
                dic2[key][2].append(countDay(dic.get(key)[i].get('case')))
                dic2[key][3].append(countDay(dic.get(key)[i].get('death')))
                
            else:
                dic2[key]=[[] for i in range (4)]
                dic2[key][0].append(findSum(dic.get(key)[i].get('case')))
                dic2[key][1].append(findSum(dic.get(key)[i].get('death')))
                dic2[key][2].append(countDay(dic.get(key)[i].get('case')))
                dic2[key][3].append(countDay(dic.get(key)[i].get('death')))
    return dic2

def findSum(lst):           # sum of case and death list
    lst2 = case_lst(lst) 
    return sum(lst2)

def checkkey(keys, dic, month, day, case, death):  # nested dict ( key == continent or country) 
    '''helper funciton to read_file'''
    if keys in dic:
        dic.get(keys)[month-1].get("day").append(day)    # keep the days in the dic just in case 
        dic.get(keys)[month-1].get("case").append(case)
        dic.get(keys)[month-1].get("death").append(death)
    else:
        dic[keys]=[{"day": [], "case": [], "death":[]} for i in range (12)]  # create 12 lists each with 3 keys with a list of values 
        dic.get(keys)[month-1].get("day").append(day)
        dic.get(keys)[month-1].get("case").append(case)
        dic.get(keys)[month-1].get("death").append(death)
    
    return dic

def parseLine(line, headerInd):           # get the data we want for each line from the file based on the index of header column
    '''helper funciton to read_file'''    # make all text data to lower case 
    line = line.strip().split(',')
    continent, country = line[headerInd[0]].strip().lower(), line[headerInd[1]].strip().lower()  
    date, month, day = line[headerInd[2]].strip(), parseDate(line[headerInd[2]])[1], parseDate(line[headerInd[2]])[0]
    case, death = line[headerInd[3]], line[headerInd[4]]
    return continent, country, case, death, month, day, date

def sortDate(date):  
    '''helper funciton to read_file'''
    date = date.split('/')
    for item in date:
        if item.isdigit() == False and len(date) != 3:  # find iff date is in the right format or not 
            return False
    return True

def parseDate(date):
    '''helper funciton to read_file'''
    date = date.split('/')
    date = [int(item.strip()) for item in date]  # change date to int 
    return (date[0], date[1])                    # return only the day and month data
      
def findcol(header,requiredCol):
    '''helper funciton to read_file'''
    emuHeader = {item: idx for idx, item in enumerate(header)}  # emumerate header to get index of header
    headerInd = [emuHeader.get(item) for item in requiredCol]
    for x in headerInd:
        if x == None:
            return []                            # return empty list iff any of the required column is missing 
    return headerInd                             # return the index of each required column
