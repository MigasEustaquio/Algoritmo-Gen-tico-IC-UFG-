from classes2 import *

populacao = Populacao(size=100)

for _ in range(1000):
    populacao.imprime_resumo()
    populacao.reproducao()

print('ultima geração completa:')
print(populacao.geracao_completa())
