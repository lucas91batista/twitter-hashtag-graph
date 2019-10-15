# Twitter-hashtag-graph

Este projeto utiliza ferramentas de Big Data para extraír dados do Twitter, processar e depois armazenar esses dados em um banco de dados NoSQL. Este projeto tem dois objetivos principais:

* Criar um rank das hashtags para descobrir os "Trend Topics" entre os Tweets baixados;
* Criar um grafo para explorar o relacionamento entre: (1) os usuários e as suas hashtags publicadas; (2) as hashtags de um mesmo tweet.

## Executando o projeto

Clique no banner abaixo para executar o projeto em uma instância Binder com as ferramentas necessárias instaladas. O projeto é executado no navegador, sem a necessidade de instalar as ferramentas na sua máquina =). 

[![Binder](https://notebooks.gesis.org/binder/badge_logo.svg)](https://notebooks.gesis.org/binder/v2/gh/lucas91batista/twitter-hashtag-graph/master?urlpath=lab)

Com o ambiente em execução, basta abrir o arquivo .ipynb e ir clicando no "Play" para executar as células:

![Executando o projeto](https://github.com/lucas91batista/twitter-hashtag-graph/blob/master/images/executeCellsJupyter.gif)


## Arquitetura e Tecnologias utilizadas


![Arquitetura](https://github.com/lucas91batista/twitter-hashtag-graph/blob/master/images/Arch-twitter-hashtag-graph.png)


## Ingestão de dados
A ferramenta utilizada para ingestão dos dados foi o **Flume**. O Flume baixa tweets diretamente do Twitter e armazena esses dados no sistema de arquivos distribuído (Hadoop HDFS). 

O Flume foi escolhido por ser uma ferramenta escalável horizontalmente, possuir tolerância a falhas, garantir a entrega das mensagens e ser facilmente integrado ao Twitter e outras tecnologias utilizadas no projeto. 

## Sistema de arquivos distribuídos
O sistema de arquivos distribuídos utilizado foi o **Hadoop HDFS**. o Hadoop HDFS armazena os Tweets que foram baixados pelo Flume.

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

```

O Hadoop Map Reduce foi escolhido por ser facilmente integrado com o Hadoop HDFS e também para fixar o conhecimento e melhorar o entendimento do Hadoop MapReduce. O código para as funções Map e Reduce foram escritos em python utilizando a biblioteca MRJob (https://mrjob.readthedocs.io/en/latest/).

Nesta etapa, utilizamos 
