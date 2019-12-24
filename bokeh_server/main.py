from charts import Charts
from global_variables import datafile, predictor, curr_doc

# data initializing
table_col_titles = datafile.get_table_column_titles()
table_data = datafile.get_table_data(50)

# charts initializing
charts = Charts(datafile.sheet)
uploading_section = charts.file_upload()
islandwide_charts = charts.get_islandwide_charts()
localwise_charts = charts.get_localwise_charts()

# predicting form
prediction_controls = predictor.form_layout()
prediction_output = predictor.prediction_output()
map_viewer = predictor.map_viewer()

# add variables and models to current document
curr_doc.template_variables['col_titles'] = table_col_titles
curr_doc.template_variables['data'] = table_data
curr_doc.add_root(uploading_section)
curr_doc.add_root(islandwide_charts)
curr_doc.add_root(localwise_charts)
curr_doc.add_root(prediction_controls)
curr_doc.add_root(prediction_output)
curr_doc.add_root(map_viewer)
