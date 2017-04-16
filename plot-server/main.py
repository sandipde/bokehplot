# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from copy import copy
from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.layouts import layout,column,row
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
xval=copy(colvar[:,0])
yval=copy(colvar[:,1])
cval=copy(colvar[:,3])
layout = create_plot(xval,yval,cval)

def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='X-Axis', value='mpg', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='hp', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + quantileable)
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None'] + quantileable)
color.on_change('value', update)

controls = widgetbox([x, y, color, size], width=200)
layout = row(controls, create_figure())



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

