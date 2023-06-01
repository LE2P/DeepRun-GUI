import numpy as np

class MultiLevelPredictor:
    def __init__(self):
        pass
    
    def predictlevel(self, output_pred):
        Yhat1 = np.argmax(output_pred[0], axis=1)
        Yhat2 = np.argmax(output_pred[1], axis=1)
        Yhat3 = np.argmax(output_pred[2], axis=1)

        for x in range(len(output_pred[0])-1):
            # Level 2 correction
            if Yhat1[x] == 0 and Yhat2[x] not in range(0, 5):
                Yhat2[x] = np.argmax(output_pred[1][x][range(0,5)])
            if Yhat1[x] == 1 and Yhat2[x] not in range(5,9):
                Yhat2[x] = np.argmax(output_pred[1][x][range(5,9)]) + 5
            if Yhat1[x] == 2 and Yhat2[x] != 9:
                Yhat2[x] = 9
            if Yhat1[x] == 3 and Yhat2[x] != 10:
                Yhat2[x] = 10
            # Level 3 correction
            if Yhat2[x] == 0 and Yhat3[x] != 0:
                Yhat3[x] = 0
            if Yhat2[x] == 1 and Yhat3[x] not in range(1,3):
                Yhat3[x] = np.argmax(output_pred[2][x][range(1,3)]) + 1
            if Yhat2[x] == 2 and Yhat3[x] not in range(3,5):
                Yhat3[x] = np.argmax(output_pred[2][x][range(3,5)]) + 3
            if Yhat2[x] == 3 and Yhat3[x] != 5:
                Yhat3[x] = 5
            if Yhat2[x] == 4 and Yhat3[x] not in range(6,11):
                Yhat3[x] = np.argmax(output_pred[2][x][range(6,11)]) + 6
            if Yhat2[x] == 5 and Yhat3[x] not in range(11,14):
                Yhat3[x] = np.argmax(output_pred[2][x][range(11,14)]) + 11
            if Yhat2[x] == 6 and Yhat3[x] not in range(14,20):
                Yhat3[x] = np.argmax(output_pred[2][x][range(14,20)]) + 14
            if Yhat2[x] == 7 and Yhat3[x] != 20:
                Yhat3[x] = 20
            if Yhat2[x] == 8 and Yhat3[x] != 21:
                Yhat3[x] = 21
            if Yhat2[x] == 9 and Yhat3[x] not in range(22,24):
                Yhat3[x] = np.argmax(output_pred[2][x][range(22,24)]) + 22
            if Yhat2[x] == 10 and Yhat3[x] not in range(24,27):
                Yhat3[x] = np.argmax(output_pred[2][x][range(24,27)]) + 24

        return Yhat1, Yhat2, Yhat3
