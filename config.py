# INSTAGRAM REEL SCRAPPER SETTINGS
INST_REAL_SCRAPER_ACTOR_ID = 'xMc5Ga1oCONPmWJIa'

reels_input_data = {
    "username": ['_top_niylon'],
    "resultsLimit": 1000,
    "scrapePosts": False,
    "scrapeReels": True,
    "scrapeStories": False
}

stdev_hot_treshold = 2
stdev_very_successful_treshold = 0.75

def z_categorize(z):
    if z > 2.0:
        return '🔥viral hit'
    elif z > 1.0:
        return '✅very successful'
    elif z > 0.2:
        return 'successful'
    elif z >= -1.0:
        return 'average'
    else:
        return 'weak'

top_reels_count = 15
bad_reels_count = 5
