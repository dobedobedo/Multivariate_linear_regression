#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 16:09:29 2018

@author: uqytu1
"""

import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoLocator, AutoMinorLocator, FormatStrFormatter

InputFile = '/home/uqytu1/Documents/PPC_calculation_colour.xlsx'

def Plot_Line(Xs, Y, XLabel, YLabel, Title):
    
    #define linear regression function
    LinearModel = linear_model.LinearRegression()
    
    #calculate linear regression
    LinearModel.fit(Xs, Y)
    
    #calculate coefficiant of determination R2
    R2 = LinearModel.score(Xs, Y)
    
    #calculate multivariate X
    if len(LinearModel.coef_) > 1:
        liney = LinearModel.predict(Xs)
        XData = (LinearModel.coef_ * Xs).sum(axis=1) + LinearModel.intercept_
        linex = XData
        equation = '$y='
        for _idx in range(len(LinearModel.coef_)):
            if _idx == 0:
                equation = ''.join([equation, '({:.2e})x_{}'.format(LinearModel.coef_[_idx], _idx+1)])
            else:
                equation = ''.join([equation, '{:+.2e}(x_{})'.format(LinearModel.coef_[_idx], _idx+1)])
        equation = ''.join([equation, '{:+.2f}$'.format(LinearModel.intercept_)])
    else:
        XData = Xs
        equation = '$y=({:.2e})x{:+.2f}$'.format(LinearModel.coef_[0], LinearModel.intercept_)
        linex = np.linspace(min(XData)*0.5, max(XData)*1.5, len(XData)*2).reshape(-1, 1)
        liney = LinearModel.predict(linex)
    
    #Configure figure
    plt.figure(1)
    plt.gca().set_ylim(min(Y)*0.9,max(Y)*1.1)
    plt.gca().set_xlim(min(XData)*0.9, max(XData)*1.1)
    plt.subplot(111).spines['bottom'].set_linewidth(2)
    plt.subplot(111).spines['left'].set_linewidth(2)
    plt.subplot(111).xaxis.set_major_locator(AutoLocator())
    plt.subplot(111).xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.subplot(111).xaxis.set_minor_locator(AutoMinorLocator())
    plt.xlabel(XLabel, size = 20, labelpad = 10)
    plt.xticks(size = 14)
    plt.ylabel(YLabel, size = 20, labelpad = 10)
    plt.yticks(size = 14)
    plt.title(Title, size = 26).set_y(1.05)
    plt.grid(which='major', alpha=0.6, ls='-')
    plt.grid(which='minor', alpha=0.3, ls='--')
    
    #Plot data
    plt.plot(XData, Y, 'bo', label='Sample Data')
    plt.plot(linex, liney, 'k-', label='Linear Regression')
    plt.annotate('{}\n$R^2={:.2f}$'.format(equation, R2), 
                 xy=(0.05, 0.8), xytext=(0, 0), xycoords=('axes fraction', 'axes fraction'),
                 textcoords='offset points',
                 verticalalignment='bottom', horizontalalignment='left', 
                 fontsize=14, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.legend(loc='lower center',bbox_to_anchor = (0.76, 0.02), fancybox = True, 
               fontsize=16, markerscale=1, ncol = 1).draggable()
    
    Plot_residuals(XData, Y, LinearModel)

    plt.show()
    
def Plot_residuals(X, Y, model):
    Predicted_Y = model.predict(X)
    residuals = Y - Predicted_Y
    plot_X = np.linspace(1, len(X)+1, len(X)).reshape(-1, 1)
    line_X = np.linspace(0, max(plot_X)+1, len(plot_X)).reshape(-1, 1)
    zero_line = np.zeros(line_X.shape)
    plt.figure(2)
    plt.gca().set_ylim(min(residuals)*0.9, max(residuals)*1.1)
    plt.gca().set_xlim(min(line_X), max(line_X))
    plt.subplot(111).spines['bottom'].set_linewidth(2)
    plt.subplot(111).spines['left'].set_linewidth(2)
    plt.xlabel('Sample number', size = 20, labelpad = 10)
    plt.xticks(size = 14)
    plt.ylabel('residual', size = 20, labelpad = 10)
    plt.yticks(size = 14)
    
    plt.plot(plot_X, residuals.reshape(-1, 1), 'ro', label='Sample residual')
    plt.plot(line_X, zero_line, 'k-', label='Zero line')
    plt.legend(loc='lower center',bbox_to_anchor = (0.76, 0.02), fancybox = True, 
               fontsize=16, markerscale=1, ncol = 1).draggable()
    
def ParseInputNumbers(selects):
    try:
        selected_index = set()
        for select in selects:
            if '-' in select:
                start, end = select.split('-')
                for i in range(int(start), int(end)+1):
                    selected_index.add(i-1)
                        
            else:
                selected_index.add(int(select)-1)
        return selected_index
    except ValueError:
        print('Can\'t recognise input. Please try again!')
        return False
    
if __name__ == '__main__':
    # Load the Excel file, with the first column as index and first row as header
    data = pd.read_excel(InputFile, index_col=0)
    
    # Get all available features
    Items = list(data.keys())
    
    # Prompt user for one feature as y-axis data
    print('Input the one feature as y-axis data:')
    for index, item in enumerate(Items):
        print('{:>2}: {:<}'.format(index+1, item))
    while True:
        try:
            YFeature = Items[int(input('>>> ').split()[0]) - 1]
            break
        except IndexError:
            continue
    print('What is the title of y-axis:')
    YLabel = input('>>> ')
    
    # Prompt user for features as x-axis data
    print('Input the feature(s) as x-axis data:')
    for index, item in enumerate(Items):
        print('{:>2}: {:<}'.format(index+1, item))
    print('e.g.: "1-3" to select 1 to 3; 1 3 to select 1 and 3')
    
    while True:
        selects = input('>>> ').split()
        selected_index = ParseInputNumbers(selects)
        if selected_index:
            break
        else:
            continue
        
    selected_features = list()
    for index in selected_index:
        selected_features.append(Items[index])
        
    print('What is the title of x-axis:')
    XLabel = input('>>> ')
    
    # Prompt user for the title of graph
    print('What is the title of the graph:')
    Title = input('>>> ')
    
    # Calculate the multi-variate linear regression and plot the graph
    Plot_Line(data.loc[:, selected_features].values, data.loc[:, YFeature].values, XLabel, YLabel, Title)
    