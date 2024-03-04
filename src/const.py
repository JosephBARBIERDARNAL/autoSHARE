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