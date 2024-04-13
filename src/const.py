yearToWave = {
        '2004/2005': 1,
        '2006/2007': 2,
        '2008/2009': 3,
        '2011/2012': 4,
        '2013': 5,
        '2015': 6,
        '2017': 7,
        '2019/2020': 8,
        '2024': 9
    }
waveToYear = {v:k for k,v in yearToWave.items()}

data_path = "static/data"


# HELP ITEMS FOR THE UI
helpColumnsNA = """
        By coching this option, you can decide of a threshold for the percentage of missing
        values in a column. Columns with a percentage of missing values above the threshold
        will be dropped from the dataset.
        """
helpExplicitNA = """
        By coching this option, missing values in categorical variables will be treated as a
        separate category. This can be useful when missing values are not missing at random.
        """
helpMissingCode = """
        By coching this option, the missing codes, such as "Don't know" or "Refusal", will be
        treated as NA values. Recommended if you don't know what to choose.
        """
helpDropNA = """
        By coching this option, all rows with at least one missing value will be dropped from
        the dataset. This is a simple and straightforward way to handle missing values, but
        it can lead to a significant loss of data.
        """
helpOutliers = """
        By coching this option, you can decide to remove outliers from the dataset. Outliers
        are defined as values that are too extreme compared to the rest of the data.
        """
helpZScore = """
        The Z-score is a measure of how many standard deviations a data point is from the mean.
        Data points with an absolute Z-score above a certain threshold are considered outliers.
        """
helpIQR = """
        The Interquartile Range (IQR) is a measure of statistical dispersion. You can decide
        to remove data points that are below Q1 - t * IQR or above Q3 + t * IQR, where t is a
        threshold you can choose.
        """
helpWave = """
        SHARE data have been collected by wave. The first wave was in 2004, and the most
        recent one in 2024. Select a wave to load the data for that year.
        """
helpColumns = """
        The data is organized in datasets, each containing a set of variables. Select the
        variables you want to load. The data will be loaded from the selected wave and the
        selected variables.
        """
helpTarget = """
        The target variable is the variable you want to predict. Select the variable you want
        to predict from the data.
        """
helpPredictors = """
        The predictor variables are the variables you want to use to predict the target variable.
        Select the variables you want to use as predictors.
        """
