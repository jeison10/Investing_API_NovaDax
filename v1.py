from novadax import RequestClient as NovaClient
import time
import keyboard
import os

# credenciais da API Code
nova_client = NovaClient('','')

#configurações Padrões
PercentGanho=float(0.15)
PercentInvest=float(0.15)
ValorInvest=str(50)
opc=0

# Classe para configurações dos parametros
#--------------------------------------------------------------------------
class config:
    def __init__(self,percentGanho,PercentInvest,ValorInvest,opc) -> None:
        self.PercentGanho=percentGanho
        self.PercentInvest=PercentInvest
        self.ValorInvest=ValorInvest
        self.opc=opc
        pass
 
 
    def configParam(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\33[32m'+'-----------------------------------------------')
        print('                Configurações                  ')
        print('-----------------------------------------------'+'\033[0m') 
        print('\n') 
        print('O valor do percentual de ganho desejado:  ' ,self.PercentGanho) 
        print('O valor do percentual ofset investimento: ' ,self.PercentInvest) 
        print('O valor que deseja investir:              ' ,self.ValorInvest) 
        print('\n') 
        print('(1) Configurar') 
        print('(2) Voltar') 
        print('\n') 
        opc2=int(input('Digite a opção desejada: '))
       
        if (opc2==1):
            os.system('cls' if os.name == 'nt' else 'clear')
            self.ganho=float(input('Digite a porcentagem de ganho: '))
            self.queda=float(input('Digite a porcentagem de queda para começar a investir: '))
            self.invest=str(input('Digite o valor para o investimento: '))
            print('Ok, configurado! \n')
            time.sleep(1)    
            os.system('cls' if os.name == 'nt' else 'clear')
            pass
            
        
        if (opc2==2):
            os.system('cls' if os.name == 'nt' else 'clear')
            self.ganho=self.PercentGanho
            self.queda=self.PercentInvest
            self.invest=self.ValorInvest
            pass
#------------------------------------------------------------------------------------------------


# funcao aprensenta resultados        
def resultados(saldo):

    conta = nova_client.get_account_balance()
    novoSaldo=conta['data'][int(tamanho)-1]['balance']
    resFinal=float(novoSaldo)-float(saldo)
    print('\n')
    print('\033[33m'+'-----------------------------------------------')
    print('   Obrigado por usar o Bot Trade By Jeison     ')
    print('-----------------------------------------------')
    print('\n')
    print('Seu novo saldo é de: ',novoSaldo)
    print(f'Voce ganhou:  {resFinal:,.2f}'+'\033[0m')
    print('\n')

# Menu principal
def menu(conta, ultimo, menor, maior, tamanho, saldo,PercentGanho,PercentInvest,ValorInvest):
    os.system('cls' if os.name == 'nt' else 'clear')    

 
    print('\33[32m'+'-----------------------------------------------')
    print('      Bem vindo ao Bot Trade By Jeison         ')
    print('-----------------------------------------------'+'\033[0m')

    print('\n')
    print('Valor atual do BTC/BRL:      ',ultimo)
    print('Maior Valor nas ultimas 24h: ',maior)
    print('Menor Valor nas ultimas 24h: ',menor)
    print('Seu saldo em conta em Reais: ',saldo)
    print('\n')

        
    print("(1) Iniciar analises e investimento")
    print("(2) Configurações")
    print('\n')
    opc=int(input('Digite a opção desejada: '))

    if (opc==2):
        configura=config(PercentGanho,PercentInvest,ValorInvest,0)
        configura.configParam()
        PercentGanho=configura.ganho
        PercentInvest=configura.queda
        ValorInvest=configura.invest
        menu(conta, ultimo, menor, maior, tamanho, saldo,PercentGanho,PercentInvest,ValorInvest)

    
    if (opc==1):
        os.system('cls' if os.name == 'nt' else 'clear')    
        tempInicial=time.time()
        y=0

        print('Execultando analise... (Pressione ESC para sair)')

        #Inicia analise ate o botão ESC
        while (keyboard.is_pressed('esc') == False):
            tempFinal=time.time()
            if ((tempFinal-tempInicial)>8):
                tempInicial=time.time()

                CGREEN = '\33[32m'
                CRED = '\033[91m'
                CEND = '\033[0m'

                
                result = nova_client.get_ticker('BTC_BRL')
                novo=float(result['data']['lastPrice'])
                percent=100-(float(ultimo)*100)/novo
                
                if (percent>0):
                    print('\n')
                    print(CGREEN +'Subindo'+CEND)
                else:
                    print('\n')
                    print(CRED+'Caindo'+CEND)

                print('\n')
                print ("Preco atual: ",novo)
                print (f'Porcentagem:  {percent:,.2f}')
                


                if ((percent<=-(PercentInvest)) and (y==0)):
                    print('\n')
                    print(CGREEN+'Realizada ordem de compra'+CEND)
                    print('\n')
                    nova_client.create_order('BTC_BRL', 'MARKET', 'BUY', value = f'{ValorInvest}')
                    ultimo=novo                      
                    y=1
                        
                    time.sleep(12)
                    result2 = nova_client.list_orders('BTC_BRL', 'FINISHED')
                    compraBTC= result2['data'][0]['filledAmount']
                        
                    

                if ((percent>=(0.20+PercentGanho)) and (y==1)):
                    print('\n')
                    print(CRED+'Realizada ordem de venda'+CEND)
                    print('\n')
                    nova_client.create_order('BTC_BRL', 'MARKET', 'SELL', amount = compraBTC )
                    y=0
                    ultimo=novo
        opc=0    


    resultados(saldo)

        


conta = nova_client.get_account_balance()
result = nova_client.get_ticker('BTC_BRL')
ultimo=result['data']['lastPrice']
menor=result['data']['low24h']
maior=result['data']['high24h']
tamanho=len(conta['data'])
saldo=conta['data'][int(tamanho)-1]['balance']

#Chama menu principal
menu(conta, ultimo, menor, maior, tamanho, saldo,PercentGanho,PercentInvest,ValorInvest)

