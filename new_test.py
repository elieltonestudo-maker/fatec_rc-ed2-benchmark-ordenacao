import os
import random
import statistics
import sys
import time
from datetime import datetime

import matplotlib.pyplot as plt

# Garante que a pasta de saída exista
os.makedirs("outputs", exist_ok=True)

# Aumenta o limite de recursão (necessário para merge/quick recursivos)
sys.setrecursionlimit(100000)

# ============================================================
# IMPLEMENTAÇÕES
# ============================================================

def bubble_sort_ingenuo(arr):
    """Versão sem flag (bubble clássico). Sempre O(n²)."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def bubble_sort_otimizado(arr):
    """Versão com flag: melhor caso O(n)."""
    n = len(arr)
    for i in range(n):
        trocou = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                trocou = True
        if not trocou:
            break

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L, R = arr[:mid], arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def _particionar(arr, low, high):
    """Particionamento in-place com pivô = primeiro elemento."""
    pivo = arr[low]
    i, j = low + 1, high
    while i <= j:
        while i <= j and arr[i] <= pivo:
            i += 1
        while i <= j and arr[j] > pivo:
            j -= 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
    arr[low], arr[j] = arr[j], arr[low]
    return j

def quick_sort_inplace(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        p = _particionar(arr, low, high)
        quick_sort_inplace(arr, low, p - 1)
        quick_sort_inplace(arr, p + 1, high)

def quick_sort_funcional(arr):
    """Versão funcional com pivô no meio (list comprehensions)."""
    if len(arr) <= 1:
        return arr
    pivo = arr[len(arr) // 2]
    esq = [x for x in arr if x < pivo]
    meio = [x for x in arr if x == pivo]
    dir_ = [x for x in arr if x > pivo]
    return quick_sort_funcional(esq) + meio + quick_sort_funcional(dir_)

# ============================================================
# MEDIÇÃO
# ============================================================

def medir(func, lista_base, repeticoes=3):
    """Roda a função N vezes sobre cópias da mesma lista. Retorna (media, desvio)."""
    tempos = []
    for _ in range(repeticoes):
        copia = lista_base.copy()
        t0 = time.perf_counter()
        func(copia)
        tempos.append(time.perf_counter() - t0)
    return statistics.mean(tempos), statistics.stdev(tempos) if len(tempos) > 1 else 0.0

def gerar_lista(n, cenario):
    if cenario == "aleatorio":
        return [random.randint(0, 100000) for _ in range(n)]
    if cenario == "ordenado":
        return list(range(n))
    if cenario == "invertido":
        return list(range(n, 0, -1))

# ============================================================
# CONFIGURAÇÃO DO BENCHMARK
# ============================================================

# Tamanhos pedidos no enunciado
# O(n²) NÃO vão até 100.000 — inviável na prática
tamanhos_quadraticos   = [100, 1000, 10000]
# O(n log n) "seguros" (Merge, Quick funcional, Timsort): todos os tamanhos
tamanhos_eficientes    = [100, 1000, 10000, 100000]
# Quick in-place: só até 10.000, porque no pior caso vira O(n²)
tamanhos_quick_inplace = [100, 1000, 10000]

cenarios = ["aleatorio", "ordenado", "invertido"]
repeticoes = 3

algoritmos_quadraticos = {
    "Bubble (ingênuo)":   bubble_sort_ingenuo,
    "Bubble (otimizado)": bubble_sort_otimizado,
    "Insertion Sort":     insertion_sort,
    "Selection Sort":     selection_sort,
}

algoritmos_eficientes = {
    "Merge Sort":         merge_sort,
    "Quick (funcional)":  lambda l: quick_sort_funcional(l.copy()),
    "Timsort (sorted)":   lambda l: sorted(l),
}

algoritmos_eficientes_lentos = {
    "Quick (in-place)":   quick_sort_inplace,
}

# ============================================================
# EXECUÇÃO
# ============================================================

resultados = {c: {} for c in cenarios}
todos_algoritmos = {**algoritmos_quadraticos, **algoritmos_eficientes, **algoritmos_eficientes_lentos}
for c in cenarios:
    for nome in todos_algoritmos:
        resultados[c][nome] = {}

inicio_total = time.perf_counter()

def log(msg):
    decorrido = time.perf_counter() - inicio_total
    print(f"[{decorrido:6.1f}s] {msg}")

log("Iniciando benchmark...")

# --- Fase 1: algoritmos O(n²) ---
for cenario in cenarios:
    log(f"=== Cenário: {cenario} (O(n²)) ===")
    for nome, func in algoritmos_quadraticos.items():
        for n in tamanhos_quadraticos:
            lista = gerar_lista(n, cenario)
            media, dp = medir(func, lista, repeticoes)
            resultados[cenario][nome][n] = (media, dp)
            log(f"  {nome:<22} n={n:<6} -> {media:.4f}s (±{dp:.4f})")

# --- Fase 2: algoritmos O(n log n) seguros ---
for cenario in cenarios:
    log(f"=== Cenário: {cenario} (O(n log n)) ===")
    for nome, func in algoritmos_eficientes.items():
        for n in tamanhos_eficientes:
            lista = gerar_lista(n, cenario)
            media, dp = medir(func, lista, repeticoes)
            resultados[cenario][nome][n] = (media, dp)
            log(f"  {nome:<22} n={n:<6} -> {media:.4f}s (±{dp:.4f})")

# --- Fase 3: Quick in-place (limitado a n≤10.000) ---
for cenario in cenarios:
    log(f"=== Cenário: {cenario} (Quick in-place, n<=10.000) ===")
    for nome, func in algoritmos_eficientes_lentos.items():
        for n in tamanhos_quick_inplace:
            lista = gerar_lista(n, cenario)
            media, dp = medir(func, lista, repeticoes)
            resultados[cenario][nome][n] = (media, dp)
            log(f"  {nome:<22} n={n:<6} -> {media:.4f}s (±{dp:.4f})")

log("Benchmark concluído. Gerando gráficos...")

# ============================================================
# GRÁFICOS
# ============================================================

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

for idx, cenario in enumerate(cenarios):
    # Linha 0: escala linear
    ax = axes[0][idx]
    for nome, dados in resultados[cenario].items():
        xs = sorted(dados.keys())
        ys = [dados[x][0] for x in xs]
        erros = [dados[x][1] for x in xs]
        ax.errorbar(xs, ys, yerr=erros, marker='o', capsize=3, label=nome)
    ax.set_xlabel("n")
    ax.set_ylabel("Tempo (s)")
    ax.set_title(f"{cenario.capitalize()} — linear")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Linha 1: escala log-log
    ax = axes[1][idx]
    for nome, dados in resultados[cenario].items():
        xs = sorted(dados.keys())
        ys = [dados[x][0] for x in xs]
        ax.plot(xs, ys, marker='o', label=nome)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("n (log)")
    ax.set_ylabel("Tempo (s, log)")
    ax.set_title(f"{cenario.capitalize()} — log-log")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", alpha=0.3)

plt.tight_layout()
plt.savefig("outputs/benchmark_ordenacao.png", dpi=150)
log("Gráfico salvo: outputs/benchmark_ordenacao.png")

# ============================================================
# RELATÓRIO
# ============================================================

with open("outputs/relatorio_ordenacao.txt", "w", encoding="utf-8") as f:
    f.write("=" * 78 + "\n")
    f.write("RELATÓRIO DE BENCHMARK - ALGORITMOS DE ORDENAÇÃO\n")
    f.write(f"Gerado em: {datetime.now():%d/%m/%Y %H:%M:%S}\n")
    f.write(f"Repetições por medição: {repeticoes} (média ± desvio padrão)\n")
    f.write(f"Tempo total de execução: {time.perf_counter() - inicio_total:.1f}s\n")
    f.write("=" * 78 + "\n")
    f.write("NOTAS METODOLÓGICAS:\n")
    f.write("  - O(n2) testados ate n=10.000 (100.000 seria inviavel na pratica).\n")
    f.write("  - Quick in-place limitado a n<=10.000 por causa do pior caso O(n2)\n")
    f.write("    em listas ordenadas/invertidas.\n")
    f.write("=" * 78 + "\n\n")

    for cenario in cenarios:
        f.write(f"\n### CENÁRIO: {cenario.upper()} ###\n")
        f.write("-" * 78 + "\n")
        f.write(f"{'Algoritmo':<22} {'n':>8} {'Média (s)':>14} {'Desvio':>12}\n")
        f.write("-" * 78 + "\n")
        for nome, dados in resultados[cenario].items():
            for n in sorted(dados.keys()):
                media, dp = dados[n]
                f.write(f"{nome:<22} {n:>8} {media:>14.4f} {dp:>12.4f}\n")
        f.write("\n")

    # Síntese final
    f.write("\n" + "=" * 78 + "\n")
    f.write("SÍNTESE — TEMPO EM n MAIS ALTO POR CENÁRIO\n")
    f.write("=" * 78 + "\n")
    for cenario in cenarios:
        f.write(f"\n[{cenario}]\n")
        for nome, dados in resultados[cenario].items():
            n_max = max(dados.keys())
            f.write(f"  {nome:<22} n={n_max:<7} -> {dados[n_max][0]:.4f}s\n")

print("\n✅ Relatório salvo em 'outputs/relatorio_ordenacao.txt'")
print("✅ Gráfico salvo em 'outputs/benchmark_ordenacao.png'")
print(f"⏱️  Tempo total: {time.perf_counter() - inicio_total:.1f}s")