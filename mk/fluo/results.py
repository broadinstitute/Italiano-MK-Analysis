import os

import pandas as pd

from utils import tools
from utils.results import ResultsImage, ResultsObject

class FluoImage(ResultsImage):
    def __init__(self, path, csv, time):
        super(FluoImage, self).__init__(path,csv,time)

    def analyze(self):
        # Set index to perform lamda calculations
        x = self.cols(self._df, ['Metadata_Well','Metadata_Site','Metadata_Time', 'ImageNumber', 'FileName_phase',
            'Count_MaskedFluoMK','Count_MaskedFluoPPLT','Count_fluo_obj','Count_mkobj',
            'Count_ppltobj',]).set_index(['Metadata_Well','Metadata_Site','Metadata_Time'])

        # x['Pct_Fluo_Pos'] = x.apply(lambda row: self.pct(row['Count_MaskedFluoPPLT'], row['Count_MaskedFluoMK']), axis=1)
        res = x.reset_index()

        res = self.sort_df(res)
        res2 = res.set_index('Metadata_Well_Site')
        res2.to_csv(self.path + os.sep + 'ImageResults.csv')

        if self.time is None:
            pass
        else:
            # pfp = self.format_results(res2, self.time, 'Pct_Fluo_Pos', self.path,'Pct_Fluo_Pos.csv')
            mfm = self.format_results(res2, self.time, 'Count_MaskedFluoMK', self.path, 'Count_MaskedFluoMK.csv')
            mfp = self.format_results(res2, self.time, 'Count_MaskedFluoPPLT', self.path, 'Count_MaskedFluoPPLT.csv')            

            # self.plot(pfp, 'line', tools.create_folder(self.path,'Pct_Fluo_Pos'))
            self.plot(mfm, 'barh', tools.create_folder(self.path,'Count_MaskedFluoMK'))
            self.plot(mfp, 'barh', tools.create_folder(self.path,'Count_MaskedFluoPPLT'))

        return res2

class FluoObject(ResultsObject):
    def __init__(self, path, csv, time, object_name):
        super(FluoObject, self).__init__(path, csv, time, object_name)

    # @staticmethod
    # def plot(df, graph_type, output_folder):
    #     # Assumes Metadata_Well_Site_Time is the index
    #     for n in list(df.index.unique()):
    #         x = df.loc[n].reset_index()
    #         if not os.path.exists(output_folder + os.sep + n + '.png'):
    #             fig = x.plot(kind=graph_type, x='ObjectNumber', y='Intensity_IntegratedIntensity_fluo').get_figure()
    #             fig.savefig(output_folder + os.sep + n + '.png')
    #         else:
    #             pass

    def analyze(self):
        x = self.cols(self._df, ['Metadata_Well','Metadata_Site','Metadata_Time','ImageNumber','ObjectNumber',
            'Location_Center_X','Location_Center_Y','Location_CenterMassIntensity_X_fluo','Location_CenterMassIntensity_Y_fluo',
            'Intensity_IntegratedIntensity_fluo'])

        res = self.sort_df(x)
        res2 = res.set_index('Metadata_Well_Site_Time_Obj')
        res2.to_csv(self.path + os.sep + self.object_name + 'Results.csv')

        # cmprot = res2.set_index('Metadata_Well_Site_Time')
        # self.plot(cmprot,'barh', tools.create_folder(self.path,'FluoObject_Intensities' + '_' + object_name))

        return res2

