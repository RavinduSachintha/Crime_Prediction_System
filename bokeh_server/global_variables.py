import os
from bokeh.io import curdoc
from data import DataFile
from predictor import Predictor

curr_doc = curdoc()

upload_filename = os.path.join(os.path.dirname(__file__), 'uploads', 'SL_CrimeDataSet.xlsx')

datafile = DataFile()

# prediction preperation
predictor = Predictor(datafile)
predictor.pre_process_data()
predictor.fit()


def static_data(area):
    if area == 'Anuradapura':
        predictor.selected['popul_den'] = 129
        predictor.selected['education_lvl'] = 67.8602678871912
        predictor.selected['economy'] = 58326
        predictor.selected['alcohol_drug_usage'] = 2368
    if area == 'Badulla':
        predictor.selected['popul_den'] = 285
        predictor.selected['education_lvl'] = 67.814777761898
        predictor.selected['economy'] = 53236
        predictor.selected['alcohol_drug_usage'] = 2074
    if area == 'Bandarawela':
        predictor.selected['popul_den'] = 922
        predictor.selected['education_lvl'] = 67.814777761898
        predictor.selected['economy'] = 53236
        predictor.selected['alcohol_drug_usage'] = 2074
    if area == 'Colombo (N)':
        predictor.selected['popul_den'] = 3300
        predictor.selected['education_lvl'] = 67
        predictor.selected['economy'] = 104581
        predictor.selected['alcohol_drug_usage'] = 39132
    if area == 'Colombo (S)':
        predictor.selected['popul_den'] = 3300
        predictor.selected['education_lvl'] = 68
        predictor.selected['economy'] = 104581
        predictor.selected['alcohol_drug_usage'] = 39132
    if area == 'Colombo ( C )':
        predictor.selected['popul_den'] = 3300
        predictor.selected['education_lvl'] = 68
        predictor.selected['economy'] = 104581
        predictor.selected['alcohol_drug_usage'] = 39132
    if area == 'Galle':
        predictor.selected['popul_den'] = 643.7
        predictor.selected['education_lvl'] = 76.6740250183959
        predictor.selected['economy'] = 63092
        predictor.selected['alcohol_drug_usage'] = 1476
    if area == 'Gampaha':
        predictor.selected['popul_den'] = 1662
        predictor.selected['education_lvl'] = 87.978546328833
        predictor.selected['economy'] = 72834
        predictor.selected['alcohol_drug_usage'] = 17036
    if area == 'Hatton':
        predictor.selected['popul_den'] = 492
        predictor.selected['education_lvl'] = 78.1803755620206
        predictor.selected['economy'] = 46517
        predictor.selected['alcohol_drug_usage'] = 899
    if area == 'Nugegoda':
        predictor.selected['popul_den'] = 3300
        predictor.selected['education_lvl'] = 70
        predictor.selected['economy'] = 104581
        predictor.selected['alcohol_drug_usage'] = 39132
    if area == 'Nuwaraeliya':
        predictor.selected['popul_den'] = 408.8
        predictor.selected['education_lvl'] = 78.1803755620206
        predictor.selected['economy'] = 46517
        predictor.selected['alcohol_drug_usage'] = 899
    if area == 'Panadura':
        predictor.selected['popul_den'] = 4143
        predictor.selected['education_lvl'] = 70.4043511702011
        predictor.selected['economy'] = 69171
        predictor.selected['alcohol_drug_usage'] = 4338
