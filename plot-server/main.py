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


def selected_point(data,xcol,ycol,indx):
   xval=copy(data[indx,xcol])
   yval=copy(data[indx,ycol])
   return xval,yval

def animate_update():
    global indx,n
    indx = slider.value + 1
    if indx > (n-1):
        indx = 0
    slider.value = indx

#def slider_update(attrname, old, new):
#    year = slider.value
#    label.text = str(year)
#    source.data = data[year]

#slider = Slider(start=years[0], end=years[-1], value=years[0], step=1, title="Year")
#def slider_callback2(src=datasrc,source=s2, window=None):
def slider_update(attrname, old, new):
    global  indx,s2
    col_dict={"cv1":0,"cv2": 1,"index": 2,"energy": 3}
    indx = slider.value
   # label.text = str(indx)
    xval,yval=selected_point(colvar,col_dict[xcol.value],col_dict[ycol.value],indx)
    s = ColumnDataSource(data=dict(xs=[xval], ys=[yval]))
    s2.data=s.data 

def animate():
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        curdoc().add_periodic_callback(animate_update, 200)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(animate_update)





def update(attr, old, new):
    global indx,s2
    col_dict={"cv1":0,"cv2": 1,"index": 2,"energy": 3}
    p1,p2,slider= create_plot(colvar,col_dict[xcol.value],col_dict[ycol.value],col_dict[ccol.value])
    xval,yval=selected_point(colvar,col_dict[xcol.value],col_dict[ycol.value],indx)
    s = ColumnDataSource(data=dict(xs=[xval], ys=[yval]))
    s2.data=s.data 
    p1.circle('xs', 'ys', source=s2, fill_alpha=1, fill_color="blue", size=10,name="mycircle")
    s=widgetbox(slider,width=1000)
    button = Button(label='► Play', width=60)
    button.on_click(animate)
    lay.children[1] = row(p1,p2)



datafile=join(dirname(__file__), 'data', 'MAPbI.dat')
colvar=np.loadtxt(datafile)
n=len(colvar)

columns=["cv1","cv2","index","energy"]
col_dict={"cv1":0,"cv2": 1,"index": 2,"energy": 3}

xcol = Select(title='X-Axis', value='cv1', options=columns)
xcol.on_change('value', update)

ycol = Select(title='Y-Axis', value='cv2', options=columns)
ycol.on_change('value', update)

ccol = Select(title='Color', value='energy', options=columns)
ccol.on_change('value', update)

controls = row([xcol, ycol, ccol])
button = Button(label='► Play', width=60)
button.on_click(animate)
indx=0
xval,yval=selected_point(colvar,col_dict[xcol.value],col_dict[ycol.value],indx)
s2 = ColumnDataSource(data=dict(xs=[xval], ys=[yval]))

p1,p2,slider= create_plot(colvar,col_dict[xcol.value],col_dict[ycol.value],col_dict[ccol.value])
s=widgetbox(slider,width=1000)
p1.circle('xs', 'ys', source=s2, fill_alpha=1, fill_color="blue", size=10,name="mycircle")
slider.on_change('value', slider_update)
plots=column(row(p1,p2),row(s,Spacer(width=20, height=30))) #,button)

lay = layout([
    [controls],
    [p1,p2],
    [slider, button],
], sizing_mode='fixed')
curdoc().add_root(lay)
curdoc().template_variables["js_files"] = ["static/jmol/JSmol.min.js"]
curdoc().title = "Sketchmap"
