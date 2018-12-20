# Multivariate linear regression
Load an Excel file and calculate the linear regression and residuals for multiple input features
  
Before executing the script, the user need to modify the _InputFile_ variable to the desired Excel spreadsheet. The default reading mode will take the first row as the header and the first column as the index to a pandas dataframe.  
  
Once the data is successfully loaded, it will prompt the user to select _**one**_ feature and the title for _**Y axis**_, and then the _**one or more**_ features and the title for _**X axis**_, and finally the title of the output graph.  
  
The output will be two figures. The first one is the either the single input or multi-variate linear regression depending on how many input features for _**X axis**_. There will be annotation about the coefficient of determination and the equation of the linear model. The second figure is the residuals. It will be useful to determine whether there is systematic error in the linear model.  
  
**Dependencies**: _numpy_, _pandas_, _scikit-learn_, and _matplotlib_.
