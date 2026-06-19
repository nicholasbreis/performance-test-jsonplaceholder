import random
from locust import HttpUser, task, between


class JSONPlaceholderUser(HttpUser):
    """
    Simula um usuário navegando em uma aplicação que consome a JSONPlaceholder API.

    """

    host = "https://jsonplaceholder.typicode.com"
    wait_time = between(1, 3)

    # ------------------------------------------------------------------
    # Cenário 1 - GET /posts
    # Peso: 30 (mais frequente - simula a página inicial de um blog)
    #
    # Justificativa do peso:
    #   A listagem de posts é a operação mais comum em qualquer sistema
    #   de conteúdo. Usuários abrem a página inicial com muito mais
    #   frequência do que realizam qualquer outra ação.
    # ------------------------------------------------------------------
    @task(30)
    def listar_posts(self):
        with self.client.get(
            "/posts",
            name="GET /posts — listar todos",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                posts = response.json()
                # Valida que a resposta contém dados esperados
                if len(posts) > 0:
                    response.success()
                else:
                    response.failure("Lista de posts veio vazia")
            else:
                response.failure(f"Status inesperado: {response.status_code}")

    # ------------------------------------------------------------------
    # Cenário 2 - GET /posts/{id}
    # Peso: 25 (segundo mais frequente - detalhe de um item)
    #
    # Justificativa do peso:
    #   Após listar, muitos usuários clicam em um post específico.
    #   O ID é sorteado entre 1 e 100 (total de posts disponíveis)
    #   para simular acesso distribuído e não favorecer cache de um
    #   único recurso.
    # ------------------------------------------------------------------
    @task(25)
    def consultar_post(self):
        post_id = random.randint(1, 100)
        with self.client.get(
            f"/posts/{post_id}",
            name="GET /posts/{id} — detalhe",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                post = response.json()
                if "id" in post and "title" in post:
                    response.success()
                else:
                    response.failure("Resposta sem campos esperados (id, title)")
            else:
                response.failure(f"Status inesperado: {response.status_code}")

    # ------------------------------------------------------------------
    # Cenário 3 - POST /posts
    # Peso: 20 (operação de escrita - menos frequente que leitura)
    #
    # Justificativa do peso:
    #   Criação de conteúdo é menos comum que consumo, mas representa
    #   a carga mais pesada no servidor. Simula um usuário autenticado
    #   publicando um novo post.
    # ------------------------------------------------------------------
    @task(20)
    def criar_post(self):
        payload = {
            "title": f"Post de teste #{random.randint(1000, 9999)}",
            "body": (
                "Este é o corpo de um post criado automaticamente "
                "durante o teste de performance com Locust."
            ),
            "userId": random.randint(1, 10),
        }
        with self.client.post(
            "/posts",
            json=payload,
            name="POST /posts — criar post",
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                criado = response.json()
                if "id" in criado:
                    response.success()
                else:
                    response.failure("Resposta de criação sem campo 'id'")
            else:
                response.failure(f"Status inesperado: {response.status_code}")

    # ------------------------------------------------------------------
    # Cenário 4 - POST /comments
    # Peso: 15 (escrita secundária - comentários são menos frequentes)
    #
    # Justificativa do peso:
    #   Nem todo leitor comenta. Representa a interação secundária de
    #   um usuário engajado. O postId é vinculado a um post existente
    #   (1–100) para simular realismo.
    # ------------------------------------------------------------------
    @task(15)
    def criar_comentario(self):
        post_id = random.randint(1, 100)
        payload = {
            "postId": post_id,
            "name": "Usuário de Teste Locust",
            "email": f"teste{random.randint(1, 999)}@exemplo.com",
            "body": (
                "Comentário gerado automaticamente durante execução "
                "do teste de carga. Verificando latência de escrita."
            ),
        }
        with self.client.post(
            "/comments",
            json=payload,
            name="POST /comments — criar comentário",
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                criado = response.json()
                if "id" in criado and "postId" in criado:
                    response.success()
                else:
                    response.failure("Campos 'id' ou 'postId' ausentes na resposta")
            else:
                response.failure(f"Status inesperado: {response.status_code}")

    # ------------------------------------------------------------------
    # Cenário 5 - GET /users
    # Peso: 10 (menos frequente - página de perfis/equipe)
    #
    # Justificativa do peso:
    #   Listagem de usuários é uma funcionalidade acessada raramente
    #   (ex: página "Sobre" ou perfil de autores). Menor peso reflete
    #   uso real em sistemas de blog/conteúdo.
    # ------------------------------------------------------------------
    @task(10)
    def listar_usuarios(self):
        with self.client.get(
            "/users",
            name="GET /users — listar usuários",
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                usuarios = response.json()
                if len(usuarios) > 0:
                    response.success()
                else:
                    response.failure("Lista de usuários veio vazia")
            else:
                response.failure(f"Status inesperado: {response.status_code}")
