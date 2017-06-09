# -*- coding: utf-8 -*-
import pandas as pd
import os
import numpy as np
from copy import copy
from bokeh.io import curdoc
from bokeh.layouts import layout,column,row
from bokeh.models.layouts import Row
from bokeh.models import (
    ColumnDataSource, HoverTool, SingleIntervalTicker, Slider, Button, Label,
    CategoricalColorMapper,
)
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, CustomJS, Rect,Spacer
from bokeh.models import HoverTool,TapTool,FixedTicker,Circle
from bokeh.models import BoxSelectTool, LassoSelectTool
from bokeh.plotting import figure
from bokeh.layouts import row, widgetbox
from bokeh.models.widgets import Select,TextInput
from cosmo import create_plot
from os.path import dirname, join
from smaplib import *
def main(dfile,pcol,appname):
    global cv,selectsrc,columns,button,slider,n,xcol,ycol,ccol,s2,xcol,ycol,ccol,plt_name,indx,controls

#initialise data
    datafile=join(dirname(__file__), 'data', dfile)
    cv=smap(name="Sketchmap")
    cv.read(datafile) 
    n=len(cv.data)
    columns=[i for i in cv.columns]

# set up selection options

    xcol = Select(title='X-Axis', value=columns[pcol[0]], options=columns,width=50)
    xcol.on_change('value', update)
    ycol = Select(title='Y-Axis', value=columns[pcol[1]], options=columns, width=50)
    ycol.on_change('value', update)
    ccol = Select(title='Color', value=columns[pcol[2]], options=columns,width=50)
    ccol.on_change('value', update)
    plt_name = Select(title='Palette',width=50, value='Inferno256', options=["Magma256","Plasma256","Spectral6","Inferno256","Viridis256","Greys256"])
    plt_name.on_change('value', update)
    xm=widgetbox(xcol,width=210,sizing_mode='fixed')
    ym=widgetbox(ycol,width=210,sizing_mode='fixed')
    cm=widgetbox(ccol,width=210,sizing_mode='fixed')
    pm=widgetbox(plt_name,width=210,sizing_mode='fixed')
    controls = Row(xm, ym, cm, pm, width=850, sizing_mode='scale_width')
#    update(cv,scol,ycol,ccol,palette,radii)
    plotpanel,slider=create_plot()

# Play button
    button = Button(label='► Play', width=60)
    button.on_click(animate)

    lay=layout([
        [controls],
        [plotpanel],
        [Row(slider,button)],
    ], sizing_mode='fixed')
    return lay



def create_plot():
    global cv,selectsrc,columns,button,slider,n,xcol,ycol,ccol,s2,xcol,ycol,ccol,plt_name,indx,controls
# Set up main plot
    p1=cv.bkplot(xcol.value,ycol.value,ccol.value,palette=plt_name.value,radii='None',ps=10,minps=8,pw=600,ph=500,toolbar_location="above")

# Set up mouse selection callbacks


# The following code is very tricky to understand properly. 
# the %s are the function or variable to pass from python depending on the slider callback or mouse callback. 
# One could write 3 seperate callbacks to connect slider,jmol and mouse selection but this way it is more compact ! 

    code="""
       var refdata = ref.get('data');
       var data = source.get('data');
       var inds = cb_obj.%s;
       var xs = refdata['x'][inds];
       var ys = refdata['y'][inds];
       data['xs'] = [xs];
       data['ys'] = [ys];
       data=refdata[inds];
       source.trigger('change');
       %s;
       var str = "" + inds;
       var pad = "0000";
       var indx = pad.substring(0, pad.length - str.length) + str;
       var settings=  " " 
       var file= "javascript:Jmol.script(jmolApplet0," + "'load  %s/static/xyz/set."+ indx+ ".xyz ;" + settings + "')" ;
       location.href=file;
       localStorage.setItem("indexref",indx);
       document.getElementById("p1").innerHTML = "Mouse selected frame:"+ indx ;
       """ 

# Set up Slider
    selectsrc=ColumnDataSource({'xs': [cv.pd[xcol.value][0]], 'ys': [cv.pd[ycol.value][0]]})
    refsrc=ColumnDataSource({'x':cv.pd[xcol.value], 'y':cv.pd[ycol.value]})
    slider = Slider(start=0, end=n-1, value=0, step=1, title="Frame No", width=700)
    slider_callback=CustomJS(args=dict(source=selectsrc, ref=refsrc,slider=slider), code=code%("value","",appname))
    slider.js_on_change('value', slider_callback)
    slider.on_change('value', slider_update)

#set up mouse
    callback=CustomJS(
         args=dict(source=selectsrc, ref=refsrc,s=slider), code=code%("get('selected')['1d'].indices[0]","s.set('value', inds)",appname))
    taptool = p1.select(type=TapTool)
    taptool.callback = callback
    p1.circle('xs', 'ys', source=selectsrc, fill_alpha=0.9, fill_color="blue",line_color='black',line_width=1, size=15,name="selectcircle")

# Set up Overview Plot
 
    p2=cv.bkplot(xcol.value,ycol.value,color='None',radii='None',ps=4,minps=2,pw=200,ph=200)
    p2.circle('xs', 'ys', source=selectsrc, fill_alpha=0.9, fill_color="blue",line_color='black',line_width=1, size=8,name="mycircle")
    source = ColumnDataSource({'xs': [], 'ys': [], 'wd': [], 'ht': []})
    jscode="""
            var data = source.get('data');
            var start = range.get('start');
            var end = range.get('end');
            data['%s'] = [start + (end - start) / 2];
            data['%s'] = [end - start];
            source.trigger('change');
         """
    p1.x_range.callback = CustomJS(
           args=dict(source=source, range=p1.x_range), code=jscode % ('xs', 'wd'))
    p1.y_range.callback = CustomJS(
           args=dict(source=source, range=p1.y_range), code=jscode % ('ys', 'ht'))
    rect = Rect(x='xs', y='ys', width='wd', height='ht', fill_alpha=0.1,
               line_color='black', fill_color='black')
    p2.add_glyph(source, rect)
    



# layout stuffs 
    spacer = Spacer(width=200, height=300)
    indx=0
    xval=cv.pd[xcol.value][indx]
    yval=cv.pd[ycol.value][indx]
    plotpanel=Row(p1, column(p2,spacer))
    return plotpanel,slider


def animate_update():
    global indx,n
    indx = slider.value + 1
    if indx > (n-1):
        indx = 0
    slider.value = indx

def slider_update(attrname, old, new):
    global  cv,indx,selectsrc,xcol,ycol,label
    indx = slider.value
#    label.text = str(indx)
    s = ColumnDataSource(data=dict(xs=[cv.pd[xcol.value][indx]], ys=[cv.pd[ycol.value][indx]]))
    selectsrc.data=s.data 

def animate():
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        curdoc().add_periodic_callback(animate_update, 500)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(animate_update)





def update(attr, old, new):
    global cv,indx,selectsrc,xval,yval,plt_name,xcol,ycol,ccol
    plotpanel,slider=create_plot()
    lay.children[1] = plotpanel

# Play button
    button = Button(label='► Play', width=60)
    button.on_click(animate)

    lay.children[2] = Row(slider,button)




#columns=["cv1","cv2","index","energy"]
#col_dict={"cv1":0,"cv2": 1,"index": 2,"energy": 3}

appname=os.path.basename(dirname(__file__))
lay=main(dfile='COLVAR',pcol=[0,1,3],appname=appname)
curdoc().add_root(lay)
curdoc().template_variables["js_files"] = [appname+"/static/jmol/JSmol.min.js"]
css=[]
for f in ["w3","introjs"]:
  css.append(appname+"/static/css/"+f+'.css')
curdoc().template_variables["css_files"] = css
curdoc().template_variables["appname"] = [appname]
curdoc().title = "Sketchmap"
