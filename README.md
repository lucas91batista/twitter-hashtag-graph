# Twitter-hashtag-graph

Este projeto utiliza ferramentas de Big Data para extraír dados do Twitter, processar e depois armazenar esses dados em um banco de dados NoSQL. Este projeto tem dois objetivos principais:

* Criar um rank das hashtags para descobrir os "Trend Topics" entre os Tweets baixados;
* Criar um grafo para explorar o relacionamento entre: (1) os usuários e as suas hashtags publicadas; (2) as hashtags de um mesmo tweet.

## Executando o projeto

Clique em algum banner abaixo para executar o projeto em uma instância Binder com as ferramentas necessárias instaladas. O projeto é executado no navegador, sem a necessidade de instalar as ferramentas na sua máquina =). 

[![Binder](https://notebooks.gesis.org/binder/badge_logo.svg)](https://notebooks.gesis.org/binder/v2/gh/lucas91batista/twitter-hashtag-graph/master?urlpath=lab)

Com o ambiente em execução, basta abrir o arquivo .ipynb e ir clicando no "Play" para executar as células:

![Executando o projeto](https://github.com/lucas91batista/twitter-hashtag-graph/blob/master/images/executeCellsJupyter.gif)


## Arquitetura e Tecnologias utilizadas


![Arquitetura](https://github.com/lucas91batista/twitter-hashtag-graph/blob/master/images/Arch-twitter-hashtag-graph.png)


## Ingestão de dados
A ferramenta utilizada para ingestão dos dados foi o **Flume**. O Flume baixa tweets diretamente do Twitter e armazena esses dados no sistema de arquivos distribuído (Hadoop HDFS). 

O Flume foi escolhido por ser uma ferramenta escalável horizontalmente, possuir tolerância a falhas, garantir a entrega das mensagens e ser facilmente integrado ao Twitter e outras tecnologias utilizadas no projeto. 

## Sistema de arquivos distribuídos
O sistema de arquivos distribuídos utilizado foi o **Hadoop HDFS**. O Hadoop HDFS armazena os Tweets que foram baixados pelo Flume.

O Hadoop HDFS foi escolhido por ser distribuído, escalável horizontalmente, tolerante a falhas e ser facilmente integrado com diversas ferramentas que foram utilizadas no projeto ou que podem ser utilizadas para outras funcionalidades no futuro.

## Processamento em Batch
Para processamento em Batch foi utilizado o **Hadoop Map Reduce**. O Hadoop Map Reduce foi utilizado para:
* Criar um rank das hashtags para descobrir os "Trend Topics" entre os Tweets baixados. Por exemplo:
```
#hadoop 30
#bigdata 50
``` 
* Criar um grafo para explorar o relacionamento entre: (1) os usuários e as suas hashtags publicadas; (2) as hashtags de um mesmo tweet. Por exemplo:

**Tweet**
``` json
{  "created_at": "Thu Apr 06 15:24:15 +0000 2017",  
   "id_str": "850006245121695744",  
   "text": "Aprendendo algumas ferramentas para manipulação de dados #Hadoop #BigData",  
   "user": {    "id": 2244994945,    "name": "Twitter User",    "screen_name": "TwitterDev",    
               "location": "Internet",    "url": "https:\/\/dev.twitter.com\/",    
               "description": "Your official source for Twitter Platform news, updates & events. 
                              Need technical help? Visit https:\/\/twittercommunity.com\/ \u2328\ufe0f #TapIntoTwitter"  },  
   "place": {     },  
   "entities": {    "hashtags": [          ],    
                    "urls": [      {        "url": "https:\/\/t.co\/XweGngmxlP",        
                    "unwound": {          "url": "https:\/\/cards.twitter.com\/cards\/18ce53wgo4h\/3xo1c",          
                    "title": "Building the Future of the Twitter API Platform"        }      }    ],    
                    "user_mentions": [         ]  }
}

```

**Informações extraídas**
``` 
Nome do usuário: Twitter User
Hashtags: #Hadoop #BigData
``` 
**Grafo gerado**

![Grafo exemplo](https://github.com/lucas91batista/twitter-hashtag-graph/blob/master/images/Graph_example.jpg)


As seguintes transformações foram aplicadas nos dados nos dois processos MapReduce:
* Remoção de caracteres não alpha-numéricos;
* Remoção de unicodes;
* Remoção de caracteres de controle (\n \t);
* Conversão das hashtags para minúsculo.

O Hadoop Map Reduce foi escolhido por ser facilmente integrado com o Hadoop HDFS e também para fixar o conhecimento e melhorar o entendimento do Hadoop MapReduce. O código para as funções Map e Reduce foram escritos em python utilizando a biblioteca MRJob (https://mrjob.readthedocs.io/en/latest/).

## Banco de Dados
Para armazenar os dados já organizados foi utilizado o **Neo4J**. O Neo4j armazena o grafo que foi gerado pelo processo MapReduce permitindo que os dados sejam explorados utilizando operações orientadas a grafo, por exemplo, detecção de comunidade, caminhos mínimos etc.

O banco de dados NoSQL escolhido foi o de grafos, pois este projeto quer explorar a conexão entre os usuários e as hashtags. O banco escolhido foi o Neo4J pois utiliza como modelo o grafo de propriedades, possui uma linguagem de consulta própria (Cypher) para explorar os dados e possui diversos algoritmos implementados que podem ser utilizados para explorar os dados (https://neo4j.com/docs/graph-algorithms/current/introduction/).

## Consumo
Com os dados do Twitter transformados e armazenados no Neo4J, podemos consumir esses dados para realizar algumas análises, testar alguma hipótese, etc. Nesta etapa foi utilizado o Python apenas para visualizar o grafo gerado.
