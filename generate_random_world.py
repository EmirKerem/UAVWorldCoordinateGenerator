#!/usr/bin/env python3
"""
TÜBİTAK İHA Yarışması - Rastgele World Generator
Hedefleri tarama alanı içinde rastgele konumlandırır
"""

import random
import math
import sys

# Tarama alanı sınırları (30x100m)
TARAMA_X_MIN = 135
TARAMA_X_MAX = 165
TARAMA_Y_MIN = -50
TARAMA_Y_MAX = 50

# Hedef boyutları (yarıçap olarak - collision için)
HEDEFLER = {
    'mavi_kare_4x4': {'size': 4.0, 'type': 'kare'},
    'kirmizi_kare_2x2': {'size': 2.0, 'type': 'kare'},
    'mavi_altigen': {'size': 2.5, 'type': 'altigen'},  # 2m kenar ~ 2.5m yarıçap
    'kirmizi_ucgen': {'size': 1.0, 'type': 'ucgen'}     # 1m kenar ~ 1m yarıçap
}

# Minimum mesafe hedefler arasında
MIN_DISTANCE_BUFFER = 3.0  # 3m tampon

class HedefKonumlayici:
    def __init__(self):
        self.yerlestirilmis_hedefler = []
    
    def mesafe_hesapla(self, pos1, pos2):
        """İki nokta arasındaki Euclidean mesafe"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def cakisma_var_mi(self, yeni_pos, yeni_boyut):
        """Yeni hedef mevcut hedeflerle çakışıyor mu?"""
        for pos, boyut in self.yerlestirilmis_hedefler:
            mesafe = self.mesafe_hesapla(yeni_pos, pos)
            gerekli_mesafe = (yeni_boyut + boyut) / 2 + MIN_DISTANCE_BUFFER
            
            if mesafe < gerekli_mesafe:
                return True
        return False
    
    def alan_icinde_mi(self, pos, boyut):
        """Hedef tarama alanı içinde mi?"""
        yaricap = boyut / 2
        
        if pos[0] - yaricap < TARAMA_X_MIN or pos[0] + yaricap > TARAMA_X_MAX:
            return False
        if pos[1] - yaricap < TARAMA_Y_MIN or pos[1] + yaricap > TARAMA_Y_MAX:
            return False
        
        return True
    
    def rastgele_konum_bul(self, hedef_adi, hedef_bilgi):
        """Uygun rastgele konum bul"""
        boyut = hedef_bilgi['size']
        max_deneme = 1000
        
        for _ in range(max_deneme):
            # Rastgele koordinat üret (hedef boyutunu dikkate alarak)
            yaricap = boyut / 2
            x = random.uniform(TARAMA_X_MIN + yaricap, TARAMA_X_MAX - yaricap)
            y = random.uniform(TARAMA_Y_MIN + yaricap, TARAMA_Y_MAX - yaricap)
            
            pos = (x, y)
            
            # Alan içinde mi ve çakışma yok mu?
            if self.alan_icinde_mi(pos, boyut) and not self.cakisma_var_mi(pos, boyut):
                self.yerlestirilmis_hedefler.append((pos, boyut))
                return pos
        
        # Uygun konum bulunamadı
        print(f"UYARI: {hedef_adi} için uygun konum bulunamadı!")
        # Fallback: merkeze yakın rastgele konum
        x = random.uniform(145, 155)
        y = random.uniform(-25, 25)
        return (x, y)
    
    def tum_hedefleri_konumlandir(self):
        """Tüm hedefleri rastgele konumlandır"""
        konumlar = {}
        
        for hedef_adi, hedef_bilgi in HEDEFLER.items():
            pos = self.rastgele_konum_bul(hedef_adi, hedef_bilgi)
            konumlar[hedef_adi] = pos
            print(f"✓ {hedef_adi}: X={pos[0]:.2f}, Y={pos[1]:.2f}")
        
        return konumlar

def world_dosyasi_olustur(konumlar, template_dosya, cikti_dosya):
    """Template'den yeni world dosyası oluştur"""
    
    # Template'i oku
    try:
        with open(template_dosya, 'r', encoding='utf-8') as f:
            icerik = f.read()
    except FileNotFoundError:
        print(f"HATA: Template dosyası bulunamadı: {template_dosya}")
        sys.exit(1)
    
    # Hedef koordinatlarını değiştir
    # Mavi 4x4 kare
    icerik = icerik.replace(
        '<model name="mavi_kare_4x4">\n      <static>true</static>\n      <pose>145 -25 0.01 0 0 0</pose>',
        f'<model name="mavi_kare_4x4">\n      <static>true</static>\n      <pose>{konumlar["mavi_kare_4x4"][0]:.3f} {konumlar["mavi_kare_4x4"][1]:.3f} 0.01 0 0 0</pose>'
    )
    
    # Kırmızı 2x2 kare
    icerik = icerik.replace(
        '<model name="kirmizi_kare_2x2">\n      <static>true</static>\n      <pose>155 -25 0.01 0 0 0</pose>',
        f'<model name="kirmizi_kare_2x2">\n      <static>true</static>\n      <pose>{konumlar["kirmizi_kare_2x2"][0]:.3f} {konumlar["kirmizi_kare_2x2"][1]:.3f} 0.01 0 0 0</pose>'
    )
    
    # Mavi altıgen
    icerik = icerik.replace(
        '<model name="mavi_altigen">\n      <static>true</static>\n      <pose>145 25 0.01 0 0 0</pose>',
        f'<model name="mavi_altigen">\n      <static>true</static>\n      <pose>{konumlar["mavi_altigen"][0]:.3f} {konumlar["mavi_altigen"][1]:.3f} 0.01 0 0 0</pose>'
    )
    
    # Kırmızı üçgen
    icerik = icerik.replace(
        '<model name="kirmizi_ucgen">\n      <static>true</static>\n      <pose>155 25 0.01 0 0 0</pose>',
        f'<model name="kirmizi_ucgen">\n      <static>true</static>\n      <pose>{konumlar["kirmizi_ucgen"][0]:.3f} {konumlar["kirmizi_ucgen"][1]:.3f} 0.01 0 0 0</pose>'
    )
    
    # Yeni dosyayı yaz
    with open(cikti_dosya, 'w', encoding='utf-8') as f:
        f.write(icerik)
    
    print(f"\n✅ Yeni world dosyası oluşturuldu: {cikti_dosya}")

def main():
    print("=" * 60)
    print("  TÜBİTAK İHA Yarışması - Rastgele World Generator")
    print("=" * 60)
    print(f"Tarama Alanı: {TARAMA_X_MAX - TARAMA_X_MIN}m x {TARAMA_Y_MAX - TARAMA_Y_MIN}m")
    print(f"Koordinatlar: X=[{TARAMA_X_MIN}, {TARAMA_X_MAX}], Y=[{TARAMA_Y_MIN}, {TARAMA_Y_MAX}]")
    print("=" * 60)
    print()
    
    # Hedefleri konumlandır
    konumlayici = HedefKonumlayici()
    konumlar = konumlayici.tum_hedefleri_konumlandir()
    
    print()
    print("-" * 60)
    
    # Template ve çıktı dosyaları
    import os
    script_dizin = os.path.dirname(os.path.abspath(__file__))
    
    # Hem .world hem .sdf için
    for uzanti in ['world', 'sdf']:
        template_dosya = os.path.join(script_dizin, f'tubitak_sabit_kanat_gorev2_template.{uzanti}')
        cikti_dosya = os.path.join(script_dizin, f'tubitak_sabit_kanat_gorev2.{uzanti}')
        
        # Template yoksa orijinali kullan
        if not os.path.exists(template_dosya):
            template_dosya = os.path.join(script_dizin, f'tubitak_sabit_kanat_gorev2.{uzanti}')
        
        if os.path.exists(template_dosya):
            world_dosyasi_olustur(konumlar, template_dosya, cikti_dosya)
    
    print()
    print("=" * 60)
    print("🚀 Gazebo'yu şu komutla başlatın:")
    print(f"   gz sim ~/Ardu/World/tubitak_sabit_kanat_gorev2.sdf")
    print("=" * 60)

if __name__ == "__main__":
    main()
