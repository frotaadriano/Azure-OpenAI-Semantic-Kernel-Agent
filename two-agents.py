import os
import asyncio
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

async def main():
    load_dotenv()
    kernel = Kernel()

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

    kernel.add_service(agente1)
    kernel.add_service(agente2)

    # Esta string armazenará todo o histórico da conversa (User, Agente1, Agente2)
    conversation_history = ""

    print(f"\nIniciando interação com 2 agentes. Digite 'exit' para sair.\n")

    while True:
        user_input = input(f"{Fore.GREEN}User > {Style.RESET_ALL}")
        if user_input.lower() == "exit":
            print("Encerrando.")
            break

        # ----------------------------------------------------------
        # 1) Adicionar a fala do usuário ao histórico
        # ----------------------------------------------------------
        conversation_history += f"\n[User]: {user_input}"

        # ----------------------------------------------------------
        # 2) Construir prompt + histórico para o Agente1
        # ----------------------------------------------------------
        prompt_agente1 = f"""
{conversation_history}

[Instruções para o Agente1]
Você é um especialista em design de personagens de RPG e criação de conceitos audiovisuais.
O usuário está lhe fornecendo ideias para um vídeo. Sua tarefa:
- Ler o histórico acima;
- Agradeça ao usuário por sua ideia;
- Crie um prompt para a criação de um vídeo baseado na última ideia do usuário;
- sua arte deve levar em conta que os vídeos só terão 5 segundos de duração.
- Forneça um breve resumo explicando o raciocínios;
- Responda com o prompt final , seu racioncinio e pergunte ao Agente 2 se ele está de acordo.
"""

        response_agente1 = await kernel.invoke_prompt(
            prompt=prompt_agente1,
            service_id="agente1"
        )

        if not response_agente1.value:
            print("Agente1 não retornou resposta.")
            continue

        resposta_texto_agente1 = response_agente1.value[0].items[0].text.strip()

        # Adiciona resposta do Agente1 ao histórico
        conversation_history += f"\n[Agente1]: {resposta_texto_agente1}"

        print(f"{Fore.BLUE}\n=== Resposta do Agente1 ==={Style.RESET_ALL}")
        print(resposta_texto_agente1)

        # ----------------------------------------------------------
        # 3) Construir prompt + histórico para o Agente2
        # ----------------------------------------------------------
        prompt_agente2 = f"""
{conversation_history}

[Instruções para o Agente2]
Você é um especialista na ferramenta Sora (OpenAI), que gera vídeos a partir de prompts. Siga as diretrizes abaixo para estruturar sua resposta:

1. Sempre inicie saudando e elogiando o Agente 1.
2. Avalie o prompt mais recente fornecido pelo Agente 1 com base nas **boas práticas**:
   - **Defina o Enredo Claro**: Certifique-se de que o enredo seja simples e focado em uma única ação ou cena.
   - **Foque nos Detalhes Visuais**: Inclua descrições detalhadas de cores, cenários, personagens e iluminação.
   - **Use Comandos Diretos**: Garanta que o prompt seja claro, conciso e preciso.
   - **Atenção à Coerência**: Verifique a fluidez e consistência narrativa do prompt.
   - **Consistência de Estilo**: Mantenha uma estética visual uniforme.
   - **Visualização e Perspectiva**: Defina distâncias e ângulos (como corpo inteiro ou close).
   - **Feedback Iterativo**: Recomende ajustes e variações para otimizar o resultado.

3. Estruture sua saída no seguinte formato:
- Inicie com uma saudação ao Agente 1.
**Resultado da Análise**
- Forneça observações detalhadas sobre os pontos positivos e áreas de melhoria no prompt enviado.
**Sugestões de Prompts em Etapas**
Forneça um ou mais exemplos de prompts aprimorados em etapas claras. Inclua descrições detalhadas quando necessário.  
- Exemplo:
  - **Etapa 1 Base**: "Uma elfa arqueira em um campo de batalha."
  - **Etapa 2 Melhoria**: "Ela está em uma pose dinâmica, pronta para disparar uma flecha. O cenário tem árvores queimadas ao fundo, com uma atmosfera de fumaça."
  - **Etapa 3 Iluminação**: "O céu é avermelhado, refletindo na armadura de couro da elfa."
**Perguntas de Melhoria**
Inclua 3 perguntas para direcionar o Agente 1 a ajustes adicionais:
- A perspectiva visual está clara (ex.: corpo inteiro, médio alcance, close)?
- O cenário complementa bem a ação principal? Há detalhes que poderiam ser adicionados?
- A iluminação e as cores ajudam a transmitir a emoção ou tema desejado?

Garanta que sua resposta seja clara, objetiva e siga o template descrito. Obrigado por sua colaboração!

"""

        response_agente2 = await kernel.invoke_prompt(
            prompt=prompt_agente2,
            service_id="agente2"
        )

        if not response_agente2.value:
            print("Agente2 não retornou resposta.")
            continue

        resposta_texto_agente2 = response_agente2.value[0].items[0].text.strip()

        # Adiciona resposta do Agente2 ao histórico
        conversation_history += f"\n[Agente2]: {resposta_texto_agente2}"

        print(f"{Fore.MAGENTA}\n=== Resposta do Agente2 ==={Style.RESET_ALL}\n")
        print(f"{Fore.LIGHTMAGENTA_EX}{resposta_texto_agente2}{Style.RESET_ALL}")


if __name__ == "__main__":
    asyncio.run(main())
