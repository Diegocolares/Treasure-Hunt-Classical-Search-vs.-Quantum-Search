# Treasure Hunt: Busca Clássica vs Busca Quântica

Este projeto apresenta uma visualização comparativa entre busca clássica e busca quântica inspirada no algoritmo de Grover. A proposta é traduzir um conceito frequentemente abstrato em uma representação visual clara, permitindo compreender, de forma intuitiva, a origem da vantagem quântica.

O problema é modelado como uma busca em um espaço discreto: um tabuleiro onde um único elemento contém o "tesouro". O objetivo é identificar sua posição.

---

## Motivação

A principal dificuldade no ensino de computação quântica não está apenas na matemática envolvida, mas na construção de intuição sobre como os algoritmos realmente operam.

Enquanto algoritmos clássicos seguem uma lógica sequencial de verificação, algoritmos quânticos exploram propriedades como superposição e interferência para modificar a distribuição de probabilidades antes da medição.

Este projeto foi desenvolvido para evidenciar essa diferença de forma direta.

---

## Descrição da abordagem

A animação apresenta dois painéis sincronizados:

### Busca clássica

No modelo clássico, o algoritmo percorre o espaço de busca de forma sequencial. A cada passo, um elemento é verificado. Caso não seja o alvo, ele é descartado, e o processo continua até a localização do tesouro.

Esse comportamento representa a complexidade típica de busca não estruturada:

$$\mathcal{O}(N)$$

---

### Busca quântica

No caso quântico, a dinâmica é global. Em vez de verificar elementos individualmente, o sistema evolui como um todo. A distribuição de probabilidades é iterativamente ajustada, aumentando a probabilidade associada ao estado correto.

Ao final do processo, uma medição revela o resultado com alta probabilidade.

Esse comportamento é característico do algoritmo de Grover, cuja complexidade é:

$$\mathcal{O}(\sqrt{N})$$

---

## Resultado demonstrado

Na configuração utilizada:

* o algoritmo quântico identifica o tesouro em aproximadamente 6 passos
* o algoritmo clássico requer 36 passos

Essa diferença não é apenas quantitativa, mas estrutural. O método quântico não reduz o número de verificações por otimização local, mas altera a forma como o espaço de busca é explorado.

---

## Elementos da visualização

A animação foi construída para destacar três aspectos principais:

* evolução da busca clássica por inspeção direta
* evolução da busca quântica por amplificação de probabilidade
* comparação simultânea entre probabilidade de sucesso e esforço computacional

A busca clássica é representada por um cursor que percorre o espaço. Já a busca quântica é representada por uma evolução distribuída, evidenciando o caráter global do algoritmo.

---

## Interpretação

A visualização permite compreender que a vantagem quântica não decorre de "adivinhar" o resultado, mas de manipular a estrutura probabilística do sistema.

O algoritmo quântico não testa explicitamente cada possibilidade. Em vez disso, ele reorganiza as amplitudes de forma que, no momento da medição, o estado correto seja obtido com alta probabilidade.

---

## Execução

### Dependências

```bash
pip install -r requirements.txt
```

### Execução do script

```bash
python src/script.py
```

Ao final, será gerado um arquivo GIF contendo a animação.

---

## Visualização no repositório

Para exibir a animação no README:

```markdown
![Animação](output/treasure_hunt_animation.gif)
```

---

## Considerações finais

Embora a animação não represente todos os detalhes formais do algoritmo de Grover, ela preserva sua característica essencial: a capacidade de amplificar a probabilidade do estado alvo por meio de evolução global do sistema.

Como ferramenta didática, a visualização oferece um meio direto de compreender a diferença entre busca sequencial e amplificação quântica, destacando de forma clara a redução de complexidade de $$\mathcal{O}(N)$$ para $$\mathcal{O}(\sqrt{N})$$.

---

## Licença

Este projeto é disponibilizado sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## Autor

Desenvolvido por [Diegocolares](https://github.com/Diegocolares)