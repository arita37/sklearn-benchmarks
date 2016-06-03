import sys
import pandas as pd
import numpy as np
import itertools
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import make_pipeline
import itertools

dataset = sys.argv[1]

# Read the data set into memory
input_data = pd.read_csv(dataset, compression='gzip', sep='\t')

for (loss, learning_rate, n_estimators,
     max_depth, max_features) in itertools.product(['deviance', 'exponential'],
                                                   np.arange(0.1, 1.01, 0.1),
                                                   [500],
                                                   [None],
                                                   [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 'sqrt', 'log2']):
    features = input_data.drop('class', axis=1).values.astype(float)
    labels = input_data['class'].values

    try:
        # Create the pipeline for the model
        clf = make_pipeline(StandardScaler(),
                            GradientBoostingClassifier(loss=loss,
                                                       learning_rate=learning_rate,
                                                       n_estimators=n_estimators,
                                                       max_depth=max_depth,
                                                       max_features=max_features))
        # 10-fold CV scores for the pipeline
        cv_scores = cross_val_score(estimator=clf, X=features, y=labels, cv=10)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        continue

    param_string = ''
    param_string += 'loss={},'.format(loss)
    param_string += 'learning_rate={},'.format(learning_rate)
    param_string += 'n_estimators={},'.format(n_estimators)
    param_string += 'max_depth={},'.format(max_depth)
    param_string += 'max_features={}'.format(max_features)

    for cv_score in cv_scores:
        out_text = '\t'.join([dataset.split('/')[-1][:-7],
                              'GradientBoostingClassifier',
                              param_string,
                              str(cv_score)])

        print(out_text)
        sys.stdout.flush()