import os
from dotenv import load_dotenv
import asyncio
import logging

from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


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

    print("Iniciando o agente de chat. Digite 'exit' para sair.")

    # Loop de interação
    while True:
        user_input = input("User > ")

        if user_input.lower() == "exit":
            print("Encerrando o agente.")
            break

        try:
            # Usar o método invoke_prompt para enviar o input do usuário ao Azure OpenAI
            response = await kernel.invoke_prompt(
                prompt=user_input,
                plugin_name=None,  # Não há necessidade de um plugin
                function_name=None  # Não há função específica
            )
            print(f"Assistant > {response.value}")
            print
        except Exception as e:
            print(f"Erro ao processar a mensagem: {e}")

# Executar o agente
if __name__ == "__main__":
    asyncio.run(main())
