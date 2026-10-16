import multiprocessing as mp
import time
import matplotlib.pyplot as plt
import os

BATAS = 100_000
JUMLAH_WORKER = [1, 2, 4, 8]


def hitung_prima_rentang(data):
    awal, akhir = data
    jumlah = 0

    for angka in range(max(2, awal), akhir + 1):
        prima = True

        for pembagi in range(2, int(angka ** 0.5) + 1):
            if angka % pembagi == 0:
                prima = False
                break

        if prima:
            jumlah += 1

    return jumlah


def buat_rentang(batas, jumlah_worker):
    ukuran = batas // jumlah_worker
    rentang = []

    for i in range(jumlah_worker):
        awal = i * ukuran + 1
        akhir = (
            (i + 1) * ukuran
            if i < jumlah_worker - 1
            else batas
        )
        rentang.append((awal, akhir))

    return rentang

if __name__ == "__main__":
    hasil_waktu = {}
    hasil_prima = {}

    for worker in [1, 2, 4, 8]:
        tugas = buat_rentang(BATAS, worker)

        print(f"Sedang menguji {worker} worker...", flush=True)

        mulai = time.perf_counter()

        with mp.get_context("spawn").Pool(
            processes=worker
        ) as pool:
            hasil = pool.map(hitung_prima_rentang, tugas)

        durasi = time.perf_counter() - mulai

        hasil_waktu[worker] = durasi
        hasil_prima[worker] = sum(hasil)

        print(f"Jumlah worker: {worker}")
        print(f"Jumlah bilangan prima: {sum(hasil)}")
        print(f"Waktu eksekusi: {durasi:.4f} detik")
        print("-" * 35)

    waktu_sekuensial = hasil_waktu[1]

    speedup = {
        worker: waktu_sekuensial / hasil_waktu[worker]
        for worker in [1, 2, 4, 8]
    }

    print("\nHASIL SPEEDUP")
    for worker, nilai in speedup.items():
        print(f"{worker} worker: {nilai:.3f}x")

    plt.figure(figsize=(8, 5))
    plt.plot(
        list(speedup.keys()),
        list(speedup.values()),
        marker="o",
        label="Speedup aktual"
    )
    plt.plot(
        [1, 2, 4, 8],
        [1, 2, 4, 8],
        linestyle="--",
        label="Speedup ideal"
    )
    plt.xlabel("Jumlah Worker")
    plt.ylabel("Speedup")
    plt.title("Analisis Speedup terhadap Jumlah Worker")
    plt.xticks([1, 2, 4, 8])
    plt.grid(True)
    plt.legend()
    plt.show()