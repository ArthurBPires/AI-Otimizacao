import random
import matplotlib.pyplot as plt

#Seleciona k indivíduos aleatóriamente e devolve os dois melhores encontrados.
def selecao(P, k):

    melhoresParticipantesSorteados = []

    for _ in range(2):
        participantesSorteados = []

        for _ in range(k):
            participanteEscolhido = P[random.randrange(len(P))]
            participantesSorteados.append(participanteEscolhido)

        melhoresParticipantesSorteados.append(tournament(participantesSorteados)) 

    return melhoresParticipantesSorteados[0], melhoresParticipantesSorteados[1]

def populacaoInicial(n):
    populacao = []
    for _ in range(n):
        novoTabuleiro = []
        for _ in range(8):
            novoTabuleiro.append(random.randint(1,8))
        populacao.append(novoTabuleiro)
    return populacao


    





def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 10.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    ataques = 0
    coluna=1
    for rainha in individual:
        linha=1
        for rainha2 in individual[coluna:]:
            if rainha == rainha2 or rainha2 == rainha + linha or rainha2 == rainha - linha :
                ataques +=1
            linha += 1
        coluna += 1

    return ataques


def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    melhorParticipante = participants[0]
    for participante in participants[1:]:
        if evaluate(melhorParticipante) > evaluate(participante):
            melhorParticipante = participante
    return melhorParticipante


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
    head1 = parent1[:index]
    tail1 = parent1[index:]
    head2 = parent2[:index]
    tail2 = parent2[index:]

    filho1 = head1 + tail2
    filho2 = head2 + tail1

    return filho1, filho2


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
        individual[ random.randrange(8) ] = random.randint(1,8)
    return individual

conflitosPorGeracao = []

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

    p = populacaoInicial(n)
    for _ in range(g):

        pd = []

        copia_populacao = p

        for _ in range(e):
            if len(pd) < n:
                melhor = tournament(copia_populacao)
                copia_populacao.remove(melhor)
                pd.append(melhor)

        while len(pd) < n:
            p1, p2 = selecao(p, k)
            o1, o2, = crossover(p1, p2, random.randrange(8))
            o1 = mutate(o1, m)
            o2 = mutate(o2, m)
            pd.append(o1)
            pd.append(o2)

        p = pd

        #Calcula quantidade de conflitos nessa geração
        conflitos = []
        for elemento in p:
            conflito = evaluate(elemento)
            conflitos.append(conflito)
        
        conflitosPorGeracao.append(conflitos)

    return tournament(p)

conflitosPorGeracao = []

#Cria gráfico que é pedido na especificação
if __name__ == '__main__':
    g = 40
    n = 150
    k = 10
    m = 0.5
    e = 5

    run_ga(g, n, k, m, e)

    minConflitos = []
    mediaConflitos = []
    maxConflitos = []

    for conflitos in conflitosPorGeracao:
        minConflitos.append(min(conflitos))
        mediaConflitos.append(sum(conflitos) / n)
        maxConflitos.append(max(conflitos))

    plt.plot(list(range(g)), minConflitos, color="green", label="Min conflitos")
    plt.plot(list(range(g)), mediaConflitos, color="blue", label="Media conflitos")
    plt.plot(list(range(g)), maxConflitos, color="red", label="Max conflitos")
    plt.legend()

    plt.title('Conflitos por geração')
    plt.ylabel('Conflitos')
    plt.xlabel('Gerações')

    plt.show()


