import numpy as np
import networkx as nx
import random

def prob_violencia(t,ts):

    if t == 0:
        p = 0
    elif t <= ts:
        p = np.exp(t-ts)
    else:
        p = 1

    return p

def interacoes():

    for atualizacao in range(L):

        #Sorteando o par de vizinhos
        noSorteado = np.random.choice(ws.nodes())

        if ws.degree[noSorteado] != 0:
            noVizinho = np.random.choice(list(ws.neighbors(noSorteado)))

        #Escolhendo o tipo de interação entre eles e realizando a mudança do estresse
        opcoes = ['boa','ruim']
        probs = [pg,1-pg]
        tipoInteracao = random.choices(opcoes,weights=probs,k=1)[0]

        if tipoInteracao == 'boa':
            ws.nodes[noSorteado]['Estresse'] = 0
            ws.nodes[noVizinho]['Estresse'] = 0
        else:
            ws.nodes[noSorteado]['Estresse'] = 1
            ws.nodes[noVizinho]['Estresse'] = 1

def interacoes_extra_escolar():

    for no in ws.nodes():

        if np.random.random() <= pext:
            ws.nodes[no]['Estresse'] = delta

    
#Parâmetros da rede
L = 1000
k = 4
p = 0.5

#Parâmetros da simulação:
tRep = 10
tPassos = 200
pg = 0.5
pext = 0.0
delta = 0 #0 para interações positivas/ 1 para interações nagetivas.

with open('L1k_pext0.0.txt', 'a') as resultados:

    for ts in range(1,31):

        mrAV = 0
        drAV = 0
        mtAV = []
        for repeticao in range(tRep):
        
            #Criando rede de Watts-Strogatz
            ws = nx.watts_strogatz_graph(L, k, p)
            #Atribuindo estados de estresse para cada indivíduo da rede
            for no in ws.nodes():
                ws.nodes[no]['Estresse'] = np.random.choice([0,1])

            tempoEstresse = [0]*L
            ato_violento = 0

            for t in range(tPassos):

                interacoes()
                interacoes_extra_escolar()
                
                for no in ws.nodes():
                    #Contabilizando os dias no estado de estresse para cada nó
                    if ws.nodes[no]['Estresse'] == 1:
                        tempoEstresse[no] += 1
                    else:
                        tempoEstresse[no] = 0
                    #Possível realização de ato violento
                    if np.random.random() <= prob_violencia(tempoEstresse[no],ts):
                        ato_violento += 1
                        tempoEstresse[no] = 0

            mtAV.append(ato_violento/tPassos)

        mtAV = np.array(mtAV)

        mrAV = np.mean(mtAV, axis=0)
        drAV = np.std(mtAV, axis=0)
        resultados.write('{:.2f}'.format(ts)+'  '+'{:.5f}'.format(mrAV)+'  '+'{:.10f}'.format(drAV)+'\n')
        print('ts:',ts)

'''
******* Testes feitos *******
1. 06/08/2024
- Criaçao da rede e atribuição de estados de estresse: OK
- Interações entre indivíduos: OK
- Contagem de tempo no estado de estresse: OK
2. 12/08/2024
- Probabilidade de realizar ato violento: OK
- Contagem de atos violentos: OK
- Checagem das repetições: OK
'''
