import random
import matplotlib.pyplot as plt

##############################################################################
# Funções Auxiliares
def aleatorios(n):
    """
    Gera n populações aleatórias
    """
    lista = []
    for _ in range(n):
        temp = []
        for _ in range(8):
            temp.append(random.randint(1,8))
        lista.append(temp)
    return lista

def selecao(P, k):
    """
    Seleciona k populações aleatórias duas vezes e devolve os dois
    melhores encontrados.
    """
    melhores = []
    for _ in range(2):
        participantes = []
        for _ in range(k):
            participantes.append(P[random.randrange(len(P))])
        melhores.append(tournament(participantes)) 
    return melhores[0], melhores[1]

def top(P):
    """
    Executa o torneio nos participantes e retorna o melhor
    """
    return tournament(P)

def numeroConflitos(P):
    listaConflitos = []
    for elemento in P:
            conflitos = evaluate(elemento)
            listaConflitos.append(conflitos)
    return listaConflitos

def imprimeGrafico(max, med, min, g):
    plt.plot([i for i in range(g)], max, color="red", label="max conflitos")
    plt.plot([i for i in range(g)], med, color="blue", label="media conflitos")
    plt.plot([i for i in range(g)], min, color="green", label="min conflitos")
    plt.legend()

    plt.xlabel('Gerações')
    plt.ylabel('Conflitos')

    plt.title('Resultados da execução')

    plt.show()


##############################################################################

def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 10.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    ataques = 0
    for i, rainha in enumerate(individual, start=1):
        for j, rainha2 in enumerate(individual[i:], start=1):
            if rainha == rainha2 or rainha2 == rainha + j or rainha2 == rainha - j :
                ataques +=1

    return ataques


def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    melhor = participants[0]
    for candidato in participants[1:]:
        if evaluate(melhor) > evaluate(candidato):
            melhor = candidato
    return melhor


def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    temp = parent1[:index]
    temp.extend(parent2[index:])
    temp2 = parent2[:index]
    temp2.extend(parent1[index:])
    return temp, temp2


def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    if random.random() < m:
        indice = random.randrange(8)
        individual[indice] = random.randint(1,8)
    return individual


def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:int - número de indivíduos no elitismo
    :return:list - melhor individuo encontrado
    """

    p = aleatorios(n)
    for _ in range(g):

        pl = []

        copia_populacao = p
        for _ in range(e):
            if len(pl) < n:
                melhor = tournament(copia_populacao)
                copia_populacao.remove(melhor)
                pl.append(melhor)

        while len(pl) < n:
            p1, p2 = selecao(p, k)
            o1, o2, = crossover(p1, p2, random.randrange(8))
            o1, o2 = mutate(o1, m), mutate(o2, m)
            pl.append(o1)
            pl.append(o2)
        p = pl

        conflitosPorGeracao.append(numeroConflitos(p))

    return top(p)

conflitosPorGeracao = []

if __name__ == '__main__':
    g = 40
    n = 150
    k = 10
    m = 0.5
    e = 5

    run_ga(g, n, k, m, e)

    quantMaximaConflitos = []
    quantMediaConflitos = []
    quantMinimaConflitos = []

    for conflitos in conflitosPorGeracao:
        quantMaximaConflitos.append(max(conflitos))
        quantMediaConflitos.append(sum(conflitos) / n)
        quantMinimaConflitos.append(min(conflitos))

    imprimeGrafico(quantMaximaConflitos, quantMediaConflitos, quantMinimaConflitos, g)


