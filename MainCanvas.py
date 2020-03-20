from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import ProcessData
import pandas as pd
import numpy as np
import math

# class cls:
#     def __init__(self):
#         self.y = APP_UI.y
class Canvas(FigureCanvas):
    # def _init(self):
    #     import APP_UI
    #     self.app_ui = APP_UI()
    def __init__(self, parent=None, width=10, height=10, dpi=80):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # self.axes.transData.transform_point([x,y])

    # def onclick(event):
    #     print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #           ('double' if event.dblclick else 'single', event.button,
    #            event.x, event.y, event.xdata, event.ydata))
    #
    # cid = FigureCanvas.mpl_connect(onclick('button_press_event'))

#do we need the following two methods?
    def spaghettiPlot(self):
        import pandas as pd
        import numpy as np
        data = ProcessData.importData('data0.csv')['SMOIS']
        self.axes.contour(np.array(data).reshape(699, 639))
        self.draw()

    def filledContour(self):

        data = ProcessData.importData('data0.csv')['SMOIS']
        self.contourf = self.axes.contourf(np.array(data).reshape(699, 639))
        self.draw()

    def clearPlt(self):
        self.fig.clear()
        self.axes = self.figure.add_subplot(111)
        self.draw()
    def clearPlt2(self):
        self.fig.clear()
        self.axes = self.figure.add_subplot(111)
    def plot_contour(self,data,level):
        self.axes.contour(np.array(data['levels']).reshape(699, 639), level, colors=['g', 'r', 'y'])
        self.draw()

    # def setTextbasedonIsoline(self):
    #     value1 = self.horizontalSlider_isoline1.value() / 100
    #     value2 = self.horizontalSlider_isoline2.value() / 100
    #     value3 = self.horizontalSlider_isoline3.value() / 100
    #     return value1,value2,value3

    def generate_images(self,filtered_graph,data,levels,column,alpha_cf = 0.7,flag_dir = 0,flag_content = 0,magnitude = 0,
                        cmap='Colormap 1',cline='copper',arrowscale = 'Linear', cvector_high2low = 'Black', cvector_low2high = 'Blue', line_opacity = 0.4,line_width=1.5):
        # b1 = 4
        # print(b1)
        #import APP_UI
        cmap_dict =  {'Colormap 1':['#7fc97f','#beaed4','#fdc086','#ffff99'],
        'Colormap 2':['#1b9e77','#d95f02','#7570b3','#e7298a'],
        'Colormap 3':['#a6cee3','#1f78b4','#b2df8a','#33a02c'],
        'Colormap 4':['#e41a1c','#377eb8','#4daf4a','#984ea3'],
        'Colormap 5' :['#66c2a5','#fc8d62','#8da0cb','#e78ac3'],
        'Colormap 6':['#8dd3c7','#ffffb3','#bebada','#fb8072']}

        #cvector_high2low_dict = {'Black':['#000000'], 'Blue': ['#0000FF'], 'Red': ['#ff0000'], 'Green': ['#00ff00']}
        self.clearPlt2()
        filtered_graph = filtered_graph[
            ['level', 'node_x', 'node_y', 'path', 'aggregated_weight', 'actual_weight', 'normalized', 'res_dir_x',
             'res_dir_y',
             'res_dir_x_1', 'res_dir_y_1', 'resultant','mag']]

        data['levels'] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())
        self.axes.contour(np.array(data['levels']).reshape(699, 639), levels, cmap=cline, alpha=line_opacity,linewidths=line_width)
        if(flag_content == 0 or flag_content == 1):
            self.axes.contourf(np.array(data['levels']).reshape(699, 639), levels, colors=cmap_dict[cmap], alpha=alpha_cf)
            # import APP_UI
            # value1 = APP_UI.horizontalSlider_isoline1.value() / 100
            # value2 = APP_UI.horizontalSlider_isoline2.value() / 100
            # value3 = APP_UI.horizontalSlider_isoline3.value() / 100
            # a = '0' + ' - ' + str(value1)
            # b = str(value1) + ' - ' + str(value2)
            # c = str(value2) + ' - ' + str(value3)
            # d = str(value3) + ' - ' + '100'

            # b=4
            # print(b)
            # import APP_UI
            # # from APP_UI import setIsoLineSlider2Listener
            # a = APP_UI.setIsoLineSlider2Listener()
            # print (a)
            # plt.colorbar()
            # proxy = [plt.Rectangle((0, 0), 1, 1, fc= 'black')]
            # texts = ["Data Description"]
            # plt.legend(proxy,texts)
            # plt.show()
            # self.axes.colorbar(np.array(data['levels']).reshape(699, 639), shrink=0.9)
            # proxy1 = plt.Rectangle((0, 0), 1, 1, fc=cmap_dict[cmap].index('0'),
            #                        alpha=0.7, linewidth=3, label='foo')
            # self.axes.patches += proxy1
            # colors = ["#78c3f1","#78c3f1","#78c3f1","#78c3f1"]
            colors= cmap_dict[cmap]
            #string1 = self.setTextbasedonIsoline()
            texts = ["0 - Isoline1", "Isoline1 - Isoline2", "Isoline2 - Isoline3", "Isoline3 - 100"]
            # texts = [a, b, c, d]
            # print (len(texts))
            patches = [mpatches.Patch(color=colors[i],label = "{:s}".format(texts[i]))for i in range(len(texts))]
            self.axes.legend(handles = patches,bbox_to_anchor = (0.5,0.01),loc = 'lower center', ncol=4)
            # plt.show()
        #self.axes[0][-1].legend()

        filtered_graph = filtered_graph[filtered_graph['normalized'] >= 0.01]
        df1 = filtered_graph[(filtered_graph['resultant'] >= 0) & (filtered_graph['mag'] > magnitude)].copy()
        df2 = filtered_graph[(filtered_graph['resultant'] < 0) & (filtered_graph['mag'] > magnitude)].copy()

# Exponential, Logarithmic and Normalized value finding
#         df1.loc[:, 'exp_x_1'] = np.exp(df1['res_dir_x_1'])
#         df1.loc[:, 'exp_y_1'] = np.exp(df1['res_dir_y_1'])
#         df1.loc[:, 'log_x_1'] = (np.log(df1['res_dir_x_1'])).values
#         df1.loc[:, 'log_y_1'] = (np.log(df1['res_dir_y_1'])).values
        x1 = df1['res_dir_x_1'].min()
        y1 = df1['res_dir_x_1'].max()
        x2 = df1['res_dir_y_1'].min()
        y2 = df1['res_dir_y_1'].max()
        df1.loc[:, 'nor_x_1'] = ((df1['res_dir_x_1'] - x1)/(y1-x1)).values
        df1.loc[:, 'nor_y_1'] = ((df1['res_dir_y_1'] - x2)/(y2-x2)).values
#
#         df2.loc[:, 'exp_x_1'] = np.exp(df2['res_dir_x_1'])
#         df2.loc[:, 'exp_y_1'] = np.exp(df2['res_dir_y_1'])
#         df2.loc[:, 'log_x_1'] = (np.log(df2['res_dir_x_1'])).values
#         df2.loc[:, 'log_y_1'] = (np.log(df2['res_dir_y_1'])).values
        x3 = df2['res_dir_x_1'].min()
        y3 = df2['res_dir_x_1'].max()
        x4 = df2['res_dir_y_1'].min()
        y4 = df2['res_dir_y_1'].max()
        df2.loc[:, 'nor_x_1'] = ((df2['res_dir_x_1'] - x3) / (y3 - x3)).values
        df2.loc[:, 'nor_y_1'] = ((df2['res_dir_y_1'] - x4) / (y4 - x4)).values
#########
        #scale = math.exp(filtered_graph['mag'].min()+20)
        if(flag_content == 0 or flag_content == 2):
            if(arrowscale == 'Linear'):
                if(flag_dir == 0 or flag_dir==1):
                    print("0 1 linear")
                    self.axes.quiver(df1['node_x'], df1['node_y'], df1['res_dir_x_1'], df1['res_dir_y_1'],
                        width=0.0009, headwidth=5.5, headlength=5.5, color= cvector_high2low, scale=1000)
                if (flag_dir == 0 or flag_dir == 2):
                    self.axes.quiver(df2['node_x'], df2['node_y'], df2['res_dir_x_1'], df2['res_dir_y_1'],
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_low2high, scale=1000)
            elif(arrowscale == 'Exponential'):
                if (flag_dir == 0 or flag_dir == 1):
                    print("0 1 Exponential")
                    self.axes.quiver(df1['node_x'], df1['node_y'], df1['res_dir_x_1'], df1['res_dir_y_1'],
                        width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_high2low, scale=200)

                if (flag_dir == 0 or flag_dir == 2):
                    self.axes.quiver(df2['node_x'], df2['node_y'], df2['res_dir_x_1'], df2['res_dir_y_1'],
                                 width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_low2high, scale=200)

            elif (arrowscale == 'Logarithmic'):
                if (flag_dir == 0 or flag_dir == 1):
                    print("0 1 Exponential")
                    self.axes.quiver(df1['node_x'], df1['node_y'], df1['res_dir_x_1'], df1['res_dir_y_1'],
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_high2low, scale=10000)

                if (flag_dir == 0 or flag_dir == 2):
                    self.axes.quiver(df2['node_x'], df2['node_y'], df2['res_dir_x_1'], df2['res_dir_y_1'],
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_low2high, scale=10000)

            elif (arrowscale == 'Normalized'):
                if (flag_dir == 0 or flag_dir == 1):
                    print("0 1 Exponential")
                    self.axes.quiver(df1['node_x'], df1['node_y'], df1['nor_x_1'], df1['nor_y_1'],
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_high2low, scale=100)

                if (flag_dir == 0 or flag_dir == 2):
                    self.axes.quiver(df2['node_x'], df2['node_y'], df2['nor_x_1'], df2['nor_y_1'],
                                     width=0.0009, headwidth=5.5, headlength=5.5, color=cvector_low2high, scale=100)
        self.draw()
#import APP_UI