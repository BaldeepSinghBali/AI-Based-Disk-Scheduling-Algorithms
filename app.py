import numpy as np
import matplotlib.pyplot as plt
import random

def total_head_movement(sequence, head):
    if not sequence:
        return 0
    distance = abs(head - sequence[0])
    for i in range(1, len(sequence)):
        distance += abs(sequence[i] - sequence[i - 1])
    return distance

def shuffle(arr):
    a = arr[:]
    random.shuffle(a)
    return a

def crossover(p1, p2):
    if len(p1) <= 1:
        return p1[:]
    point = random.randint(1, len(p1) - 1)
    child = p1[:point]
    for i in p2:
        if i not in child:
            child.append(i)
    return child

def mutate(ind):
    if len(ind) > 1:
        i, j = random.sample(range(len(ind)), 2)
        ind[i], ind[j] = ind[j], ind[i]

def sstf(requests, head):
    seq = []
    pending = requests[:]
    current = head
    while pending:
        closest = min(pending, key=lambda x: abs(x - current))
        seq.append(closest)
        pending.remove(closest)
        current = closest
    return seq

def scan(requests, head):
    sorted_req = sorted(requests)
    left = [r for r in sorted_req if r < head][::-1]
    right = [r for r in sorted_req if r >= head]
    return right + left

def run_ga(requests, head, pop_size=10, generations=50):
    if len(requests) <= 1:
        return requests[:]

    population = [shuffle(requests) for _ in range(pop_size)]

    for _ in range(generations):
        population.sort(key=lambda x: total_head_movement(x, head))
        next_gen = population[:2]

        while len(next_gen) < pop_size:
            p1, p2 = population[0], population[1]
            child = crossover(p1, p2)
            if random.random() < 0.2:
                mutate(child)
            next_gen.append(child)

        population = next_gen

    return min(population, key=lambda x: total_head_movement(x, head))

def plot_sequences(head, ga_seq, fcfs_seq, sstf_seq, scan_seq):
    x = list(range(len(fcfs_seq) + 1))
    plt.figure(figsize=(10, 6))

    plt.plot(x, [head] + ga_seq, label='Genetic Algorithm', marker='o', color='green')
    plt.plot(x, [head] + fcfs_seq, label='FCFS', marker='o', color='red')
    plt.plot(x, [head] + sstf_seq, label='SSTF', marker='o', color='blue')
    plt.plot(x, [head] + scan_seq, label='SCAN', marker='o', color='orange')

    plt.title("Disk Scheduling Comparison")
    plt.xlabel("Request Order")
    plt.ylabel("Disk Cylinder")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

requests_input = input("Enter disk requests separated by spaces: ")
requests = list(map(int, requests_input.strip().split())) if requests_input.strip() else []
head_start = int(input("Enter initial head position: "))

ga_seq = run_ga(requests, head_start)
fcfs_seq = requests[:]
sstf_seq = sstf(requests, head_start) if requests else []
scan_seq = scan(requests, head_start) if requests else []

ga_movement = total_head_movement(ga_seq, head_start)
fcfs_movement = total_head_movement(fcfs_seq, head_start)
sstf_movement = total_head_movement(sstf_seq, head_start)
scan_movement = total_head_movement(scan_seq, head_start)

print("\nBest GA Sequence:", ' -> '.join(map(str, ga_seq)))
print("Total Head Movement (GA):", ga_movement)

print("\nFCFS Sequence:", ' -> '.join(map(str, fcfs_seq)))
print("Total Head Movement (FCFS):", fcfs_movement)

print("\nSSTF Sequence:", ' -> '.join(map(str, sstf_seq)))
print("Total Head Movement (SSTF):", sstf_movement)

print("\nSCAN Sequence:", ' -> '.join(map(str, scan_seq)))
print("Total Head Movement (SCAN):", scan_movement)

movements = {
    "Genetic Algorithm": ga_movement,
    "FCFS": fcfs_movement,
    "SSTF": sstf_movement,
    "SCAN": scan_movement
}

best_algo = min(movements, key=movements.get)
print(f"\nRecommended Algorithm: {best_algo} (Least Total Head Movement)")

if requests:
    plot_sequences(head_start, ga_seq, fcfs_seq, sstf_seq, scan_seq)
