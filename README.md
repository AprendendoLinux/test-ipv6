# Detecção de IPv6

Olá!

Eu sou Henrique Fagundes e criei uma aplicação para detectar se você tem IPv6 na sua rede. Esta ferramenta verifica a presença de IPv6 e pode ser útil para entender melhor a configuração da sua rede.

## Como Funciona

A aplicação realiza uma verificação simples para identificar se o IPv6 está disponível na sua rede e fornece um relatório sobre a detecção.

## Instruções de Uso

1. **Habilite o IPv6 no Docker**: Para que a aplicação funcione corretamente, você precisa habilitar o IPv6 no Docker. Siga as [instruções oficiais](https://docs.docker.com/engine/daemon/ipv6/) para configurar isso.
2. **Crie um Arquivo `docker-compose.yml`**: Crie um arquivo `docker-compose.yml` com o seguinte conteúdo:

    ```yaml
    networks:
      network-ipv6:
        driver: bridge
        enable_ipv6: true

    services:
      test-ipv6:
        depends_on:
          - proxy
        container_name: test-ipv6
        hostname: test-ipv6
        networks:
          - network-ipv6
        image: aprendendolinux/test-ipv6
        restart: always
        ports:
          - '5000:5000'
    ```

3. **Suba o Contêiner**: Execute o comando abaixo para iniciar o contêiner:

    ```bash
    docker-compose up -d
    ```

4. **Acesse a Aplicação**: Depois que o contêiner estiver em execução, acesse a aplicação de fora usando o seguinte endereço:

    ```
    http://endereco-do-servidor.dominio:5000
    ```

5. **Verifique a Detecção de IPv6**: A aplicação irá mostrar se o IPv6 está disponível na sua rede.

Se você tiver alguma dúvida ou precisar de suporte, sinta-se à vontade para entrar em contato!

Obrigado por usar a minha aplicação!

Henrique Fagundes
