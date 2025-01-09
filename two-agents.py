import os
from dotenv import load_dotenv
import asyncio
import logging

from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from pprint import pprint  # Importar para saída mais legível

def print_response_details(response):
    # (seu método de debug permanece inalterado)
    ...

async def main():
    kernel = Kernel()
    load_dotenv()

    # 1) Crie cada "AzureChatCompletion"
    agente1 = AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    agente2 = AzureChatCompletion(
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    # 2) Defina o "service_id" dentro do objeto antes de adicioná-lo
    agente1.service_id = "agente1"
    agente2.service_id = "agente2"

    # 3) Agora, adicione ao Kernel sem passar service_id como param
    kernel.add_service(agente1)  # Ele já tem service_id = "agente1"
    kernel.add_service(agente2)  # Ele já tem service_id = "agente2"

    # setup_logging()
    # logging.getLogger("semantic_kernel").setLevel(logging.DEBUG)

    print("Iniciando interação com 2 agentes. Digite 'exit' para sair.")

    while True:
        user_input = input("User > ")
        if user_input.lower() == "exit":
            print("Encerrando o agente.")
            break

        try:
            # ============ Agente1 ============
            response_agente1 = await kernel.invoke_prompt(
                prompt=user_input,
                service_id="agente1"  # Agora sim, passamos o ID do agente
            )

            if not response_agente1.value:
                print("Agente1 não retornou resposta.")
                continue

            resposta_texto_agente1 = response_agente1.value[0].items[0].text

            print("\n--- Resposta do Agente1 ---")
            print(resposta_texto_agente1)

            # ============ Agente2 ============
            # Montar prompt para revisão
            prompt_revisao = (
                "Você é um revisor especializado. "
                "Revise, corrija e melhore o texto a seguir:\n\n"
                f"{resposta_texto_agente1}"
            )

            response_agente2 = await kernel.invoke_prompt(
                prompt=prompt_revisao,
                service_id="agente2"
            )

            if not response_agente2.value:
                print("Agente2 não retornou resposta.")
                continue

            resposta_texto_agente2 = response_agente2.value[0].items[0].text

            print("\n--- Resposta do Agente2 (Revisão) ---")
            print(resposta_texto_agente2)

        except Exception as e:
            print(f"Erro ao processar a mensagem: {e}")

if __name__ == "__main__":
    asyncio.run(main())
