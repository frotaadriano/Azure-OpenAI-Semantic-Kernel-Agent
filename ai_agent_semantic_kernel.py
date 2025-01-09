import os
from dotenv import load_dotenv
import asyncio
import logging

from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from pprint import pprint  # Importar para saída mais legível


# Supondo que `response` é o objeto retornado
# Supondo que `response` seja o objeto retornado
def print_response_details(response):
    print("\n--- Detalhes do Objeto Retornado ---")
    pprint(vars(response))  # Inspeciona os atributos principais do objeto

    print("\n--- Resposta Gerada pela IA ---")
    try:
        # Acessar o conteúdo dentro de `inner_content` (ChatMessageContent)
        if hasattr(response, "inner_content") and response.inner_content:
            inner_content = response.inner_content

            # Inspecionar atributos do inner_content
            pprint(vars(inner_content))

            # Acessar as escolhas e o conteúdo da mensagem
            chat_completion = inner_content
            if hasattr(chat_completion, "choices") and chat_completion.choices:
                choice = chat_completion.choices[0]  # Pega a primeira escolha
                message = choice.message  # Acessa a mensagem gerada
                print(f"Mensagem do Assistente: {message.content}")
                print(f"Razão para Terminar: {choice.finish_reason}")

                # Informações sobre tokens
                if hasattr(chat_completion, "usage"):
                    usage = chat_completion.usage
                    print("\n--- Informações sobre o Uso de Tokens ---")
                    print(f"Tokens do Prompt: {usage.prompt_tokens}")
                    print(f"Tokens da Resposta: {usage.completion_tokens}")
                    print(f"Tokens Totais: {usage.total_tokens}")

                # Detalhes de filtragem de conteúdo
                print("\n--- Detalhes da Filtragem de Conteúdo ---")
                pprint(choice.content_filter_results)
            else:
                print("Não foi possível acessar as escolhas da IA.")

        else:
            print("Nenhum `inner_content` encontrado no objeto retornado.")

    except AttributeError as e:
        print(f"Erro ao acessar atributo: {e}")


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
            #print(f"Assistant > {response.value}")
            if response.value[0]:
                print("response.value[0] é True")
                print("response.value[0]: ", response.value[0])
                print("response: ", response.value)
                print("\n\n")

                # Imprimindo partes do objeto
                print("--- Detalhes da Resposta ---")

                # Acessando o primeiro elemento de response.value
                response_content = response.value[0]

                #--------------------------------------------#
                # Texto gerado pela IA
                #--------------------------------------------#
                if hasattr(response_content, "items") and response_content.items:
                    print("Texto Gerado pela IA:", response_content.items[0].text)


                # Modelo usado
                if hasattr(response_content, "ai_model_id"):
                    print("Modelo Usado:", response_content.ai_model_id)

                # Informações sobre Tokens
                if hasattr(response_content, "metadata") and "usage" in response_content.metadata:
                    usage = response_content.metadata["usage"]
                    print("\n--- Uso de Tokens ---")
                    print(f"usage : {usage}")
                    # print(f"Tokens do Prompt: {usage.prompt_tokens}")
                    # print(f"Tokens da Resposta: {usage.completion_tokens}")
                    # print(f"Tokens Totais: {usage.total_tokens}")

                # Informações do Filtro de Conteúdo
                if hasattr(response_content, "inner_content"):
                    if hasattr(response_content.inner_content, "choices") and response_content.inner_content.choices:
                        choice = response_content.inner_content.choices[0]
                        print("\n--- Filtro de Conteúdo ---")
                        print("Resultados de Filtragem:", choice.content_filter_results)

                        
            #print_response_details(response)
        except Exception as e:
            print(f"Erro ao processar a mensagem: {e}")

# Executar o agente
if __name__ == "__main__":
    asyncio.run(main())
