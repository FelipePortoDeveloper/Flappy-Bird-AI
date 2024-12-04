# NEAT: Aprendendo a Jogar Flappy Bird 

Este projeto utiliza o algoritmo NEAT [(NeuroEvolution of Augmenting Topologies)](https://neat-python.readthedocs.io/en/latest/neat_overview.html) para treinar uma Inteligência Artificial a jogar um jogo simples.
O principal objetivo é explorar o funcionamento do NEAT e aprender como aplicá-lo em Python, enquanto também oferece a possibilidade de o usuário jogar o jogo manualmente, caso deseje.

## 🔍 Como funciona o NEAT

NEAT é um algoritmo genético para gerar redes neurais artificiais que evoluem ao longo de gerações:

1. **População inicial:** Criação de redes neurais simples.
2. **Avaliação:** As redes são testadas dentro do ambiente do jogo e um fitness (A pontuação) é atribuído.
3. **Seleção natural:** Redes com o maior fitness tem chance maior de passar seus genes para a proxima geração.
4. **Mutação:** As conexões e neuronios sofrem modificações e até novos são criados.
5. **Repetição:** O processo se repete até que o agente alcance o desempenho esperado (Nesse caso, durar enquanto o programa estiver rodando).

Para jogos simples é comum algum agente ja ser gerado com uma rede que sabe como jogar perfeitamente, por esse motivo, adicionei uma dificuldade a mais para aumentar o desafio do agente (O que se provou não suficiente, como será mostrado na demonstracão).

## 🚀 Como executar o projeto

1. Clone o repositório:
```bash
git clone https://github.com/FelipePortoDeveloper/Flappy-Bird-AI.git
cd Flappy-Bird-AI
```
2. Execute o script pricipal:
```bash
python FlappyBird.py
```
3. Acompanhe a evolução do agente. Durante a execução, gráficos ou logs podem ser exibidos mostrando o progresso do treinamento.

## 📂 Estrutura do código

```bash
Flappy-Bird-AI/
│
├── config.txt               # Configuração do algoritmo NEAT
├── FlappyBird.py            # Script principal para rodar o treinamento
├── images/                   # Utilitários e funções auxiliares
└── README.md                # Documentação do projeto
```


## 🎮 Demonstração

No modo fácil os agentes aprendem as regras do jogo em apenas duas gerações | No modo difícil os agentes aprenderam a jogar em apenas quatro, mesmo que o modo seja mais difícil
-- | --
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![Modo Fácil](https://github.com/user-attachments/assets/7f61d24a-c4d3-4762-9b88-645f5180f4a6) | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![Modo Difícil](https://github.com/user-attachments/assets/0c265b3c-cbe4-4e61-ab3f-a351a4e077d9) |

## 📬 Contato

Se tiver dúvidas ou sugestões:


Autor: Felipe Porto


E-mail: felipeportodeveloper5@gmail.com


GitHub: [FelipePortoDeveloper](https://github.com/FelipePortoDeveloper)
