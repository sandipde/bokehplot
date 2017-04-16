import numpy as np
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

def create_plot(xval,yval,cval):
   colors=cosmo_colors(cval)
   datasrc = ColumnDataSource(
           data=dict(
               x=xval,
               y=yval,
               colors=colors,
           )
       )
   
   source = ColumnDataSource({'xs': [], 'ys': [], 'wd': [], 'ht': []})
   
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
   TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select,tap,save"
   #TOOLS="pan,wheel_zoom,box_select,lasso_select,reset"
   # The main Plot of tab 1
   p1 = figure(title=title,tools=TOOLS,height=800,width=800,toolbar_location="above")
   p1.circle('x','y',source=datasrc,size=5,fill_color='colors', fill_alpha=0.8, line_color=None,name="mycircle")
   p1.x_range.callback = CustomJS(
          args=dict(source=source, range=p1.x_range), code=jscode % ('xs', 'wd'))
   p1.y_range.callback = CustomJS(
          args=dict(source=source, range=p1.y_range), code=jscode % ('ys', 'ht'))
   
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
   
   # The overview plot
   p2 = figure(tools='',height=300,width=300)
   p2.xgrid.grid_line_color = None
   p2.ygrid.grid_line_color = None
   p2.xaxis[0].ticker=FixedTicker(ticks=[])
   p2.yaxis[0].ticker=FixedTicker(ticks=[])
   p2.circle('x','y',source=datasrc,size=5,fill_color=colors, fill_alpha=0.8, line_color=None,name='mycircle')
   renderer = p2.select(name="mycircle")
   renderer.selection_glyph = selected_circle
   renderer.nonselection_glyph = nonselected_circle
   p2.outline_line_width = 0
   p2.outline_line_alpha = 0.3
   p2.outline_line_color = "white"
   p2.xaxis.axis_line_width = 0
   p2.xaxis.axis_line_color = "white"
   p2.yaxis.axis_line_width = 0
   p2.yaxis.axis_line_color = "white"
   rect = Rect(x='xs', y='ys', width='wd', height='ht', fill_alpha=0.1,
              line_color='black', fill_color='black')
   p2.add_glyph(source, rect)
   
   callback=CustomJS(code="""
       var inds = cb_obj.get('selected')['1d'].indices[0];
       var str = "" + inds;
       var pad = "0000";
       var indx = pad.substring(0, pad.length - str.length) + str;
       var settings=  "connect 1.0 1.2 (carbon) (hydrogen) SINGLE CREATE ; connect 1.0 1.2 (nitrogen) (hydrogen) SINGLE CREATE ; connect 1.0 4.2 (carbon) (nitrogen) SINGLE CREATE ; connect 3.0 5 (phosphorus) (iodine) SINGLE CREATE ; set perspectiveDepth OFF "
       var file= "javascript:Jmol.script(jmolApplet0," + "'load  plot-server/static/set."+ indx+ ".xyz ;" + settings + "')" ;
       location.href=file;
       """)
   taptool = p1.select(type=TapTool)
   taptool.callback = callback
   return row(p1,p2)

def cosmo_colors(cval):
   color_palatte=energy_color_palatte()
   color_palatte.reverse()
   colormap=RGBAColorMapper(min(cval),max(cval),color_palatte)
   rgb=colormap.color(cval)
   colors = ["#%02x%02x%02x" % (c[0],c[1],c[2]) for c in rgb]
   return colors

def hex_to_rgb(value):
    """Given a color in hex format, return it in RGB."""

    values = value.lstrip('#')
    lv = len(values)
    rgb = list(int(values[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return rgb


class RGBAColorMapper(object):
    """Maps floating point values to rgb values over a palette"""

    def __init__(self, low, high, palette):
        self.range = np.linspace(low, high, len(palette))
       # self.r, self.g, self.b = np.array(zip(*[hex_to_rgb(i) for i in palette])) #python 2.7
        self.r, self.g, self.b = np.array(list(zip(*[hex_to_rgb(i) for i in palette])))

    def color(self, data):
        """Maps your data values to the pallette with linear interpolation"""

        red = np.interp(data, self.range, self.r)
        blue = np.interp(data, self.range, self.b)
        green = np.interp(data, self.range, self.g)
        # Style plot to return a grey color when value is 'nan'
        red[np.isnan(red)] = 240
        blue[np.isnan(blue)] = 240
        green[np.isnan(green)] = 240
        colors = np.dstack([red.astype(np.uint8),
                          green.astype(np.uint8),
                          blue.astype(np.uint8),
                          np.full_like(data, 255, dtype=np.uint8)])
        #return colors.view(dtype=np.uint32).reshape(data.shape)
        c=[]
        for i in range(len(data)):
          c.append([red[i],green[i],blue[i]])
        return c

def energy_color_palatte():
 
 color_palatte=["#ddf0fe", "#dcf0fe", "#dcf0fe", "#dbf0fe", "#dbf0fe", "#dbeffe", \
"#daeffe", "#daeffe", "#d9effe", "#d9effe", "#d8eefe", "#d8eefe", \
"#d7eefe", "#d7eefe", "#d6edfe", "#d6edfe", "#d5edfe", "#d5edfe", \
"#d4edfe", "#d4ecfe", "#d3ecfe", "#d3ecfe", "#d2ecfe", "#d2ebfe", \
"#d1ebfe", "#d1ebfe", "#d0ebfe", "#d0eafe", "#d0eafe", "#cfeafe", \
"#cfeafe", "#cee9fe", "#cee9fd", "#cde9fd", "#cce9fd", "#cce9fd", \
"#cbe8fd", "#cbe8fd", "#cae8fd", "#cae8fd", "#c9e7fd", "#c9e7fd", \
"#c8e7fd", "#c8e7fd", "#c7e6fd", "#c7e6fd", "#c6e6fd", "#c6e6fd", \
"#c5e5fd", "#c5e5fd", "#c4e5fd", "#c4e5fd", "#c3e4fd", "#c3e4fd", \
"#c2e4fd", "#c2e3fd", "#c1e3fd", "#c0e3fd", "#c0e3fd", "#bfe2fd", \
"#bfe2fd", "#bee2fd", "#bee2fd", "#bde1fd", "#bde1fd", "#bce1fd", \
"#bce1fd", "#bbe0fd", "#bae0fd", "#bae0fd", "#b9dffd", "#b9dffd", \
"#b8dffd", "#b8dffd", "#b7defd", "#b7defd", "#b6defd", "#b5defd", \
"#b5ddfc", "#b4ddfc", "#b4ddfc", "#b3dcfc", "#b3dcfc", "#b2dcfc", \
"#b2dcfc", "#b1dbfc", "#b0dbfc", "#b0dbfc", "#afdbfc", "#afdafc", \
"#aedafc", "#aedafc", "#add9fc", "#acd9fc", "#acd9fc", "#abd9fc", \
"#abd8fc", "#aad8fc", "#a9d8fc", "#a9d7fc", "#a8d7fc", "#a8d7fc", \
"#a7d7fc", "#a7d6fc", "#a6d6fc", "#a5d6fc", "#a5d5fc", "#a4d5fc", \
"#a4d5fc", "#a3d4fc", "#a2d4fc", "#a2d4fc", "#a1d4fc", "#a1d3fc", \
"#a0d3fc", "#9fd3fc", "#9fd2fc", "#9ed2fc", "#9ed2fb", "#9dd2fb", \
"#9cd1fb", "#9cd1fb", "#9bd1fb", "#9bd0fb", "#9ad0fb", "#99d0fb", \
"#99cffb", "#98cffb", "#98cffb", "#97cffb", "#96cefb", "#96cefb", \
"#95cefb", "#95cdfb", "#94cdfb", "#93cdfb", "#93ccfb", "#92ccfb", \
"#92ccfb", "#91cbfb", "#90cbfb", "#90cbfb", "#8fcbfb", "#8fcafb", \
"#8ecafb", "#8dcafb", "#8dc9fb", "#8cc9fb", "#8bc9fb", "#8bc8fb", \
"#8ac8fb", "#8ac8fb", "#89c7fb", "#88c7fb", "#88c7fa", "#88c6fa", \
"#87c6fa", "#87c6fa", "#87c5fa", "#86c5fa", "#86c5fa", "#86c4fa", \
"#85c4fa", "#85c4fa", "#85c3f9", "#84c3f9", "#84c2f9", "#84c2f9", \
"#83c2f9", "#83c1f9", "#83c1f9", "#82c1f9", "#82c0f9", "#82c0f8", \
"#82bff8", "#81bff8", "#81bff8", "#81bef8", "#80bef8", "#80bef8", \
"#80bdf8", "#7fbdf8", "#7fbdf7", "#7fbcf7", "#7ebcf7", "#7ebbf7", \
"#7ebbf7", "#7dbbf7", "#7dbaf7", "#7dbaf7", "#7dbaf7", "#7cb9f6", \
"#7cb9f6", "#7cb8f6", "#7bb8f6", "#7bb8f6", "#7bb7f6", "#7bb7f6", \
"#7ab6f6", "#7ab6f5", "#7ab6f5", "#79b5f5", "#79b5f5", "#79b5f5", \
"#78b4f5", "#78b4f5", "#78b3f5", "#78b3f5", "#77b3f4", "#77b2f4", \
"#77b2f4", "#76b2f4", "#76b1f4", "#76b1f4", "#76b0f4", "#75b0f4", \
"#75b0f3", "#75aff3", "#74aff3", "#74aef3", "#74aef3", "#74aef3", \
"#73adf3", "#73adf3", "#73adf2", "#73acf2", "#72acf2", "#72abf2", \
"#72abf2", "#71abf2", "#71aaf2", "#71aaf2", "#71a9f1", "#70a9f1", \
"#70a9f1", "#70a8f1", "#70a8f1", "#6fa7f1", "#6fa7f1", "#6fa7f1", \
"#6fa6f0", "#6ea6f0", "#6ea5f0", "#6ea5f0", "#6ea5f0", "#6da4f0", \
"#6da4f0", "#6da4f0", "#6da3ef", "#6ca3ef", "#6ca2ef", "#6ca2ef", \
"#6ca2ef", "#6ba1ef", "#6ba1ef", "#6ba0ee", "#6ba0ee", "#6aa0ee", \
"#6a9fee", "#6a9fee", "#6a9eee", "#699eee", "#699eee", "#699ded", \
"#699ded", "#689ced", "#689ced", "#689ced", "#689bed", "#679bed", \
"#679aec", "#679aec", "#679aec", "#6699ec", "#6699ec", "#6698ec", \
"#6698ec", "#6598ec", "#6597eb", "#6597eb", "#6596eb", "#6596eb", \
"#6496eb", "#6495eb", "#6495eb", "#6494ea", "#6394ea", "#6394ea", \
"#6393ea", "#6393ea", "#6392ea", "#6292ea", "#6292e9", "#6291e9", \
"#6291e9", "#6191e9", "#6190e9", "#6190e9", "#618fe9", "#618fe8", \
"#608fe8", "#608ee8", "#608ee8", "#608de8", "#5f8de8", "#5f8de8", \
"#5f8ce8", "#5f8ce7", "#5f8be7", "#5e8be7", "#5e8be7", "#5e8ae7", \
"#5e8ae7", "#5e89e7", "#5d89e6", "#5d89e6", "#5d88e6", "#5d88e6", \
"#5d87e6", "#5c87e6", "#5c87e6", "#5c86e5", "#5c86e5", "#5c85e5", \
"#5b85e5", "#5b85e5", "#5b84e5", "#5b84e5", "#5b83e4", "#5a83e4", \
"#5a83e4", "#5a82e4", "#5a82e4", "#5a81e4", "#5981e4", "#5981e3", \
"#5980e3", "#5980e3", "#597fe3", "#587fe3", "#587fe3", "#587ee3", \
"#587ee2", "#587de2", "#577de2", "#577de2", "#577ce2", "#577ce2", \
"#577be2", "#577be1", "#567be1", "#567ae1", "#567ae1", "#5679e1", \
"#5679e1", "#5579e1", "#5578e0", "#5578e0", "#5577e0", "#5577e0", \
"#5577e0", "#5476e0", "#5476df", "#5475df", "#5475df", "#5475df", \
"#5474df", "#5374df", "#5373df", "#5373de", "#5373de", "#5372de", \
"#5272de", "#5271de", "#5271de", "#5271de", "#5270dd", "#5270dd", \
"#5170dd", "#516fdd", "#516fdd", "#516edd", "#516edd", "#516edc", \
"#506ddc", "#506ddc", "#506cdc", "#506cdc", "#506cdc", "#506bdc", \
"#506bdb", "#4f6adb", "#4f6adb", "#4f6adb", "#4f69db", "#4f69db", \
"#4f68da", "#4e68da", "#4e68da", "#4e67da", "#4e67da", "#4e67da", \
"#4e66da", "#4d66d9", "#4d65d9", "#4d65d9", "#4d65d9", "#4d64d9", \
"#4d64d9", "#4d63d9", "#4c63d8", "#4c63d8", "#4c62d8", "#4c62d8", \
"#4c61d8", "#4c61d8", "#4c61d7", "#4c60d7", "#4c60d7", "#4c60d7", \
"#4c5fd6", "#4c5fd6", "#4b5fd6", "#4b5ed6", "#4b5ed6", "#4b5ed5", \
"#4b5ed5", "#4b5dd5", "#4b5dd5", "#4b5dd4", "#4b5cd4", "#4b5cd4", \
"#4b5cd4", "#4b5bd3", "#4b5bd3", "#4b5bd3", "#4b5ad3", "#4b5ad3", \
"#4b5ad2", "#4b59d2", "#4b59d2", "#4b59d2", "#4b58d1", "#4b58d1", \
"#4b58d1", "#4b57d1", "#4b57d0", "#4b57d0", "#4b56d0", "#4b56d0", \
"#4b56d0", "#4b55cf", "#4b55cf", "#4b55cf", "#4b54cf", "#4b54ce", \
"#4b54ce", "#4b54ce", "#4a53ce", "#4a53cd", "#4a53cd", "#4a52cd", \
"#4a52cd", "#4a52cd", "#4a51cc", "#4a51cc", "#4a51cc", "#4a50cc", \
"#4a50cb", "#4a50cb", "#4a4fcb", "#4a4fcb", "#4a4fca", "#4a4eca", \
"#4a4eca", "#4a4eca", "#4a4ec9", "#4a4dc9", "#4a4dc9", "#4a4dc9", \
"#4a4cc9", "#4a4cc8", "#4a4cc8", "#4a4bc8", "#4a4bc8", "#4a4bc7", \
"#4a4ac7", "#4a4ac7", "#4a4ac7", "#4a4ac6", "#4a49c6", "#4a49c6", \
"#4a49c6", "#4a48c5", "#4a48c5", "#4a48c5", "#4a47c5", "#4a47c5", \
"#4a47c4", "#4a46c4", "#4a46c4", "#4a46c4", "#4a46c3", "#4a45c3", \
"#4a45c3", "#4a45c3", "#4a44c2", "#4a44c2", "#4a44c2", "#4a43c2", \
"#4a43c1", "#4a43c1", "#4a43c1", "#4a42c1", "#4a42c0", "#4a42c0", \
"#4a41c0", "#4a41c0", "#4a41c0", "#4a40bf", "#4a40bf", "#4b40bf", \
"#4b40bf", "#4b3fbe", "#4b3fbe", "#4b3fbe", "#4b3ebe", "#4b3ebd", \
"#4b3ebd", "#4b3ebd", "#4b3dbd", "#4b3dbc", "#4b3dbc", "#4b3cbc", \
"#4b3cbc", "#4b3cbb", "#4b3bbb", "#4b3bbb", "#4b3bbb", "#4b3bba", \
"#4b3aba", "#4b3aba", "#4b3aba", "#4b39ba", "#4b39b9", "#4b39b9", \
"#4b39b9", "#4b38b9", "#4b38b8", "#4b38b8", "#4b37b8", "#4b37b8", \
"#4b37b7", "#4b37b7", "#4b36b7", "#4b36b7", "#4b36b6", "#4b35b6", \
"#4b35b6", "#4c35b6", "#4c35b5", "#4c34b5", "#4c34b5", "#4c34b5", \
"#4c33b4", "#4c33b4", "#4c33b4", "#4c33b4", "#4c32b3", "#4c32b3", \
"#4c32b3", "#4c32b3", "#4c31b3", "#4c31b2", "#4c31b2", "#4c30b2", \
"#4c30b2", "#4c30b1", "#4c30b1", "#4c2fb1", "#4c2fb1", "#4c2fb0", \
"#4d2eb0", "#4d2eb0", "#4d2eb0", "#4d2eaf", "#4d2daf", "#4d2daf", \
"#4d2daf", "#4d2dae", "#4d2cae", "#4d2cae", "#4d2cae", "#4d2cad", \
"#4d2bad", "#4d2bad", "#4d2bad", "#4d2aac", "#4d2aac", "#4d2aac", \
"#4d2aac", "#4e29ab", "#4e29ab", "#4e29ab", "#4e29ab", "#4e28aa", \
"#4e28aa", "#4e28aa", "#4e28aa", "#4e27a9", "#4e27a9", "#4e27a9", \
"#4e27a9", "#4e26a8", "#4e26a8", "#4e26a8", "#4f26a8", "#4f25a7", \
"#4f25a7", "#4f25a7", "#4f25a7", "#4f24a6", "#4f24a6", "#4f24a6", \
"#4f24a6", "#4f23a5", "#4f23a5", "#4f23a5", "#4f23a5", "#4f22a4", \
"#5022a4", "#5022a4", "#5022a4", "#5021a3", "#5021a3", "#5021a3", \
"#5021a3", "#5020a2", "#5020a2", "#5020a2", "#5020a1", "#501fa1", \
"#511fa1", "#511fa1", "#511fa0", "#511ea0", "#511ea0", "#511ea0", \
"#511e9f", "#511d9f", "#511d9f", "#511d9f", "#511d9e", "#521d9e", \
"#521c9e", "#521c9e", "#521c9d", "#521c9d", "#521b9d", "#521b9d", \
"#521b9c", "#521b9c", "#521a9c", "#531a9b", "#531a9b", "#531a9b", \
"#531a9b", "#53199a", "#53199a", "#53199a", "#53199a", "#531999", \
"#531899", "#541899", "#541899", "#541898", "#541798", "#541798", \
"#541797", "#541797", "#541797", "#551697", "#551696", "#551696", \
"#551696", "#551696", "#551595", "#551595", "#551595", "#551594", \
"#551594", "#551594", "#551593", "#551593", "#551593", "#551592", \
"#551592", "#551592", "#551591", "#551591", "#551591", "#551590", \
"#551590", "#551590", "#55158f", "#55158f", "#55158f", "#55158e", \
"#55158e", "#55158e", "#55158d", "#55158d", "#54158c", "#54158c", \
"#54158c", "#54158b", "#54158b", "#54158b", "#54158a", "#54158a", \
"#54158a", "#541589", "#541589", "#541589", "#541588", "#541588", \
"#541588", "#541587", "#541587", "#541586", "#541586", "#541586", \
"#541585", "#541585", "#541585", "#541584", "#541584", "#541584", \
"#541583", "#541583", "#541583", "#551582", "#551582", "#551581", \
"#551581", "#551581", "#551580", "#551580", "#551580", "#55157f", \
"#55167f", "#55167e", "#55167e", "#55167e", "#55167d", "#55167d", \
"#55167d", "#55167c", "#55167c", "#55167b", "#55167b", "#55167b", \
"#56167a", "#56167a", "#56167a", "#561679", "#561679", "#561678", \
"#561778", "#561778", "#561777", "#561777", "#561777", "#561776", \
"#571776", "#571775", "#571775", "#571775", "#571774", "#571774", \
"#571773", "#571873", "#571873", "#581872", "#581872", "#581871", \
"#581871", "#581871", "#581870", "#581870", "#59186f", "#59196f", \
"#59196f", "#59196e", "#59196e", "#59196d", "#5a196d", "#5a196d", \
"#5a196c", "#5a196c", "#5a1a6b", "#5a1a6b", "#5b1a6b", "#5b1a6a", \
"#5b1a6a", "#5b1a69", "#5b1a69", "#5c1b68", "#5c1b68", "#5c1b68", \
"#5c1b67", "#5c1b67", "#5d1b66", "#5d1b66", "#5d1c66", "#5d1c65", \
"#5d1c65", "#5e1c64", "#5e1c64", "#5e1c63", "#5e1d63", "#5f1d63", \
"#5f1d62", "#5f1d62", "#5f1d61", "#601d61", "#601e60", "#601e60", \
"#611e5f", "#611e5f", "#611e5f", "#611f5e", "#621f5e", "#621f5d", \
"#621f5d", "#631f5c", "#63205c", "#63205b", "#64205b", "#64205b", \
"#64205a", "#65215a", "#652159", "#652159", "#662158", "#662258", \
"#662257", "#672257", "#672256", "#682356", "#682356", "#682355", \
"#692355", "#692454", "#6a2454", "#6a2453", "#6a2453", "#6b2552", \
"#6b2552", "#6c2551", "#6c2651", "#6d2650", "#6d2650", "#6d264f", \
"#6e274f", "#6e274e", "#6f274e", "#6f284d", "#70284d", "#70284c", \
"#71294c", "#71294c", "#72294b", "#72294b", "#732a4a", "#732a4a", \
"#742b49", "#742b49", "#752b48", "#762c48", "#762c47", "#772c47", \
"#772d46", "#782d46", "#782d45", "#792e45", "#7a2e44", "#7a2f43", \
"#7b2f43", "#7b2f42", "#7c3042", "#7d3041", "#7d3041", "#7e3140", \
"#7f3140", "#7f323f", "#80323f", "#81333e", "#81333e", "#82333d", \
"#83343d", "#84343c", "#84353c", "#85353b", "#86363b", "#86363a", \
"#87373a", "#883739", "#893838", "#8a3838", "#8a3937", "#8b3937", \
"#8c3a36", "#8d3a36", "#8e3b35", "#8e3b35", "#8f3c34", "#903c34", \
"#913d33", "#923d32", "#933e32", "#943e31", "#943f31", "#953f30", \
"#964030", "#97412f", "#98412e", "#99422e", "#9a422d", "#9b432d", \
"#9c442c", "#9d442c", "#9e452b", "#9f452a", "#a0462a", "#a14729", \
"#a24729", "#a34828", "#a44928", "#a54927", "#a64a26", "#a74b26", \
"#a94b25", "#aa4c25", "#ab4d24", "#ac4d23", "#ad4e23", "#ae4f22", \
"#af4f22", "#b15021", "#b25120", "#b35220", "#b4521f", "#b5531f", \
"#b7541e", "#b8551d", "#b9551d", "#bb561c", "#bc571c", "#bd581b", \
"#be591a", "#c0591a", "#c15a19", "#c25b18", "#c45c18", "#c55d17", \
"#c75e17", "#c85e16", "#c95f15", "#cb6015", "#cc6114", "#ce6213", \
"#cf6313", "#d16412", "#d26511", "#d46611", "#d56610", "#d767f", \
"#d968f", "#da69e", "#dc6ae", "#dd6bd", "#df6cc", "#e16dc", "#e26eb", \
"#e46fa", "#e670a", "#e7719", "#e9728", "#eb738", "#ed747", "#ee756", \
"#f0776", "#f2785", "#f4794", "#f67a3", "#f77b3", "#f97c2", "#fb7d1", \
"#fd7e1", "#ff800"]
 return color_palatte
