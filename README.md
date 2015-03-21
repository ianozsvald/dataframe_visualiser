# dataframe_visualiser
Make simple high-level visualisations of a Pandas dataframe to help when starting new data projects

 * Summarise single variables
 * Summarise each variable and its dependency on a boolean column
 * Show high-level overview of a subsampled set of cells

This is a Python 3 project (and with some tiny edits it would run in Python 2.7).

To run:

    >>> # assuming IPython and Python 3.4
    >>> import visualise_dataframe
    >>> visualise_dataframe.summarise(df)  # draw single-variable plot
    >>> visualise_dataframe.summarise(df, dependent_col='some_col_name_in_df')  # draw dependent-variable plot

If you run the script then the example will load the Kaggle Titanic competition's `train.csv` file and will draw a single-variable plot.

## Examples

Using the Kaggle Titanic example http://www.kaggle.com/c/titanic-gettingStarted data set we can draw each variable independently: 

![Single variable](https://github.com/ianozsvald/dataframe_visualiser/blob/master/example_titanic_single_variable.png)

We can also ask it to draw each variable when dependent on a boolean (in the case against `Survived`): 

![Dependent variable](https://github.com/ianozsvald/dataframe_visualiser/blob/master/example_titanic_dependent_variable.png)

Finally with `show_cells` we can subsample a set of rows and show their dtypes and whether they're NaN or not:

![show_cells](https://github.com/ianozsvald/dataframe_visualiser/blob/master/example_titanic_show_cells.png)
