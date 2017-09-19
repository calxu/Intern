import sys
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn import metrics
# import matplotlib.pyplot as plt

def readData():
    """ Read the data. """
    y = []
    pred = []
    for row in sys.stdin:
        record = row.rstrip().split('\t')
        y.append(int(record[1]))
        pred.append(float(record[2]))
    return (y, pred)

def auc(y, pred):
    y = np.array(y)
    pred = np.array(pred)
    print y
    print pred
    fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
    print(metrics.auc(fpr, tpr))
    print(roc_auc_score(y, pred))
    return (fpr, tpr)

def draw(fpr, tpr):
    plt.figure()
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.plot(fpr, tpr)
    plt.xlim([0.0, 1.02])
    plt.ylim([0.0, 1.02])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    # plt.legend(loc="lower right")
    plt.show()
    

if __name__ == '__main__':
    y, pred = readData()
    fpr, tpr = auc(y, pred)
    # draw(fpr, tpr)
