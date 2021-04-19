from fns.cluster import *
from fns.constants import *
from fns.dataframe import *
from fns.decorators import *
from fns.exceptions import *
from fns.json_encoders import *
from fns.metrics import *
from fns.model_selection import *
from fns.preprocessing import *
from fns.streamlit_utils import *
from fns.text import *
from fns.vision import *
from fns.fns import *
from fns.plot import *
from sklearn.datasets import (make_classification,
                              make_regression)
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, ExtraTreeClassifier, ExtraTreeRegressor
from sklearn.linear_model import (LogisticRegression,
                                  LogisticRegressionCV,
                                  LinearRegression,
                                  SGDRegressor,
                                  SGDClassifier,
                                  RidgeClassifier,
                                  RidgeClassifierCV,
                                  Lasso,
                                  LassoCV,
                                  ElasticNet,
                                  Ridge,
                                  RidgeCV,
                                  )
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.neighbors import (KNeighborsClassifier,
                               RadiusNeighborsClassifier,
                               RadiusNeighborsRegressor)
from sklearn.svm import SVC, LinearSVC, LinearSVR, SVR, OneClassSVM
from sklearn.ensemble import (RandomForestClassifier,
                              RandomForestRegressor,
                              ExtraTreesClassifier,
                              ExtraTreesRegressor,
                              BaggingClassifier,
                              BaggingRegressor,
                              AdaBoostClassifier,
                              AdaBoostRegressor,
                              GradientBoostingClassifier,
                              GradientBoostingRegressor)
from sklearn.cluster import KMeans, AffinityPropagation, AgglomerativeClustering
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import PCA, TruncatedSVD, NMF, LatentDirichletAllocation
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.model_selection import StratifiedKFold, KFold, ParameterGrid, cross_val_predict
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, HashingVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.preprocessing import (normalize,
                                   scale,
                                   minmax_scale,
                                   RobustScaler,
                                   MinMaxScaler,
                                   MaxAbsScaler,
                                   OneHotEncoder,
                                   FunctionTransformer,
                                   PowerTransformer,
                                   StandardScaler,
                                   MultiLabelBinarizer,
                                   LabelBinarizer,
                                   Normalizer,
                                   PolynomialFeatures,
                                   )
from sklearn.multiclass import (OneVsOneClassifier,
                                OneVsRestClassifier)
from sklearn.metrics import (accuracy_score,
                             precision_score,
                             recall_score,
                             confusion_matrix,
                             silhouette_score,
                             classification_report,
                             f1_score,
                             fbeta_score,
                             mean_squared_error,
                             mean_absolute_error,
                             hamming_loss)
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity, euclidean_distances
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
from itertools import chain, product, permutations, combinations, islice
from functools import lru_cache
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path
import math

imports = """
import seaborn as sns
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import Dataset, TensorDataset, DataLoader
from torch.utils.tensorboard import SummaryWriter
import nltk
import spacy
from textblob import TextBlob
import ipywidgets as widgets
from pprint import pprint
from typing import List, Dict, Tuple, Union, Optional
""".strip().splitlines()

for import_line in imports:
    try:
        exec(import_line)
    except Exception:
        pass
