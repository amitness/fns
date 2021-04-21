from typing import List

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import ParameterGrid, GridSearchCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from fns.model_selection import view_result_table
import numpy as np
import os

__all__ = ['MultiLabelTextClassifier']


def generate_grid(grid):
    for grid_class, param_grid in grid.items():
        for p in ParameterGrid(param_grid):
            if grid_class in [LogisticRegression, SGDClassifier]:
                yield OneVsRestClassifier(grid_class(**p))
            else:
                yield grid_class(**p)


grid = {
    'models': {KNeighborsClassifier: {'n_neighbors': [5]},
               LogisticRegression: {'class_weight': ['balanced'],
                                    'max_iter': [5000],
                                    'C': np.linspace(0.001, 1, 50),
                                    'fit_intercept': [True, False]},
               SGDClassifier: {
                   'loss': ['hinge', 'log'],
                   'penalty': ['l1', 'l2', 'elasticnet'],
                   'alpha': np.logspace(-4, 1, 5),
                   'class_weight': ['balanced'],
                   'max_iter': [5000]
               },
               DecisionTreeClassifier: {
                   'class_weight': ['balanced']
               },
               RandomForestClassifier: {
                   'class_weight': ['balanced']
               }
               },
    'vectorizer': {TfidfVectorizer: {
        'ngram_range': [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3)],
        'stop_words': [None, 'english'],
        'analyzer': ['word'],
        'binary': [True, False],
        'max_df': [1.0, 0.75, 0.5, 0.25],
        'strip_accents': ['unicode', None],
    }}
}


class MultiLabelTextClassifier:
    def __init__(self,
                 models: List = None,
                 vectorizers: List = None,
                 vectorizers_default=generate_grid(grid['vectorizer']),
                 models_default=generate_grid(grid['models'])):
        self.models = [] if not models else models
        self.vectorizers = [] if not vectorizers else vectorizers
        self.params = {'vectorizer': [*vectorizers_default,
                                      *self.vectorizers],
                       'model': [*models_default,
                                 *self.models],
                       }

    def fit(self,
            x_train,
            y_train,
            cv=3,
            scoring='f1_samples',
            memory=('/dev/shm/joblib' if os.name == 'posix' else None)):
        pipeline = Pipeline([('vectorizer', TfidfVectorizer()),
                             ('model', OneVsRestClassifier(LogisticRegression()))],
                            memory=memory)
        hpo = GridSearchCV(pipeline,
                           self.params,
                           cv=cv,
                           scoring=scoring,
                           n_jobs=-1,
                           verbose=1,
                           refit=True)
        hpo.fit(x_train, y_train)
        print(f'Best F1-score: {hpo.best_score_}')
        print(f'Best Estimator: {hpo.best_estimator_}')
        df = view_result_table(hpo)
        df.to_csv('grid-search.csv', index=False)
        return df
