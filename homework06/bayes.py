from collections import defaultdict, Counter
from math import log

class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.x_frequency = None
        self.y_frequency = None

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        # класс написан универсально для любого количества уникальных y
        total_rows = len(y)  # количество строк в данных

        # ищем частоты меток
        y_frequency = Counter()  # частота каждой метки
        for key in y:
            y_frequency[key] += 1
        for key in y_frequency.keys():
            # вместо количества записываем отношение
            y_frequency[key] /= total_rows

        # создаем defaultdict со значением по умолчанию {'good': 0, 'maybe': 0, 'never': 0}
        def default():
            return {label: 0 for label in y_frequency.keys()}
        x_count = defaultdict(default)  # сколько раз каждое слово встречается в каждом классе
        y_count = defaultdict(lambda: 0)  # количество слов для каждого класса
        # итерируем через все слова во всех запросах и заносим словарь
        for text, label in zip(X, y):
            for word in text:
                x_count[word][label] += 1
                y_count[label] += 1
                
        # вычисляем вероятность принадлежности слов к каждому из классов
        x_frequency = defaultdict(default)  # вероятности
        d = len(x_count)  # размерность вектора признаков
        for word in x_count.keys():
            for label in x_count[word].keys():
                # print(word, label, x_count[word][label], y_count[label])
                x_frequency[word][label] = (x_count[word][label] + self.alpha) / (y_count[label] + d * self.alpha)

        # запоминаем частоты
        self.x_frequency = x_frequency
        self.y_frequency = y_frequency


    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        y = []  # на выходе список в том же порядке
        for text in X:
            predictions = {}  # вероятности данного предложения по каждой из меток
            for label in self.y_frequency.keys():
                # сумма логарифмированных вероятностей слов
                log_sum = sum((log(self.x_frequency[word][label]) for word in text if word in self.x_frequency.keys()))
                #print(text, label, log_sum)
                # вероятность данного предложения с данной меткой
                predictions[label] = log(self.y_frequency[label]) + log_sum
            y.append(max(predictions, key=predictions.get))  # добавляем ключ наибольшего элемента словаря
        return y


    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        y = self.predict(X_test)
        accurate = 0
        for prediction, test in zip(y, y_test):
            if prediction == test:
                accurate += 1
        return accurate / len(X_test)
