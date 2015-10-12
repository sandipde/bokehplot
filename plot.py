#!/usr/bin/env python
# (c) 2015 Sandip De
# mail: 1sandipde@gmail.com
# A python script to generate interactive plotsfor website
#==============================================================
import argparse
from bokeh.plotting import output_file, figure, show, hplot
from bokeh.models import ColumnDataSource, CustomJS, Rect
from bokeh.models import HoverTool
from copy import copy
from math import exp

def main(file,pcol,psize,image_prefix,title=''):

 file=file[0]
 with open(file) as f:
    last_pos = f.tell()
    li=f.readline().strip()
    if li.startswith("#"):
      f.seek(last_pos)
      header= [x for x in f.readline().split()]
      data = [[float(x) for x in line.split()] for line in f]
    else:
      f.seek(last_pos)
      data = [[float(x) for x in line.split()] for line in f]
    
 column=[]
# setting first coloumn = index in case only one column needs to be plotted
 col=[]
 for index in range (len(data)):
   col.append(index)
 column.append(col)
# Now append all the columns
 for jframe in range (len(data[0])):
   col=[]
   for iframe in range(len(data)):
     try: 
       col.append(data[iframe][jframe])
     except:  # in case some columns are incomplete 
       col.append(0)
   column.append(col)
# setting last but one column to be 0 in case no color column is provided
 col=[]
 for index in range (len(data)):
   col.append(1)
 column.append(col)
# setting last column to be 1 in case no size column is provided
 col=[]
 for index in range (len(data)):
   col.append(1)
 column.append(col)

 icol=pcol[0]
 try:
  jcol=pcol[1]
  try:
    kcol=pcol[2]
    try:
      scol=pcol[3]
    except:
      scol=len(column)-1
  except:
    kcol=len(column)-2
    scol=len(column)-1
 except:
   jcol=0
   kcol=len(column)-2
   scol=len(column)-1
# set up color and size column properly
 cval=copy(column[kcol][:])
 mincolor=min(cval)
 maxcolor=max(cval)
 #print mincolor,maxcolor
 difcolor=maxcolor-mincolor
 if difcolor==0:difcolor=1 
 for i in range(len(cval)): cval[i]=(cval[i]-mincolor)/difcolor
 #print min(cval),max(cval)
 radii=copy(column[scol][:])
 minr=min(radii)
 for i in range(len(radii)):
    radii[i]=psize+100*psize*(radii[i]-minr)

 output_file(file+".html", title=file, mode="cdn")

 image=[]
 for i in range (len(data)):
    image.append(image_prefix+str(i+1)+".png")
    
 datasrc = ColumnDataSource(
        data=dict(
            x=column[icol],
            y=column[jcol],
            z=column[kcol],
            size=column[scol],
            imgs =image
        )
    )

 if (image_prefix !=""):
   hover = HoverTool(
        tooltips="""
            <div>
            <div>
                <img
                    src="@imgs" height="142" alt="@imgs" width="142"
                    style="float: left; margin: 0px 0px 0px 0px;"
                    border="0"
                ></img>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">value=@z</span>
                <span style="font-size: 15px; color: #966;">[$index]</span>
            </div>
        </div>
        """
    )
 else:
   hover = HoverTool(
           tooltips = [
             ("index: ", "$index"),
             ("(x,y)", "($x, $y)"),
            ]
        )

 TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select,tap,save"
# maxval=max(column[kcol])
# minval=min(column[kcol])
# minval=abs(minval)
# if minval>maxval:maxval=minval
# width=max(column[icol])-min(column[icol])
# print maxval
 colors = ["#%02x%02x%02x" % (exp(-(r-0.99)**2/0.1)*255,200*exp(-(r-0.7)**2/0.05) ,255*exp(-(r-0.4)**2/0.1)) for r, g in zip(cval,cval)]
 source = ColumnDataSource({'x': [], 'y': [], 'width': [], 'height': []})

 jscode="""
        var data = source.get('data');
        var start = range.get('start');
        var end = range.get('end');
        data['%s'] = [start + (end - start) / 2];
        data['%s'] = [end - start];
        source.trigger('change');
     """


 if title=='': title=file
 p1 = figure(title=title,tools=[TOOLS,hover])
# p1.responsive=True
 #p1.scatter(column[icol],column[jcol],radius=width*0.01,fill_color=colors, fill_alpha=0.6, line_color=None)
 p1.circle('x','y',source=datasrc,size=radii,fill_color=colors, fill_alpha=0.8, line_color=None)
 p1.x_range.callback = CustomJS(
        args=dict(source=source, range=p1.x_range), code=jscode % ('x', 'width'))
 p1.y_range.callback = CustomJS(
        args=dict(source=source, range=p1.y_range), code=jscode % ('y', 'height'))
 p1.title_text_color = "firebrick"
 p1.title_text_font = "times"
 p1.title_text_font_style = "italic"
 p2 = figure(tools='')
# p2.responsive=True
 p2.circle('x','y',source=datasrc,size=radii,fill_color=colors, fill_alpha=0.8, line_color=None)
# p2.outline_line_width = 7
# p2.outline_line_alpha = 0.3
# p2.outline_line_color = "navy"
 rect = Rect(x='x', y='y', width='width', height='height', fill_alpha=0.1,
            line_color='black', fill_color='black')
 p2.add_glyph(source, rect)
 layout = hplot(p1, p2)
 show(layout)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="A python script to generate interactive web graphics using bokeh")
  parser.add_argument("filename", nargs=1,help="filename")
  parser.add_argument("-u",  type=str, default='1:2:3:4',help="columns of the data file to plot eg. -u 1:2:3:4 to plot 1st column vs 2nd column. color the data using 3rd coloumn and 4th column to varry the point size (optional)")
  parser.add_argument("-ps",  type=float, default='1',help="point size")
  parser.add_argument("-t",  type=str, default='',help="Title of the plot")
  parser.add_argument("--image_prefix",  type=str, default='',help="prefix of the image file name to display on mouse hover")
  args = parser.parse_args()
  pcol = map(int,args.u.split(':'))
  main(args.filename,pcol,args.ps,args.image_prefix,title=args.t)
