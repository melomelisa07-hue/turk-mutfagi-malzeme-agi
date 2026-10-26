# Türk Mutfağı Malzeme Ağı

## Araştırma sorusu
Türk mutfağında malzemeler hangi "lezzet topluluklarını" oluşturuyor ve hangi malzemeler bu toplulukları birbirine bağlıyor?

## Veri kaynağı
- Veri seti: mmkocak/turkish-recipes-175K
- Link: https://huggingface.co/datasets/mmkocak/turkish-recipes-175K
- Lisans: Apache-2.0
- Toplama tarihi: 26 Ekim 2026
- Ham veri 497 MB olduğu için depoya yüklenmedi, ilk 500 tarif `ornek_tarifler.csv` içindedir.

## Ağ tanımı
- Düğüm: malzeme (en sık geçen 1000 malzeme)
- Kenar: iki malzemenin aynı tarifte birlikte geçmesi
- Ağırlık: birlikte geçtikleri tarif sayısı (en az 20)
- Önce tarif–malzeme (iki parçalı) ağı kuruldu, sonra malzeme–malzeme ağına projeksiyon yapıldı.

## Temel istatistikler
- Tarif sayısı: [ 174975,]
- Düğüm sayısı: [987,]
- Kenar sayısı: [41230,]
- Yoğunluk: [0.0847,]
- Bileşen sayısı: [1,]

## Dosyalar
- `edges.csv`: kenar listesi
- `nodes.csv`: düğüm listesi
- `malzeme_agi.graphml`: ağ dosyası
- `istatistikler.json`: istatistikler
- `ag_kur.py`: ağı kuran kod

## Yapay zekâ beyanı
Kod yazımında Claude'dan yardım alınmıştır. Kullanılan yöntemleri açıklayabilirim.
