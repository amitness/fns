from functools import partial
from typing import List

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import ParameterGrid, GridSearchCV, RandomizedSearchCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from fns.decorators import to
from fns.model_selection import view_result_table
import numpy as np
import os

__all__ = ['BaselineTextClassifier']


@to(list)
def generate_grid(grid,
                  multi_label: bool = False):
    for grid_class, param_grid in grid.items():
        for p in ParameterGrid(param_grid):
            if multi_label and (grid_class in [LogisticRegression, SGDClassifier, MultinomialNB, BernoulliNB]):
                yield OneVsRestClassifier(grid_class(**p))
            else:
                yield grid_class(**p)


grid = {
    'models': {LogisticRegression: {'class_weight': ['balanced'],
                                    'max_iter': [5000],
                                    'C': np.logspace(-4, 0, 50),
                                    'fit_intercept': [True, False],
                                    'solver': ['lbfgs']},
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
        'lowercase': [True, False],
        'max_df': [1.0, 0.75, 0.5, 0.25],
        'strip_accents': ['unicode', None],
    }}
}

baseline_grid = {
    'naive_bayes': {
        'models': {MultinomialNB: {}
                   },
        'vectorizer': {CountVectorizer: {
            'stop_words': [None, 'english'],
            'strip_accents': ['unicode', None],
        }}
    },
    'bernoulli_nb': {
        'models': {BernoulliNB: {}
                   },
        'vectorizer': {CountVectorizer: {
            'stop_words': [None, 'english'],
            'binary': [True],
            'strip_accents': ['unicode', None],
        }}
    },
    'dummy': {
        'models': {DummyClassifier: {
            'strategy': ['stratified', 'most_frequent', 'prior', 'uniform']
        }},
        'vectorizer': {CountVectorizer: {}
                       }
    },
    'knn': {
        'models': {KNeighborsClassifier:
                       {'n_neighbors': [1, 5]}
                   },
        'vectorizer': {TfidfVectorizer: {}}
    },
}


class BaselineTextClassifier:
    def __init__(self,
                 models: List = None,
                 vectorizers: List = None,
                 default_vectorizer: bool = True,
                 default_model: bool = True,
                 multi_label=False):
        self.multi_label = multi_label
        self.models = [] if not models else models
        self.vectorizers = [] if not vectorizers else vectorizers
        generate = partial(generate_grid, multi_label=multi_label)

        if default_vectorizer:
            self.vectorizers += generate(grid['vectorizer'])
        if default_model:
            self.models += generate(grid['models'])

        self.params = []
        for model_name, model_grid in baseline_grid.items():
            self.params.append({'vectorizer': [*generate(model_grid['vectorizer'])],
                                'model': [*generate(model_grid['models'])],
                                })

        if self.vectorizers and self.models:
            self.params.append({'vectorizer': self.vectorizers,
                                'model': self.models,
                                })

    def fit(self,
            x_train,
            y_train,
            cv=3,
            scoring=None,
            memory=('/dev/shm/baseline' if os.name == 'posix' else None),
            search='grid',
            n_iter: int = 10):
        if scoring is None:
            scoring = 'f1_samples' if self.multi_label else 'f1_macro'
        classifier_pipeline = Pipeline([('vectorizer', TfidfVectorizer()),
                                        ('model', OneVsRestClassifier(LogisticRegression()))],
                                       memory=memory)

        common_params = dict(cv=cv,
                             verbose=1,
                             refit=True,
                             scoring=scoring,
                             n_jobs=-1)

        if search == 'grid':
            hpo = GridSearchCV(classifier_pipeline,
                               param_grid=self.params,
                               **common_params)
        else:
            hpo = RandomizedSearchCV(classifier_pipeline,
                                     param_distributions=self.params,
                                     n_iter=n_iter,
                                     **common_params)

        hpo.fit(x_train, y_train)
        print(f'Best F1-score: {hpo.best_score_}')
        print(f'Best Estimator: {hpo.best_estimator_}')
        scores_df = view_result_table(hpo)
        return scores_df
