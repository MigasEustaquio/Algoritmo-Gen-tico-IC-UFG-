import random
import math

class Cromossomo():
    def __init__(self, cromossomox=None, cromossomoy=None) -> None:
        self.score = 0
#Herda os genes
        if cromossomox is not None and cromossomoy is not None:
            self.cromossomox = cromossomox
            self.cromossomoy = cromossomoy
#Geração inicial aleatória
        else:
            self.cromossomox = []
            self.cromossomoy = []
            for _ in range(22):
                self.cromossomox.append(random.randint(0,1))
                self.cromossomoy.append(random.randint(0,1))

        self.score = self.decodificar()

#herdando genes dos pais utilizando crossover 1 ponto
    def heranca(self, ponto_corte: int, outro_cromossomo):
        novo_cromossomox1 = []
        novo_cromossomoy1 = []
        novo_cromossomox2 = []
        novo_cromossomoy2 = []

        if ponto_corte == 0:
            return [Cromossomo(self.cromossomox, self.cromossomoy), Cromossomo(outro_cromossomo.cromossomox, outro_cromossomo.cromossomoy)]
        else:
            i=0
            while i<=ponto_corte:
                if i<22:
                    novo_cromossomox1.append(self.cromossomox[i])
                    novo_cromossomox2.append(outro_cromossomo.cromossomox[i])
                else:
                    novo_cromossomoy1.append(self.cromossomoy[i-22])
                    novo_cromossomoy2.append(outro_cromossomo.cromossomoy[i-22])
                i+=1
            while i<=43:
                if i<22:
                    novo_cromossomox1.append(outro_cromossomo.cromossomox[i])
                    novo_cromossomox2.append(self.cromossomox[i])
                else:
                    novo_cromossomoy1.append(outro_cromossomo.cromossomoy[i-22])
                    novo_cromossomoy2.append(self.cromossomoy[i-22])
                i+=1

        return [Cromossomo(novo_cromossomox1, novo_cromossomoy1), Cromossomo(novo_cromossomox2, novo_cromossomoy2)]


    def mutacao(self, taxa_mutacao):
        novo_cromossomox = []
        novo_cromossomoy = []

        for gene in self.cromossomox:
            if int(random.random()*100) < taxa_mutacao*100:
                if gene == 0: novo_cromossomox.append(1)
                else: novo_cromossomox.append(0)
            else:
                novo_cromossomox.append(gene)
        for gene in self.cromossomoy:
            if int(random.random()*100) < taxa_mutacao*100:
                if gene == 0: novo_cromossomoy.append(1)
                else: novo_cromossomoy.append(0)
            else:
                novo_cromossomoy.append(gene)
        return Cromossomo(novo_cromossomox, novo_cromossomoy)

#Get
    def get_score(self) -> int:
        return self.score

#Sobreescrevendo o método para usar print
    def __str__(self) -> str:
        string = "score = %.16f" % (self.score) +"   |"
        for gene in self.cromossomox:
            string = string + str(gene)
        string = string + "|"
        for gene in self.cromossomoy:
            string = string + str(gene)
        return string + "|"

#Método que converte valores binários para decimais passando pro string depois int
    def conversao_base10(self):
        string1 = ''
        for gene in self.cromossomox:
            string1 = string1 + str(gene)
        string2 = ''
        for gene in self.cromossomoy:
            string2 = string2 + str(gene)
        return [int(string1, 2), int(string2, 2)]

#Função F6(x,y)
    def fitness(self, x, y) -> float:
        return (0.5 - ((((math.sin(math.sqrt((x**2)+(y**2))))**2)-0.5) / (1+0.001*((x**2)+(y**2))**2) ))

#Método que faz todo o processo de decodificação e retorna o score do cromossomo
    def decodificar(self) -> int:
        base10=self.conversao_base10()
        base10[0]=(base10[0]*(200)/((2**22)-1))-100
        base10[1]=(base10[1]*(200)/((2**22)-1))-100
        return self.fitness(base10[0], base10[1])



class Populacao(object):
    def __init__(self, size=100, taxa_mutacao = 0.008, taxa_crossover = 0.65) -> None:
        self.size = size
        self.geracao = 0
        self.score_total = 0
        self.populacao_atual = self.cria_populacao()

        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.size=size

#Método que printa o melhor cromossomo da geração e a média de score
    def imprime_resumo(self):
        print('Geração: %03d' % self.geracao, "Fitness médio: %.16f" % (self.score_total/self.size) ,"-- Melhor: ", self.melhor_da_geracao())

    def melhor_da_geracao(self):
        return max(self.populacao_atual, key=Cromossomo.get_score)

#Método que printa todos os cromossomos de uma geração
    def geracao_completa(self):
        for cromossomo in self.populacao_atual:
            print(cromossomo)

#Método que cria a população inicial
    def cria_populacao(self):
        lista = []
        for _ in range(self.size):
            cromossomo = Cromossomo()
            lista.append(cromossomo)
            self.score_total += cromossomo.score
        return lista

#Método que faz a seleção dos pais de forma aleatória com probabilidade baseada no score
    def roleta(self) -> Cromossomo:
        escolha_aleatoria = int(random.random()*self.score_total)
        total_parcial = 0
        aux = 0
        while True: 
            total_parcial += self.populacao_atual[aux].score
            if total_parcial >= escolha_aleatoria:
                break
            aux += 1
        return self.populacao_atual[aux]

#Método que faz a passagem de geração de forma geral
    def reproducao(self):
        self.geracao+=1
        pais=self.seleciona_pais()
        filhos=[]
        filhos_mutados=[]
        i=0
        while i < self.size:
            filhos += self.crossover(pais[i], pais[i+1])
            i+=2

        for filho in filhos:
            filhos_mutados.append(filho.mutacao(self.taxa_mutacao))

        filhos_mutados[int(random.random()*(self.size-1))] = self.melhor_da_geracao()
        self.populacao_atual = filhos_mutados

#Método que guarda o score total e seleciona os pais utilizando a roleta
    def seleciona_pais(self):
        self.score_total=0
        pais = []
        for cromossomo in self.populacao_atual:
            self.score_total = self.score_total + cromossomo.score
        while len(pais) < len(self.populacao_atual):
            pais.append(self.roleta())
        return pais

#Método que verifica se vai ocorrer e prepara o crossover
    def crossover(self, pai: Cromossomo, mae: Cromossomo):
        pronto_de_corte=0
        if int(random.random()*100) < self.taxa_crossover*100:
            pronto_de_corte=int(random.random()*44)
        
        return pai.heranca(pronto_de_corte, mae)
