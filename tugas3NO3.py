
import multiprocessing as mp
import time


JUMLAH_DATA = 10


def producer(queue):
    """Menghasilkan data dan mengirimkannya ke Queue."""
    for i in range(1, JUMLAH_DATA + 1):
        data = f"Data-{i}"
        queue.put(data)
        print(f"[Producer] Mengirim: {data}", flush=True)
        time.sleep(0.2)

    # Penanda bahwa producer telah selesai
    queue.put(None)
    print("[Producer] Selesai menghasilkan data.", flush=True)


def consumer(queue):
    """Menerima dan memproses data dari Queue."""
    while True:
        data = queue.get()

        if data is None:
            break

        print(f"[Consumer] Memproses: {data}", flush=True)
        time.sleep(0.3)

    print("[Consumer] Selesai memproses data.", flush=True)


if __name__ == "__main__":
    ctx = mp.get_context("spawn")
    queue = ctx.Queue()

    p = ctx.Process(target=producer, args=(queue,))
    c = ctx.Process(target=consumer, args=(queue,))

    mulai = time.perf_counter()

    p.start()
    c.start()

    p.join()
    c.join()

    waktu = time.perf_counter() - mulai

    queue.close()
    queue.join_thread()

    print("\n=== HASIL PENGUJIAN ===")
    print(f"Jumlah data      : {JUMLAH_DATA}")
    print(f"Waktu eksekusi   : {waktu:.4f} detik")
    print(f"Status producer  : {p.exitcode}")
    print(f"Status consumer  : {c.exitcode}")

#Implementasi producer-consumer berbasis multiprocessing tetap mempertahankan pola produksi dan konsumsi data, 
#tetapi komunikasi dilakukan menggunakan multiprocessing.Queue. Perubahan utama terletak pada penggunaan proses 
#terpisah dan mekanisme komunikasi antarp­roses. Peningkatan performa tidak selalu terjadi karena multiprocessing 
#memiliki biaya pembentukan proses dan komunikasi yang lebih besar. Keuntungan performa lebih mungkin diperoleh 
#ketika pekerjaan yang dilakukan bersifat CPU-bound dan memiliki beban komputasi yang cukup besar.