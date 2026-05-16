import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

class Confusion:
    @staticmethod
    def getMatrix(actual, predict, display=True):
        if len(actual) != len(predict):
            raise ValueError("Input vectors have different lengths")
        
        unique_actual = np.unique(actual)
        unique_predict = np.unique(predict)
        
        if not np.array_equal(unique_actual, unique_predict):
            raise ValueError("Class list in given inputs are different")
        
        class_list = unique_actual
        print("Class List in given sample")
        print(class_list)
        print(f"\nTotal Instance = {len(actual)}")
        
        c_matrix = confusion_matrix(actual, predict, labels=class_list)
        c_matrix_table = pd.DataFrame(c_matrix, index=[f'Actual_class{i+1}' for i in range(len(class_list))],
                                      columns=[f'Predicted_class{i+1}' for i in range(len(class_list))])
        print("Confusion Matrix")
        print(c_matrix_table)
        
        result, reference_result = Confusion.get_values(c_matrix)
        
        if display:
            if len(class_list) > 2:
                print("Multi-Class Confusion Matrix Output")
                print(reference_result)
            else:
                print("Two-Class Confusion Matrix")
                print(c_matrix)
            print("Overall values")
            print(result)
        
        return c_matrix, result, reference_result
    
    @staticmethod
    def getValues(c_matrix):
        if c_matrix.shape[0] != c_matrix.shape[1]:
            raise ValueError("Confusion matrix dimension is wrong")
        
        n_class = c_matrix.shape[0]
        TP = np.diag(c_matrix)
        FP = np.sum(c_matrix, axis=0) - TP
        FN = np.sum(c_matrix, axis=1) - TP
        TN = np.sum(c_matrix) - (FP + FN + TP)
        
        P = TP + FN
        N = FP + TN
        
        accuracy = np.sum(TP) / np.sum(c_matrix)
        error = 1 - accuracy
        
        if n_class == 2:
            sensitivity = TP[0] / P[0]
            specificity = TN[0] / N[0]
            precision = TP[0] / (TP[0] + FP[0])
            FPR = FP[0] / N[0]
            F1_score = 2 * (precision * sensitivity) / (precision + sensitivity)
            MCC = (TP[0] * TN[0] - FP[0] * FN[0]) / np.sqrt((TP[0] + FP[0]) * (TP[0] + FN[0]) * (TN[0] + FP[0]) * (TN[0] + FN[0]))
            p0 = accuracy
            pe = ((P[0] * (TP[0] + FP[0])) + (N[0] * (FN[0] + TN[0]))) / np.sum(c_matrix)**2
            kappa = (p0 - pe) / (1 - pe)
        else:
            sensitivity = TP / P
            specificity = TN / N
            precision = TP / (TP + FP)
            FPR = FP / N
            F1_score = 2 * (precision * sensitivity) / (precision + sensitivity)
            MCC = (TP * TN - FP * FN) / np.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))
            p0 = accuracy
            pe = np.sum((P * (TP + FP)) + (N * (FN + TN))) / np.sum(c_matrix)**2
            kappa = (p0 - pe) / (1 - pe)
        
        result = {
            'Accuracy': round(accuracy, 4),
            'Error': round(error, 4),
            'Sensitivity': round(np.mean(sensitivity), 4),
            'Specificity': round(np.mean(specificity), 4),
            'Precision': round(np.mean(precision), 4),
            'FalsePositiveRate': round(np.mean(FPR), 4),
            'F1_score': round(np.mean(F1_score), 4),
            'MatthewsCorrelationCoefficient': round(np.mean(MCC), 4),
            # 'Kappa': round(np.mean(kappa), 4)
        }
        
        reference_result = {
            'AccuracyInTotal': np.round(accuracy, 4),
            'ErrorInTotal': np.round(error, 4),
            'Sensitivity': np.round(sensitivity, 4),
            'Specificity': np.round(specificity, 4),
            'Precision': np.round(precision, 4),
            'FalsePositiveRate': np.round(FPR, 4),
            'F1_score': np.round(F1_score, 4),
            'MatthewsCorrelationCoefficient': np.round(MCC, 4),
            # 'Kappa': np.round(kappa, 4),
            'TruePositive': TP,
            'FalsePositive': FP,
            'FalseNegative': FN,
            'TrueNegative': TN
        }
        
        # return result, reference_result
        return pd.DataFrame.from_dict(result, orient='index', columns=['Value']) #reference_result