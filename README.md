# zabbix-glpi
Integração para abertura de incidentes do servidor zabbix com o sistema de chamado GLPI.

O script deve ser colocado no diretorio de execução de scripts externos do zabbix:
por exemplo:
/usr/lib/zabbix/externalscripts

Pacotes necessarios:
python3.6 e o pacotes requests do python


Help:

./chamado.py --help

usage: chamado.py [-h] [--chamado CHAMADO CHAMADO] [--addhost ADDHOST]
                  [--delhost DELHOST]
                  [--acompanhamento ACOMPANHAMENTO ACOMPANHAMENTO]
                  [--fechamento FECHAMENTO]

Abertura de chamados GLPI via zabbix

optional arguments:
  -h, --help            show this help message and exit
  --chamado CHAMADO CHAMADO
                        --chamado "titulo" "corpo do chamado"
  --addhost ADDHOST     --addhost "{HOST.NAME}"
  --delhost DELHOST     --delhost "{HOST.NAME}"
  --acompanhamento ACOMPANHAMENTO ACOMPANHAMENTO
                        --acompanhamento
                        "Problem:{HOST.NAME}-{EVENT.NAME}-{EVENT.ID}" "Texto
                        de acompanhamento"
  --fechamento FECHAMENTO
                        Ex: --fechamento "Problem:{HOST.NAME}-{EVENT.NAME}"
                        

Exemplo:

Abertura de chamado:

/usr/bin/python3.6 /usr/lib/zabbix/externalscripts/glpi/chamado.py --chamado "Problem:LAB-HOST-Zabbix agent on LAB-HOST is unreachable for 5 minutes-1383" "Problema inciado as 12:28:08 do dia 2020.03.17
Problema: Zabbix agent on LAB-CENTRIX is unreachable for 5 minutes
HOSTNAME: LAB-HOST
IPHOST: 192.168.100.101
SEVERIDADE: Average
Original problem ID: 1383"

Acompanhamento:

/usr/bin/python3.6 /usr/lib/zabbix/externalscripts/glpi/chamado.py --acompanhamento "Problem:LAB-HOST-Zabbix agent on LAB-HOST is unreachable for 5 minutes-1383" "Digite seu texto"

Fechar chamado:

/usr/bin/python3.6 /usr/lib/zabbix/externalscripts/glpi/chamado.py --fechamento "Problem:LAB-HOST-Zabbix agent on LAB-HOST is unreachable for 5 minutes"
