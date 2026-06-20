# Teste de Performance — JSONPlaceholder API

Testes de carga com [Locust](https://locust.io) sobre a API pública [JSONPlaceholder](https://jsonplaceholder.typicode.com).

---

## Pré-requisitos

- Python 3.8+
- pip

---

## Instalação

```bash
pip install locust
```

Verifique a instalação:

```bash
locust --version
```

---

## Execução dos testes

### Modo headless (recomendado para coleta de métricas)

Execute os três níveis de carga abaixo. Cada comando gera arquivos CSV com os resultados.

```bash
# 10 usuários simultâneos
locust -f locustfile.py --headless -u 10 -r 2 --run-time 60s --csv=results_10u

# 50 usuários simultâneos
locust -f locustfile.py --headless -u 50 -r 5 --run-time 60s --csv=results_50u

# 100 usuários simultâneos
locust -f locustfile.py --headless -u 100 -r 10 --run-time 60s --csv=results_100u
```

**Parâmetros:**

| Flag              | Descrição                            |
| ----------------- | ------------------------------------ |
| `-u`              | Número total de usuários simultâneos |
| `-r`              | Taxa de spawn (usuários por segundo) |
| `--run-time`      | Duração total do teste               |
| `--csv=<prefixo>` | Prefixo dos arquivos CSV gerados     |

### Modo interface web (opcional, para exploração)

```bash
locust -f locustfile.py
```

Acesse `http://localhost:8089` no navegador.

---

## Arquivos CSV gerados

Para cada execução, o Locust gera três arquivos:

| Arquivo                       | Conteúdo                                               |
| ----------------------------- | ------------------------------------------------------ |
| `<prefixo>_stats.csv`         | Métricas agregadas por endpoint (p50, p90, p95, req/s) |
| `<prefixo>_stats_history.csv` | Evolução das métricas ao longo do tempo                |
| `<prefixo>_failures.csv`      | Requisições com falha                                  |

---

## Cenários cobertos

| #   | Método | Endpoint      | Peso | Justificativa                          |
| --- | ------ | ------------- | ---- | -------------------------------------- |
| 1   | GET    | `/posts`      | 30%  | Listagem — operação mais frequente     |
| 2   | GET    | `/posts/{id}` | 25%  | Detalhe — segundo acesso mais comum    |
| 3   | POST   | `/posts`      | 20%  | Criação de conteúdo — escrita primária |
| 4   | POST   | `/comments`   | 15%  | Comentários — escrita secundária       |
| 5   | GET    | `/users`      | 10%  | Perfis — acesso raro                   |

---

## Execução com Docker (ponto extra)

### Pré-requisito

- Docker e Docker Compose instalados

### Subir o ambiente

```bash
docker-compose up
```

Isso executa os três níveis de carga automaticamente e salva os CSVs na pasta `results/`.

### Apenas um nível de carga

```bash
docker-compose run locust-10u
```

## Estrutura do projeto

```
.
├── locustfile.py         # Cenários de teste
├── generate_report.py    # Geração automática de relatório
├── docker-compose.yml    # Orquestração Docker
├── Dockerfile            # Imagem do Locust
├── results/              # CSVs gerados (criado automaticamente)
└── README.md             # Este arquivo
```
