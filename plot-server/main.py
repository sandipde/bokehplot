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
from bokeh.models.mappers import LinearColorMapper
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from cosmo import cosmo_colors
#from data import process_data
from os.path import dirname, join

datafile=join(dirname(__file__), 'data', 'MAPbI.dat')
colvar=np.loadtxt(datafile)
colors=cosmo_colors(colvar[:,3])
xval=np.zeros(len(colvar))
xval=copy(colvar[:,0])
yval=np.zeros(len(colvar))
yval=copy(colvar[:,1])
datasrc = ColumnDataSource(
        data=dict(
            x=xval,
            y=yval,
            colors=colors,
        )
    )

source = ColumnDataSource({'x': [], 'y': [], 'width': [], 'height': []})

jscode="""
        var data = source.get('data');
        var start = range.get('start');
        var end = range.get('end');
        data['%s'] = [start + (end - start) / 2];
        data['%s'] = [end - start];
        source.trigger('change');
     """
initial_circle = Circle(x='x', y='y')
selected_circle = Circle(fill_alpha=1, fill_color="firebrick", size=20)
nonselected_circle = Circle(fill_alpha=0.4,fill_color='colors',line_color=None)
title="Sketchmap"
TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select,tap,save"
# The main Plot of tab 1
p1 = figure(title=title,tools=[TOOLS],height=800,width=800)
p1.circle('x','y',source=datasrc,size=5,fill_color='colors', fill_alpha=0.8, line_color=None,name="mycircle")
p1.x_range.callback = CustomJS(
       args=dict(source=source, range=p1.x_range), code=jscode % ('x', 'width'))
p1.y_range.callback = CustomJS(
       args=dict(source=source, range=p1.y_range), code=jscode % ('y', 'height'))
#p1.title_text_color = "firebrick"
#p1.title_text_font = "times"
#p1.title_text_font_style = "italic"
renderer = p1.select(name="mycircle")
renderer.selection_glyph = selected_circle
renderer.nonselection_glyph = nonselected_circle
p1.xgrid.grid_line_color = None
p1.ygrid.grid_line_color = None
p1.xaxis[0].ticker=FixedTicker(ticks=[])
p1.yaxis[0].ticker=FixedTicker(ticks=[])
p1.outline_line_width = 0
p1.outline_line_color = "white"
p1.xaxis.axis_line_width = 0
p1.xaxis.axis_line_color = "white"
p1.yaxis.axis_line_width = 0
p1.yaxis.axis_line_color = "white"

layout = column(row(p1), row(Spacer(width=200, height=200)))

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

