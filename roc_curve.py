
shaper = rfc.oob_decision_function_[:, 1]
test_y = results.race_w



fpr = dict()
tpr = dict()
roc_auc = dict()
random_indices = permutation(black.index)
test_cutoff = math.floor(black.shape[0]/4)
test_black = black.loc[random_indices[test_cutoff:]]
cv_black = black.loc[random_indices[:test_cutoff]]

random_indices = permutation(white.index)
test_cutoff = math.floor(white.shape[0]/4)
test_white = white.loc[random_indices[test_cutoff:]]
cv_white = white.loc[random_indices[:test_cutoff]]


rfc = RandomForestClassifier(n_estimators = 800, max_features ="auto", oob_score = True, class_weight = 'balanced')
results = [test_white, test_black, test_black, test_black, test_black, 
test_black, test_black, test_black, test_black, test_black, test_black]
results = pd.concat(results)

cv_tot = [cv_black, cv_white]
cv_tot = pd.concat(cv_tot)

trainer = rfc.fit(results[x_cols], results.race_w)

test_y = cv_tot.race_w
predicts = rfc.predict_proba(cv_tot[x_cols])
shaper = predicts[:, 1]



fpr[0], tpr[0], _ = roc_curve(test_y, shaper)
roc_auc[0] = auc(fpr[0], tpr[0])

# Compute micro-average ROC curve and ROC area
fpr["micro"], tpr["micro"], _ = roc_curve(test_y, shaper)
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])



plt.figure()
lw = 2
plt.plot(fpr[0], tpr[0], color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc[0])
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic, White vs Black, Bootstrapped')
plt.legend(loc="lower right")
plt.show()
