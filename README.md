# PDF Generation API

O **PDF Generation API** é um serviço REST desenvolvido em Python que permite a criação dinâmica de documentos PDF a partir de dados fornecidos pelo usuário.

## Funcionalidades

- **Geração Flexível de PDFs**: Crie documentos PDF utilizando modelos personalizáveis e dados dinâmicos fornecidos pelo usuário.
- **Personalização de Conteúdo**: Preencha modelos PDF com dados dinâmicos, permitindo a geração de documentos personalizados e orientados por dados.
- **Opções de Entrega de Conteúdo**: Escolha entre receber o PDF gerado como uma resposta em fluxo ou como uma string codificada em Base64, conforme a preferência do cliente.

## Requisitos

- **Python**: Certifique-se de ter o Python instalado em sua máquina.
- **Poetry**: Utilizado para gerenciamento de dependências.

## Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/inspetor-industrial/pdf-generation-api.git
   ```

2. **Navegue até o diretório do projeto**:

   ```bash
   cd pdf-generation-api
   ```

3. **Instale as dependências usando o Poetry**:

   ```bash
   poetry install
   ```

## Uso

1. **Ative o ambiente virtual gerenciado pelo Poetry**:

   ```bash
   poetry shell
   ```

2. **Inicie o servidor**:

   ```bash
   python main.py
   ```

   O servidor estará disponível em `http://localhost:5000`.

## Configuração de CORS

As configurações de CORS podem ser ajustadas no arquivo `cors.json` para permitir ou restringir origens específicas.

## Licença

Este projeto está licenciado sob a licença MIT.
