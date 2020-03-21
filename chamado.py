#!/usr/bin/python3.6
import requests
import json
import argparse

user_token = 'user_token TOKEN DO USUARIO'
app_token = 'TOKEN DA API GLPI'
host = "HOST GLPI"

class Glpi():
    
    
    def __init__(self , user_token,app_token,host):
        self.user_token = user_token
        self.app_token = app_token
        self.url = "http://{}/glpi/apirest.php/initSession".format(host)
        self.host = host
        
        self.headers = {'Content-Type': 'application/json',
        'Authorization': user_token,
        'App-Token': app_token}

        try:

            r = requests.get(self.url,headers=self.headers).json()
            r = r['session_token']
            self.sessao_glpi ={'Content-Type': 'application/json',
            'Session-Token': r,
            'App-Token': app_token}

        except requests.exceptions.ConnectionError:
            print('Sem conexão com o GLPI, informe a URL correta')
                
    
    def AddHost(self,namehost):
        namehost = namehost.upper()
        resultado = self.BuscaHost(namehost)
        if resultado == 111:
            url = "http://{}/glpi/apirest.php/computer".format(self.host)
            data = json.dumps({"input": {"name":namehost,
                                         'firstname':namehost,
                                         'is_ids_visible':1}})
            
            r = requests.post(url,data=data, headers=self.sessao_glpi).json()
        
        return resultado
    
      
    def BuscaHost(self,namehost):
        url ='http://{}/glpi/apirest.php/search/computer?\
criteria[0][itemtype]=computer\
&criteria[0][field]=1\
&criteria[0][searchtype]=contains\
&criteria[0][value]={}\
&&forcedisplay[0]=2'.format(self.host,namehost.upper())
        r = requests.get(url,headers=self.sessao_glpi).json()
        try:
            
            if namehost.upper() in r['data'][0]['1']:
                """ Host ja existe"""
                return 110
                
        except KeyError:
            """" Host não existe"""
            return 111
        
    def DelHost(self,namehost):
        try:
            url ='http://{}/glpi/apirest.php/search/computer?\
criteria[0][itemtype]=computer\
&criteria[0][field]=1\
&criteria[0][searchtype]=contains\
&criteria[0][value]={}\
&&forcedisplay[0]=2'.format(self.host,namehost.upper())

            r = requests.get(url,headers=self.sessao_glpi).json()
            id_comp = r['data'][0]['2']
            
            url = "http://{}/glpi/apirest.php/computer".format(self.host)
            data = json.dumps({'input': {'id':id_comp},'force_purge': True})
            r = requests.delete(url,data=data,headers=self.sessao_glpi).json()
            return r
        except KeyError:
            return "404"
        
    def AbrirChamado(self,titulo,content):
        
        url = "http://{}/glpi/apirest.php/ticket".format(self.host)

        data = json.dumps({"input": [{
                    "name": titulo,
                    "content": content,
                    "itilcategories_id": 14,
                    "status": 4,
                    }]})


        r = requests.post(url, data=data, headers=self.sessao_glpi).json()

    def FecharChamado(self,titulochamado):
        try:
            consultachamado = self.BuscaChamado(titulochamado)
            
            for chamado in consultachamado:
                url ='http://{}/glpi/apirest.php/ticket/{}'.format(self.host,chamado)
                data = json.dumps({"input": {"status" : 5}})
                r = requests.put(url,data=data,headers=self.sessao_glpi).json()
            return f"tickets {consultachamado[0]} foram fechados"
        except KeyError:
            return 404
    
    def AcompanhamentoChamado(self,titulo,content):
        try:
            consultachamado = self.BuscaChamado(titulo)
            url ='http://{}/glpi/apirest.php/ticket/{}/TicketFollowup'.format(self.host,max(consultachamado))
            data = json.dumps({"input": {"tickets_id":max(consultachamado),
                "content" : content}})
            r = requests.post(url,data=data,headers=self.sessao_glpi).json()
            return r
        except KeyError:
            return 404
                   
    def BuscaChamado(self,*args):
        titulochamado = args[0]
        url ='http://{}/glpi/apirest.php/search/ticket?\
criteria[0][itemtype]=ticket\
&criteria[0][field]=1\
&criteria[0][searchtype]=contains\
&criteria[0][value]={}\
&criteria[1][link]=AND\
&criteria[1][field]=12\
&criteria[1][searchtype]=equal\
&criteria[1][value]=4\
&&forcedisplay[0]=2'.format(self.host,str(titulochamado))
        r = requests.get(url,headers=self.sessao_glpi).json()
        
        id_chamado = [chamado for chamado in range(len(r['data']))]
        chamados = []
        for chamado in id_chamado:
            chamados.append(r['data'][chamado]['2'])
        return chamados


chamado = Glpi(user_token,app_token,host)

parser = argparse.ArgumentParser(description='Abertura de chamados GLPI via zabbix')

parser.add_argument('--chamado',nargs=2,
                    help= '--chamado "titulo" "corpo do chamado"')

parser.add_argument('--addhost', nargs=1 ,
                    help='--addhost "{HOST.NAME}"')

parser.add_argument('--delhost', nargs=1 ,
                    help='--delhost "{HOST.NAME}"')

parser.add_argument('--acompanhamento', nargs=2,
                    help='--acompanhamento "Problem:{HOST.NAME}-{EVENT.NAME}-{EVENT.ID}" "Texto de acompanhamento"')

parser.add_argument('--fechamento', nargs=1,
                    help='Ex: --fechamento "Problem:{HOST.NAME}-{EVENT.NAME}"')

glpi = parser.parse_args()

if glpi.chamado !=None:
    print(chamado.AbrirChamado(glpi.chamado[0],glpi.chamado[1]))
    
if glpi.addhost !=None:
    print(chamado.AddHost(glpi.addhost[0]))

if glpi.delhost !=None:
    print(chamado.DelHost(glpi.delhost[0]))
    
if glpi.acompanhamento !=None:
    print(chamado.AcompanhamentoChamado(glpi.acompanhamento[0],glpi.acompanhamento[1]))
    
if glpi.fechamento !=None:
    print(chamado.FecharChamado(glpi.fechamento[0]))