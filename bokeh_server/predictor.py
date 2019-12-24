import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import TextInput, Select, Slider, Button, Div, Panel, Tabs
from sklearn import preprocessing
from sklearn.ensemble import AdaBoostClassifier

import global_variables


class Predictor:

    def __init__(self, datafile):
        # selected data
        self.selected = {
            'area': [0],
            'month': [1],
            'day': [1],
            'hour': [0],
            'temp': 0,
            'popul_den': 0,
            'education_lvl': 0,
            'economy': 0,
            'alcohol_drug_usage': 0
        }

        # load file
        self.datafile = datafile
        self.df = datafile.df
        self.dfn = None

        # initialize model
        self.model = AdaBoostClassifier(n_estimators=120)

    def pre_process_data(self):
        # missing values fixing
        self.df['Education Level (O/L pass rate)'] \
            .fillna(self.df['Education Level (O/L pass rate)'].mode()[0], inplace=True)
        self.df.dropna(inplace=True)

        # new data set with required features
        self.dfn = self.df.drop(columns=['Year', 'NumOfCrime', 'Penalty'])
        self.dfn.columns = ['area', 'crime', 'month', 'day', 'hour', 'danger_lvl',
                            'temp', 'popul_den', 'education_lvl', 'economy', 'alcohol_drug_usage']

        # categorical data encoding
        label_encoder = preprocessing.LabelEncoder()
        self.dfn['area'] = label_encoder.fit_transform(self.dfn['area'])
        self.dfn['crime'] = label_encoder.fit_transform(self.dfn['crime'])

        # Convert Categorical Variables into Dummy Variables
        self.dfn['area'] = self.dfn['area'].astype('object')
        self.dfn['crime'] = self.dfn['crime'].astype('object')
        self.dfn['month'] = self.dfn['month'].astype('object')
        self.dfn['day'] = self.dfn['day'].astype('object')
        self.dfn['hour'] = self.dfn['hour'].astype('object')

    def fit(self):
        x_train = self.dfn.drop(['danger_lvl', 'crime'], axis=1)
        y_train = self.dfn.copy(deep=True)['danger_lvl']
        self.model.fit(x_train, y_train)

    def predict(self, data):
        return self.model.predict(data)

    def select_box(self, lst, selection, title):
        def input_handler(attr, old, new):
            self.selected[str(selection)] = [lst[new]]
            global_variables.static_data(new)

        options = list(lst.keys())
        select = Select(value=options[0], options=options, title=str(title), margin=[12, 30, 0, 30])
        select.on_change("value", input_handler)
        return select

    def input_box(self, name, selection, placeholder):
        def input_handler(attr, old, new):
            self.selected[str(selection)] = float(new)

        input_text = TextInput(name=str(name), placeholder=str(placeholder))
        input_text.on_change("value", input_handler)
        return input_text

    def form_layout(self):
        def temp_onchange(attr, old, new):
            self.selected['temp'] = float(new)

        options1 = self.datafile.get_area_choices()
        options1_indexes = list(self.datafile.get_area_choices().values())
        areas_select_box = self.select_box(options1, "area", "District")

        options2 = self.datafile.get_month_choices()
        options2_indexes = list(self.datafile.get_month_choices().values())
        months_select_box = self.select_box(options2, "month", "Month")

        options3 = self.datafile.get_day_choices()
        options1_indexes = list(self.datafile.get_day_choices().values())
        days_select_box = self.select_box(options3, "day", "Date")

        options4 = self.datafile.get_hour_choices()
        options4_indexes = list(self.datafile.get_month_choices().values())
        hours_select_box = self.select_box(options4, "hour", "Hour")

        temperature_slider = Slider(start=0, end=60, value=0, step=.5, title="Temperature(Celsius)",
                                    margin=[12, 35, 12, 35])
        temperature_slider.on_change("value", temp_onchange)

        controls1 = column(areas_select_box, months_select_box, days_select_box, hours_select_box, temperature_slider,
                           css_classes=['rounded', 'shadow-sm'], background='#999999',
                           sizing_mode="stretch_width", margin=(0, 0, 10, 0))

        return row(controls1, name="prediction_ctrl", sizing_mode="scale_both")

    def prediction_output(self):
        def get_div(value):
            return Div(text='0'+str(value), style={'font-size': '6rem', 'color': 'red'}, align="center")

        def submit_button():
            layout1.children[0] = get_div(int(self.predict(pd.DataFrame(self.selected))))

        button = Button(label="Calculate", button_type="success", sizing_mode="scale_width", align="center")
        button.on_click(submit_button)

        div = get_div(0)
        layout1 = row(div, align="center", sizing_mode="fixed")
        return column(layout1, button, margin=[0, 0, 50, 50], name="prediction_output", sizing_mode="scale_width")

    def map_viewer(self):
        p1 = Div(text="""<img src="bokeh_server/static/images/map_anuradhapura.png" width="965"/>""", width=965,
                  sizing_mode="fixed")
        p2 = Div(text="""<img src="bokeh_server/static/images/map_badulla.png" width="965"/>""", width=965,
                 sizing_mode="fixed")
        p3 = Div(text="""<img src="bokeh_server/static/images/map_bandarawela.png" width="965"/>""", width=965,
                 sizing_mode="fixed")
        p4 = Div(text="""<img src="bokeh_server/static/images/map_colombo.png" width="965"/>""", width=965,
                 sizing_mode="fixed")
        p5 = Div(text="""<img src="bokeh_server/static/images/map_galle.png" width="965"/>""", width=965,
                 sizing_mode="fixed")
        p6 = Div(text="""<img src="bokeh_server/static/images/map_gampaha.png" width="965"/>""", width=965,
                 sizing_mode="fixed")
        p7 = Div(text="""<img src="bokeh_server/static/images/map_hatton.png" width="965"/>""", width=965,
                 sizing_mode="fixed")
        p8 = Div(text="""<img src="bokeh_server/static/images/map_nugegoda.png" width="965"/>""", width=965,
                 sizing_mode="fixed")
        p9 = Div(text="""<img src="bokeh_server/static/images/map_nuwaraeliya.png" width="965"/>""", width=965,
                 sizing_mode="fixed")
        p10 = Div(text="""<img src="bokeh_server/static/images/map_panadura.png" width="965"/>""", width=965,
                 sizing_mode="fixed")

        tab1 = Panel(child=p1, title="Anuradhapura")
        tab2 = Panel(child=p2, title="Badulla")
        tab3 = Panel(child=p3, title="Bandarawela")
        tab4 = Panel(child=p4, title="Colombo")
        tab5 = Panel(child=p5, title="Galle")
        tab6 = Panel(child=p6, title="Gampaha")
        tab7 = Panel(child=p7, title="Hatton")
        tab8 = Panel(child=p8, title="Nugegoda")
        tab9 = Panel(child=p9, title="Nuwara Eliya")
        tab10 = Panel(child=p10, title="Panadura")

        tabs = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10], margin=(0, 0, 0, 0))

        return column(tabs, margin=(0, 0, 0, 0), name="map_viewer", sizing_mode="scale_width")
