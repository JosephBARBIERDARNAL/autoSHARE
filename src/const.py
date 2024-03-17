yearToWave = {
        '2004/2005': 1,
        '2006/2007': 2,
        '2008/2009': 3,
        '2011/2012': 4,
        '2013': 5,
        '2015': 6,
        '2017': 7,
        '2019/2020': 8
    }
waveToYear = {v:k for k,v in yearToWave.items()}

data_path = "static/data"


# HELP ITEMS FOR THE UI
helpExplicitNA = """
        By coching this option, missing values in categorical variables will be treated as a
        separate category. This can be useful when missing values are not missing at random.
        """
helpMissingCode = """
        By coching this option, the missing codes, such as "Don't know" or "Refusal", will be
        treated as NaN values. Recommended if you don't know what to choose.
        """
helpDropNA = """
        By coching this option, all rows with at least one missing value will be dropped from
        the dataset. This is a simple and straightforward way to handle missing values, but
        it can lead to a significant loss of data.
        """
helpWave = """
        SHARE data have been collected by wave. The first wave was in 2004, and the most
        recent one in 2019. Select a wave to load the data for that year.
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
