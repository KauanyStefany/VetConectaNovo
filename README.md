# 🐾 VetConecta

<div align="center">
  <img src="static/img/logos/vetconecta-cor.png" alt="VetConecta Logo" width="200"/>

  **Plataforma de Conexão Veterinária**

  [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
  [![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
  [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.8-purple.svg)](https://getbootstrap.com/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

---

## 📖 Sobre o Projeto

O **VetConecta** é uma plataforma web que conecta tutores de animais e veterinários em um ambiente digital que valoriza informação de qualidade, cuidado responsável e amor pelos pets. A aplicação oferece conteúdos confiáveis, revisados por profissionais, abordando temas como saúde, nutrição, comportamento e cuidados preventivos.

### 🎯 Principais Funcionalidades

- 📝 **Artigos Veterinários** - Conteúdo educativo criado por veterinários verificados
- 📸 **Petgram** - Feed de fotos e histórias de pets (estilo Instagram)
- 💬 **Sistema de Comentários** - Interação entre tutores e veterinários
- ❤️ **Curtidas** - Engajamento com conteúdos favoritos
- 🔍 **Busca Avançada** - Encontre artigos e posts por palavras-chave
- 🎫 **Sistema de Chamados** - Suporte técnico para usuários
- ✅ **Verificação CRMV** - Selo verificado para veterinários registrados
- 👤 **Perfis Personalizados** - Para tutores, veterinários e administradores
- 📊 **Dashboard de Estatísticas** - Métricas de visualizações e engajamento

---

## 👩‍💻 Autoras

Este projeto foi desenvolvido com dedicação e carinho por alunas do **Instituto Federal do Espírito Santo – Campus Cachoeiro de Itapemirim**:

<table align="center">
  <tr>
    <td align="center">
      <img src="static/img/alunas/brenda.jpg" width="100px;" alt="Brenda Souza"/><br>
      <sub><b>Brenda Souza Oliveira</b></sub>
    </td>
    <td align="center">
      <img src="static/img/alunas/kauany.jpg" width="100px;" alt="Kauany Stefany"/><br>
      <sub><b>Kauany Stefany Gomes de Oliveira</b></sub>
    </td>
    <td align="center">
      <img src="static/img/alunas/luana.jpg" width="100px;" alt="Luana Santos"/><br>
      <sub><b>Luana Santos Neves</b></sub>
    </td>
    <td align="center">
      <img src="static/img/alunas/sofia.jpg" width="100px;" alt="Sofia Koppe"/><br>
      <sub><b>Sofia Koppe Fernandes Bettcher</b></sub>
    </td>
  </tr>
</table>

**Instituição**: Instituto Federal do Espírito Santo (IFES)
**Campus**: Cachoeiro de Itapemirim
**Curso**: Técnico em Informática / Desenvolvimento de Sistemas
**Ano**: 2025

---

## 🚀 Tecnologias Utilizadas

### Backend
- **[Python 3.11+](https://www.python.org/)** - Linguagem de programação
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI
- **[SQLite](https://www.sqlite.org/)** - Banco de dados relacional
- **[Pydantic](https://docs.pydantic.dev/)** - Validação de dados

### Frontend
- **[Jinja2](https://jinja.palletsprojects.com/)** - Engine de templates
- **[Bootstrap 5.3.8](https://getbootstrap.com/)** - Framework CSS
- **[Bootstrap Icons](https://icons.getbootstrap.com/)** - Biblioteca de ícones
- **[JavaScript Vanilla](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)** - Interatividade

### Segurança
- **[bcrypt](https://pypi.org/project/bcrypt/)** - Hash de senhas
- **[python-multipart](https://pypi.org/project/python-multipart/)** - Upload de arquivos
- **[Pillow](https://pillow.readthedocs.io/)** - Validação de imagens
- **[SlowAPI](https://github.com/laurentS/slowapi)** - Rate limiting

### Desenvolvimento
- **[pytest](https://pytest.org/)** - Framework de testes
- **[pytest-cov](https://pytest-cov.readthedocs.io/)** - Cobertura de testes
- **[mypy](https://mypy.readthedocs.io/)** - Type checking

---

## 📁 Estrutura do Projeto

```
VetConecta/
├── app/                      # Estrutura moderna (em desenvolvimento)
│   ├── config/              # Configurações Pydantic
│   ├── db/                  # Conexão de banco de dados
│   ├── models/              # Models Pydantic
│   └── schemas/             # DTOs e schemas
├── config/                  # Configurações de upload
├── data/                    # Dados seed (JSON)
│   ├── categorias_artigos.json
│   ├── postagens_artigos.json
│   ├── postagens_feeds.json
│   ├── tutores.json
│   └── veterinarios.json
├── dtos/                    # Data Transfer Objects
├── model/                   # Dataclasses de domínio
├── repo/                    # Repositórios (camada de dados)
├── routes/                  # Rotas FastAPI
│   ├── admin/              # Rotas administrativas
│   ├── publico/            # Rotas públicas
│   ├── tutor/              # Rotas do tutor
│   ├── usuario/            # Rotas gerais de usuário
│   └── veterinario/        # Rotas do veterinário
├── sql/                     # Queries SQL organizadas
├── static/                  # Arquivos estáticos
│   ├── css/                # Estilos customizados
│   ├── img/                # Imagens e logos
│   └── js/                 # Scripts JavaScript
├── templates/               # Templates Jinja2
│   ├── admin/              # Templates administrativos
│   ├── componentes/        # Componentes reutilizáveis
│   ├── publico/            # Templates públicos
│   ├── tutor/              # Templates do tutor
│   ├── usuario/            # Templates de usuário
│   └── veterinario/        # Templates do veterinário
├── tests/                   # Testes automatizados
├── util/                    # Utilitários e helpers
├── logs/                    # Logs da aplicação
├── main.py                  # Ponto de entrada da aplicação
├── requirements.txt         # Dependências Python
├── .env.example            # Exemplo de variáveis de ambiente
├── CLAUDE.md               # Documentação técnica do projeto
├── PENDENCIAS.md           # Funcionalidades pendentes
├── GUIA_IMPLEMENTACAO.md   # Guia para desenvolvedores
└── README.md               # Este arquivo
```

---

## ⚙️ Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/vetconecta.git
cd vetconecta
```

### 2. Criar Ambiente Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Gerar SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Editar .env e adicionar as chaves geradas
nano .env  # ou seu editor preferido
```

**Variáveis obrigatórias no `.env`:**
```env
SECRET_KEY=sua_chave_secreta_aqui
CSRF_SECRET_KEY=outra_chave_secreta
DATABASE_PATH=dados.db
ENVIRONMENT=development
```

### 5. Inicializar o Banco de Dados

O banco de dados SQLite será criado automaticamente na primeira execução:

```bash
python main.py
```

O sistema irá:
- ✅ Criar o arquivo `dados.db`
- ✅ Criar todas as 16 tabelas
- ✅ Importar dados seed (categorias, artigos, posts, usuários)
- ✅ Configurar índices e relacionamentos

### 6. Acessar a Aplicação

Abra seu navegador e acesse:

```
http://127.0.0.1:8000
```

**Documentação interativa da API:**
```
http://127.0.0.1:8000/docs
```

---

## 🧪 Executar Testes

### Rodar todos os testes

```bash
pytest
```

### Rodar com cobertura

```bash
pytest --cov=repo --cov=model --cov=util
```

### Rodar testes específicos

```bash
pytest tests/test_usuario_repo.py -v
```

### Rodar apenas testes unitários

```bash
pytest -m unit
```

---

## 👥 Usuários de Teste

O sistema já vem com usuários pré-cadastrados para testes:

### Administrador
- **Email:** admin@vetconecta.com
- **Senha:** admin123
- **Acesso:** Painel administrativo completo

### Veterinário
- **Email:** vet1@email.com
- **Senha:** senha123
- **Acesso:** Criar artigos, solicitar verificação CRMV

### Tutor
- **Email:** tutor1@email.com
- **Senha:** senha123
- **Acesso:** Criar posts no Petgram, comentar, curtir

---

## 📚 Documentação

- **[CLAUDE.md](CLAUDE.md)** - Documentação técnica completa do projeto
  - Arquitetura e padrões
  - Comandos de desenvolvimento
  - Referência de API
  - Guia de estilos CSS

- **[PENDENCIAS.md](PENDENCIAS.md)** - Funcionalidades pendentes de implementação
  - Relatório detalhado de tarefas
  - Código de referência completo
  - Estimativas de tempo

- **[GUIA_IMPLEMENTACAO.md](GUIA_IMPLEMENTACAO.md)** - Guia passo a passo
  - Ordem recomendada de implementação
  - Tutoriais práticos
  - Checklist de conclusão

- **[TODOS_CONSOLIDADOS.md](TODOS_CONSOLIDADOS.md)** - Lista de TODOs
  - Resumo de todas as pendências
  - Status de cada funcionalidade

---

## 🎨 Design System

O VetConecta possui um sistema de design consistente baseado em:

### Paleta de Cores

```css
--cor-roxo: #44345A       /* Primary purple */
--cor-laranja: #FA811D    /* Accent orange */
--cor-verde: #2D5D5C      /* Success green */
--cor-bege: #ffe6ba       /* Warm beige */
--cor-bege-claro: #fff9ef /* Light beige */
--cor-rosa: #CA567C       /* Accent pink */
```

### Componentes Reutilizáveis

- ✅ Cards de artigos e posts
- ✅ Sistema de paginação
- ✅ Carrosséis responsivos
- ✅ Sistema de toast notifications
- ✅ Avatares com fallback
- ✅ Badges de status

Ver `static/css/base.css` para detalhes completos (440 linhas de utilities).

---

## 🔐 Segurança

O projeto implementa diversas camadas de segurança:

- 🔒 **Autenticação baseada em sessão** com cookies seguros
- 🔐 **Senhas hasheadas** com bcrypt (work factor 12)
- 🛡️ **CSRF Protection** em todos os formulários
- 📝 **Validação de entrada** com Pydantic
- 🚦 **Rate limiting** em endpoints sensíveis
- 🖼️ **Validação de arquivos** com magic bytes
- 🔍 **SQL Injection prevention** com queries parametrizadas
- 🚫 **XSS Protection** via Content Security Policy
- 📁 **Path traversal prevention** em uploads

---

## 🌐 API Endpoints

### Públicos (sem autenticação)
- `GET /` - Homepage
- `GET /artigos` - Lista de artigos
- `GET /artigos/{id}` - Detalhes do artigo
- `GET /petgram` - Feed de posts
- `GET /petgram/{id}` - Detalhes do post
- `POST /login` - Autenticação
- `POST /cadastro` - Registro de usuário

### Tutor (requer autenticação)
- `GET /tutor/` - Dashboard
- `POST /tutor/fazer_postagem_feed` - Criar post
- `PUT /tutor/editar_postagem_feed` - Editar post
- `DELETE /tutor/excluir_postagem_feed` - Excluir post

### Veterinário (requer autenticação)
- `GET /veterinario/` - Dashboard
- `POST /veterinario/cadastrar_postagem_artigo` - Criar artigo
- `GET /veterinario/listar_estatisticas` - Estatísticas
- `POST /veterinario/fazer_solicitacao_crmv` - Solicitar verificação

### Administrador (requer autenticação)
- `GET /administrador/` - Dashboard admin
- `GET /administrador/listar_chamados` - Gerenciar chamados
- `POST /administrador/responder_chamado` - Responder chamado
- `GET /administrador/listar_denuncias` - Moderar denúncias
- `POST /administrador/responder_verificacao_crmv` - Verificar CRMV

Ver documentação completa em `/docs` quando o servidor estiver rodando.

---

## 🤝 Como Contribuir

Este projeto está em desenvolvimento ativo como trabalho acadêmico. Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### Padrões de Código

- Seguir PEP 8 para Python
- Usar type hints
- Escrever testes para novas funcionalidades
- Documentar funções e classes
- Manter cobertura de testes acima de 80%

### Commits Semânticos

```
feat: Nova funcionalidade
fix: Correção de bug
docs: Atualização de documentação
style: Formatação de código
refactor: Refatoração
test: Adição de testes
chore: Tarefas de manutenção
```

---

## 📝 Status do Projeto

**Versão Atual:** 1.0.0 (em desenvolvimento)

### ✅ Funcionalidades Completas (26%)

- Sistema de autenticação e autorização
- CRUD de categorias de artigos (admin)
- Visualização pública de artigos e posts
- Sistema de visualizações (view tracking)
- Sistema de toasts/notificações
- Perfil de usuário (edição de dados, senha, foto)
- Paginação de conteúdo
- Recuperação de senha (sem envio de email)

### 🚧 Em Desenvolvimento (74%)

- Sistema de curtidas (backend)
- Sistema de comentários (backend)
- Área do tutor (gerenciar posts)
- Área do veterinário (gerenciar artigos)
- Área administrativa completa
- Sistema de chamados
- Sistema de denúncias
- Verificação de CRMV
- Sistema de busca
- Dashboard de estatísticas

Ver **[PENDENCIAS.md](PENDENCIAS.md)** para lista completa e detalhada.

---

## 📊 Estatísticas do Projeto

```
📦 Linhas de Código:      ~15.000 linhas
🗂️ Arquivos Python:       ~80 arquivos
🎨 Templates HTML:        ~45 templates
🧪 Testes:               ~30 testes
📚 Documentação:         ~2.000 linhas
🗃️ Entidades de Banco:   16 tabelas
🎯 Endpoints API:        ~70 rotas
```

---

## 🐛 Problemas Conhecidos

- [ ] Envio de email na recuperação de senha não implementado
- [ ] Sistema de busca em desenvolvimento
- [ ] Upload de múltiplas imagens por post não suportado
- [ ] Notificações em tempo real não implementadas

Reportar novos bugs em: [Issues](https://github.com/seu-usuario/vetconecta/issues)

---

## 📄 Licença

Este projeto está sob a licença MIT. Ver arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato

**Instituição:** Instituto Federal do Espírito Santo

**Campus:** Cachoeiro de Itapemirim

**Email:** contato@vetconecta.cachoeiro.es

**Site:** [vetconecta.cachoeiro.es](https://vetconecta.cachoeiro.es)

---

## 🙏 Agradecimentos

- **IFES - Campus Cachoeiro de Itapemirim** pelo suporte e infraestrutura
- **Professores orientadores** pela mentoria e orientação
- **Comunidade FastAPI** pela excelente documentação
- **Bootstrap Team** pelo framework CSS
- **Todos os colaboradores** que ajudaram a tornar este projeto realidade

---

<div align="center">
  <p>Desenvolvido com 💜 por alunas do IFES Cachoeiro</p>
  <p>© 2025 VetConecta. Todos os direitos reservados.</p>

  **[⬆ Voltar ao topo](#-vetconecta)**
</div>
