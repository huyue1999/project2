import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.widgets import CheckButtons, Cursor

# ---------- Drawing ----------
def mypicture(x,X,y2,y2_label,y3,y3_label,y_tick = 2500):
    x_mean = np.mean(x)
    ma = max(list(y2)+list(y3))
    text = [str(X[n])+"\n"+"· "+str(y2_label)+": "+str(y2[n])+"\n"+"· "+str(y3_label)+": "+str(y3[n]) for n in range(len(x))]
    text2 = [str(X[n])+"\n"+"· "+str(y2_label)+": "+str(y2[n]) for n in range(len(x))]
    text3 = [str(X[n])+"\n"+"· "+str(y3_label)+": "+str(y3[n]) for n in range(len(x))]
    fig, ax = plt.subplots(figsize=(15, 8))
    li1, = plt.plot(x, y2, marker = '.', mec = 'w', mfc = 'w',ms = 5, c="red", lw=2, label='1',zorder=0)
    li2, = plt.plot(x, y3, marker = '.', mec = 'w', mfc = 'w',ms=5, c="orange",  lw=2, label='2',zorder=0)

    plt.xticks(x, list(X),rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    tick_spacing = 6
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(y_tick))
    plt.grid(axis="y")
    plt.subplots_adjust(top=0.8, bottom=0.2)
    ax.set_ylim(bottom=0.)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.title('New confirmed/suspected cases in China')

    vlines = []
    for i in range(len(x)):
        xy=(x[i],y2[i])
        line1 = plt.vlines(x[i], 0, ma, colors = "c", linestyles = "dashed",alpha=0,linewidth = 1.5)
        line2 = plt.vlines(x[i], 0, ma, colors = "lightgray", linestyles = "dashed",linewidth = 1.5,zorder=0)
        circle1 = plt.scatter(x[i], y2[i], color='w', marker='o', edgecolors='firebrick',s =50)
        circle2 = plt.scatter(x[i], y3[i], color='w', marker='o', edgecolors='gold',s =50)
        offset = 15
        bbox = dict(boxstyle="round", fc='w',ec = 'lightgray',linewidth = 1)
        annotation = plt.annotate(text[i], xy=(x[i], (np.random.random()+1)*(ma/3)), xytext=(offset, 0),
                                  textcoords='offset points', bbox=bbox,size=15) if x[i]<x_mean else plt.annotate(text[i], xy=(x[i], (np.random.random()+1)*(ma/3)),
                                                                                                                  xytext=(-23*offset, 0),textcoords='offset points', bbox=bbox,size=15)
        annotation2 = plt.annotate(text2[i], xy=(x[i], y2[i]), xytext=(offset, offset),
                                  textcoords='offset points', bbox=bbox,size=15) if x[i]<x_mean else plt.annotate(text2[i], xy=(x[i], y2[i]),
                                                                                                                  xytext=(-23*offset, offset),textcoords='offset points', bbox=bbox,size=15)
        annotation3 = plt.annotate(text3[i], xy=(x[i], y3[i]), xytext=(offset, offset),
                                  textcoords='offset points', bbox=bbox,size=15) if x[i]<x_mean else plt.annotate(text3[i], xy=(x[i], y3[i]),
                                                                                                                  xytext=(-23*offset, offset),textcoords='offset points', bbox=bbox,size=15)
        # 默认鼠标未指向时不显示标注信息
        annotation.set_visible(False)
        annotation2.set_visible(False)
        annotation3.set_visible(False)
        line2.set_visible(False)
        circle1.set_visible(False)
        circle2.set_visible(False)
        vlines.append([line1,line2,circle1,circle2,annotation,annotation2,annotation3])
    def on_move(event):
        visibility_changed = False
        for line1,line2,circle1,circle2,annotation,annotation2,annotation3 in vlines:
            should_be_visible = (line1.contains(event)[0] == True)
            if should_be_visible != line2.get_visible():
                visibility_changed = True
                line2.set_visible(should_be_visible)
                if li1.get_visible() == True and li2.get_visible() == True:
                    annotation.set_visible(should_be_visible)
                    circle1.set_visible(should_be_visible)
                    circle2.set_visible(should_be_visible)
                if li1.get_visible() == True and li2.get_visible() != True:
                    circle1.set_visible(should_be_visible)
                    annotation2.set_visible(should_be_visible)
                if li2.get_visible() == True and li1.get_visible() != True:
                    circle2.set_visible(should_be_visible)
                    annotation3.set_visible(should_be_visible)
        
        if visibility_changed:
            plt.draw()

            
    lines = [li1,li2]

    # Make checkbuttons with all plotted lines with correct visibility
    rax = plt.axes([0.8, 0.82, 0.1, 0.1])
    labels = [str(line.get_label()) for line in lines]
    visibility = [line.get_visible() for line in lines]
    check = CheckButtons(rax, labels, visibility)

    def func(label):
        index = labels.index(label)
        lines[index].set_visible(not lines[index].get_visible())
        plt.draw()


    check.on_clicked(func)
    on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)
    plt.show()
    
# ---------- main----------
file_path = 'cov_china.csv'
df_all = pd.DataFrame(pd.read_csv(file_path, encoding='gbk'))
df_all = df_all.set_index(pd.DatetimeIndex(pd.to_datetime(df_all.date)))
df_1 = df_all[:75]

X = df_1['date']
x = np.arange(0,len(X))

y2 = df_1["new_confirm"]
y3 = df_1["suspect"]

mypicture(x,X,y2,"The number of new confirmed cases",y3,"The number of new suspected cases",2500)
