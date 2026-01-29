# Gorev2World

Bu repo, **TÜBİTAK İHA Yarışması (Görev 2)** için Gazebo’da kullanılacak bir **world (SDF)** dosyası ve hedefleri tarama alanı içinde **rastgele konumlandıran** küçük bir script içerir.

## Dosyalar

- **`tubitak_sabit_kanat_gorev2.sdf`**: Gazebo world dosyası (direkler, tarama alanı çerçevesi, hedefler vb.).
- **`generate_random_world.py`**: Hedeflerin konumunu tarama alanı içinde rastgele seçer ve world dosyasına yazar.

## Tarama alanı

Script içindeki sınırlar:

- **X**: `135` – `165`
- **Y**: `-50` – `50`

## Hedefler

Script, şu hedefleri konumlandırır:

- `mavi_kare_4x4`
- `kirmizi_kare_2x2`
- `mavi_altigen`
- `kirmizi_ucgen`

Hedefler arası çakışmayı engellemek için yaklaşık bir **tampon mesafe** uygulanır (`MIN_DISTANCE_BUFFER`).

## Çalıştırma

Python 3 ile:

```bash
python generate_random_world.py
```

Script çalışınca hedeflerin (X, Y) koordinatlarını basar ve `.sdf` (varsa `.world`) çıktısını üretir/günceller.

## Gazebo’da açma

SDF’yi Gazebo Sim ile açmak için örnek:

```bash
gz sim tubitak_sabit_kanat_gorev2.sdf
```

> Not: Script, eğer mevcutsa `tubitak_sabit_kanat_gorev2_template.sdf` / `.world` dosyalarını template olarak kullanır. Template yoksa aynı isimli `.sdf` / `.world` dosyasını baz alır.
