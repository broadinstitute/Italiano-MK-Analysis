import os, sys
from shutil import move

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

from util import tools

# Iterate through the rows by timepoint, to split up the long list of results.
def iter_time(df, time, column):
    res = pd.DataFrame()
    for i in range(0, len(df), time):
        slc = df.iloc[i:i+time, df.columns.get_level_values(0).isin([column])]
        slc = slc.reset_index(drop=True)
        res = pd.concat([res,slc], axis=1, ignore_index=True)
    return res

def heatmap(x,y,z,output):
    temp = y.join(x)
    hm = temp.join(z)
    plt.figure(figsize=(26,16))
    hm = sns.heatmap(hm.corr(),annot=True,linewidth=1,cmap='coolwarm').get_figure()
    hm.savefig(output + 'heatmap.png')

# Process csvs in a folder through dataframes
class ResultsDF:
    def __init__(self, path, csv, time):
        self.path = path
        self.csv = csv
        self.time = time
        self._df = pd.DataFrame()

    @property
    def df(self):
        file = self.open_csv(self.path, self.csv)
        self._df = pd.read_csv(file)  
        return self._df 

    # Open excel csv by passing the path and csv_name (str)
    @staticmethod
    def open_csv(path, csv):
        try:
            file = open(os.path.join(path, csv))
            return file
        except FileNotFoundError:
            sys.exit(f">>> {csv} not found. Check path & csv name.")

    # Select specific columns by passing a list of column names. ie: ['CountMK','CountPplt', ...]
    @staticmethod
    def cols(df, cols_list):
        frame = df[cols_list]
        return frame

    # Calculate percentage of 2 values, if one or both don't exist, return 0.00
    @staticmethod
    def pct(numerator, denominator):
        try:
            return ((numerator/(denominator)) * 100) 
        except ZeroDivisionError:
            return float(0.00)

    # Check if value exists, otherwise return 0.00
    @staticmethod
    def value(num):
        try:
            return num
        except ValueError:
            return float(0.00)

    # Sort dataframe alphanumerically by *FileName_phase*. Assumes there is no index.
    @staticmethod
    def sort_df(df):
        if df.empty:
            pass
        else:
            df["Metadata_Well_Site"] = df["Metadata_Well"].map(str) + '_' + df["Metadata_Site"].map(str) 
            df["Metadata_Well_Site_Time"] = df["Metadata_Well"].map(str) + '_' + df["Metadata_Site"].map(str) + '_' + df["Metadata_Time"].map(str)
            frame = tools.sort_dataframe(df, 'Metadata_Well_Site_Time')
            frame = frame.set_index("Metadata_Well_Site")
        return frame

    # Iterate over dataframe rows using time (slices per stack) and extract data (per well/site/time)
    @staticmethod
    def format_results(df, time, column, output_folder, csv_name):
        res = iter_time(df, time, column)
        res.columns = list(df.index.unique())
        res['Timepoint'] = list(range(1, (time+1)))
        res = res.set_index('Timepoint')
        res = res[tools.alphanumeric_sort(res.columns)]
        res.to_csv(os.path.join(output_folder, csv_name))
        return res

    @staticmethod
    def plot(df, graph_type, output_folder):
        # Assumes Timepoint index set in format_results is still in place.
        cols = list(df)
        x = df.reset_index()
        for n in cols:
            if not os.path.exists(output_folder + os.sep + n + '.png'):
                fig = x.plot(kind=graph_type, x='Timepoint', y=n).get_figure()
                fig.savefig(output_folder + os.sep + n + '.png')
            else:
                pass

class ResultsImage(ResultsDF):
    def __init__(self, path, csv, time):
        super(ResultsImage, self).__init__(path,csv,time)

    @staticmethod
    def image_means(df):
        x = df.reset_index()
        x = x.drop(['ImageNumber','FileName_phase','Metadata_Well_Site',
        'Metadata_Well_Site_Time','Metadata_Well','Metadata_Site'],axis=1)
        x = x.groupby('Metadata_Time').mean()
        return x

    def analyze(self):
        # Set index to perform lamda calculations
        x = self.cols(self._df, ['Metadata_Well','Metadata_Site','Metadata_Time', 'ImageNumber', 'FileName_phase',
            'AreaOccupied_AreaOccupied_mk_filter', 'AreaOccupied_AreaOccupied_pplt_filter', 'AreaOccupied_TotalArea_mk_filter', 
            'AreaOccupied_TotalArea_pplt_filter','Count_mk_filter','Count_pplt_filter'])

        x['Pct_Pplt_Prod'] = x.apply(lambda row: self.pct(row['Count_pplt_filter'], row['Count_mk_filter']), axis=1)
        x['Area_MK'] = x.apply(lambda row: self.value(row['AreaOccupied_AreaOccupied_mk_filter']), axis=1)
        x['Area_Pplt'] = x.apply(lambda row: self.value(row['AreaOccupied_AreaOccupied_pplt_filter']), axis=1)

        # Drop duplicate Area cols
        x = x.drop(['AreaOccupied_AreaOccupied_mk_filter','AreaOccupied_AreaOccupied_pplt_filter',
        'AreaOccupied_TotalArea_mk_filter','AreaOccupied_TotalArea_pplt_filter'],axis=1)
        
        x = self.sort_df(x)
        x.to_csv(self.path + os.sep + 'ImageResults.csv')

        if self.time is None:
            pass
        else:
            cm = self.format_results(x, self.time, 'Count_mk_filter', self.path,'MKCount.csv')
            cp = self.format_results(x, self.time, 'Count_pplt_filter', self.path, 'PPLTCount.csv')
            ppp = self.format_results(x, self.time, 'Pct_Pplt_Prod', self.path, 'PctPPLTProd.csv')         
            am = self.format_results(x, self.time, 'Area_MK', self.path, 'MKArea.csv')
            ap = self.format_results(x, self.time, 'Area_Pplt', self.path, 'PPLTArea.csv')

            self.plot(cm, 'barh', tools.create_folder(self.path,'MKCount'))
            self.plot(cp, 'barh', tools.create_folder(self.path,'PPLTCount'))
            self.plot(ppp, 'line', tools.create_folder(self.path,'PctPPLTProd'))
            self.plot(am, 'line', tools.create_folder(self.path,'MKArea'))
            self.plot(ap, 'line', tools.create_folder(self.path,'PPLTArea'))

        x = self.image_means(x)

        return x
        
# results_mk_filter & results_pplt_filter (CellProfiler MeasureObjectArea module)
class ResultsObject(ResultsDF):
    def __init__(self, path, csv, time, object_name):
        super(ResultsObject, self).__init__(path,csv,time)
        self.object_name = object_name

    @staticmethod
    def object_means(df,object_name):
        x = df.reset_index()
        x = x.drop(['Metadata_Well_Site','Metadata_Well_Site_Time_Obj','Metadata_Well','Metadata_Site',
        'ImageNumber','ObjectNumber','Location_Center_X','Location_Center_Y','AreaShape_Center_X',
        'AreaShape_Center_Y'],axis=1)
        x = x.groupby('Metadata_Time').mean()
        x.columns = [str(col) + '_' + object_name for col in x.columns]

        return x
        
    @staticmethod
    def sort_df(df):
        if df.empty:
            pass
        else:
            df["Metadata_Well_Site"] = df["Metadata_Well"].map(str) + '_' + df["Metadata_Site"].map(str) 
            # df["Metadata_Well_Site_Time"] = df["Metadata_Well"].map(str) + '_' + df["Metadata_Site"].map(str) + '_' + df["Metadata_Time"].map(str)
            df["Metadata_Well_Site_Time_Obj"] = df["Metadata_Well"].map(str) + '_' + df["Metadata_Site"].map(str) + '_' + df["Metadata_Time"].map(str) + '_' + df["ObjectNumber"].map(str)
            frame = tools.sort_dataframe(df, 'Metadata_Well_Site_Time_Obj')
            frame = frame.set_index("Metadata_Well_Site")
        return frame

    def analyze(self):
        x = self.cols(self._df, ['Metadata_Well','Metadata_Site','Metadata_Time','ImageNumber','ObjectNumber','Location_Center_X',
            'Location_Center_Y','AreaShape_Center_X','AreaShape_Center_Y','AreaShape_Area','AreaShape_Orientation','AreaShape_Perimeter',
            'AreaShape_Solidity','AreaShape_Compactness','AreaShape_Eccentricity','AreaShape_Extent','AreaShape_FormFactor',
            'AreaShape_MajorAxisLength','AreaShape_MinorAxisLength','AreaShape_MaxFeretDiameter','AreaShape_MinFeretDiameter',
            'AreaShape_MaximumRadius','AreaShape_MeanRadius','AreaShape_MedianRadius'])
        x = self.sort_df(x)
        x.to_csv(self.path + os.sep + self.object_name + 'Results.csv')

        x = self.object_means(x,self.object_name)

        return x