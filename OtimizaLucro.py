from pulp import *

class OtimizaLucro():

    def __init__(self, retornos, custos, capitalInvestimento):
        '''
            Classe Responsável por Gerar o Modelo Baseado em Programação Linear e Otimizar os Lucros.

            :param retornos: Possível Retorno de cada Opção de Investimento (Inteiro ou Real).
            :param custos: Custo da Opções de Investimento do Problema (Inteiro ou Real).
            :param capitalInvestimento: Valor do Capital de Investimento Exitente para a Aplicação.
            
        '''

        self.__qtdeOpcoes = 13
        self.__variaveis = [None]*self.__qtdeOpcoes
        
        self.__retornos = retornos
        self.__custos = custos
        self.__capitalInvestimento = capitalInvestimento
        self.__FO = None
        self.__qtdeBaixoRisco = 2
        self.__qtdeMedioRisco = 2
        self.__qtdeAltoRisco = 1

        self.__custoPorBaixoRisco = 1200000
        self.__custoPorMedioRisco = 1500000
        self.__custoPorAltoRisco = 900000

        self.__nomeOpcoes = ["Ampliação da capacidade do armazém ZDP em 5%",
                             "Ampliação da capacidade do armazém MGL em 7%",
                             "Compra de empilhadeira",
                             "Projeto de P&D I", 
                             "Projeto de P&D II",
                             "Aquisição de novos equipamentos",
                             "Capacitação de funcionários",
                             "Ampliação da estrutura de carga rodoviária",
                             "Construção de datacenter",
                             "Aquisição de empresa concorrente",
                             "Compra de serviços em nuvem",
                             "Criação de aplicativo mobile e desktop",
                             "Terceirizar serviço de otimização da logística"]

        self.__model = LpProblem("Desafio_Enacom_2023",LpMaximize)
        self.__constroiFO()
        self.__model += self.__FO
        self.__constroiRestricoes()
    
    def __constroiFO(self):
        '''
        Método Privado Responsável por Construir a Função Objetivo na Qual se Deseja Máximizar. 
        '''
        
        x = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
        for i in range(self.__qtdeOpcoes):
            self.__variaveis[i] = LpVariable(x[i], cat=LpBinary)
            self.__FO += self.__retornos[i]*self.__variaveis[i]


    def __constroiRestricoes(self):
        '''
        Método Privado Responsável por Construir as Restrições do Modelo.   
        '''

        self.__model += self.__variaveis[7] + self.__variaveis[8] + self.__variaveis[9] >= self.__qtdeAltoRisco # Pelo menos 1 (um) investimento de risco alto

        self.__model += self.__variaveis[2] + self.__variaveis[3] + self.__variaveis[4] + self.__variaveis[5] + self.__variaveis[6] + self.__variaveis[12] >= self.__qtdeMedioRisco # Pelo menos 2 (dois) investimentos de risco médio

        self.__model += self.__variaveis[0] + self.__variaveis[1] + self.__variaveis[10] + self.__variaveis[11] >= self.__qtdeBaixoRisco # Pelo menos 2 (dois) investimentos de risco baixo
        
        self.__model += self.__custos[0]*self.__variaveis[0] + self.__custos[1]*self.__variaveis[1] + self.__custos[10]*self.__variaveis[10] + self.__custos[11]*self.__variaveis[11] <= self.__custoPorBaixoRisco # A soma dos custos dos investimentos Baixo Risco não deve ultrapassar R$1.200.000

        self.__model += self.__custos[2]*self.__variaveis[2] + self.__custos[3]*self.__variaveis[3] + self.__custos[4]*self.__variaveis[4] + self.__custos[5]*self.__variaveis[5] + self.__custos[6]*self.__variaveis[6] + self.__custos[12]*self.__variaveis[12] <= self.__custoPorMedioRisco # A soma dos custos dos investimentos Medio Risco não deve ultrapassar R$1.500.000

        self.__model += self.__custos[7]*self.__variaveis[7] + self.__custos[8]*self.__variaveis[8] + self.__custos[9]*self.__variaveis[9] <= self.__custoPorAltoRisco # A soma dos custos dos investimentos Alto Risco não deve ultrapassar R$900.000

        self.__model += self.__custos[0]*self.__variaveis[0] + self.__custos[1]*self.__variaveis[1] + self.__custos[2]*self.__variaveis[2] + self.__custos[3]*self.__variaveis[3] + self.__custos[4]*self.__variaveis[4] + self.__custos[5]*self.__variaveis[5] + self.__custos[6]*self.__variaveis[6] + self.__custos[7]*self.__variaveis[7] + self.__custos[8]*self.__variaveis[8] + self.__custos[9]*self.__variaveis[9] + self.__custos[10]*self.__variaveis[10] + self.__custos[11]*self.__variaveis[11] + self.__custos[12]*self.__variaveis[12] <= self.__capitalInvestimento  # Considerando um capital para investimento de R$2.400.000

    
    def resolver(self):
        '''
            Método Responsável por Otimizar o Modelo. Lista no Terminal o Valor Ótimo, e as Opções de Investimento Selecionadas para Isso.
        '''

        self.__model.solve()
        print("Model Status:{}".format(LpStatus[self.__model.status]))
        print('----------------------------------------------------')
        print("O Valor Ótimo de Retorno das Opções de Investimento será de: R$", round(value(self.__model.objective), 3),"\n")

        self.opcoesSelecionadas()
        
        
    def opcoesSelecionadas(self):
        '''
        Lista no Terminal as Opções de Investimento Escolhidas Após a Otimização
        '''
        print("----- Opções de Investimentos Selecionadas -----\n")

        for i in range(13):
            if self.__model.variables()[i].varValue == 1:
                print(self.__nomeOpcoes[i])
            #x[i] = int(self.__model.variables()[i].varValue)


    def testesUnitarios(self):
        '''
        Classe Responsável por Realizar os Testes Unitários, Verificando se a Otimização respeita todas as Restrições.
        '''
        x = [None]*self.__qtdeOpcoes        
        for i in range(13):
            x[i] = int(self.__model.variables()[i].varValue)

        self.__testeRestricao1(x)
        self.__testeRestricao2(x)
        self.__testeRestricao3(x)
        self.__testeRestricao4(x)
        self.__testeRestricao5(x)
        self.__testeRestricao6(x)
        self.__testeRestricao7(x)


    def __testeRestricao1(self, x):            
        ''' 
        Testa se a Quantidade Mínima Desejada de Investimentos de Risco Alto foi Selecionado
        '''
        print("------------------ Restrição 1 -------------------")
        print(f"Pelo menos {self.__qtdeAltoRisco} investimento de risco alto")
        print("X8 + X9 + X10 >= {self.__qtdeAltoRisco}")
        print(f"{x[7]} + {x[8]} + {x[9]} >= {self.__qtdeAltoRisco}")
        print(f"{x[7] + x[8] + x[9]} >= {self.__qtdeAltoRisco}")

        if x[7] + x[8] + x[9] >= self.__qtdeAltoRisco:
            print("Restrição 1 Satisfeita!\n")
            

        else:
            print("Restrição 1 Não Satisfeita!\n'")


    def __testeRestricao2(self, x):                  
        ''' 
        Testa se a Quantidade Mínima Desejada de Investimentos de Risco Médio foi Selecionado
        '''
        print("------------------ Restrição 2 -------------------")
        print(f"Pelo menos {self.__qtdeMedioRisco} investimentos de risco médio")
        print("X3 + X4 + X5 + X6 + X7 + X13 >= {self.__qtdeMedioRisco}")
        print(f"{x[2]} + {x[3]} + {x[4]} + {x[5]} + {x[6]} + {x[12]} >= {self.__qtdeMedioRisco}")
        print(f"{x[2] + x[3] + x[4] + x[5] + x[6] + x[12]} >= {self.__qtdeMedioRisco}")

        if x[2] + x[3] + x[4] + x[5] + x[6] + x[12] >= self.__qtdeMedioRisco:
            print("Restrição 2 Satisfeita!\n")
        else:
            print("Restrição 2 Não Satisfeita!\n")


    def __testeRestricao3(self, x):                  
        ''' 
        Testa se a Quantidade Mínima Desejada de Investimentos de Risco Baixo foi Selecionado
        '''
        print("------------------ Restrição 3 -------------------")
        print(f"Pelo menos {self.__qtdeBaixoRisco} investimentos de risco baixo")
        print(f"X1 + X2 + X11 + X12 >= {self.__qtdeBaixoRisco}")
        print(f"{x[0]} + {x[1]} + {x[10]} + {x[11]} >= {self.__qtdeBaixoRisco}")
        print(f"{x[0] + x[1] + x[10] + x[11]}  >= {self.__qtdeBaixoRisco}")

        if x[0] + x[1] + x[10] + x[11] >= self.__qtdeBaixoRisco:
            print("Restrição 3 Satisfeita!\n")
        else:
            print("Restrição 3 Não Satisfeita!\n")
        
    def __testeRestricao4(self, x):  
        ''' 
        Testa se A Soma dos Custos dos Investimentos Baixo Risco não Ultrapassou o Valor Máximo Definido para Esse Tipo de Opção de Investimento
        '''
        print("------------------ Restrição 4 -------------------")
        print(f"A Soma dos Custos dos Investimentos Baixo Risco não deve Ultrapassar R${self.__custoPorBaixoRisco}")
        print(f"470.000*X1 + 400.000*X2 + 120.000*X11 + 150.000*X12 <= {self.__custoPorBaixoRisco}")
        print(f"{470000*x[0]} + {400000*x[1]} + {120000*x[10]} + {150000*x[11]} <= {self.__custoPorBaixoRisco}")
        print(f"{470000*x[0] + 400000*x[1] + 120000*x[10] + 150000*x[11]}  <= {self.__custoPorBaixoRisco}")

        if 470000*x[0] + 400000*x[1] + 120000*x[10] + 150000*x[11] <= self.__custoPorBaixoRisco:
            print("Restrição 4 Satisfeita!\n")

        else:
            print("Restrição 4 Não Satisfeita!\n")

    def __testeRestricao5(self, x):  
        ''' 
        Testa se A Soma dos Custos dos Investimentos de Médio Risco não Ultrapassou o Valor Máximo Definido para Esse Tipo de Opção de Investimento
        '''
        print("------------------ Restrição 5 -------------------")
        print(f"A soma dos custos dos investimentos Médio Risco não deve ultrapassar R${self.__custoPorMedioRisco}")
        print(f"170.000*X3 + 270.000*X4 + 340.000*X5 + 230.000*X6 + 50.000*X7 + 300.000*X13 <= {self.__custoPorMedioRisco}")
        print(f"{170000*x[2]} + {270000*x[3]} + {340000*x[4]} + {230000*x[5]} + {50000*x[6]} + {300000*x[12]} <= {self.__custoPorMedioRisco}")
        print(f"{170000*x[2] + 270000*x[3] + 340000*x[4] + 230000*x[5] + 50000*x[6] + 300000*x[12]}  <= {self.__custoPorMedioRisco}")

        if 170000*x[2] + 270000*x[3] + 340000*x[4] + 230000*x[5] + 50000*x[6] + 300000*x[12] <= self.__custoPorMedioRisco:
            print("Restrição 5 Satisfeita!\n")
            
        else:
            print("Restrição 5 Não Satisfeita!\n")

    def __testeRestricao6(self, x):  
        ''' 
        Testa se A Soma dos Custos dos Investimentos de Alto Risco não Ultrapassou o Valor Máximo Definido para Esse Tipo de Opção de Investimento
        '''
        print("------------------ Restrição 6 -------------------")
        print(f"A Soma dos Custos dos Investimentos Alto Risco não Deve Ultrapassar R${self.__custoPorAltoRisco}")
        print(f"440.000*X8 + 320.000*X9 + 800.000*X10 <= {self.__custoPorAltoRisco}")
        print(f"{440000*x[7]} + {320000*x[8]} + {800000*x[9]} <= {self.__custoPorAltoRisco}")
        print(f"{440000*x[7] + 320000*x[8] + 800000*x[9]}  <= {self.__custoPorAltoRisco}")

        if 440000*x[7] + 320000*x[8] + 800000*x[9] <= self.__custoPorAltoRisco:
            print("Restrição 6 Satisfeita!\n")
            
        else:
            print("Restrição 6 Não Satisfeita!\n")

    def __testeRestricao7(self, x):  
        ''' 
        Testa se a Soma dos Custos das Opções de Investimento Escolhidas Não Ultrapassou o Capital de Investimento Máximo
        '''
        print("------------------ Restrição 7 -------------------")
        print(f"Considerando um Capital para Investimento de R${self.__capitalInvestimento}")
        print(f"470.000*X1 + 400.000*X2 + 170.000*X3 + 270.000*X4 + 340.000*X5 + 230.000*X6 + 50.000*X7 + 440.000*X8 + 320.000*X9 + 800.000*X10 + 120.000*X11 + 150.000*X12 + 300.000*X13 <= {self.__capitalInvestimento} ")
        print(f"{470000*x[0]} + {400000*x[1]} + {170000*x[2]} + {270000*x[3]} + {340000*x[4]} + {230000*x[5]} + {50000*x[6]} + {440000*x[7]} + {320000*x[8]} + {800000*x[9]} + {120000*x[10]} + {150000*x[11]} + {300000*x[12] } <= {self.__capitalInvestimento}")
        print(f"{470000*x[0] + 400000*x[1] + 170000*x[2] + 270000*x[3] + 340000*x[4] + 230000*x[5] + 50000*x[6] + 440000*x[7] + 320000*x[8] + 800000*x[9] + 120000*x[10] + 150000*x[11] + 300000*x[12] }  <= {self.__capitalInvestimento} ")

        if 470000*x[0] + 400000*x[1] + 170000*x[2] + 270000*x[3] + 340000*x[4] + 230000*x[5] + 50000*x[6] + 440000*x[7] + 320000*x[8] + 800000*x[9] + 120000*x[10] + 150000*x[11] + 300000*x[12]  <= self.__capitalInvestimento :
            print("Restrição 7 Satisfeita!\n")
            
        else:
            print("Restrição 7 Não Satisfeita!\n")


    @property
    def qtdeBaixoRisco(self):
        '''
        Retorna a Quantidade de Investimento por Opções de Baixo Risco 
        '''
        return self.__qtdeBaixoRisco

    @qtdeBaixoRisco.setter
    def qtdeBaixoRisco(self, qtdeBaixoRisco):
        '''
        Define uma Nova Quantidade de Investimento por Opções de Baixo Risco
        '''
        self.__qtdeBaixoRisco = qtdeBaixoRisco
    

    @property
    def qtdeMedioRisco(self):
        '''
        Retorna a Quantidade de Investimento por Opções de Médio Risco 
        '''
        return self.__qtdeMedioRisco
    
    @qtdeMedioRisco.setter
    def qtdeMedioRisco(self, qtdeMedioRisco):
        '''
        Define uma Nova Quantidade de Investimento por Opções de Médio Risco
        '''
        self.__qtdeMedioRisco = qtdeMedioRisco
    
    
    @property
    def qtdeAltoRisco(self):
        '''
        Retorna a Quantidade de Investimento por Opções de Alto Risco 
        '''
        return self.__qtdeAltoRisco
    
    @qtdeAltoRisco.setter
    def qtdeAltoRisco(self, qtdeAltoRisco):
        '''
        Define uma Nova Quantidade de Investimento por Opções de Alto Risco
        '''
        self.__qtdeAltoRisco = qtdeAltoRisco


    @property
    def custoPorBaixoRisco(self):
        '''
        Retorna o Valor de Investimento por Opções de Baixo Risco 
        '''
        return self.__custoPorBaixoRisco
    
    @custoPorBaixoRisco.setter
    def custoPorBaixoRisco(self, custoPorBaixoRisco):
        '''
        Define um Novo Valor de Investimento por Opções de Baixo Risco
        '''
        self.__custoPorBaixoRisco = custoPorBaixoRisco
    

    
    @property
    def custoPorMedioRisco(self):
        '''
        Retorna o Valor de Investimento por Opções de Médio Risco 
        '''
        return self.__custoPorMedioRisco
    
    @custoPorMedioRisco.setter
    def custoPorMedioRisco(self, custoPorMedioRisco):
        '''
        Define um Novo Valor de Investimento por Opções de Médio Risco
        '''
        self.__custoPorMedioRisco = custoPorMedioRisco
    
    
    @property
    def custoPorAltoRisco(self):
        '''
        Retorna o Valor de Investimento por Opções de Alto Risco 
        '''
        return self.__custoPorAltoRisco
    
    @custoPorAltoRisco.setter
    def custoPorAltoRisco(self, custoPorAltoRisco):
        '''
        Define um Novo Valor de Investimento por Opções de Alto Risco
        '''
        self.__custoPorAltoRisco = custoPorAltoRisco


    @property
    def capitalInvestimento(self):
        '''
        Retorna o Valor do Capital de Investimento 
        '''
        return self.__capitalInvestimento
    
    @capitalInvestimento.setter
    def capitalInvestimento(self, capitalInvestimento):
        '''
        Define um Novo Valor do Capital de Investimento
        '''
        self.__capitalInvestimento = capitalInvestimento