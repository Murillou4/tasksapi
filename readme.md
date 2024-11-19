# **API de Autenticação e Gerenciamento de Tarefas**

Uma API RESTful desenvolvida em **Flask** para autenticação de usuários e gerenciamento de tarefas, com suporte a tokens JWT e integração com SQLite. A API permite gerenciar usuários e suas tarefas associadas de forma segura e eficiente.

---

## **Recursos Principais**

### **Gerenciamento de Usuários**
- Modelo de usuário com os seguintes atributos:
  - `UUID` (identificação única do usuário).
  - `nome` (nome completo do usuário).
  - `foto` (armazenada em formato binário blob).
  - `e-mail` (único por usuário).
  - `senha` (armazenada com hash seguro).
- Funcionalidades:
  - Geração de token JWT para autenticação (sem expiração).
  - Registro e login de usuários com validação de e-mail.
  - Gerenciamento do perfil do usuário:
    - Obter detalhes do perfil.
    - Atualizar a foto do perfil.
    - Excluir a conta do usuário.

### **Gerenciamento de Tarefas**
- Modelo de tarefa com os seguintes atributos:
  - `ID` (identificação única da tarefa).
  - `tópico` (descrição ou título da tarefa).
  - `timestamp` (data e hora de criação, gerado automaticamente no servidor).
  - `UUID` do usuário (para vincular a tarefa a um usuário específico).
  - `status de conclusão` (indicando se a tarefa foi concluída).
- Funcionalidades:
  - Operações CRUD completas:
    - Criar, ler, atualizar e excluir tarefas.
  - Vinculação de tarefas ao usuário autenticado.
  - Manipulação automática de timestamps.

---

## **Endpoints da API**

### **Autenticação**

#### **Login**
- **Descrição:** Valida o e-mail e a senha do usuário e retorna um token JWT.
- **URL:** `/auth/login`
- **Método:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Corpo da Requisição:**
  ```json
  {
    "email": "usuario@example.com",
    "password": "senhaSegura123"
  }
  ```
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "message": "Login successful",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Exemplo de Resposta de Erro (Usuário Não Encontrado):**
  ```json
  {
    "message": "User not found"
  }
  ```

#### **Registro**
- **Descrição:** Cria um novo usuário, valida a unicidade do e-mail e retorna um token JWT.
- **URL:** `/auth/register`
- **Método:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Corpo da Requisição:**
  ```json
  {
    "name": "João Silva",
    "email": "joao.silva@example.com",
    "password": "senhaSegura123"
  }
  ```
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "message": "Register successful",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```
- **Exemplo de Resposta de Erro (E-mail Já Existe):**
  ```json
  {
    "message": "Email already exists"
  }
  ```

### **Operações de Usuário**

#### **Obter Detalhes do Usuário Autenticado**
- **Descrição:** Retorna as informações do usuário autenticado.
- **URL:** `/user/me`
- **Método:** `GET`
- **Headers:**
  - `Authorization: Bearer <token>`
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "name": "João Silva",
    "email": "joao.silva@example.com",
    "photo": "base64EncodedImageString"
  }
  ```
- **Exemplo de Resposta de Erro (Token Inválido):**
  ```json
  {
    "message": "Invalid token"
  }
  ```

#### **Atualizar Foto do Perfil**
- **Descrição:** Atualiza a foto do perfil do usuário autenticado.
- **URL:** `/user/update/photo`
- **Método:** `PUT`
- **Headers:**
  - `Authorization: Bearer <token>`
  - `Content-Type: multipart/form-data`
- **Corpo da Requisição:**
  - **Form Data:**
    - `photo`: Arquivo de imagem (formatos permitidos: `.png`, `.jpg`, `.jpeg`)
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "message": "Photo updated successfully",
    "photo": "base64EncodedImageString"
  }
  ```
- **Exemplo de Resposta de Erro (Formato de Imagem Inválido):**
  ```json
  {
    "message": "Invalid photo format"
  }
  ```

#### **Excluir Conta do Usuário**
- **Descrição:** Exclui a conta do usuário autenticado.
- **URL:** `/user/delete`
- **Método:** `DELETE`
- **Headers:**
  - `Authorization: Bearer <token>`
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "message": "User account deleted successfully"
  }
  ```
- **Exemplo de Resposta de Erro (Token Inválido):**
  ```json
  {
    "message": "Invalid token"
  }
  ```

### **Operações de Tarefa**

#### **Obter Todas as Tarefas do Usuário Autenticado**
- **Descrição:** Retorna todas as tarefas associadas ao usuário autenticado.
- **URL:** `/tasks/byuser`
- **Método:** `GET`
- **Headers:**
  - `Authorization: Bearer <token>`
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "message": "Tasks fetched successfully",
    "tasks": [
      {
        "id": 1,
        "topic": "Comprar mantimentos",
        "created_at": "2023-10-01T10:00:00",
        "completed": false
      },
      {
        "id": 2,
        "topic": "Estudar Flask",
        "created_at": "2023-10-02T14:30:00",
        "completed": true
      }
    ]
  }
  ```
- **Exemplo de Resposta de Erro (Token Inválido):**
  ```json
  {
    "message": "Invalid token"
  }
  ```

#### **Criar Nova Tarefa**
- **Descrição:** Adiciona uma nova tarefa para o usuário autenticado.
- **URL:** `/tasks/add`
- **Método:** `POST`
- **Headers:**
  - `Authorization: Bearer <token>`
  - `Content-Type: application/json`
- **Corpo da Requisição:**
  ```json
  {
    "topic": "Ler documentação do projeto"
  }
  ```
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "message": "Task added successfully",
    "task": {
      "id": 3,
      "topic": "Ler documentação do projeto",
      "created_at": "2023-10-03T09:15:00",
      "completed": false
    }
  }
  ```
- **Exemplo de Resposta de Erro (Tópico Não Informado):**
  ```json
  {
    "message": "Topic is required"
  }
  ```

#### **Atualizar Tópico da Tarefa**
- **Descrição:** Atualiza o tópico de uma tarefa existente. Somente o proprietário pode atualizar.
- **URL:** `/tasks/update/topic`
- **Método:** `PUT`
- **Headers:**
  - `Authorization: Bearer <token>`
  - `Content-Type: application/json`
- **Corpo da Requisição:**
  ```json
  {
    "id": 3,
    "topic": "Ler documentação completa do projeto"
  }
  ```
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "message": "Task updated successfully",
    "task": {
      "id": 3,
      "topic": "Ler documentação completa do projeto",
      "created_at": "2023-10-03T09:15:00",
      "completed": false
    }
  }
  ```
- **Exemplo de Resposta de Erro (Tarefa Não Encontrada):**
  ```json
  {
    "message": "Task not found"
  }
  ```
- **Exemplo de Resposta de Erro (Não é o Proprietário da Tarefa):**
  ```json
  {
    "message": "You are not the owner of this task"
  }
  ```

#### **Atualizar Status de Conclusão da Tarefa**
- **Descrição:** Atualiza o status de conclusão de uma tarefa existente. Somente o proprietário pode atualizar.
- **URL:** `/tasks/update/completed`
- **Método:** `PUT`
- **Headers:**
  - `Authorization: Bearer <token>`
  - `Content-Type: application/json`
- **Corpo da Requisição:**
  ```json
  {
    "id": 3,
    "completed": true
  }
  ```
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "message": "Task updated successfully",
    "task": {
      "id": 3,
      "topic": "Ler documentação completa do projeto",
      "created_at": "2023-10-03T09:15:00",
      "completed": true
    }
  }
  ```
- **Exemplo de Resposta de Erro (Tarefa Não Encontrada):**
  ```json
  {
    "message": "Task not found"
  }
  ```
- **Exemplo de Resposta de Erro (Não é o Proprietário da Tarefa):**
  ```json
  {
    "message": "You are not the owner of this task"
  }
  ```

#### **Excluir Tarefa**
- **Descrição:** Exclui uma tarefa existente. Somente o proprietário pode excluir.
- **URL:** `/tasks/delete`
- **Método:** `DELETE`
- **Headers:**
  - `Authorization: Bearer <token>`
  - `Content-Type: application/json`
- **Corpo da Requisição:**
  ```json
  {
    "id": 3
  }
  ```
- **Exemplo de Resposta Sucesso:**
  ```json
  {
    "message": "Task deleted successfully"
  }
  ```
- **Exemplo de Resposta de Erro (Tarefa Não Encontrada):**
  ```json
  {
    "message": "Task not found"
  }
  ```
- **Exemplo de Resposta de Erro (Não é o Proprietário da Tarefa):**
  ```json
  {
    "message": "You are not the owner of this task"
  }
  ```

---

## **Tecnologias Utilizadas**
- **Linguagem**: Python
- **Framework**: Flask
- **Banco de Dados**: SQLite
- **Autenticação**: JWT (JSON Web Tokens)
- **Hash de Senha**: `bcrypt`
- **Documentação**: Flask-RESTx ou Swagger

---

## **Como Executar o Projeto**

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/sua-api.git
   cd sua-api
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o servidor:
   ```bash
   flask run
   ```

5. Acesse a API em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## **Estrutura do Projeto**

