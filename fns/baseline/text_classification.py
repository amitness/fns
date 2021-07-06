from functools import partial
from typing import List, Optional

import optuna
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import ParameterGrid, cross_val_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from fns.decorators import to

__all__ = ["BaselineTextClassifier", "generate_grid"]


@to(list)
def generate_grid(grid, multi_label: bool = False):
    for grid_class, param_grid in grid.items():
        for p in ParameterGrid(param_grid):
            if multi_label and (
                grid_class
                in [LogisticRegression, SGDClassifier, MultinomialNB, BernoulliNB]
            ):
                yield OneVsRestClassifier(grid_class(**p))
            else:
                yield grid_class(**p)


def evaluate_trial(trial, x, y, cv, scoring, vectorizers, multi_label=False):
    model_class = trial.suggest_categorical(
        "model_class",
        [
            "LogisticRegression",
            "SGDClassifier",
            "DecisionTreeClassifier",
            "RandomForestClassifier",
            "DummyClassifier",
            "MLPClassifier",
        ],
    )
    if vectorizers is None:
        vectorizers = [TfidfVectorizer()]
    else:
        vectorizers += [TfidfVectorizer()]
    vectorizer_choices = {v.__class__.__name__: v for v in vectorizers}
    vectorizer_name = trial.suggest_categorical(
        "vectorizer_name", list(vectorizer_choices)
    )

    if vectorizer_name == "TfidfVectorizer":
        ngram_range = trial.suggest_int("ngram_range", 1, 3)
        vectorizer_params = {
            "ngram_range": (1, ngram_range),
            "stop_words": trial.suggest_categorical("stop_words", [None, "english"]),
            "analyzer": "word",
            "binary": trial.suggest_categorical("binary", [True, False]),
            "lowercase": trial.suggest_categorical("lowercase", [True, False]),
            "sublinear_tf": trial.suggest_categorical("sublinear_tf", [True, False]),
            "max_df": trial.suggest_discrete_uniform("max_df", 0.2, 1.0, 0.1),
            "strip_accents": trial.suggest_categorical(
                "strip_accents", ["unicode", None]
            ),
        }
        vectorizer = TfidfVectorizer(**vectorizer_params)
    else:
        vectorizer = vectorizer_choices[vectorizer_name]

    if model_class == "LogisticRegression":
        base_class = LogisticRegression
        params = {
            "C": trial.suggest_loguniform("C", 1e-5, 10),
            "class_weight": "balanced",
            "max_iter": 5000,
            "fit_intercept": trial.suggest_categorical("fit_intercept", [True, False]),
        }
    elif model_class == "SGDClassifier":
        base_class = SGDClassifier
        params = {
            "loss": trial.suggest_categorical("loss", ["hinge", "log"]),
            "penalty": trial.suggest_categorical("penalty", ["l1", "l2", "elasticnet"]),
            "alpha": trial.suggest_loguniform("alpha", 1e-5, 10),
            "class_weight": "balanced",
            "max_iter": 5000,
        }
    elif model_class == "DecisionTreeClassifier":
        base_class = DecisionTreeClassifier
        params = {"class_weight": "balanced"}
    elif model_class == "RandomForestClassifier":
        base_class = RandomForestClassifier
        params = {"class_weight": "balanced"}
    elif model_class == "MLPClassifier":
        base_class = MLPClassifier
        params = {
            "activation": trial.suggest_categorical(
                "activation", ["relu", "tanh", "identity", "logistic"]
            ),
            "solver": "adam",
            "alpha": trial.suggest_loguniform("alpha", 1e-4, 10),
            "early_stopping": trial.suggest_categorical(
                "early_stopping", [True, False]
            ),
        }
    else:
        base_class = DummyClassifier
        params = {
            "strategy": trial.suggest_categorical(
                "strategy", ["stratified", "most_frequent", "prior", "uniform"]
            )
        }

    model = base_class(**params)
    if multi_label and (base_class in [LogisticRegression, SGDClassifier]):
        model = OneVsRestClassifier(model)

    pipeline = Pipeline([("vectorizer", vectorizer), ("model", model)])

    return cross_val_score(pipeline, x, y, cv=cv, scoring=scoring).mean()


class BaselineTextClassifier:
    def __init__(self, study_name: str = "baseline", reset=False):
        if reset:
            import os

            os.remove(f"{study_name}.db")
        self.study = optuna.create_study(
            study_name=study_name,
            storage=f"sqlite:///{study_name}.db",
            direction="maximize",
            load_if_exists=True,
        )

    def fit(
        self,
        x: List[str],
        y,
        cv: int = 5,
        scoring: str = "f1_macro",
        multi_label: bool = False,
        vectorizers: Optional[List] = None,
        n_trials: Optional[int] = None,
        timeout: Optional[int] = None,
    ):
        optimize_function = partial(
            evaluate_trial,
            x=x,
            y=y,
            cv=cv,
            scoring=scoring,
            vectorizers=vectorizers,
            multi_label=multi_label,
        )
        self.study.optimize(optimize_function, n_trials=n_trials, timeout=timeout)
