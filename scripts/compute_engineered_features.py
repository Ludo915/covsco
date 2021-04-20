import pandas as pd
from datetime import timedelta
from datetime import datetime
from operator import itemgetter
import time
import itertools
import statistics
itertools.imap = lambda *args, **kwargs: list(map(*args, **kwargs))

class Compute_Engineered_Features_for_df:

    def __init__(self):
        self.file_name = None
        self.data = None
        self.pm25tuple = None
        self.no2tuple = None
        self.o3tuple = None
        self.pm10tuple = None
        self.cotuple = None
        self.tothospituple = None
        self.newhospituple = None
        self.newreanim = None
        self.dicpm25 = None
        self.dicno2 = None
        self.dico3 = None
        self.dicpm10 = None
        self.dicco = None
        self.dictothospi = None
        self.dicnewhospi = None
        self.dicnewreanim = None

    def max_normalize(self, x):
        return (x - x.min()) / (x.max() - x.min())

    def get_data(self):
        print("Computing then engineered features: 1M Trailing Maximal Pollution Concentrations (1M-TMPCs),1M Trailing Average Pollution Concentrations (1M-TAPCs), 7D Trailing Average Pollution Concentrations (7D-TAPCs) and the previous day's total hospitalizations...")
        self.file_name = '../data/train/all_data_merged/fr/Enriched_Covid_history_data.csv'
        self.data = pd.read_csv(self.file_name)
        return None

    def max_normalize_data(self):
        self.data["normpm25"]=self.max_normalize(self.data["pm25"])
        self.data["normno2"]=self.max_normalize(self.data["no2"])
        self.data["normo3"]=self.max_normalize(self.data["o3"])
        self.data["normpm10"]=self.max_normalize(self.data["pm10"])
        self.data["normco"]=self.max_normalize(self.data["co"])
        self.data["time"]=pd.to_datetime(self.data["time"])
        return None
    
    def compute_dictionnaries(self):

        self.pm25tuple = (self.data['numero'], self.data['time'], self.data["pm25"], self.data["normpm25"] )
        self.no2tuple = (self.data['numero'], self.data['time'], self.data["no2"], self.data["normno2"])
        self.o3tuple = (self.data['numero'], self.data['time'], self.data["o3"], self.data["normo3"])
        self.pm10tuple = (self.data['numero'], self.data['time'],self.data["pm10"], self.data["normpm10"])
        self.cotuple = (self.data['numero'], self.data['time'], self.data["co"], self.data["normco"])
        self.tothospituple = (self.data['numero'], self.data['time'], self.data["hospi"])
        self.newhospituple = (self.data['numero'], self.data['time'], self.data["newhospi"])
        self.newreanimtuple = (self.data['numero'], self.data['time'], self.data["newreanim"])

        self.dicpm25 = {(i, j) : (k,l) for (i, j, k, l) in zip(*self.pm25tuple)}
        self.dicno2 = {(i, j) : (k,l)  for (i, j, k, l) in zip(*self.no2tuple)}
        self.dico3 = {(i, j) : (k,l)  for (i, j, k, l) in zip(*self.o3tuple)}
        self.dicpm10 = {(i, j) : (k,l)  for (i, j, k, l) in zip(*self.pm10tuple)}
        self.dicco = {(i, j) : (k,l) for (i, j, k, l) in zip(*self.cotuple)}
        self.dictothospi = {(i, j) : k for (i, j, k) in zip(*self.tothospituple)}
        self.dicnewhospi = {(i, j) : k for (i, j, k) in zip(*self.newhospituple)}
        self.dicnewreanim = {(i, j) : k for (i, j, k) in zip(*self.newreanimtuple)}

        return None

    def compute_Engineered_Features(self, row):
        referencedate = self.data["time"].min()
        datalist = []
        datalist2 = []
        datalist3 = []
        datalist4 = []
        datalist5 = []
        datalist6 = []

        date = row['time'] - pd.Timedelta("30 days")
        date2 = row['time'] - pd.Timedelta("6 days")
        date3 = row['time'] - pd.Timedelta("2 days") 
        dateprevday = row['time'] - pd.Timedelta("1 days")

        dates = pd.date_range(start = date, periods=31).tolist()
        dates2 = pd.date_range(start = date2, periods=7).tolist()
        dates3 = pd.date_range(start = date3, periods = 3).tolist()

        if (dateprevday < referencedate):
            prevdaytothospi = "NaN"
        else:
            prevdaytothospi = self.dictothospi[(row['numero'], dateprevday)] 

        for valuedate in dates:
            if(valuedate < referencedate):
                datalist.append((('NaN','Nan'),('NaN','Nan'),('NaN','Nan'),('NaN','Nan'),('NaN','Nan')))
            
            else:
                datalist.append((self.dicpm25[(row['numero'], pd.to_datetime(str(valuedate)))], \
                                self.dicno2[(row['numero'], pd.to_datetime(str(valuedate)))], \
                                self.dico3[(row['numero'], pd.to_datetime(str(valuedate)))], \
                                self.dicpm10[(row['numero'], pd.to_datetime(str(valuedate)))],\
                                self.dicco[(row['numero'], pd.to_datetime(str(valuedate)))]))


        for valuedate in dates2:
            if(valuedate < referencedate):
                datalist2.append((('NaN','Nan'),('NaN','Nan'),('NaN','Nan'),('NaN','Nan'),('NaN','Nan')))
                datalist3.append('NaN')
                datalist4.append("NaN")
            
            else:
                datalist2.append((self.dicpm25[(row['numero'], pd.to_datetime(str(valuedate)))], \
                                self.dicno2[(row['numero'], pd.to_datetime(str(valuedate)))], \
                                self.dico3[(row['numero'], pd.to_datetime(str(valuedate)))], \
                                self.dicpm10[(row['numero'], pd.to_datetime(str(valuedate)))],\
                                self.dicco[(row['numero'], pd.to_datetime(str(valuedate)))]))
                datalist3.append(self.dicnewhospi[(row['numero'], pd.to_datetime(str(valuedate)))])
                datalist4.append(self.dicnewreanim[(row['numero'], pd.to_datetime(str(valuedate)))])
        
        for valuedate in dates3:
            if(valuedate < referencedate):
                datalist5.append('NaN')
                datalist6.append("NaN")
            
            else:
                datalist5.append(self.dicnewhospi[(row['numero'], pd.to_datetime(str(valuedate)))])
                datalist6.append(self.dicnewreanim[(row['numero'], pd.to_datetime(str(valuedate)))])

        
        cleanedList = [((float(x),float(a)),(float(y),float(b)),(float(z),float(c)),(float(w),float(d)),(float(v),float(e))) \
            for ((x,a),(y,b),(z,c),(w,d),(v,e)) in datalist \
                if ((str(x),str(a)),(str(y),str(b)),(str(z),str(c)),(str(w),str(d)),(str(v),str(e))) \
                    != (('NaN','Nan'),('NaN','Nan'),('NaN','Nan'),('NaN','Nan'),('NaN','Nan'))]

        cleanedList2 = [((float(x),float(a)),(float(y),float(b)),(float(z),float(c)),(float(w),float(d)),(float(v),float(e))) \
            for ((x,a),(y,b),(z,c),(w,d), (v,e)) in datalist2 \
                if ((str(x),str(a)),(str(y),str(b)),(str(z),str(c)),(str(w),str(d)),(str(v),str(e))) \
                    != (('NaN','Nan'),('NaN','Nan'),('NaN','Nan'),('NaN','Nan'),('NaN','Nan'))]

        cleanedList3 = [int(x) for x in datalist3 if str(x) != 'NaN']
        cleanedList4 = [int(x) for x in datalist4 if str(x) != 'NaN']
        cleanedList5 = [int(x) for x in datalist5 if str(x) != 'NaN']
        cleanedList6 = [int(x) for x in datalist6 if str(x) != 'NaN']

        avg = [tuple(sum(j)/len(cleanedList) for j in zip(*i)) for i in zip(*cleanedList)]
        avg2 = [tuple(sum(j)/len(cleanedList2) for j in zip(*i)) for i in zip(*cleanedList2)]
        avg3 = statistics.mean(cleanedList3)
        avg4 = statistics.mean(cleanedList4)
        avg5 = statistics.mean(cleanedList5)
        avg6 = statistics.mean(cleanedList6)
        
        return (max(cleanedList,key=itemgetter(0))[0][0],\
                max(cleanedList,key=itemgetter(1))[1][0],\
                max(cleanedList,key=itemgetter(2))[2][0],\
                max(cleanedList,key=itemgetter(3))[3][0],\
                max(cleanedList,key=itemgetter(4))[4][0],\
                max(cleanedList,key=itemgetter(0))[0][1],\
                max(cleanedList,key=itemgetter(1))[1][1],\
                max(cleanedList,key=itemgetter(2))[2][1],\
                max(cleanedList,key=itemgetter(3))[3][1],\
                max(cleanedList,key=itemgetter(4))[4][1],\
                prevdaytothospi,\
                avg[0][0],\
                avg[1][0],\
                avg[2][0],\
                avg[3][0],\
                avg[4][0],\
                avg2[0][0],\
                avg2[1][0],\
                avg2[2][0],\
                avg2[3][0],\
                avg2[4][0],
                avg[0][1],\
                avg[1][1],\
                avg[2][1],\
                avg[3][1],\
                avg[4][1],\
                avg2[0][1],\
                avg2[1][1],\
                avg2[2][1],\
                avg2[3][1],\
                avg2[4][1],\
                avg3,\
                avg4,\
                avg5,\
                avg6)
                
    def compute_Engineered_features_assign_to_df(self):
        self.data[['1MMaxpm25','1MMaxno2','1MMaxo3','1MMaxpm10','1MMaxco',\
                '1MMaxnormpm25','1MMaxnormno2','1MMaxnormo3','1MMaxnormpm10','1MMaxnormco', 
                'hospiprevday',
                'pm257davg','no27davg','o37davg', 'pm107davg','co7davg',\
                'pm251Mavg','no21Mavg','o31Mavg','pm101Mavg','co1Mavg',\
                "normpm257davg","normno27davg","normo37davg","normpm107davg","normco7davg",\
                "normpm251Mavg","normno21Mavg","normo31Mavg","normpm101Mavg","normco1Mavg","newhospi7davg","newreanim7davg","newhospi3davg","newreanim3davg"]] \
                    = self.data.apply(self.compute_Engineered_Features, axis=1).apply(pd.Series)
        print("\n")
        print(self.data)
        print("\n")
        self.data.to_csv('../data/train/all_data_merged/fr/Enriched_Covid_history_data.csv', index = False)
        return None

if __name__ == '__main__':
    Engineered_Features = Compute_Engineered_Features_for_df()
    Engineered_Features.get_data()
    Engineered_Features.max_normalize_data()
    Engineered_Features.compute_dictionnaries()
    Engineered_Features.compute_Engineered_features_assign_to_df()

   

    
        



