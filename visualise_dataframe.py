import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import math


def summarise(df, subsample_rows=50, dependent_col=None):
    """Visually summarise with some opinions a sample of rows from dataframe"""
    f = plt.figure()

    if dependent_col:
        if df[dependent_col].dtype != np.bool_:
            assert False, "not allowed"
        print("Showing how values depend on", dependent_col)

    print("Sampling {} rows from df".format(subsample_rows))
    df = df.ix[np.random.choice(df.index, subsample_rows, replace=False)]
    cols = df.columns

    #cols = ['PassengerId', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
    grid_cols = min(3, len(cols))
    grid_rows = math.ceil(len(cols) / grid_cols)

    # make a grid, iterate over each grid entry
    gs = plt.GridSpec(grid_rows, grid_cols)
    for gs_idx, grid_spec in enumerate(list(gs)):
        if gs_idx == len(cols):
            # break if our grid is bigger than the number of items that fit in
            # it
            break
        col_name = cols[gs_idx]
        print("Plotting colum:", gs_idx, col_name)
        sp = plt.subplot(grid_spec)
        series = df[col_name]
        # count nbr nulls for later dispaly
        nbr_null = sum(series.isnull())
        # extract not-null values for graphing
        series_notnull_indices = series.isnull() == False
        nbr_not_null = sum(series_notnull_indices)
        series_notnull = series[series_notnull_indices]
        value_counts = series_notnull.value_counts()
        all_values_unique = len(value_counts) == len(series_notnull)
        if nbr_not_null > 0:
            if dependent_col:
                ax = sns.pointplot(series_notnull, df[dependent_col][series_notnull_indices])
            else:
                subsample_values_to = 5
                if all_values_unique and len(series_notnull) > subsample_values_to:
                    # subsample just a few for these unique items
                    step_every = int(len(series_notnull) / subsample_values_to)
                    series_notnull = series_notnull[0::step_every]
                    value_counts = series_notnull.value_counts()
                if series.dtype == np.int_ or \
                series.dtype == np.float_ or \
                series.dtype == np.bool_:
                    ax = sns.barplot(x=series_notnull)
                if series.dtype == np.object_:
                    ax = sns.barplot(x=series_notnull)

            # rotate labels by 30 degrees
            labels = [lbl.get_text() for lbl in ax.get_xticklabels()]
            def clean_label(lbl):
                if len(lbl) > 10:
                    lbl = lbl[:10] + "..."
                return lbl
            labels = [clean_label(lbl) for lbl in labels]
            ax.set_xticklabels(labels=labels, rotation=30)
        else:
            plt.xlabel(col_name)

        # try to explain the plot a little
        title = "{} nulls, {}".format(nbr_null, series.dtype)
        if all_values_unique:
            title += ", subsampled as all values unique"
        sp.set_title(title)

    plt.show()
    plt.tight_layout()
    return f


def show_cells(df, subsample_rows=40):
    """Try to give a "view from a balloon" on the whole dataframe"""
    if len(df) > subsample_rows:
        print("Sampling {} rows from df".format(subsample_rows))
        df = df.ix[np.random.choice(df.index, subsample_rows, replace=False)]
    cells = np.zeros((df.shape))
    for col_nbr, dtype in enumerate(df.dtypes):
        colour = None
        if dtype == np.int_:
            colour = 0
        if dtype == np.float_:
            colour = 1
        if dtype == np.bool_:
            colour = 2
        if dtype == np.object_:
            colour = 3
        # TODO deal with timedelta64/datetime64?
        if colour >= 0:
            cells[:, col_nbr] = colour
        else:
            print("NOTE - unhandled", col_nbr, dtype, df.columns[col_nbr])

        col_name = df.columns[col_nbr]
        col = df[col_name]
        if col.dtype != np.object_:
            for row_nbr, value in enumerate(col):
                if np.isnan(col.values[row_nbr]):
                    cells[row_nbr, col_nbr] = 10
    plt.matshow(cells, cmap=matplotlib.cm.Spectral_r)
    plt.xticks(range(len(df.columns)), df.columns, rotation=45, ha="left")
    return cells


if __name__ == "__main__":
    if True:
        # DEMO work with Kaggle Titanic training data
        df = pd.io.parsers.read_table("kaggle_titanic_train.csv", sep=",")
        fig = summarise(df)
        #cells = show_cells(df)

    if False:
        # DEMO work with Kaggle Titanic training data and a dependent variable
        df = pd.io.parsers.read_table("kaggle_titanic_train.csv", sep=",")
        df['Survived'] = df['Survived'].astype(np.bool_)
        fig = summarise(df, dependent_col="Survived")

    #if False:
        ## work with PyData London growth data
        #df = pd.io.parsers.read_table("PyData-London-Meetup_Member_List_on_03-17-15.xls")
        ##summarise(df)
        #df['Intro'] = df['Intro'].map(lambda x: x == "Yes")  # boolean-ise
        #df['Attended_'] = df['Meetups attended'].map(lambda x: x > 0)  # boolean-ise
        #summarise(df, dependent_col="Attended_")

        ## plot cumulative sum of members at pydata
        #if True:
            #import dateutil.parser as dt_parser
            #df['Joined Group on'] = df['Joined Group on'].map(lambda x: dt_parser.parse(x, dayfirst=False))
            #df['Member growth'] = 1
            #df.set_index('Joined Group on', inplace=True)
            #df.sort(inplace=True)  # sort on the index
            #df['Member growth'].cumsum().plot()


    if False:
        # Try to maximize the window and use a tight_layout
        # but NOTE you might have to do tight_layout() manually to actually make it
        # render cleanly (it is very OS/system/speed dependent!)
        if plt.get_backend() == "Qt4Agg":
            # maximize: http://stackoverflow.com/a/22418354/18688
            figManager = plt.get_current_fig_manager()
            #was_maximized = figManager.window.isMaximized()
            figManager.window.showMaximized()
            # ask for a tight_layout, now the window is maximised
            plt.tight_layout()
