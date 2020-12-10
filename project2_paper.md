<h1 style="text-align: center"> Improving Line Charts for Confirmed and Suspected COVID-19 Cases in China </h1>
<div style="text-align: center"><small>Author: Yue Hu, Yuhe Zhang, Xiyuan Chang</small></div>
<div style="text-align: center"><small>Student Id: 320180939790, 320180939580, 320180940570</small></div>
<div style="text-align: center"><small>Date: December 10, 2020</small></div>

___
<div style="text-align: center"><b>Statement of Academic Integrity</b></div>

*We hereby acknowledge that thr thesis submitted is a product of our own indepent research, and that all the data, statistics, picture and materials are reliable and trustworthy, and that all the previous research and sources are appropriately marked in the thesis, and that the intellectual property of the thesis belongs to the school. We are fully aware of the legal effect of this statement.*

<div style="text-align: center"><b>Abstract</b></div>

*123*

**Keywords:** *123*

___
- [1. Introduction](#1-introduction)
    - [1.1 Background and meaning](#11-background-and-meaning)
    - [1.2 Visual story](#12-visual-story)
- [2. Visual data preprocessing](#2-visual-data-preprocessing)
    - [2.1 Data mining](#21-data-mining)
- [3. Information visualization design](#3-information-visualization-design)
    - [3.1 Problems and improvements](#31-problems-and-improvements)
    - [3.2 Concrete implementation](#32-concrete-implementation)
- [4. Result show](#4-result-show)
- [5. Summary and problems](#5-summary-and-problems)
    - [5.1 Summary](#51-summary)
    - [5.2 Problems](#52-problems)
- [6. Reference](#6-reference)

____
## 1. Introduction

### 1.1 Background and meaning

### 1.2 Visual story

____
## 2. Visual data preprocessing

### 2.1 Data mining
____
## 3. Information visualization design
### 3.1 Problems and improvements
1. We want both lines to be displayed at the same time and separately. Because the two lines cover each other badly when displayed at the same time, it will seriously affect readers' reading and understanding. But it is necessary to show both polylines because there is a comparable relationship between the number of newly confirmed and suspected cases.
2. Change the X-axis date display so that the date is displayed vertically, and change the X-axis scale to make the scale distribution less crowded. Skewed dates reduce readability. Due to the large amount of data, it is decided to increase the scale distance of the coordinate axis, which is easy for readers to read.
3. Change the type and size of the markers on the line. The circle marker on the line are too large to cover the line itself. In order not to cover the line, so that readers can see the details of the line carefully, we decided to use white dots instead of circles.
4. Remove unwanted data. At the end of the two lines, the values of the data all tend to 0. We believe that such an excessive amount of data is useless, because the trend of the epidemic situation has been basically reflected by the previous data. Too many data points will cause congestion of the marks and reduce readability.
5. Change the line color to increase contrast.The color of the two lines is similar, the contrast is not obvious and is too light to be easily recognized, which is not friendly to some readers with visual impairme.
6. Add dynamically interactive annotations to each data point. Consider that the user may need real data for each data point, but there are too many data points and each one will be overwritten by displaying comments. So we decided to use interactive annotation displays.
### 3.2 Concrete implementation
- The lines cover each other badly.
  - Add a custom check button using the Matplotlib interaction module [matplotlib.widgets]("https://matplotlib.org/3.1.1/gallery/widgets/check_buttons.html") so that users can select the graphics for different labels to display. 
  ```python
    rax = plt.axes([0.8, 0.82, 0.1, 0.1])
    labels = [str(line.get_label()) for line in lines]
    visibility = [line.get_visible() for line in lines]
    check = CheckButtons(rax, labels, visibility)

    def func(label):
        index = labels.index(label)
        lines[index].set_visible(not lines[index].get_visible())
        plt.draw()


    check.on_clicked(func)
  ```
- The scale spacing of coordinate axes is too small and X-axis scale labels are not displayed vertically.
  - Customize the scale range of the coordinate axis using [matplotlib.ticker]("https://matplotlib.org/api/ticker_api.html"):  
  ```python
  ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))  
  ax.yaxis.set_major_locator(ticker.MultipleLocator(y_tick))
  ```
  - Set ticks on the X-axis to rotate by 90 degrees:
  ```python
  plt.xticks(x, list(X),rotation=90, fontsize=10)
  ```
- The circle marker on the line are too large to cover the line itself.
  - Changing the type, color and size of the marker:
  ```python
  li1, = plt.plot(x, y2, marker = '.', mec = 'w', mfc = 'w',ms = 5, c = 'red', lw=2, label='1',zorder=0)
  li2, = plt.plot(x, y3, marker = '.', mec = 'w', mfc = 'w',ms=5, c = 'orange', lw=2, label='2',zorder=0)
  ```
- Too many data points lead to congestion of markers, covering the original lines.
  - Useless data were deleted. In the data of the second half of the year, the number of patients fluctuated around 0, which was no longer helpful for us to analyze the development of the epidemic, so they were deleted.
- The lines in the original picture are too light in color and the color contrast is not strong.
  - Change the color of the lines, and be careful to be color - blind.
- In the original image, the reader is not able to obtain specific numbers on the number of cases and suspected confirmed cases on each date, which is unfriendly.
  - We add dynamic interactive annotations to each data point using [set_visible]("https://matplotlib.org/api/_as_gen/matplotlib.artist.Artist.set_visible.html"). When the mouse moves to the vertical line of x axis corresponding to the point, the annotation will be displayed, which can effectively display the data and prevent overwriting caused by too many annotations.
  ```python
  vlines = []
  for i in range(len(x)):
      xy=(x[i],y2[i])
      line1 = plt.vlines(x[i], 0, ma, colors = "c", linestyles = "dashed",alpha=0,linewidth = 1.5)
      line2 = plt.vlines(x[i], 0, ma, colors = "lightgray", linestyles = "dashed",linewidth = 1.5,zorder=0)
      circle1 = plt.scatter(x[i], y2[i], color='w', marker='o', edgecolors='firebrick',s =50)
      circle2 = plt.scatter(x[i], y3[i], color='w', marker='o', edgecolors='gold',s =50)
      offset = 15
      bbox = dict(boxstyle="round", fc='w',ec = 'lightgray',linewidth = 1)
      annotation = plt.annotate(text[i], xy=(x[i], (np.random.random()+1)*(ma/3)), xytext=(offset, 0),textcoords='offset points', bbox=bbox,size=15) if x[i]<x_mean else plt.annotate(text[i], xy=(x[i], (np.random.random()+1)*(ma/3)), xytext=(-23*offset, 0),textcoords='offset points', bbox=bbox,size=15)
      annotation2 = plt.annotate(text2[i], xy=(x[i], y2[i]), xytext=(offset, offset),textcoords='offset points', bbox=bbox,size=15) if x[i]<x_mean else plt.annotate(text2[i], xy=(x[i], y2[i]),xytext=(-23*offset, offset),textcoords='offset points', bbox=bbox,size=15)
      annotation3 = plt.annotate(text3[i], xy=(x[i], y3[i]), xytext=(offset, offset),textcoords='offset points', bbox=bbox,size=15) if x[i]<x_mean else plt.annotate(text3[i], xy=(x[i], y3[i]),xytext=(-23*offset, offset),textcoords='offset points', bbox=bbox,size=15)
      #The default mouse pointer does not display the annotation information
      annotation.set_visible(False)
      annotation2.set_visible(False)
      annotation3.set_visible(False)
      line2.set_visible(False)
      circle1.set_visible(False)
      circle2.set_visible(False)  
      vlines.append([line1,line2,circle1,circle2,annotation,annotation2，annotation3])
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
  on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)
  ```
_____
## 4. Result show
1. When the mouse moves, the annotation is displayed.
![image](img(1).png)
2. Click the check button in the upper right corner to implement interactive drawing.
![image](img(2).png)
![image](img(3).png)
3. Use the ipywidgets package's method widgets to zooming in and out of images.(This method idle embedded, but jupyter does not)
![image](img(4).png)
![image](img(5).png)
***You can see these directly in the video Manual***
_____
## 5. Summary and problems
### 5.1 Summary
Our code outputs an interactive matlotlib image, implements interactive check buttons and mouse-following annotations, rocessing the data and changing the color of the lines rejected cognitive deficits and color blindness. And the result basically improves the readability of the original image.
### 5.2 Problems
As a result of jupyter does not support interactive matplotlib, jupyter default output images are static, can not be enlarged and other operations, need to add an extra magic instruction `% matplotlib notebook`. And use `import ipyWidgets as Widgets` to make CheckButtons display properly, so there are some differences between the code of jupyter and my_picture.py files. Also due to problems with the jupyter mechanism, it cannot properly display CheckButtons by calling functions in the my_picture.py file.
____
## 6. Reference
>https://matplotlib.org/3.1.1/gallery/widgets/check_buttons.html
>https://matplotlib.org/api/ticker_api.html
>https://matplotlib.org/api/_as_gen/matplotlib.artist.Artist.set_visible.html