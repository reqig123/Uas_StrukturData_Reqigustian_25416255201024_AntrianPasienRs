import csv
import os

#Struktur data: Queue
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

    def get_queue(self):
        return self.items

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)



# Manajemen Antrian Rs
class RumahSakit:
    def __init__(self):
        # agar mengunci file csv (database) agar selalu satu folder dengan antrian.py
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.file_name = os.path.join(BASE_DIR, 'pasien.csv')
        
        self.antrian = Queue()
        # Struktur data: hash map yang berguna sebagai (Dictionary)
        self.data_pasien = {} 
        self.init_csv()
        self.load_data()

    def init_csv(self):
        """Membuat file CSV beserta header jika belum ada."""
        if not os.path.exists(self.file_name):
            with open(self.file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Nama', 'Umur', 'Keluhan', 'Status'])

    def load_data(self):
        """Membaca data dari CSV ke Hash Map dan Queue."""
        self.data_pasien.clear()
        self.antrian = Queue()
        with open(self.file_name, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                if row:
                    id_pasien, nama, umur, keluhan, status = row
                    # Simpan ke Hash Map
                    self.data_pasien[id_pasien] = {'Nama': nama, 'Umur': umur, 'Keluhan': keluhan, 'Status': status}
                    # Jika statusnya Menunggu, masukkan ke Queue
                    if status == 'Menunggu':
                        self.antrian.enqueue(id_pasien)

    def save_to_csv(self):
        """Menyimpan seluruh isi Hash Map kembali ke CSV."""
        with open(self.file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Nama', 'Umur', 'Keluhan', 'Status'])
            for id_pasien, detail in self.data_pasien.items():
                writer.writerow([id_pasien, detail['Nama'], detail['Umur'], detail['Keluhan'], detail['Status']])

    # Create
    def tambah_pasien(self):
        print("\n--- Pendaftaran Pasien Baru ---")
        id_pasien = input("Masukkan ID Pasien (misal: P001): ")
        if id_pasien in self.data_pasien:
            print("Peringatan: ID Pasien sudah terdaftar!")
            return

        nama = input("Nama Pasien: ")
        umur = input("Umur: ")
        keluhan = input("Keluhan: ")
        status = 'Menunggu'

        # Tambah ke Hash Map dan Queue
        self.data_pasien[id_pasien] = {'Nama': nama, 'Umur': umur, 'Keluhan': keluhan, 'Status': status}
        self.antrian.enqueue(id_pasien)
        self.save_to_csv()
        print(f"Sukses: Pasien {nama} berhasil didaftarkan dan masuk antrean!")

    # read dan sorting ( baca dan mesortingkan nama pasiean)
    def tampilkan_semua_pasien(self):
        print("\n--- Data Seluruh Pasien (Diurutkan Berdasarkan Nama) ---")
        if not self.data_pasien:
            print("Belum ada data pasien.")
            return

        # Mengambil data dari Hash Map untuk di-Sort
        daftar_pasien = [[k, v['Nama'], v['Umur'], v['Keluhan'], v['Status']] for k, v in self.data_pasien.items()]
        
        # Sorting: Bubble Sort
        n = len(daftar_pasien)
        for i in range(n):
            for j in range(0, n-i-1):
                if daftar_pasien[j][1] > daftar_pasien[j+1][1]: # Sort berdasarkan Nama (indeks 1)
                    daftar_pasien[j], daftar_pasien[j+1] = daftar_pasien[j+1], daftar_pasien[j]

        print(f"{'ID':<10} | {'Nama':<20} | {'Umur':<5} | {'Keluhan':<20} | {'Status'}")
        print("-" * 75)
        for p in daftar_pasien:
            print(f"{p[0]:<10} | {p[1]:<20} | {p[2]:<5} | {p[3]:<20} | {p[4]}")

    # Searching (mencari data pasien yang terdaftar)
    def cari_pasien(self):
        print("\n--- Cari Pasien ---")
        id_cari = input("Masukkan ID Pasien yang dicari: ")
        # Pencarian instan (O(1)) menggunakan Hash Map
        if id_cari in self.data_pasien:
            p = self.data_pasien[id_cari]
            print("\nData Ditemukan:")
            print(f"ID     : {id_cari}")
            print(f"Nama   : {p['Nama']}")
            print(f"Umur   : {p['Umur']}")
            print(f"Keluhan: {p['Keluhan']}")
            print(f"Status : {p['Status']}")
        else:
            print("Peringatan: Data pasien tidak ditemukan.")

    # Update ( mengperbarui data pasien)
    def ubah_data_pasien(self):
        print("\n--- Ubah Data Pasien ---")
        id_pasien = input("Masukkan ID Pasien yang akan diubah: ")
        if id_pasien not in self.data_pasien:
            print("Peringatan: ID Pasien tidak ditemukan!")
            return

        print("Kosongkan isian dan tekan Enter jika tidak ingin mengubah data tersebut.")
        nama = input(f"Nama ({self.data_pasien[id_pasien]['Nama']}): ")
        umur = input(f"Umur ({self.data_pasien[id_pasien]['Umur']}): ")
        keluhan = input(f"Keluhan ({self.data_pasien[id_pasien]['Keluhan']}): ")

        if nama: self.data_pasien[id_pasien]['Nama'] = nama
        if umur: self.data_pasien[id_pasien]['Umur'] = umur
        if keluhan: self.data_pasien[id_pasien]['Keluhan'] = keluhan

        self.save_to_csv()
        print("Sukses: Data pasien berhasil diperbarui!")

    # Menghapus data pasien ketika sudah selesai diperiksa (DELETE)
    def hapus_pasien(self):
        print("\n--- Hapus Data Pasien ---")
        id_pasien = input("Masukkan ID Pasien yang akan dihapus: ")
        if id_pasien in self.data_pasien:
            del self.data_pasien[id_pasien]
            self.antrian.remove_item(id_pasien)
            self.save_to_csv()
            print("Sukses: Data pasien berhasil dihapus dari sistem!")
        else:
            print("Peringatan: ID Pasien tidak ditemukan!")

    # Proses Queue
    def proses_antrean(self):
        print("\n--- Panggil Pasien Selanjutnya ---")
        if self.antrian.is_empty():
            print("Tidak ada pasien dalam antrean saat ini.")
            return

        id_pasien = self.antrian.dequeue()
        nama_pasien = self.data_pasien[id_pasien]['Nama']
        print(f"Memanggil pasien: {nama_pasien} (ID: {id_pasien}) untuk masuk ruang periksa.")
        
        # Update status menjadi selesai
        self.data_pasien[id_pasien]['Status'] = 'Selesai Diperiksa'
        self.save_to_csv()

# ==========================================
# MAIN LOOP (COMMAND LINE INTERFACE)
# ==========================================
def main():
    rs = RumahSakit()
    while True:
        print("\n" + "="*45)
        print("SISTEM MANAJEMEN ANTRIAN RUMAH SAKIT")
        print("="*45)
        print("1. Tambah Pasien Baru (Create & Enqueue)")
        print("2. Tampilkan Semua Pasien (Read & Sort)")
        print("3. Cari Data Pasien (Search / Hash Map)")
        print("4. Ubah Data Pasien (Update)")
        print("5. Hapus Data Pasien (Delete)")
        print("6. Panggil Pasien Antrean (Dequeue)")
        print("0. Keluar")
        print("="*45)
        
        pilihan = input("Pilih menu (0-6): ")
        
        if pilihan == '1':
            rs.tambah_pasien()
        elif pilihan == '2':
            rs.tampilkan_semua_pasien()
        elif pilihan == '3':
            rs.cari_pasien()
        elif pilihan == '4':
            rs.ubah_data_pasien()
        elif pilihan == '5':
            rs.hapus_pasien()
        elif pilihan == '6':
            rs.proses_antrean()
        elif pilihan == '0':
            print("Keluar dari sistem. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
