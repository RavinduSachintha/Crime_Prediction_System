import base64
import numbers
from math import pi

import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, FileInput, Button, CustomJS, Panel, Tabs
from bokeh.palettes import Category20c, Category20b, Accent7, Reds6
from bokeh.plotting import figure
from bokeh.transform import cumsum

from data import DataFile
from global_variables import predictor, upload_filename
import global_variables


class Charts:

    def __init__(self, sheet):
        self.sheet = sheet
        self.datafile = DataFile()

    # Crime counts in major Cities - 2018
    def get_chart1_data(self):
        cells = [cell[0].value for cell in self.sheet['B3':'B11087']]
        return {i: cells.count(i) for i in pd.Series(cells).unique() if isinstance(i, str)}

    # Crime counts in months - 2018
    def get_chart2_data(self):
        month_list = [
            'January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December'
        ]
        cells = [cell[0].value for cell in self.sheet['E3':'E11087']]
        return {month_list[int(i) - 1]: cells.count(i) for i in sorted(pd.Series(cells).unique())
                if isinstance(i, numbers.Number) and not pd.isnull(i)}

    # Types of Crimes - 2018
    def get_chart3_data(self):
        cells = [cell[0].value for cell in self.sheet['C3':'C11087']]
        return {i: cells.count(i) for i in pd.Series(cells).unique() if isinstance(i, str)}

    # Types of Crimes according to area & month - 2018
    def get_chart4_data(self, area, month):
        cells = [cell[0].value for cell in self.sheet['C3':'C11087']
                 if str(self.sheet.cell(row=cell[0].row, column=2).value) == str(area) and
                 int(self.sheet.cell(row=cell[0].row, column=5).value) == int(month)]
        return {i: cells.count(i) for i in pd.Series(cells).unique() if isinstance(i, str)}

    # Danger Level variation according to area, month & date
    def get_chart5_data(self, area, month, date):
        def getPredicted(hour):
            obj = {
                'area': [area],
                'month': [month],
                'day': [date],
                'hour': [hour],
                'temp': 33,
                'popul_den': 270,
                'education_lvl': 65,
                'economy': 40000,
                'alcohol_drug_usage': 5500
            }
            return int(predictor.predict(pd.DataFrame(obj)))

        return {str(i): getPredicted(i) for i in range(0, 24)}

    # Crime counts in major Cities - 2018
    def get_chart1(self, name):
        x1 = self.get_chart1_data()

        data = pd.Series(x1).reset_index(name='value').rename(columns={'index': 'city'})
        data['angle'] = data['value'] / data['value'].sum() * 2 * pi
        data['color'] = Category20c[len(x1)]

        s1 = figure(title="Crime counts in major Cities - 2018", toolbar_location=None, name=str(name),
                    tools="hover", tooltips="@city: @value", x_range=(-0.5, 1.0), sizing_mode="stretch_width")
        s1.wedge(x=0, y=1, radius=0.4,
                 start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                 line_color="white", fill_color='color', legend_field='city', source=data)
        s1.axis.axis_label = None
        s1.axis.visible = False
        s1.grid.grid_line_color = None
        s1.outline_line_color = None
        return s1

    # Crime counts in months - 2018
    def get_chart2(self, name):
        x2 = self.get_chart2_data()

        data = pd.Series(x2).reset_index(name='value').rename(columns={'index': 'month'})
        data['angle'] = data['value'] / data['value'].sum() * 2 * pi
        data['color'] = Category20b[len(x2)]

        s2 = figure(title="Crime counts in months - 2018", toolbar_location=None, name=str(name),
                    tools="hover", tooltips="@month: @value", x_range=(-0.5, 1.0), sizing_mode="stretch_width")
        s2.wedge(x=0, y=1, radius=0.4,
                 start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                 line_color="white", fill_color='color', legend_field='month', source=data)
        s2.axis.axis_label = None
        s2.axis.visible = False
        s2.grid.grid_line_color = None
        s2.outline_line_color = None
        return s2

    # Types of Crimes - 2018
    def get_chart3(self, name):
        x3 = self.get_chart3_data()

        types = list(x3.keys())
        counts = list(x3.values())
        data = ColumnDataSource(data=dict(types=types, counts=counts, colors=Accent7 * 4))

        s3 = figure(x_range=types, toolbar_location=None, title="Types of Crimes - 2018", name=str(name),
                    tools="hover", tooltips="@types: @counts", sizing_mode="stretch_both", plot_height=1500)
        s3.vbar(x='types', top='counts', width=1, source=data, line_color='white',
                fill_color='colors')
        s3.y_range.start = 0
        s3.x_range.range_padding = 0.05
        s3.xgrid.grid_line_color = None
        s3.xaxis.major_label_orientation = 1
        s3.outline_line_color = None
        return s3

    # Types of Crimes according to area & month - 2018
    def get_chart4(self, area, month):
        x4 = self.get_chart4_data(area, month)
        types = list(x4.keys())
        counts = list(x4.values())
        source = ColumnDataSource(data=dict(types=types, counts=counts, colors=Accent7 * 4))

        s4 = figure(x_range=types, toolbar_location=None, css_classes=['shadow-sm'],
                    title="Types of Crimes according to the Area & Month - 2018",
                    tools="hover", tooltips="@types: @counts", sizing_mode="stretch_width", plot_height=800)
        s4.vbar(x='types', top='counts', width=1, source=source, line_color='white',
                fill_color='colors')
        s4.y_range.start = 0
        s4.x_range.range_padding = 0.05
        s4.xgrid.grid_line_color = None
        s4.xaxis.major_label_orientation = 1
        s4.outline_line_color = None

        return s4

    # Danger Level variation according to area, month & date
    def get_chart5(self, area, month, date):
        x5 = self.get_chart5_data(area, month, date)
        types = list(x5.keys())
        counts = list(x5.values())
        source = ColumnDataSource(data=dict(types=types, counts=counts, colors=Reds6 * 4))

        s5 = figure(x_range=types, toolbar_location=None, css_classes=['shadow-sm'],
                    title="Danger Level variation according to Area, Month & Date",
                    tools="hover", tooltips="Danger Level: @counts", sizing_mode="stretch_width", plot_height=250)
        s5.vbar(x='types', top='counts', width=1, source=source, line_color='white',
                fill_color='colors')
        s5.y_range.start = 0
        s5.y_range.end = 5
        s5.x_range.range_padding = 0.05
        s5.xgrid.grid_line_color = None
        s5.xaxis.major_label_orientation = 1
        s5.outline_line_color = None

        return s5

    # Get table data
    # def get_table(self):


    # File upload
    def file_upload(self):
        def on_click():
            if file_input.filename is not "":
                decoded = base64.b64decode(file_input.value)
                tmp = open(upload_filename, 'wb')
                tmp.write(decoded)
                tmp.close()
                global_variables.datafile = DataFile()

        file_input = FileInput(accept=".xlsx")
        btn_upload = Button(label="Upload New Dataset", button_type="success")
        btn_upload.on_click(on_click)
        callbacks = CustomJS(args=dict(input=file_input),
                             code="if(input.filename){"
                                  "alert('File successfully uploaded.'); location.reload();"
                                  "}else{"
                                  "alert('No file selected. Try again.');"
                                  "}")
        btn_upload.callback = callbacks
        return row(file_input, btn_upload, name="uploading_section", sizing_mode="scale_both")

    # Island layout
    def get_islandwide_charts(self):
        chart1 = self.get_chart1("chart1")
        chart2 = self.get_chart2("chart2")
        chart3 = self.get_chart3("chart3")
        return column(row(chart1, chart2), row(chart3),
                      name="islandwide_charts", sizing_mode="scale_both")

    # District layout
    def get_localwise_charts(self):
        def update(attr, old, new):
            layout1.children[1] = self.get_chart4(str(select_area1.value), int(select_month1.value))
            layout2.children[1] = self.get_chart5(options3_indexes[options3.index(select_area2.value)],
                                                  options4_indexes[options4.index(select_month2.value)],
                                                  options5_indexes[options5.index(select_date2.value)])

        options1 = list(self.datafile.get_area_choices().keys())
        select_area1 = Select(value=options1[0], options=options1, title="District")

        options2 = list(self.datafile.get_month_choices().keys())
        select_month1 = Select(value=options2[0], options=options2, title="Month")

        options3 = list(self.datafile.get_area_choices().keys())
        options3_indexes = list(self.datafile.get_area_choices().values())
        select_area2 = Select(value=options3[0], options=options3, title="District")

        options4 = list(self.datafile.get_month_choices().keys())
        options4_indexes = list(self.datafile.get_month_choices().values())
        select_month2 = Select(value=options4[0], options=options4, title="Month")

        options5 = list(self.datafile.get_day_choices().keys())
        options5_indexes = list(self.datafile.get_day_choices().values())
        select_date2 = Select(value=options5[0], options=options5, title="Date")

        select_area1.on_change("value", update)
        select_month1.on_change("value", update)
        select_area2.on_change("value", update)
        select_month2.on_change("value", update)
        select_date2.on_change("value", update)

        controls1 = row(select_area1, select_month1, css_classes=['rounded', 'shadow-sm'], background='#999999',
                        sizing_mode="stretch_width", margin=(0, 0, 10, 0))
        layout1 = column(controls1, self.get_chart4(str(select_area1.value), int(select_month1.value)))

        controls2 = row(select_area2, select_month2, select_date2, css_classes=['rounded', 'shadow-sm'],
                        background='#999999', sizing_mode="stretch_width", margin=(40, 0, 10, 0))
        layout2 = column(controls2, self.get_chart5(options3_indexes[options3.index(select_area2.value)],
                                                    options4_indexes[options4.index(select_month2.value)],
                                                    options5_indexes[options5.index(select_date2.value)]))

        # Data Tables
        tabs = []
        for area in self.datafile.get_area_choices().keys():
            tmp_tbl = self.datafile.get_table_by_area(area=str(area), rows=21)
            tabs.append(Panel(child=tmp_tbl, title=str(area)))
        tabs = Tabs(tabs=tabs, margin=(50, 0, 10, 0))

        return column(layout1, layout2, row(tabs), name="localwise_charts", sizing_mode="scale_both")
