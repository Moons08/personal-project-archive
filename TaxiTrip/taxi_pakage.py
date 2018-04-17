import pandas as pd
import numpy as np
import scipy as sp
import holidays

import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.graphics import regressionplots
from statsmodels.stats.stattools import durbin_watson

import sklearn as sk
from sklearn.model_selection import KFold

import datetime as dt
from patsy import dmatrix

import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
sns.set()
sns.set_style("whitegrid")
sns.set_color_codes(palette="muted")


def strptime(x):
    return dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
def date_to_zero(x):
    datezero = dt.datetime(2016, 1, 1, 0, 0, 1) # 기준
    return int((x-datezero).days)
def time_to_zero(x):
    datezero = dt.datetime(2016, 1, 1, 0, 0, 1) # 기준
    return int((x-datezero).seconds)
def week_num(x):
    return int(x.weekday()) + 1 # erase 0


def holiday(x):
    us_holidays = holidays.US(state='NY', years=2016)
    if x in us_holidays:
        return 1
    else:
        x = x.weekday()
    if x > 4:
        return 0
    else:
        return 0

def get_features(data, start_num=0, end_num=None, scale=False):
    """
    from data, choose the columns to use OLS
    (default is all columns)

    """
    features = list(data.columns)[start_num:end_num]
    feature_n = len(features)

    if scale:
        features = list(map(lambda x: "scale({})".format(x), features))
        features = " + ".join(features)

    else:
        features = " + ".join(features)

    return feature_n, features

def erase_outlier_np(result, data, category=False, dropped=False):
    """
    get the fitted model result, then erase outliers in data,
    by Fox' Outlier Recommendation.

    return arranged data, dropped data(when True)
    """

    influence = result.get_influence()

    if category:
        fox_cr = 4 / (len(data) - result.df_model + 1)
    else:
        fox_cr = 4 / (len(data) - result.df_model)

    cooks_d2, pvals = influence.cooks_distance
    idx = np.where(cooks_d2 > fox_cr)[0]

    dropped_data = data.iloc[idx]
    data = data.drop(data.index[idx])
    data.reset_index(drop=True, inplace=True)

    if dropped:

        return data, dropped_data

    return data

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    """

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c

    return km

def storage(result, result_sets, remark) :
    """
    test storage
    """
    result.summary()
    put = {
        "R-square" :round(result.rsquared, 3),
        "AIC" : round(result.aic, 3),
        "BIC" : round(result.bic, 3),
        "Pb(Fstatics)" : round(result.f_pvalue, 3),
        "Pb(omnibus)" : round(result.diagn['omnipv'], 3),
        "Pb(jb)" : round(result.diagn['jbpv'], 3),
        "Cond.No." : round(result.diagn['condno'], 3),
        "Dub-Wat": round(durbin_watson(result.wresid), 3),
        "Remarks" : remark,
    }
    result_sets.loc[len(result_sets)] = put

def RMSLE(prediction, real):
    """
    check root mean squared logarithmic error
    """
    logarithmic_error = np.log1p(prediction) - np.log1p(real)
    score = np.sqrt(1/len(real) *np.sum(logarithmic_error**2))
    return score

def cross_validater(formula, dataset, times, target_log=False, shuffle=True, r_seed=0):

    score_set = []
    result_sets = pd.DataFrame(
                        columns = ["R-square", "AIC", "BIC", "Cond.No.",
                                    "Pb(Fstatics)", "Pb(omnibus)",
                                    "Pb(jb)", "Dub-Wat","Remarks"
                                    ])

    if shuffle == False:
        cv = KFold(n_splits=times, shuffle=False, random_state=r_seed)
    else:
        cv = KFold(n_splits=times, shuffle=True, random_state=r_seed)

    for i, (train_index, test_index) in enumerate(cv.split(dataset)):
        model =  sm.OLS.from_formula(formula, dataset.iloc[train_index])
        result = model.fit()
        storage(result, result_sets, formula)

        if target_log:
            prediction = np.exp(result.predict(dataset.iloc[test_index]))
        else:
            prediction = result.predict(dataset.iloc[test_index])

        real = dataset['trip_duration'].iloc[test_index]
        score_set.append(RMSLE(prediction, real))

    return score_set, result_sets
