
import multiprocessing as mp
import random
import time

JUMLAH_PROSES = 4
JUMLAH_ANGKA = 1_000_000
SEED = 12345


# Fungsi worker untuk metode Queue
def hitung_queue(args):
    seed, jumlah = args
    rng = random.Random(seed)

    subtotal = sum(rng.random() for _ in range(jumlah))

    return subtotal


def program_queue():
    ctx = mp.get_context("spawn")
    tugas = [(SEED + i, JUMLAH_ANGKA)
             for i in range(JUMLAH_PROSES)]

    with ctx.Pool(processes=JUMLAH_PROSES) as pool:
        subtotal = pool.map(hitung_queue, tugas)

    total = sum(subtotal)
    return total


# Fungsi worker untuk metode Shared Memory
def hitung_shared(args):
    seed, jumlah, nilai_bersama, lock = args
    rng = random.Random(seed)

    subtotal = sum(rng.random() for _ in range(jumlah))

    # Lock digunakan agar penambahan nilai berlangsung aman
    with lock:
        nilai_bersama.value += subtotal


def program_shared():
    ctx = mp.get_context("spawn")
    nilai_bersama = ctx.Value("d", 0.0)
    lock = ctx.Lock()

    tugas = [
        (SEED + i, JUMLAH_ANGKA, nilai_bersama, lock)
        for i in range(JUMLAH_PROSES)
    ]

    proses = [
        ctx.Process(target=hitung_shared, args=(arg,))
        for arg in tugas
    ]

    for p in proses:
        p.start()

    for p in proses:
        p.join()

    if any(p.exitcode != 0 for p in proses):
        raise RuntimeError("Salah satu proses gagal dijalankan.")

    return nilai_bersama.value

if __name__ == "__main__":
    # Pengukuran waktu Queue
    mulai = time.perf_counter()
    total_queue = program_queue()
    waktu_queue = time.perf_counter() - mulai

    # Pengukuran waktu Shared Memory
    mulai = time.perf_counter()
    total_shared = program_shared()
    waktu_shared = time.perf_counter() - mulai

    # Menampilkan hasil pengukuran
    print("=== HASIL PENGUJIAN ===")
    print(f"Jumlah proses       : {JUMLAH_PROSES}")
    print(f"Angka per proses    : {JUMLAH_ANGKA:,}")
    print(f"Total angka         : {JUMLAH_PROSES * JUMLAH_ANGKA:,}")
    print(f"Total Queue         : {total_queue:.6f}")
    print(f"Waktu Queue         : {waktu_queue:.4f} detik")
    print(f"Total Shared Memory : {total_shared:.6f}")
    print(f"Waktu Shared Memory : {waktu_shared:.4f} detik")
    print(f"Selisih total       : {abs(total_queue - total_shared):.12f}")

    if waktu_queue < waktu_shared:
        print("Metode lebih cepat  : Queue (Message Passing)")
    elif waktu_shared < waktu_queue:
        print("Metode lebih cepat  : Shared Memory")
    else:
        print("Waktu kedua metode hampir sama.")