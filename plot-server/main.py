# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from copy import copy
from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.layouts import layout,column,row
from bokeh.models.layouts import HBox
from bokeh.models import (
    ColumnDataSource, HoverTool, SingleIntervalTicker, Slider, Button, Label,
    CategoricalColorMapper,
)
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, CustomJS, Rect,Spacer
from bokeh.models import HoverTool,TapTool,FixedTicker,Circle
from bokeh.models import BoxSelectTool, LassoSelectTool
from bokeh.models.mappers import LinearColorMapper
from bokeh.plotting import figure
from bokeh.layouts import row, widgetbox
from bokeh.models import Select
from cosmo import create_plot
#from data import process_data
from os.path import dirname, join

datafile=join(dirname(__file__), 'data', 'MAPbI.dat')
colvar=np.loadtxt(datafile)


def update(attr, old, new):
    p1,p2,slider= create_plot(colvar,col_dict[xcol.value],col_dict[ycol.value],col_dict[ccol.value])
    plots=column(row(p1,p2),row(slider,Spacer(width=200, height=30)))
    layout.children[1] = plots

columns=["cv1","cv2","index","energy"]
col_dict={"cv1":0,"cv2": 1,"index": 2,"energy": 3}

xcol = Select(title='X-Axis', value='cv1', options=columns)
xcol.on_change('value', update)

ycol = Select(title='Y-Axis', value='cv2', options=columns)
ycol.on_change('value', update)

ccol = Select(title='Color', value='energy', options=columns)
ccol.on_change('value', update)

controls = row([xcol, ycol, ccol])

p1,p2,slider= create_plot(colvar,col_dict[xcol.value],col_dict[ycol.value],col_dict[ccol.value])
plots=column(row(p1,p2),row(slider,Spacer(width=200, height=30)))
layout = column(controls,plots)



curdoc().add_root(layout)
curdoc().template_variables["js_files"] = ["static/jmol/JSmol.min.js"]
curdoc().title = "Sketchmap"

#def animate_update():
#    year = slider.value + 1
#    if year > years[-1]:
#        year = years[0]
#    slider.value = year
#
#
#def slider_update(attrname, old, new):
#    year = slider.value
#    label.text = str(year)
#    source.data = data[year]
#
#slider = Slider(start=years[0], end=years[-1], value=years[0], step=1, title="Year")
#slider.on_change('value', slider_update)


#def animate():
#    if button.label == '► Play':
#        button.label = '❚❚ Pause'
#        curdoc().add_periodic_callback(animate_update, 200)
#    else:
#        button.label = '► Play'
#        curdoc().remove_periodic_callback(animate_update)
#
#button = Button(label='► Play', width=60)
#button.on_click(animate)


#layout = layout([plots])
#    [plot],
#    [slider, button],
#], sizing_mode='scale_width')

