"""
This file contains the help messages for the different widgets.
"""

HELPCOLUMNSNA = """
        By coching this option, you can decide of a threshold for the percentage of missing
        values in a column. Columns with a percentage of missing values above the threshold
        will be dropped from the dataset.
        """
HELPEXPLICITNA = """
        By coching this option, missing values in categorical variables will be treated as a
        separate category. This can be useful when missing values are not missing at random.
        """
HELPMISSINGCODE = """
        By coching this option, the missing codes, such as "Don't know" or "Refusal", will be
        treated as NA values. Recommended if you don't know what to choose.
        """
HELPDROPNA = """
        By coching this option, all rows with at least one missing value will be dropped from
        the dataset. This is a simple and straightforward way to handle missing values, but
        it can lead to a significant loss of data.
        """
HELPOUTLIERS = """
        By coching this option, you can decide to remove outliers from the dataset. Outliers
        are defined as values that are too extreme compared to the rest of the data.
        """
HELPZSCORE = """
        The Z-score is a measure of how many standard deviations a data point is from the mean.
        Data points with an absolute Z-score above a certain threshold are considered outliers.
        """
HELPIQR = """
        The Interquartile Range (IQR) is a measure of statistical dispersion. You can decide
        to remove data points that are below Q1 - t * IQR or above Q3 + t * IQR, where t is a
        threshold you can choose.
        """
HELPWAVE = """
        SHARE data have been collected by wave. The first wave was in 2004, and the most
        recent one in 2024. Select a wave to load the data for that year.
        """
HELPCOLUMNS = """
        The data is organized in datasets, each containing a set of variables. Select the
        variables you want to load. The data will be loaded from the selected wave and the
        selected variables. At the moment, the maximum number of variables you can select is 10.
        """
HELPUPLOADCONFIG = """
        Here you can drop your configAutoSHARE.json file that you may have downloaded when using the
        app. If you lost this file, you will have to fill all parameters again.
        """
HELPTARGET = """
        Select the target variable you want to predict. This variable will be removed from the
        dataset and used as the target variable in the prediction model.
        """
HELPPREDICTORS = """
        Select the predictor variables you want to use in the prediction model. These variables
        will be used to predict the target variable.
        """
