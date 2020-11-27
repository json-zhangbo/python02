# Load libraries
import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

def __mydata__():
    #url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    url="/Users/zhangbo/个人文档/开发/iris.data"
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = pandas.read_csv(url, names=names)
    print(dataset.shape)
    print(dataset.head(20))
    #单变量图形：现在我们可以看看对每个属性的统计摘要，包含了数量、平均值、最大值、最小值，还有一些百分位数值。
    #print(dataset.describe())
    #dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
    #plt.show()
    #单变量图形：我们也可以为每个输入变量创建一个直方图以了解它们的分布状况
    #dataset.hist()
    #plt.show()
    #多变量图形：首先，我们看看全部属性对的散点图，这有助于我们看出输入变量之间的结构化关系。
    #scatter_matrix(dataset)
    #plt.show()

    #创建验证集
    array = dataset.values
    X = array[:, 0:4]
    Y = array[:, 4]
    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size,
                                                                                    random_state=seed)
    #测试工具
    seed = 7
    scoring = 'accuracy'
    #搭建模型，常用算法逻辑回归（LR）线性判别分析（LDA）K最近邻算法（KNN）分类和回归树（CART）高斯朴素贝叶斯（NB）支持向量机（SVM）

    models = []
    models.append(('LR', LogisticRegression()))
    models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC()))
    # evaluate each model in turn
    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed,shuffle=True)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
    #选择最佳模型
    fig = plt.figure()
    fig.suptitle('Algorithm Comparison')
    ax = fig.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names)
    plt.show()

    #做出预测
    knn = KNeighborsClassifier()
    knn.fit(X_train, Y_train)
    predictions = knn.predict(X_validation)
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))

if __name__ == '__main__':
    __mydata__()