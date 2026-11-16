# SureBetHunter

> 🇧🇷 [Português](#o-que-você-encontrará-neste-repositório) · 🇺🇸 [English](#what-will-you-find-in-this-repository)

## O que você encontrará neste repositório?

Robô caçador de situações de [Sure Bet](https://en.wikipedia.org/wiki/Arbitrage_betting) com funcionamento 24/7, para
jogos simultâneos da NBA em diferentes casas de aposta. Construído utilizando Selenium, entre **maio e junho de 2021**.

Uma *sure bet* (arbitragem) acontece quando as odds de duas casas para os dois lados de um mesmo jogo são altas o
bastante para que, dividindo o valor entre elas, o retorno seja maior que o investido qualquer que seja o resultado.

São dois robôs:

- **Tireless Hunter** — abre a SportingBet (Chrome) e a BetWarrior (Firefox) lado a lado, lista os jogos ao vivo,
  compara as odds de cada partida e calcula a divisão do valor. Ao achar uma brecha, tira capturas de tela, registra
  tudo no arquivo `gaps` e **simula** a aposta: os cliques finais estão comentados, então ele só confere se as odds
  ainda valiam e anota se a aposta "teria dado certo".
- **Accurate Hunter** — versão de um lado só: dada uma primeira aposta feita em outra casa (`stake1` a `odd1`), fica
  observando a SportingBet até a odd oposta garantir o lucro desejado e então faz a aposta.

`Functions/` reúne as funções comuns: cliques e leituras com nova tentativa, conversão de números no formato brasileiro,
capturas de tela e a rotina de aposta.

> Observação do autor: a utilização indevida destes scripts não é de minha responsabilidade. Os mesmos foram criados por
> pura ludicidade e exploração de limites, nenhum provento foi recebido e nenhuma regulação legal foi quebrada.

### Ferramentas

Python 3, Selenium 3 (Chrome e Firefox, com ChromeDriver e GeckoDriver).

### Como usar

```bash
git clone https://github.com/tofolo17/sure-bet-hunter.git
cd sure-bet-hunter
pip install -r requirements.txt
```

O código usa a API do Selenium 3 (`find_element_by_*`, `executable_path`), por isso a versão fica fixada. Antes de rodar:

- informe o caminho do ChromeDriver e do GeckoDriver em `chrome_path` / `firefox_path` (ou `path`, no Accurate Hunter);
- preencha usuário e senha nas chamadas `fill(...)` de login, que vêm vazias no código.

```bash
cd "Tireless Hunter"
mkdir Screenshots
PYTHONPATH=.. python main.py
```

Os arquivos `gap_count`, `gaps` e a pasta `Screenshots/` são lidos e escritos na pasta de onde o script roda.

### Limitações conhecidas

- Os seletores (XPaths) dependem do layout dos sites em 2021 e certamente já não funcionam.
- Os reinícios chamam `nba()` recursivamente, o que faz a pilha crescer em execuções longas.
- No Accurate Hunter, a variável `position` nunca é atualizada, então o robô sempre escolhe a segunda opção do jogo.
- Os registros chamam a BetWarrior de "BetWay".

### Licença

[MIT](LICENSE)

---

## What will you find in this repository?

Bot hunter of [Sure Bet](https://en.wikipedia.org/wiki/Arbitrage_betting) situations with 24/7 operation, for
simultaneous NBA games at different bookmakers. Built with Selenium between **May and June 2021**.

A *sure bet* (arbitrage) happens when two bookmakers' odds for the two sides of the same game are high enough that,
splitting the stake between them, the return beats the investment whatever the result.

There are two bots:

- **Tireless Hunter** — opens SportingBet (Chrome) and BetWarrior (Firefox) side by side, lists the live games,
  compares each match's odds and computes the stake split. When it finds a gap, it takes screenshots, logs everything
  to the `gaps` file and **simulates** the bet: the final clicks are commented out, so it only re-checks whether the
  odds still held and records whether the bet "would have worked".
- **Accurate Hunter** — a one-sided version: given a first bet placed at another bookmaker (`stake1` at `odd1`), it
  watches SportingBet until the opposite odd guarantees the desired profit and then places the bet.

`Functions/` holds the shared helpers: clicks and reads with retries, Brazilian-format number parsing, screenshots and
the betting routine.

> Author's note: the misuse of these scripts is not my responsibility. They were created by pure playfulness and
> exploitation of limits, no earnings were received and no legal regulations were broken.

### Tools

Python 3, Selenium 3 (Chrome and Firefox, with ChromeDriver and GeckoDriver).

### How to use

```bash
git clone https://github.com/tofolo17/sure-bet-hunter.git
cd sure-bet-hunter
pip install -r requirements.txt
```

The code uses the Selenium 3 API (`find_element_by_*`, `executable_path`), so the version is pinned. Before running:

- set the ChromeDriver and GeckoDriver paths in `chrome_path` / `firefox_path` (or `path`, in Accurate Hunter);
- fill in username and password in the login `fill(...)` calls, which ship empty.

```bash
cd "Tireless Hunter"
mkdir Screenshots
PYTHONPATH=.. python main.py
```

The `gap_count` and `gaps` files and the `Screenshots/` folder are read and written in the folder the script runs from.

### Known limitations

- The selectors (XPaths) depend on the sites' 2021 layout and surely no longer work.
- Restarts call `nba()` recursively, so the stack grows on long runs.
- In Accurate Hunter, the `position` variable is never updated, so the bot always picks the game's second option.
- The logs call BetWarrior "BetWay".

### License

[MIT](LICENSE)
