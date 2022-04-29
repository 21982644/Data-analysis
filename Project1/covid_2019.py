'''This program which analyses data from a file. If only one country and statistics are entered,the program
return a list of minimum, maximum, average, standard deviation of each month in the order from Jan to Dec.
If two countries and correlation are entered, the program return the corelation between the two countries of
the 4 lists (minimum, maximum, average, standard deviation).'''

# main funciton return differnt set of data based on the stat (stat or corre) and 1 or 2 countries entered. 

def main(csv,country,stat):
    
    if type(country) == str and stat.lower().strip() =="statistics": 
        country_list = find_country(csv,country) # 1 list stored in the variable
        mn1,mx1,avg,std = find_mnmxavg_std(country_list)
        avg1 = [round(num, 4) for num in avg] #round avg to 4 decimal places
        std1 = [round(num, 4) for num in std] #round std to 4 decimal places
        return mn1,mx1,avg1,std1
    
    elif type(country) == list and len(country) == 2 and stat.lower().strip() =="correlation":
        country0,country1 = find_country2(csv,country) # 2 lists stored in two variables
        mn2 = correlComini(country0, country1) 
        mx2 = correlComaxi(country0, country1)
        avg2 = correlComavg(country0, country1)
        std2 = correlComstd(country0, country1)
        return mn2, mx2, avg2, std2
   
    else:
        return None

# Function split line by comma and only return country, month and new_cases.

def pharseLine(fileline):
    tmp = fileline.split(",")
    return tmp[2].lower().strip(), pharseMonth(tmp[3].strip()), int(tmp[4].strip())

# Function only return the month of the date and convert to int.
    
def pharseMonth(date):
    return int(date.split("/")[1]) 

# Read the file and return list containing contry, month and new_cases

def read_file (filename):
    file = open(filename, 'r')
    next(file)  #skip the header
    allDataList = []
    for line in file:
        location, month, new_cases = pharseLine(line)
        allDataList.append(location)
        allDataList.append(month)
        allDataList.append(new_cases)
        
    file.close()
    
    return allDataList

# return a list for one country.

def find_country(csv,country):
    allList = read_file(csv)
    case_list = []
    for i in range(0,len(allList),3):
        if allList[i] == country.lower().strip():
            case_list.append(allList[i+1])
            case_list.append(allList[i+2])
    
    return case_list

# Function that return two list for two country (if country is a list).

def find_country2(csv,country):
    allList = read_file(csv)
    country0 = []
    country1 = []
    for i in range(0,len(allList),3):
        if country[0].lower().strip() == allList[i]:
            country0.append(allList[i+1])
            country0.append(allList[i+2])
        if country[1].lower().strip() == allList[i]:
            country1.append(allList[i+1])
            country1.append(allList[i+2])
    
    return country0,country1
 
# Function that sort new_cases data in order from Jan to Dec          

def sort_Data(countryList):  
    insertSubIndex = 0
    date_caseList = [[] for _ in range(12)]  # create a list containing 12 empty lsit 
    for i in range(0,len(countryList),2):  # add month data to date_caseLis in the order of 1-12
        insertSubIndex = countryList[i]-1
        date_caseList[insertSubIndex].append(countryList[i+1]) 
    
    return date_caseList
        
# find min, max ,average,standard deviation of a given list                  

def find_mnmxavg_std(date_caseList): 
    
    date_caseList = sort_Data(date_caseList)  # call the sort_Data() to sort data and store the returned value in a variable
    
    mnx = []  # create empty list of mn, max, avg, std
    mxx = []
    avgx = []
    stdx = []
    
    for lst in date_caseList:   # find the max, min, avg
        maxi = max((i for i in lst if i > 0), default=0) # min>0 and if list is empty, min = 0
        mini = min((i for i in lst if i > 0), default=0) # maz>0 and if list is empty, max = 0
        avge = sum(lst)/(len(lst) or 1)  # sum of a list and if list is empty, sum = 0
        mnx.append(mini)
        mxx.append(maxi)
        avgx.append(avge)
        
            
    for lst in date_caseList:  #find the std
        tmpvar = 0
        tmpstd = 0.0
        if len(lst) == 0: # if list is empty, std = 0
            tmpstd = 0
        else:
            for k in range (len(lst)):
                tmpvar += pow(lst[k]-((sum(lst)/(len(lst)))),2)/len(lst)
                tmpstd = tmpvar**0.5
        stdx.append(tmpstd)

    return mnx,mxx,avgx,stdx

# calculate correlation of 2 countries

def mean(counList):  # Calculate the mean of a list (list is not empty)
    total = 0.0
    for a in counList:
        total += float(a)
        avge = total/len(counList)
    return avge

def standDev(counList): # Calculate the standDev of a list (list is not empty)
    
    listMean = mean(counList)
    dev = 0.0
    for i in range(len(counList)):
        dev += (counList[i]-listMean)**2
    dev = dev**0.5
    return dev

def correlComini(country1, country2): # Calculate the correlation of min.
    
    mnx1 = find_mnmxavg_std(country1)[0] # Call find_mnmxavg_std() and only want the first returned value
    mnx2 = find_mnmxavg_std(country2)[0] 
    meanmnx1 = mean(mnx1)                # average of a list by calling the mean()
    meanmnx2 = mean(mnx2)                
    standDevmnx1 = standDev(mnx1)        # average of a list by calling the standDev()
    standDevmnx2 = standDev(mnx2)  
        
    # numerator
    cNum = 0
    
    for i in range(len(mnx1)):           #Caluculate the correlation according to formula 
        cNum += (mnx1[i]-meanmnx1)*(mnx2[i]-meanmnx2)

    # denominator
    cDen = standDevmnx1 * standDevmnx2
    mn =  cNum/cDen
    mn = round(mn,4) #round the 4 decimal places
    
    return mn

def correlComaxi(country1, country2): # Calculate the correlation of max.
    
    max1 = find_mnmxavg_std(country1)[1] # Call find_mnmxavg_std() and only want the 2nd returned value
    max2 = find_mnmxavg_std(country2)[1]
    meanmax1 = mean(max1)
    meanmax2 = mean(max2)
    standDevmax1 = standDev(max1)
    standDevmax2 = standDev(max2)  
                
    # numerator of the corre formula
    cNum = 0.0
    
    for i in range(len(max1)):
        cNum += (max1[i]-meanmax1)*(max2[i]-meanmax2)

    # denominator the corre formula
    cDen = standDevmax1 * standDevmax2

    mx =  cNum/cDen
    mx = round(mx,4)
    
    return mx
    

def correlComavg(country1, country2): # Calculate the correlation of average.
    
    avg1 = find_mnmxavg_std(country1)[2] # Call find_mnmxavg_std() and only want the 3rd returned value
    avg2 = find_mnmxavg_std(country2)[2]
    meanavg1 = mean(avg1)
    meanavg2 = mean(avg2)
    standDevavg1 = standDev(avg1)
    standDevavg2 = standDev(avg2)  
              
    # numerator
    cNum = 0.0
    
    for i in range(len(avg1)):
        cNum += (avg1[i]-meanavg1)*(avg2[i]-meanavg2)

    # denominator
    cDen = standDevavg1*standDevavg2

    avg =  cNum/cDen
    avg = round(avg,4)
    return avg

def correlComstd(country1, country2): # Calculate the correlation of standard deviation.
    
    std1 = find_mnmxavg_std(country1)[3] # Call find_mnmxavg_std() and only want the last returned value
    std2 = find_mnmxavg_std(country2)[3]
    meanstd1 = mean(std1)
    meanstd2 = mean(std2)
    standDevstd1 = standDev(std1)
    standDevstd2 = standDev(std2)
    
    # numerator
    cNum = 0.0
    
    for i in range(len(std1)):
        cNum += (std1[i]-meanstd1)*(std2[i]-meanstd2)

    # denominator
    cDen =  standDevstd1 * standDevstd2

    std =  cNum/cDen
    std = round(std,4)
    
    return std
