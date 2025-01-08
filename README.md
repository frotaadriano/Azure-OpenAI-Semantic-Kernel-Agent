# Azure OpenAI Semantic Kernel Agent

Este repositório contém um exemplo básico de agente de IA construído utilizando o [Semantic Kernel](https://github.com/microsoft/semantic-kernel) e o serviço [Azure OpenAI](https://learn.microsoft.com/azure/cognitive-services/openai/). Este projeto serve como uma base inicial para explorar e expandir as capacidades de um agente de IA, incluindo a futura implementação de group chat agents.

This repository contains a basic example of an AI agent built using [Semantic Kernel](https://github.com/microsoft/semantic-kernel) and the [Azure OpenAI](https://learn.microsoft.com/azure/cognitive-services/openai/) service. This project serves as an initial foundation to explore and expand the capabilities of an AI agent, including the future implementation of group chat agents.

## Recursos / Features

- **Agente de IA interativo / Interactive AI Agent**: Um agente que utiliza o modelo Azure OpenAI para responder interativamente a entradas do usuário.
  - An agent that uses the Azure OpenAI model to interactively respond to user inputs.
- **Configuração simplificada / Simplified Setup**: Código fácil de configurar para trabalhar com o Azure OpenAI.
  - Easy-to-configure code for working with Azure OpenAI.
- **Base extensível / Extensible Foundation**: Pode ser ampliado para funcionalidades como memória de conversação e interação multiagente.
  - Can be expanded for functionalities like conversational memory and multi-agent interaction.

## Pré-requisitos / Prerequisites

1. **Conta do Azure com acesso ao Azure OpenAI / Azure account with Azure OpenAI access**:
   - Chave de API / API Key.
   - Endpoint do Azure OpenAI / Azure OpenAI Endpoint.
   - Nome do deployment do modelo / Model deployment name (e.g., `text-davinci-003`).

2. **Python 3.8+**

3. **Dependências do Python / Python Dependencies**:
   - Instale o Semantic Kernel / Install Semantic Kernel:
     ```bash
     pip install semantic-kernel
     ```

## Configuração / Setup

1. Clone este repositório / Clone this repository:
   ```bash
   git clone https://github.com/seu-usuario/azure-openai-semantic-kernel-agent.git
   cd azure-openai-semantic-kernel-agent
   ```

2. Crie um arquivo `.env` com suas credenciais do Azure OpenAI / Create a `.env` file with your Azure OpenAI credentials:
   ```env
   AZURE_OPENAI_API_KEY=sua-chave-api-aqui
   AZURE_OPENAI_ENDPOINT=https://seu-endpoint-aqui.openai.azure.com/
   AZURE_DEPLOYMENT_NAME=nome-do-seu-deployment
   ```

3. Execute o agente / Run the agent:
   ```bash
   python ai_agent_semantic_kernel.py
   ```

## Uso / Usage

1. Inicie o programa e interaja com o agente fornecendo entradas no terminal.
   - Start the program and interact with the agent by providing inputs in the terminal.
2. Para encerrar, digite `sair`, `exit` ou `quit`.
   - To exit, type `sair`, `exit`, or `quit`.

## Estrutura do Projeto / Project Structure

```
.
├── ai_agent_semantic_kernel.py  # Código principal do agente / Main agent code
├── .env                        # Configurações sensíveis / Sensitive configurations
├── README.md                    # Documentação do projeto / Project documentation
```

## Próximos Passos / Next Steps

- Adicionar memória conversacional.
  - Add conversational memory.
- Expandir para suportar múltiplos agentes em um ambiente de chat em grupo.
  - Expand to support multiple agents in a group chat environment.
- Integrar a serviços adicionais, como bancos de dados ou APIs externas.
  - Integrate with additional services like databases or external APIs.
- Melhorar a interface com suporte a UI ou integração com plataformas de chat (exemplo: Discord, Slack).
  - Improve the interface with UI support or integration with chat platforms (e.g., Discord, Slack).

## Licença / License

Este projeto é licenciado sob a [MIT License](LICENSE).
  - This project is licensed under the [MIT License](LICENSE).
