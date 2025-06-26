# Bot Registro Sobrenatural - Discord
Obrigado por prestigiar este código! 🙏
Este é o primeiro bot de Discord que eu desenvolvi, e fico feliz em compartilhar com vocês. Espero que seja útil e que você aprenda bastante com ele!


Bot para automação de registro de usuários via mensagem em canal específico do Discord. O bot atribui cargos e altera o apelido do usuário com base nas informações enviadas.

---

## Modelo esperado para registro

O usuário deve enviar uma mensagem no canal de registro seguindo exatamente o modelo abaixo, preenchendo as informações:

Nome: <Nome real>
Nome Sobrenatural: <Nome sobrenatural>
ID: <ID único>
Raça: <Raça>
Clã: <Clã> (opcional)
Proficiência: <Proficiência>


**Exemplo:**

Nome: Luke Pym
Nome Sobrenatural: Luna Montgomery
ID: 152
Raça: Anjo
Clã: Ex Nihilo
Proficiência: Herbalista


---

## Campos obrigatórios

- **Nome** (não pode estar em branco)
- **Nome Sobrenatural** (não pode estar em branco)
- **ID** (não pode estar em branco)
- **Raça** (não pode estar em branco)
- **Proficiência** (não pode estar em branco)

---

## Campos opcionais

- **Clã** (caso não seja informado, o registro continua normalmente)

---

## Funcionamento do bot

- Ao receber uma mensagem no canal configurado, o bot valida o formato e campos obrigatórios.
- Se algum campo obrigatório estiver faltando ou incorreto, ele reage com ❌ e responde explicando o erro.
- Utiliza fuzzy matching para encontrar cargos que mais se aproximem do texto informado em "Clã" e "Proficiência".
- Caso o clã informado não exista, sugere opções próximas disponíveis no servidor.
- Se a proficiência não bater com cargos existentes, retorna erro.
- Após registro correto:
  - Edita o apelido do usuário para `<Nome Sobrenatural> | <ID>`
  - Adiciona os cargos correspondentes (Clã, Proficiência e cargo sobrenatural padrão)
  - Remove um cargo específico (configurado no código)
  - Reage com ✅ e responde confirmando o registro.

---

## Proficiências válidas (exemplos)

- Gemólogo  
- Herbalista  
- Alquimista  
- Ferreiro  
- Joalheiro  
- Mercador  

---

## Configuração

### Arquivo `.env`

Defina as variáveis:

```env
DISCORD_TOKEN=seu_token_aqui
CANAL_REGISTRO_ID=123456789012345678
SOBRENATURAL_ROLE_ID=987654321098765432
```

DISCORD_TOKEN: Token do bot no Discord.

CANAL_REGISTRO_ID: ID do canal onde o bot irá monitorar mensagens para registro.

SOBRENATURAL_ROLE_ID: ID do cargo padrão que será adicionado após o registro.

# Permissões do bot
O bot precisa das permissões:

Ler mensagens e histórico

Enviar mensagens

Adicionar reações

Gerenciar apelidos

Gerenciar cargos

Como usar
Configure o arquivo .env com as informações do seu servidor e bot.
Execute o bot (python main.py).
Envie mensagens no canal de registro seguindo o modelo indicado.
O bot irá validar e fazer o registro automático.

# Avisos
Atenção para a ortografia e acentuação ao enviar o registro para evitar erros de reconhecimento.
Caso o campo "Clã" esteja incorreto, o bot enviará sugestões dos clãs disponíveis no servidor.
O campo "Proficiência" é obrigatório e deve estar de acordo com os cargos existentes no servidor.

# Contato
Para dúvidas ou sugestões, abra uma issue no repositório.

Obrigado por usar o Bot Registro Sobrenatural!
