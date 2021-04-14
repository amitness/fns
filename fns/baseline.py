import tempfile
from shutil import rmtree
from typing import List, Union

from joblib import Memory
from sklearn.decomposition import TruncatedSVD, NMF, PCA
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.model_selection import ParameterGrid, GridSearchCV, RandomizedSearchCV
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC, LinearSVC

from fns.model_selection import view_result_table


def text_classification_baseline(x_train: List[str],
                                 y_train: List[Union[str, int]],
                                 search_type='grid',
                                 n_iter: int = 10):
    """
    Train classic baseline pipelines for text classification.

    Args:
        x_train: List of texts
        y_train: List of labels
        search_type: 'grid' or 'random'
        n_iter: Number of iterations for random search.

    Returns:
        Pandas DataFrame sorted by best scoring configurations.
    """
    temporary_location = tempfile.mkdtemp()
    memory = Memory(location=temporary_location, verbose=0)

    classifier_pipeline = Pipeline([
        ('vectorization', TfidfVectorizer()),
        ('dimensionality_reduction', 'passthrough'),
        ('model', GaussianNB())
    ], memory=memory)

    params = list(ParameterGrid({'stop_words': ['english', None],
                                 'lowercase': [True, False],
                                 'analyzer': ['word', 'char'],
                                 'binary': [True, False],
                                 'strip_accents': [None, 'ascii'],
                                 'ngram_range': [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]}))

    vectorizers = ([CountVectorizer(**p) for p in params]
                   + [TfidfVectorizer(**p) for p in params]
                   + [HashingVectorizer()])

    grid = {
        'vectorization': [*vectorizers],
        'model': [LogisticRegression(class_weight='balanced', max_iter=5000),
                  RidgeClassifier(class_weight='balanced', max_iter=5000),
                  GaussianNB(),
                  BernoulliNB(),
                  SVC(),
                  LinearSVC(max_iter=5000)],
        'dimensionality_reduction': [TruncatedSVD(2), PCA(0.9), NMF(2), 'passthrough']
    }

    common_params = dict(cv=10,
                         verbose=1,
                         refit=True,
                         scoring='f1_macro',
                         n_jobs=-1)

    if search_type == 'grid':
        hpo = GridSearchCV(classifier_pipeline,
                           param_grid=grid,
                           **common_params)
    else:
        hpo = RandomizedSearchCV(classifier_pipeline,
                                 param_distributions=grid,
                                 n_iter=n_iter,
                                 **common_params)
    hpo.fit(x_train, y_train)
    print(f'Best F1-score: {hpo.best_score_}')
    print(f'Best Estimator: {hpo.best_estimator_}')
    memory.clear(warn=False)
    rmtree(temporary_location)
    return view_result_table(hpo)
