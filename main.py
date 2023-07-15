from OtimizaLucro import OtimizaLucro
from unidecode import unidecode
import pandas as pd
import numpy as np
import os

modelo = None
otimizado = False

def menu():
    opcao=int(input('''
    O Que Deseja Realizar?
    1 - Entrar os Dados Manualmente
    2 - Ler Arquivo com os Dados
    3 - Otimizar Retornos (lucros)
    4 - Testes Unitários
    5 - Listar Opções de Investimento Selecionadas
    6 - Alterar Capital de Investimento
    7 - Alterar Quantidade Total de Opções de Baixo Risco 
    8 - Alterar Quantidade Total de Opções de Médio Risco 
    9 - Alterar Quantidade Total de Opções de Alto Risco                 
    10 - Alterar Investimento Total por Opções de Baixo Risco 
    11 - Alterar Investimento Total por Opções de Médio Risco 
    12 - Alterar Investimento Total por Opções de Alto Risco 
    0 - Fechar Menu 
    Escolha:  '''))
    
    if opcao == 1:
        inputManual()


    elif opcao == 2:
        inputArquivo()


    elif opcao == 3:
        if(modelo == None):
            print("Insira os dados de Investimento Necessários para Otimizar!")
            
        else:            
            modelo.resolver()


            global otimizado
            otimizado = True


    elif opcao == 4:
        if(modelo == None or otimizado == False):
            print("Primeiro é necessário Otimizar o Modelo para depois realizar os Testes Unitários!")

        else:
            modelo.testesUnitarios()


    elif opcao == 5:
        if(modelo == None or otimizado == False):
            print("Primeiro é necessário Otimizar o Modelo para depois Obter as opções de investimento selecionadas!")
        else:
            modelo.opcoesSelecionadas()


    elif opcao == 6:
        if(modelo == None):
            print("Primeiro é Necessário Carregar os dados, ou inserí-los Manualmente!")

        else:    
            print("O Capital de Investimento Atual é de: R$", modelo.capitalInvestimento)
            while True:
                try:  
                    capitalInvestimento = float(input(f'Digite o Capital de Investimento Desejado: '))
                    modelo.capitalInvestimento = capitalInvestimento
                    break

                except ValueError:
                    print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')
        
    
    elif opcao == 7: 
        if(modelo == None):
            print("Primeiro é Necessário Carregar os dados, ou inserí-los Manualmente!")

        else:    
            print("A Quantidade Total de Opções de Baixo Risco Atual é de: ", modelo.qtdeBaixoRisco)
            while True:
                try:  
                    qtdeBaixoRisco = float(input(f'Digite a Quantidade Total de Opções de Baixo Risco Desejado: '))
                    modelo.qtdeBaixoRisco = qtdeBaixoRisco
                    break

                except ValueError:
                    print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')


    elif opcao == 8:
        if(modelo == None):
            print("Primeiro é Necessário Carregar os dados, ou inserí-los Manualmente!")

        else:    
            print("A Quantidade Total de Opções de Médio Risco Atual é de: ", modelo.qtdeMedioRisco)
            while True:
                try:  
                    qtdeMedioRisco = float(input(f'Digite a Quantidade Total de Opções de Médio Risco Desejado: '))
                    modelo.qtdeMedioRisco = qtdeMedioRisco
                    break

                except ValueError:
                    print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')
    

    elif opcao == 9:
        if(modelo == None):
            print("Primeiro é Necessário Carregar os dados, ou inserí-los Manualmente!")

        else:    
            print("A Quantidade Total de Opções de Alto Risco Atual é de: ", modelo.qtdeAltoRisco)
            while True:
                try:  
                    qtdeAltoRisco = float(input(f'Digite a Quantidade Total de Opções de Alto Risco Desejado: '))
                    modelo.qtdeAltoRisco = qtdeAltoRisco
                    break

                except ValueError:
                    print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')


    elif opcao == 10:
        if(modelo == None):
            print("Primeiro é Necessário Carregar os dados, ou inserí-los Manualmente!")

        else:    
            print("O Investimento Total por Opções de Baixo Risco Atual é de: ", modelo.custoPorBaixoRisco)
            while True:
                try:  
                    custoPorBaixoRisco = float(input(f'Digite o Investimento Total por Opções de Baixo Risco Desejado: '))
                    modelo.custoPorBaixoRisco = custoPorBaixoRisco
                    break

                except ValueError:
                    print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')


    elif opcao == 11:
        if(modelo == None):
            print("Primeiro é Necessário Carregar os dados, ou inserí-los Manualmente!")

        else:    
            print("O Investimento Total de Opções de Médio Risco Atual é de: ", modelo.custoPorMedioRisco)
            while True:
                try:  
                    custoPorMedioRisco = float(input(f'Digite o Investimento Total por Opções de Médio Risco Desejado: '))
                    modelo.custoPorMedioRisco = custoPorMedioRisco
                    break

                except ValueError:
                    print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')


    elif opcao == 12:
        if(modelo == None):
            print("Primeiro é Necessário Carregar os dados, ou inserí-los Manualmente!")

        else:    
            print("O Investimento Total de Opções de Alto Risco Atual é de: ", modelo.custoPorAltoRisco)
            while True:
                try:  
                    custoPorAltoRisco = float(input(f'Digite o Investimento Total por Opções de Alto Risco Desejado: '))
                    modelo.custoPorAltoRisco = custoPorAltoRisco
                    break

                except ValueError:
                    print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')


    elif opcao == 0:
        exit()
    else:
        print("Opção Inválida! Tente novamente.\n")
        menu()
    

def inputManual():
    
    while True:
        try:  
            capitalInvestimento = float(input(f'Digite o Capital de Investimento existente para a aplicação: '))
            break

        except ValueError:
            print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')

  
    qtdeVariaveis = 13
    retornos = [None]*qtdeVariaveis
    while True:
        try:
            for i in range(qtdeVariaveis):
                retornos[i] = float(input(f'Digite o retorno esperado pela {i + 1}° opção de investimento: '))
            break

        except ValueError:
            print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')

    print('----- Retornos Cadastrados Com Sucesso !! -----\n')

    custos = [None]*qtdeVariaveis
    while True:
        try:
            for i in range(qtdeVariaveis):
                custos[i] = float(input(f'Digite o custo pela {i + 1}° opção de investimento: '))
            break

        except ValueError:
            print('Opção Inválida! Entre com um valor Inteiro ou Real!.\n')

    print('----- Custos Cadastrados Com Sucesso !! -----\n')

    global modelo
    modelo = OtimizaLucro(retornos, custos, capitalInvestimento)



def inputArquivo():
    if(os.path.isfile("Desafio.xlsx")):
        dados = np.asarray(pd.read_excel("Desafio.xlsx"))
        custos = dados[:, 0]
        retornos = dados[:, 1]   
        capitalInvestimento = 2400000
        
        global modelo
        modelo = OtimizaLucro(retornos, custos, capitalInvestimento)
        print("----- Dados Carregados com Sucesso -----")
    else:
        print("O Arquivo 'Desafio.xlsx' não existe!")

def OtimizarRetornos():
    modelo.resolver()


print("\n------ Desafio ENACOM 2023 - 3° Bootcamp ------")
print("Esse Sistema é Responsável por Receber Suas Opções de Investimento assim como seus respectivos retornos esperados, e seus custos. Com base no seu Capital de Investimento informado o sistema retornará a opção ótima de investimento, isso é, aquela que resultará no maior retorno de investimento com base nas restrições. ")

while True:
    try:
        menu()
    except ValueError:
        print("Isso não é um número! tente novamente.\n")