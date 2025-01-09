import os
from dotenv import load_dotenv
import asyncio
import logging

from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Configurar personagem do jogador
PLAYER_CHARACTER = {
    "nome": "Aelith",  # Nome do personagem
    "classe": "Mago",
    "nivel": 5,
    "habilidades": ["Bola de Fogo", "Mísseis Mágicos", "Escudo Arcano"],
    "equipamentos": ["Cajado arcano", "Livro de feitiços", "Manto de proteção"],
    "historia": "Um mago prodígio que deixou a academia de magia em busca de conhecimento proibido."
}

def narrar_intro():
    """Função para introduzir o cenário inicial."""
    return (
        "Você está em uma sala escura e úmida, iluminada apenas por uma tocha tremulante presa à parede. "
        "O som de gotas caindo ecoa pelo ambiente. Há uma porta pesada de madeira à sua frente, "
        "com runas brilhando fracamente em sua superfície. O que você faz?"
    )

async def main():
    # Inicializar o Kernel
    kernel = Kernel()
    load_dotenv()

    # Configurar Azure OpenAI
    chat_completion = AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    kernel.add_service(chat_completion)

    # Configurar logging
    setup_logging()
    logging.getLogger("semantic_kernel").setLevel(logging.DEBUG)

    print("Bem-vindo ao mundo de Dungeons & Dragons. Digite 'exit' para sair.")

    # Introdução do jogo
    history = [f"Introdução: {narrar_intro()}"]
    print("Narrador >", narrar_intro())

    # Loop de interação
    while True:
        user_input = input("Você > ")

        if user_input.lower() == "exit":
            print("Narrador > Obrigado por jogar. Até a próxima aventura!")
            break

        try:
            # Adicionar a entrada do jogador ao histórico
            history.append(f"Jogador: {user_input}")

            # Construir o prompt com histórico
            context = "\n".join(history[-10:])  # Mantém apenas as últimas 10 interações para controle
            prompt = (
                f"Você é um mestre de RPG narrando um jogo de Dungeons & Dragons. "
                f"O jogador controla o personagem {PLAYER_CHARACTER['nome']}, um {PLAYER_CHARACTER['classe']} de nível {PLAYER_CHARACTER['nivel']}. "
                f"Aqui está a descrição do personagem: {PLAYER_CHARACTER['historia']}.\n\n"
                f"Histórico recente:\n{context}\n\n"
                f"O jogador disse: '{user_input}'. Responda como um mestre de RPG, narrando o que acontece em seguida."
            )

            # Enviar o prompt para o Azure OpenAI
            response = await kernel.invoke_prompt(prompt=prompt)

            # Processar a resposta do mestre de RPG
            narracao = response.value.strip()
            print("Narrador >", narracao)

            # Adicionar a resposta do mestre ao histórico
            history.append(f"Narrador: {narracao}")

        except Exception as e:
            print(f"Erro ao processar a mensagem: {e}")

# Executar o agente
if __name__ == "__main__":
    asyncio.run(main())
