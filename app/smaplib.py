#from bokeh.io import output_notebook
from bokeh.layouts import layout,row
#output_notebook()
import numpy as np
import pandas as pd

class smap:
    import numpy as np
    import pandas as pd 
    from bokeh.palettes import Spectral6
    from bokeh.palettes import Spectral6,Inferno256,Viridis256,Greys256,Magma256,Plasma256
    def __init__(self, name='smapdata'):
        self.name = name
        self.data = []    # creates a new empty list 
        self.columns = []
        self.pd=pd.DataFrame(self.data,columns=self.columns)
        
    def add_data(self,data,columns=[]):
        self.data=data
        ncol=len(data[0])
        self.columns=columns
        self.check_columns()
        self.pd=pd.DataFrame(self.data,columns=self.columns)
        
    def read_data(self,filename):
        self.data=np.loadtxt(filename)
        self.get_columns(filename)
        self.pd=pd.DataFrame(self.data,columns=self.columns)
        
    def read(self,filename,sep='\s+',**kwargs):
        self.pd=pd.read_csv(filename,sep=sep,**kwargs)
        self.data=self.pd.values
        self.columns=self.pd.columns
        
    def write(self,filename='',sep='\t',**kwargs):
        if (filename==''):filename=self.name+'-COLVAR.dat'
        self.pd.to_csv(filename,sep='\t',index=False) 

    def read_properties(self,propfile,sep='\s+',**kwargs):
        prop=pd.read_csv(propfile,sep=sep,**kwargs)
        if (len(prop) != len(self.data)): 
            print "data length and property length mismtch"
            pass
        df=self.pd
        self.pd=pd.concat([df,prop],axis=1)
        self.data=self.pd.values
        self.columns=self.pd.columns
        
    def get_columns(self,file):
        with open(file) as f:
            last_pos = f.tell()
            li=f.readline().strip()
            if li.startswith("#"):
                self.columns=li.split()[1:]

            else:
                pcount=len(li.split())
                for i in range(pcount):
                    self.columns.append["prop_"+str(i+1)]
        self.check_columns()
        
    def check_columns(self):
        ncol=len(self.data[0])
        if (len(self.columns)< ncol):
            pcount=len(self.columns)
            for i in range(pcount,ncol):
                self.columns.append("col_"+str(i+1))
        self.columns=self.columns[:ncol]

    def normalize(self,v):
    	norm=np.linalg.norm(v)
    	if norm==0: 
    	   return v
    	v=v/norm
    	return v-min(v)

    def bkplot(self,x,y,color='None',radii='None',ps=20,minps=0,alpha=0.8,pw=600,ph=400,palette='Inferno256',title='',**kwargs):
        from bokeh.layouts import row, widgetbox,column
        from bokeh.models import HoverTool,TapTool,FixedTicker,Circle
        from bokeh.models import CustomJS, Slider,ColorBar,HoverTool,LinearColorMapper, BasicTicker
        from bokeh.plotting import figure
        from bokeh.palettes import Spectral6,Inferno256,Viridis256,Greys256,Magma256,Plasma256
        from bokeh.models import LogColorMapper, LogTicker, ColorBar,BasicTicker,LinearColorMapper
        import pandas as pd
        if (title==''): title=self.name
        data=self.pd
        COLORS=locals()[palette]
        proplist=[]
        for prop in data.columns:
            if prop not in ["CV1","CV2","Cv1","Cv2","cv1","cv2","colors","radii"]: proplist.append((prop,'@'+prop))
        TOOLS="resize,crosshair,pan,wheel_zoom,reset,tap,save,"
        hover = HoverTool(names=["mycircle"],
                tooltips=[
                    ("index", "$index"),
                    ("(x,y)", "($x, $y)")
                ]
            )
        for prop in proplist:
             hover.tooltips.append(prop)
        plot=figure(title=title,plot_width=pw,active_scroll="wheel_zoom", plot_height=ph,tools=[TOOLS,hover],**kwargs)
        initial_circle = Circle(x='x', y='y')
        selected_circle = Circle(fill_alpha=1, fill_color="colors", size=ps)
        nonselected_circle = Circle(fill_alpha=0.7,fill_color='colors',line_color=None)
        if radii == 'None':
            r=[ps for i in range(len(data))]
            data['radii']=r
        else:
            r=[val for val in data[radii]]
            rn=normalize(r)
            rad=[minps+ps*np.sqrt(val) for val in rn ]
            data['radii']=rad
            
        if color == 'None':
           c = ["#31AADE" for i in range(len(data))]
           data['colors']=c
           plot.circle(x,y,source=data,size='radii',fill_color='colors', fill_alpha=alpha, line_color=None,name="mycircle")
           renderer = plot.select(name="mycircle")
           renderer.selection_glyph = selected_circle
           renderer.nonselection_glyph = nonselected_circle
           return plot
        else:
            groups = pd.cut(data[color].values, len(COLORS))
            c = [COLORS[xx] for xx in groups.codes]
            data['colors']=c
            plot.circle(x,y,source=data,size='radii',fill_color='colors', fill_alpha=alpha, line_color=None,name="mycircle")
            renderer = plot.select(name="mycircle")
            renderer.selection_glyph = selected_circle
            renderer.nonselection_glyph = nonselected_circle
            color_mapper=LinearColorMapper(palette, low=data[color].min(), high=data[color].max())
            colorbar = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(),label_standoff=12, border_line_color=None, location=(0,0))
            plot.add_layout(colorbar, 'left')
            return plot


class Distance_matrix:
    import numpy as np
    import pandas as pd 

    
    def __init__(self, name='distance-matrix'):
        self.name = name
        self.data = []    # creates a new empty list 
        self.filename=''
        self.colvar=[]
    def read(self,filename):
        self.filename=filename
        self.data=np.loadtxt(filename)
        
    def plot(self,width=12,height=9,**kwargs):
        import seaborn as sns; sns.set(style="ticks", color_codes=True)
        import matplotlib.pyplot as plt
        f, ax = plt.subplots(figsize=(width, height))
        title='Distance Matrix for: '+self.name
        ax.set(title=title)
        sns.heatmap(self.data,square=True,**kwargs)
        plt.show()
    
    def histogram(self,width=8,height=6,**kwargs):
        import seaborn as sns; sns.set(style="ticks", color_codes=True)
        import matplotlib.pyplot as plt
        f, ax = plt.subplots(figsize=(width, height))
        title='Histogram for: '+self.name
        ax.set(title=title)
        sns.distplot(self.data.flatten(),**kwargs)
        plt.show()

    def histogram_with_sigmoid(self,sigma=0.3,aa=6.0,bb=6.0,Interactive=True):
        n,m = self.data.shape
        a = self.data.copy()
        rangea = (np.amin(a),np.amax(a))
        nbin = int((rangea[1]- rangea[0])/2e-3)
        hist, bins = np.histogram(a, bins=nbin)
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        b = np.true_divide(hist, np.amax(hist))
        # print 'Max of the distribution is at x={:.3f}'.format(center[np.argmax(b)])
        #  print 'A good sigma could be at sigma={:.3f}'.format(0.8*center[np.argmax(b)])

        if Interactive is True:
           histogram=self.plot_hist_sigmoid_interactive(center,b,sigma,aa,bb)
        else:
           fig, ax1 = plt.subplots(1)
           ax1.bar(center, b, align='center', width=width,color='#006D9C',linewidth=0)
           ax1.grid()
           plt.show()
        return histogram

    def plot_hist_sigmoid_interactive(self,center,hist,sigma,a,b):
        from bokeh.layouts import row, widgetbox,column
        from bokeh.models import CustomJS, Slider,ColorBar,HoverTool,LinearColorMapper, BasicTicker
        from bokeh.plotting import figure, ColumnDataSource,show,reset_output,output_file
        from bokeh.models.widgets import Select
        import matplotlib.pylab as plt
        from bokeh.io import output_notebook
        from bokeh.palettes import Spectral6,Inferno256,Viridis256,Greys256,Magma256,Plasma256
        from bokeh.models import LogColorMapper, LogTicker, ColorBar,BasicTicker,LinearColorMapper
        output_notebook()
        from bokeh.embed import notebook_div
        from bokeh.palettes import Spectral6,Inferno256,Viridis256,Greys256,Magma256,Plasma256
        from bokeh.models import LogColorMapper, LogTicker, ColorBar,BasicTicker,LinearColorMapper
        plot = figure(y_range=(0,1), plot_width=400, plot_height=200)
        plot.line(x=center,y=hist,line_color='#EF1735',line_width=2)
        #   a=6.;b=3.;sigma=0.5;
        x = np.linspace(0, 1, 500)
        y = 1.-np.power(1.+(np.power(2.,(a/b))-1.)*np.power(x/sigma,a),(-b/a))

        datasource = ColumnDataSource(data=dict(xs=x, ys=y))

        plot.line('xs', 'ys', source=datasource, line_width=2, line_alpha=0.8)

        callback = CustomJS(args=dict(source=datasource), code="""
           var data = source.data;
           var a = a.value;
           var b = b.value;
           var sigma = sigma.value;
           x = data['xs']
           y = data['ys']
           for (i = 0; i < x.length; i++) {
               y[i] = 1.-Math.pow(1.+(Math.pow(2.,(a/b))-1.)*Math.pow(x[i]/sigma,a),(-b/a));
           }
           source.trigger('change');
        """)

        a_slider = Slider(start=1., end=20., value=a, step=1.,title="a", callback=callback)
        callback.args["a"] = a_slider

        b_slider = Slider(start=1., end=20., value=b, step=1.,title="b", callback=callback)
        callback.args["b"] = b_slider

        sigma_slider = Slider(start=0.001, end=1., value=sigma, step=.001,title="sigma", callback=callback)
        callback.args["sigma"] = sigma_slider


        layout = row(plot,widgetbox(a_slider, b_slider, sigma_slider))
        # layout = widgetbox(a_slider, b_slider, sigma_slider)
        #output_file("slider.html", title="sl/home/de/bin/sketch-map.shider.py example")
        return layout
        #   show(layout,notebook_handle=True);

        
    def smap(self,sigma,a,b):
        simfile=self.filename
        sim=self.data
        n=len(sim)
        prefix=simfile+"smap-"+str(sigma)+'-'+str(a)+''+str(b)
        get_ipython().system(u'./sketch-map.sh $n $simfile $prefix $sigma $a $b >log')
        get_ipython().system(u'rm -f $prefix*.gmds_* $prefix*.imds $prefix*.ismap global.*')
        cv=np.loadtxt(prefix+'.gmds')
        self.colvar=cv

