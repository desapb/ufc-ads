# PROJETO DE AVALIAÇÃO DE DESEMPENHO

#### Requisitos
- Python 3.8
- Docker 20.10.16
- Docker-compose 1.29.2
- NLTK-Stopwords (python -m nltk.downloader stopwords)

#### Resultados consolidados
https://docs.google.com/spreadsheets/d/1gesHLp9ouoI3U0zouuIIYiBWd4h--jx2JyCV8j6g1uk/edit?usp=sharing



## CENÁRIO A
Executar o comando:
- $ export PYTHONPATH='/home/ubuntu/avaliacao-desempenho'

#### Redis
- executar: '$ python3 /home/ubuntu/avaliacao-desempenho/redis-controller/produtor.py <quantidade de iteracoes> &'
- O resultado será armazenado no arquivo /home/ubuntu/avaliacao-desempenho/logs/redis/cenario_a.csv

#### RabbitMQ
- executar: '$ python3 /home/ubuntu/avaliacao-desempenho/rabbitmq-controller/produtor.py <quantidade de iteracoes> &'
- O resultado será armazenado no arquivo /home/ubuntu/avaliacao-desempenho/logs/rabbitmq/cenario_a.csv

#### Kafka
- executar: '$ python3 /home/ubuntu/avaliacao-desempenho/kafka-controller/produtor.py <quantidade de iteracoes> &'
- O resultado será armazenado no arquivo /home/ubuntu/avaliacao-desempenho/logs/kafka/cenario_a.csv



## Cenário B
Executar o comando:
- $ export PYTHONPATH='/home/ubuntu/avaliacao-desempenho'

#### Redis
- executar: '$ python3 /home/ubuntu/avaliacao-desempenho/redis-controller/consumidor.py <quantidade de iteracoes> &'
- O resultado será armazenado no arquivo /home/ubuntu/avaliacao-desempenho/logs/redis/cenario_b.csv

#### RabbitMQ
- executar: '$ python3 /home/ubuntu/avaliacao-desempenho/rabbitmq-controller/consumidor.py <quantidade de iteracoes> &'
- O resultado será armazenado no arquivo /home/ubuntu/avaliacao-desempenho/logs/rabbitmq/cenario_b.csv

#### Kafka
- executar: '$ python3 /home/ubuntu/avaliacao-desempenho/kafka-controller/consumidor.py <quantidade de iteracoes> &'
- O resultado será armazenado no arquivo /home/ubuntu/avaliacao-desempenho/logs/kafka/cenario_b.csv