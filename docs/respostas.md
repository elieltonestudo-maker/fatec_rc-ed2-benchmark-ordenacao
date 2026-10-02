# Analise Critica - Benchmark de Ordenacao

## 1. Quais algoritmos se comportam melhor para listas pequenas?

Para listas pequenas (n = 100), todos os algoritmos apresentaram tempos
praticamente indistinguiveis - entre 0,0000s e 0,0007s. A diferenca entre o
mais rapido (Timsort: ~0,0000s) e o mais lento (Bubble otimizado: ~0,0005s)
ficou dentro da margem de ruido do sistema operacional, tornando qualquer
escolha aceitavel nesse tamanho.

Isso confirma o que o material da disciplina afirma: "o algoritmo bubble sort
tem bom desempenho em listas relativamente pequenas". Para n=100, ate
algoritmos teoricamente ruins (O(n2)) sao viaveis porque o numero absoluto de
operacoes e pequeno (~10.000 comparacoes).

**Conclusao pratica:** para listas pequenas, simplicidade de implementacao
importa mais do que eficiencia assintotica.

---

## 2. Quais escalam melhor para listas grandes?

Para listas grandes (n = 100.000), a diferenca e dramatica:

| Algoritmo | Tempo em n=100.000 (aleatorio) |
|---|---|
| Timsort (sorted) | **0,0147s** |
| Quick (funcional) | 0,1950s |
| Merge Sort | 0,2853s |
| Bubble / Insertion / Selection | inviaveis (nao testados) |
| Quick (in-place) | 0,0148s em n=10.000, mas 171x mais lento em ordenado/invertido |

Os algoritmos O(n2) nao foram testados com n=100.000 porque, conforme visto
em aula, "o bubble sort nao deve ser usado para ordenar listas grandes".

**Destaque - QuickSort in-place:** no cenario aleatorio ele e rapido, mas nos
cenarios ordenado e invertido ele cai para 2,5340s em n=10.000 - um aumento
de 171 vezes, exatamente como o material da disciplina preve para o pior caso.

**Conclusao pratica:** para listas grandes, use Timsort (sorted/list.sort).

---

## 3. Os resultados experimentais confirmam a complexidade teorica?

**Sim, confirmam com precisao.** Evidencias:

| Algoritmo | Complexidade teorica | Evidencia empirica | Confirma? |
|---|---|---|---|
| Bubble (ingenuo) | O(n2) sempre | 4,97s -> 2,92s -> 6,22s em n=10.000 | Sim |
| Bubble (otimizado) | O(n2) / O(n) melhor | 5,09s -> 0,0006s - 8.483x mais rapido | Sim |
| Insertion | O(n2) / O(n) melhor | 2,17s -> 0,0010s - 2.170x mais rapido | Sim |
| Selection | O(n2) SEMPRE | 2,17s / 2,06s / 2,13s - praticamente iguais | Sim |
| Merge | O(n log n) | 0,29s em n=100.000 | Sim |
| Quick (funcional) | O(n log n) | 0,20s em n=100.000 | Sim |
| Quick (in-place) | O(n2) pior caso | 0,0148s -> 2,53s (ordenado) - 171x mais lento | Sim |
| Timsort | O(n log n) / O(n) melhor | 0,0147s -> 0,0008s (ordenado) - 18x mais rapido | Sim |

**Evidencias especificas:**

- Selection Sort teve tempos quase identicos nos 3 cenarios, confirmando
  que o algoritmo e O(n2) mesmo no melhor caso.
- Bubble otimizado teve queda de 8.483x no cenario ordenado, confirmando O(n)
  no melhor caso.
- Quick in-place explodiu no cenario ordenado: 171x mais lento, confirmando
  o pior caso O(n2).
- Timsort foi o mais rapido em todos os cenarios.

**Conclusao:** os dados confirmam empiricamente a teoria de complexidade.

---

## Bonus - Analise das referencias complementares

### sorted() vs list.sort() (Luciano Ramalho)

list.sort() ordena in-place e retorna None; sorted() cria uma nova lista.
No benchmark usamos sorted() para preservar a lista original entre as
repeticoes. Em producao, list.sort() economiza memoria.

### Timsort (Wikipedia)

Algoritmo hibrido que combina Insertion Sort (blocos pequenos) e Merge Sort
(mesclagem). Explora "runs naturais" - sequencias ja ordenadas. Por isso e
consistentemente o mais rapido: no cenario ordenado (n=100.000) levou apenas
0,0008s, detectando a lista inteira como um unico run.