import numpy as np


def derivadaTheta(theta_0, theta_1, data, final):
    n = len(data)
    parciais = []
    for x,y in data:

        aux = (theta_0 + theta_1 * x) - y

        if final == 0:
            parciais.append(aux)

        elif final == 1:
            parciais.append(aux * x)

    somaDasParciais =  sum(parciais)
    resultado = 2/n * somaDasParciais
    
    return resultado




def compute_mse(theta_0, theta_1, data):
    """
    Calcula o erro quadratico medio
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """

    n = len(data)
    parciais = []

    for x,y in data:
        erro = (theta_0 + theta_1 * x) - y
        erro = erro * erro
        parciais.append(erro)
    
    somaDasParciais = sum(parciais)
    resultado = somaDasParciais / n
    return resultado

def step_gradient(theta_0, theta_1, data, alpha):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de theta_0 e theta_1.
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de theta_0 e theta_1, respectivamente
    """

    deltaTheta_0 = (alpha * derivadaTheta(theta_0, theta_1, data, 0))
    deltaTheta_1 = (alpha * derivadaTheta(theta_0, theta_1, data, 1))

    novo_theta_0 = theta_0 - deltaTheta_0
    novo_theta_1 = theta_1 - deltaTheta_1

    return novo_theta_0, novo_theta_1


def fit(data, theta_0, theta_1, alpha, num_iterations):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de theta_0 e theta_1.
    Ao final, retorna duas listas, uma com os theta_0 e outra com os theta_1
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os theta_0 e outra com os theta_1 obtidos ao longo da execução
    """
    thetas_0 = []
    thetas_1 = []

    for _ in range(num_iterations):

        theta_0, theta_1 = step_gradient(theta_0, theta_1, data, alpha)
        thetas_0.append(theta_0)
        thetas_1.append(theta_1)

    return thetas_0, thetas_1
