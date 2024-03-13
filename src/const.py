yearToWave = {
        2004: 1,
        2006: 2,
        2008: 3,
        2011: 4,
        2013: 5,
        2015: 6,
        2017: 7,
        2019: 8
    }
waveToYear = {v:k for k,v in yearToWave.items()}

dataPath = "../SHARE/data/"


# HELP ITEMS FOR THE UI
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