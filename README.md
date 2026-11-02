# kaloriku-web

Situs marketing KaloriKu (Android). Statis murni — HTML, CSS, sedikit JavaScript.
Tanpa build step, tanpa dependency.

Repo terpisah dari `isyarharun.github.io` (rumah kebijakan privasi + `app-ads.txt`).

## Struktur

```
index.html            halaman Bahasa Indonesia (root)
en/index.html         halaman English
css/style.css         satu stylesheet untuk kedua bahasa
js/main.js            menu mobile, FAQ, animasi reveal
assets/img/           logo, screenshot, foto hidangan, og.jpg
assets/fonts/         Plus Jakarta Sans (self-host, latin + latin-ext)
scripts/              utilitas pengembangan (tidak ikut dipakai runtime)
   set-domain.py      suntik domain → canonical, hreflang, sitemap, CNAME, robots
   prep-assets.py     potong logo/screenshot dari aset aplikasi
   og.html + og.js    render og.png 1200×630
   capture.js         screenshot QA (desktop 1440, mobile 390, EN)
```

## Pratinjau lokal

```bash
python3 -m http.server 8123
# http://127.0.0.1:8123/      → ID
# http://127.0.0.1:8123/en/   → EN
```

## Memasang domain

```bash
python3 scripts/set-domain.py kaloriku.id
```

Sekali jalan: `canonical`, `hreflang` (id / en / x-default), `og:url`, `og:image`
absolut, `sitemap.xml`, `CNAME`, dan `robots.txt`. Aman dijalankan berulang.

Tanpa argumen, skrip menampilkan domain yang sedang terpasang.

## Deploy

**Cloudflare Pages (dipakai):**

1. Tambahkan domain ke Cloudflare (Free), lalu ganti nameserver di registrar.
2. Workers & Pages → Create → Pages → Connect to Git → repo `kaloriku-web`.
   Framework preset `None`, build command kosong, output directory `/`.
3. Custom domains: `kaloriku.id` dan `www.kaloriku.id` (CNAME dibuat otomatis).
4. `_headers` mengatur cache aset + header keamanan; `_redirects` menutup `/en` → `/en/`.
5. Setelah domain aktif: `python3 scripts/set-domain.py kaloriku.id` lalu push,
   dan verifikasi dengan `python3 scripts/check-live.py kaloriku.id`.

GitHub Pages (alternatif):

1. Push isi folder ini ke branch `main`.
2. Settings → Pages → Source: `main` / root. File `CNAME` sudah berisi domain.
3. Di DNS registrar: `A` record ke `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153`; `CNAME www` ke `<user>.github.io`.
   Aktifkan "Enforce HTTPS" setelah sertifikat terbit.

## Aset

Semua visual berasal dari aplikasi, bukan ilustrasi stok:

- `logo-*.png`, `mark-512.png` — dari `KaloriKu_Logo.png` / `splash_logo.png`,
  latar putih di-key jadi transparan (`prep-assets.py`).
- `screen-home.webp`, `screen-history.webp` — screenshot asli dari emulator
  (1080×2400, diperkecil ke 720 px). Bukan mockup.
- `meals-card.webp` — potongan kartu "Makanan Hari Ini" dari layar Beranda asli.
  Angkanya konsisten: 90 + 250 + 320 + 650 = 1.310 kkal dari 2.000.
- `og.png`/`og.jpg` — komposit logo + dua screenshot, dirender dari `scripts/og.html`.

## Catatan

- `app-ads.txt` disalin dari repo developer. Kalau situs developer di Play Console
  dipindah ke domain baru ini, file sudah tersedia di root.
- Halaman privasi & syarat tetap di `https://isyarharun.github.io/kaloriku-privacy/`
  (repo terpisah). Jangan hapus dari sana selama URL itu terdaftar di Play Console.
- Angka di situs (500+ unduhan, 3 scan/hari, 10 scan/hari Premium, 650/320/250/90 kkal)
  diambil dari Play Store, kode aplikasi, dan data yang benar-benar dicatat di
  emulator. Perbarui kalau berubah.
