# Diagrama de Classes - VetConecta

## Visão Geral
Este diagrama representa a estrutura de classes do sistema VetConecta, um portal web que conecta tutores de pets a veterinários.

## Diagrama de Classes em Mermaid

```mermaid
classDiagram
    class Usuario {
        +int id_usuario
        +str nome
        +str email
        +str senha
        +str telefone
    }
    
    class Tutor {
    }
    
    class Veterinario {
        +str crmv
        +bool verificado
        +str bio
    }
    
    class Administrador {
        +int id_admin
        +str nome
        +str email
        +str senha
    }
    
    class CategoriaArtigo {
        +int id
        +str nome
        +str|None descricao
    }
    
    class PostagemArtigo {
        +int id
        +int id_veterinario
        +str titulo
        +str conteudo
        +int id_categoria_artigo
        +date data_publicacao
        +int visualizacoes
        +Veterinario veterinario
        +CategoriaArtigo categoria_artigo
    }
    
    class PostagemFeed {
        +int id_postagem_feed
        +int id_tutor
        +str|None imagem
        +str descricao
        +date data_postagem
        +Tutor tutor
    }
    
    class Comentario {
        +int id
        +Usuario id_usuario
        +PostagemArtigo id_artigo
        +str texto
        +str data_comentario
        +str|None data_moderacao
    }
    
    class CurtidaArtigo {
        +Usuario usuario
        +PostagemArtigo artigo
        +str data_curtida
    }
    
    class CurtidaFeed {
        +int id_usuario
        +int id_postagem_feed
        +str|None data_curtida
    }
    
    class Seguida {
        +int id_veterinario
        +int id_tutor
        +date data_inicio
        +Veterinario veterinario
        +Tutor tutor
    }
    
    class Chamado {
        +int id
        +int id_usuario
        +int id_admin
        +str titulo
        +str descricao
        +str status
        +str data
    }
    
    class RespostaChamado {
        +int|None id
        +int id_chamado
        +str titulo
        +str descricao
        +date|None data
    }
    
    class Denuncia {
        +int|None id_denuncia
        +int id_usuario
        +int id_admin
        +str motivo
        +str data_denuncia
        +str status
    }
    
    class VerificacaoCRMV {
        +int id
        +int|Veterinario veterinario
        +Administrador administrador
        +str data_verificacao
        +str status_verificacao
    }
    
    %% Heranças
    Tutor --|> Usuario : herda
    Veterinario --|> Usuario : herda
    
    %% Relacionamentos de Composição/Agregação
    PostagemArtigo --> Veterinario : autor
    PostagemArtigo --> CategoriaArtigo : categoria
    PostagemFeed --> Tutor : autor
    
    %% Relacionamentos de Associação
    Comentario --> Usuario : autor
    Comentario --> PostagemArtigo : artigo
    
    CurtidaArtigo --> Usuario : usuário
    CurtidaArtigo --> PostagemArtigo : artigo
    
    CurtidaFeed --> Usuario : usuário
    CurtidaFeed --> PostagemFeed : postagem
    
    Seguida --> Veterinario : seguido
    Seguida --> Tutor : seguidor
    
    Chamado --> Usuario : solicitante
    Chamado --> Administrador : atendente
    
    RespostaChamado --> Chamado : chamado
    
    Denuncia --> Usuario : denunciante
    Denuncia --> Administrador : moderador
    
    VerificacaoCRMV --> Veterinario : verificado
    VerificacaoCRMV --> Administrador : verificador
```

## Descrição das Classes

### Classes de Usuário
- **Usuario**: Classe base para todos os tipos de usuários do sistema
- **Tutor**: Herda de Usuario, representa donos de pets
- **Veterinario**: Herda de Usuario, possui informações profissionais (CRMV, bio, status de verificação)
- **Administrador**: Usuário administrativo do sistema (não herda de Usuario)

### Classes de Conteúdo
- **PostagemArtigo**: Artigos escritos por veterinários, categorizados
- **PostagemFeed**: Posts do feed social criados por tutores
- **CategoriaArtigo**: Categorização para artigos veterinários

### Classes de Interação
- **Comentario**: Comentários em artigos
- **CurtidaArtigo**: Curtidas em artigos
- **CurtidaFeed**: Curtidas em posts do feed
- **Seguida**: Relacionamento de seguir entre tutores e veterinários

### Classes Administrativas
- **Chamado**: Tickets de suporte
- **RespostaChamado**: Respostas aos chamados
- **Denuncia**: Denúncias de conteúdo/usuários
- **VerificacaoCRMV**: Processo de verificação de registro veterinário

## Observações
- O sistema possui clara separação entre conteúdo de feed (social) e artigos (profissional)
- Existe um sistema completo de moderação com denúncias e verificação de credenciais
- Os relacionamentos mostram um sistema de rede social especializada para o contexto veterinário