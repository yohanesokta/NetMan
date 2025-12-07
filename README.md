# ⚡ ~~POST~~ NET Man
|   *sangat cepat* **KLIEN API**

## Cara Instalasi

1.  **Clone repositori ini:**
    ```bash
    git clone https://github.com/Yohanes-otka/NetMan.git
    ```
2.  **Masuk ke direktori proyek:**
    ```bash
    cd NetMan
    ```
3.  **Instal dependensi:**
    Disarankan untuk menggunakan lingkungan virtual (virtual environment).
    ```bash
    pip install -r requerements.txt
    ```
4.  **Jalankan aplikasi:**
    ```bash
    python main.py
    ```

## Pola Desain: Adapter

Proyek ini menggunakan pola desain **Adapter** untuk membuat antarmuka yang stabil dan konsisten dalam melakukan permintaan HTTP. Tujuan utama dari pola ini adalah untuk memungkinkan objek dengan antarmuka yang tidak kompatibel untuk berkolaborasi. Dalam kasus kami, ini berfungsi sebagai pembungkus di sekitar pustaka `requests`, menyediakan antarmuka yang disederhanakan dan terpadu untuk sisa aplikasi.

### Cara Kerja

Inti dari pola ini adalah kelas `HttpAdapter`, yang terletak di `lib/http_adapter.py`. Kelas ini "mengadaptasi" pustaka `requests` ke antarmuka yang lebih sederhana dan lebih spesifik untuk aplikasi. Sisa aplikasi tidak perlu mengetahui seluk-beluk pustaka `requests`; ia hanya perlu berinteraksi dengan `HttpAdapter` kami.

Berikut adalah uraian siklus permintaan:

1.  **Interaksi UI**: Pengguna mengisi detail permintaan (URL, metode, header, body) di `RequestWidget` (satu tab).
2.  **Inisiasi Permintaan**: Ketika tombol "Send" diklik, metode `RequestAction` di `view/request_widget_logic.py` dipanggil.
3.  **Pembuatan Worker**: Sebuah `request_worker` baru (sebuah `QThread`) diinstansiasi untuk setiap permintaan. Ini mencegah UI membeku selama permintaan.
4.  **Transfer Data**: Data permintaan ditransfer dari `RequestWidget` ke `request_worker`.
5.  **Pemanggilan Adapter**: Metode `run` dari `request_worker` memanggil metode `HttpAdapter.fetch()`, meneruskan parameter permintaan.
6.  **Adaptasi**: Metode `HttpAdapter.fetch()` menerima data permintaan dan menerjemahkannya ke dalam panggilan ke pustaka `requests`. Ini menangani logika untuk mengirim body sebagai JSON atau data formulir berdasarkan parameter `body_type`.
7.  **Penanganan Respons**: `HttpAdapter` menangkap respons dari pustaka `requests`. Ini mencakup penanganan kesalahan untuk masalah jaringan dan untuk respons yang bukan JSON yang valid.
8.  **Emisi Sinyal**: `HttpAdapter` mengembalikan respons (atau kesalahan) ke `request_worker`, yang kemudian memancarkan sinyal `progress` dengan data respons.
9.  **Pembaruan UI**: Metode `RequestParse` dari `RequestWidget`, yang terhubung ke sinyal `progress`, menerima data respons dan memperbarui UI untuk menampilkannya.

### Metode `HttpAdapter.fetch()`

Metode `fetch` adalah inti dari adapter. Ini menyediakan antarmuka tunggal dan bersih untuk membuat segala jenis permintaan HTTP.

`fetch(self, url, method='GET', headers=None, body=None, body_type='json')`

-   `url`: URL untuk permintaan.
-   `method`: Metode HTTP yang akan digunakan (misalnya, 'GET', 'POST', 'PUT', 'DELETE', 'PATCH').
-   `headers`: Kamus header untuk disertakan dengan permintaan.
-   `body`: Kamus yang mewakili payload permintaan.
-   `body_type`: String yang menentukan bagaimana `body` harus dikodekan. Ini bisa berupa `'json'` atau `'form'`.

### Manfaat Pola Adapter

Menggunakan pola Adapter dalam proyek ini memberikan beberapa keuntungan utama:

-   **Dekopling**: Aplikasi tidak terlalu terkait erat dengan pustaka `requests`. Jika kita memutuskan untuk beralih ke pustaka HTTP yang berbeda di masa mendatang (misalnya, `httpx`), kita hanya perlu memodifikasi kelas `HttpAdapter`. Sisa kode aplikasi akan tetap tidak berubah.
-   **Antarmuka Sederhana**: `HttpAdapter` menyediakan antarmuka tingkat tinggi yang sederhana untuk membuat permintaan HTTP. Ini membuat kode di `RequestWidget` dan `request_worker` lebih bersih dan lebih mudah dipahami.
-   **Logika Terpusat**: Semua logika untuk membuat permintaan HTTP dan menangani kesalahan umum terpusat di `HttpAdapter`. Ini membuat kode lebih mudah dipelihara dan di-debug.
-   **Keterbacaan yang Ditingkatkan**: Kode lebih mudah dibaca dan mendokumentasikan diri karena tujuan `HttpAdapter` jelas.