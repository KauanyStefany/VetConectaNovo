describe("Login de usuário - VetConecta", () => {
    it("Deve preencher e enviar o formulário de login com sucesso", () => {
        // Acesse a página de login
        cy.visit("http://127.0.0.1:8000/login")

        // Preencha os campos de e-mail e senha
        cy.get("input[name='email']").type("usuario@vetconecta.com")
        cy.get("input[name='senha']").type("senhaSegura123")

        // Clique no botão de enviar
        cy.get("button[type='submit']").click()

        // Verifique se o login foi bem-sucedido (ajuste conforme o comportamento da sua aplicação)
        cy.url().should("not.include", "/login") // Saiu da tela de login
        cy.contains("Bem-vindo").should("be.visible") // Ou o texto exibido após login
    })

    it("Deve exibir erro ao tentar logar com credenciais inválidas", () => {
        cy.visit("http://127.0.0.1:8000/login")

        // Preencha com dados incorretos
        cy.get("input[name='email']").type("emailinvalido@teste.com")
        cy.get("input[name='senha']").type("senhaErrada")

        // Envie o formulário
        cy.get("button[type='submit']").click()

        // Verifique se a mensagem de erro geral aparece
        cy.contains("Email ou senha incorretos").should("be.visible")
    })

    it("Deve validar campos obrigatórios", () => {
        cy.visit("http://127.0.0.1:8000/login")

        // Tente enviar sem preencher nada
        cy.get("button[type='submit']").click()

        // O navegador deve marcar os campos como inválidos
        cy.get("input[name='email']:invalid").should("exist")
        cy.get("input[name='senha']:invalid").should("exist")
    })

    it("Deve redirecionar para a página de cadastro ao clicar em 'Cadastre-se!'", () => {
        cy.visit("http://127.0.0.1:8000/login")

        cy.contains("Cadastre-se!").click()

        // Verifica se foi redirecionado corretamente
        cy.url().should("include", "/cadastro")
    })

    it("Deve redirecionar para a página de recuperação de senha ao clicar em 'Esqueci minha senha'", () => {
        cy.visit("http://127.0.0.1:8000/login")

        cy.contains("Esqueci minha senha").click()

        cy.url().should("include", "/esqueci-senha")
    })
})
