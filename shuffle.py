

iris = datasets.load_iris()
X = iris.data
y = iris.target
n_classes = np.unique(y).size


rfc = RandomForestClassifier(n_estimators = 1500, max_features =7, oob_score = True, class_weight = 'balanced')
cv = StratifiedKFold(10)

score, permutation_scores, pvalue = permutation_test_score(
    rfc, data_array, data_array_y, scoring="roc_auc", cv=cv, n_permutations=100)