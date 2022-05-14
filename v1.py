from novadax import RequestClient as NovaClient
import time
import keyboard
import os


nova_client = NovaClient('','')

PercentGanho=float(0.15)
PercentInvest=float(0.15)
ValorInvest=str(50)

os.system('cls' if os.name == 'nt' else 'clear')  

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

def configParam(PercentGanho,PercentInvest,ValorInvest,opc):
    print('\33[32m'+'-----------------------------------------------')
    print('                Configurações                  ')
    print('-----------------------------------------------'+'\033[0m') 
    print('\n') 
    print('O valor do percentual de ganho desejado:  ' ,PercentGanho) 
    print('O valor do percentual ofset investimento: ' ,PercentInvest) 
    print('O valor que deseja investir:              ' ,ValorInvest) 
    print('\n') 
    print('(2) Iniciar Investimentos') 
    print('\n') 
    opc2=int(input('Digite a opção desejada: '))
    if (opc2==2):
        opc=1
        return
        
        


conta = nova_client.get_account_balance()
result = nova_client.get_ticker('BTC_BRL')


ultimo=result['data']['lastPrice']
menor=result['data']['low24h']
maior=result['data']['high24h']

tamanho=len(conta['data'])
saldo=conta['data'][int(tamanho)-1]['balance']

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
    os.system('cls' if os.name == 'nt' else 'clear')
    configParam(PercentGanho,PercentInvest,ValorInvest,opc)



    
if (opc==1):
    os.system('cls' if os.name == 'nt' else 'clear')    
    tempInicial=time.time()
    y=0

    print('Execultando analise... (Pressione ESC para sair)')

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

        
