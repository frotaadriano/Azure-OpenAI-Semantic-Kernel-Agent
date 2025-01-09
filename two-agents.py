import os
from dotenv import load_dotenv
import asyncio
# import logging  # não vamos mais precisar do logging para esse exemplo

from semantic_kernel import Kernel
# from semantic_kernel.utils.logging import setup_logging  # não usaremos mais
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from pprint import pprint

# 1) Importe e inicie o colorama
import colorama
from colorama import Fore, Style

# Inicia o colorama (no Windows, habilita ANSI escape sequences)
colorama.init(autoreset=True)


def print_response_details(response):
    # (seu método de debug permanece inalterado)
    ...
    

async def main():
    kernel = Kernel()
    load_dotenv()

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

    agente1.service_id = "agente1"
    agente2.service_id = "agente2"

    # Adiciona ao kernel sem passar service_id como parâmetro
    kernel.add_service(agente1)
    kernel.add_service(agente2)

    # Se não quiser poluir com debug:
    # setup_logging()
    # logging.getLogger("semantic_kernel").setLevel(logging.DEBUG)

    print(f"\nIniciando interação com 2 agentes. Digite 'exit' para sair.\n")

    while True:
        # 2) Peça input do usuário com cor
        print(f"{Fore.GREEN}================================================ {Style.RESET_ALL}")
        user_input = input(f"{Fore.GREEN}User > {Style.RESET_ALL}")
        print(f"{Fore.GREEN}================================================ {Style.RESET_ALL}")

        if user_input.lower() == "exit":
            print("Encerrando o agente.")
            break

        try:
            # ============ Agente 1 ============
            # Monte um prompt que instrui o Agente1 a agir como especialista em design de personagens de RPG.
            # Ele deve pegar a ideia do usuário e devolver apenas um prompt para geração de vídeo, sem explicações.

            prompt_agente1 = f"""
                Você é um especialista em design de personagens de RPG e em criação de conceitos audiovisuais.
                O usuário lhe forneceu esta ideia para um vídeo: "{user_input}"

                Sua tarefa:
                - Crie APENAS um prompt para a criação de um vídeo baseado nessa ideia.
                - Não forneça explicações ou raciocínios.  
                - Responda exclusivamente com o prompt final em uma única resposta.

                Responda agora:
                """
            # ============ Agente1 ============
            response_agente1 = await kernel.invoke_prompt(
                prompt=prompt_agente1,
                service_id="agente1"
            )

            if not response_agente1.value:
                print("Agente1 não retornou resposta.")
                continue

            resposta_texto_agente1 = response_agente1.value[0].items[0].text

 

            # 3) Imprimir a resposta do Agente1 em azul
            print(f"{Fore.BLUE}\n=============================================={Style.RESET_ALL}")
            print(f"\n{Fore.BLUE}--- Resposta do Agente1 (Especialista em RPG) ---{Style.RESET_ALL}")
            print(resposta_texto_agente1)
            print(f"{Fore.BLUE}=============================================={Style.RESET_ALL}")
           
            # ============ Agente2 ============
            # ============ Agente 2 ============
            # Monte um prompt que instrui o Agente2 a agir como especialista na ferramenta Sora.
            # Ele deve:
            #  - Sempre começar elogiando ou tratando o Agente1 pelo nome.
            #  - Rever e ajustar o prompt recebido (resposta do Agente1) para adequá-lo à ferramenta Sora.

            prompt_agente2 = f"""
            Você é um especialista na ferramenta Sora (OpenAI), que gera vídeos a partir de prompts.
            A seguir está um prompt criado pelo Agente1 (especialista em RPG). 
            Sua tarefa:
            - Sempre inicie saudando ou elogiando o Agente1.
            - Ajuste e refine o prompt para se adequar melhor à ferramenta Sora.
            - Garanta que o prompt final esteja bem estruturado, claro e detalhado.

            Prompt criado pelo Agente1: 
            {resposta_texto_agente1}

            Responda agora:
            """

            response_agente2 = await kernel.invoke_prompt(
                prompt=prompt_agente2,
                service_id="agente2"
            )

            if not response_agente2.value:
                print("Agente2 não retornou resposta.")
                continue

            resposta_texto_agente2 = response_agente2.value[0].items[0].text

            # 4) Imprimir a resposta do Agente2 em magenta
            print(f"{Fore.MAGENTA}\n================================================================={Style.RESET_ALL}")
            print(f"\n{Fore.MAGENTA}--- Resposta do Agente2 (Especialista em Sora) ---{Style.RESET_ALL}")
            print(resposta_texto_agente2)
            print(f"{Fore.MAGENTA}\n================================================================={Style.RESET_ALL}")


        except Exception as e:
            print(f"Erro ao processar a mensagem: {e}")


if __name__ == "__main__":
    asyncio.run(main())
