# Türk Mutfağı Malzeme Ağı - Ara Kontrol Scripti
# Colab'da çalıştır:  !pip install datasets networkx pandas
import re, json, itertools, collections
import pandas as pd
import networkx as nx

TOP_N = 1000        # en sık geçen kaç malzeme düğüm olsun
MIN_WEIGHT = 20     # iki malzeme en az kaç tarifte birlikte geçsin

# 1) VERİYİ İNDİR (tüm split'leri birleştirir)
from datasets import load_dataset, concatenate_datasets
dd = load_dataset("mmkocak/turkish-recipes-175K")
df = concatenate_datasets(list(dd.values())).to_pandas()
print("Tarif sayısı:", len(df))

# 2) MALZEME TEMİZLEME
BIRIMLER = r"su bardağı|çay bardağı|yemek kaşığı|tatlı kaşığı|çay kaşığı|çorba kaşığı|kahve fincanı|çay fincanı|bardak|kaşık|fincan|kase|avuç|tutam|adet|tane|diş|dilim|demet|paket|kutu|konserve|litre|lt|ml|kg|gr|gram|cl|cm|santim|yaprak|parça|top|dal|küp|baş|çubuk|damla|porsiyon|kadar|miktarı"
SIFATLAR = r"büyük|küçük|orta boy|orta|boy|bol|yarım|yarısı|çeyrek|isteğe göre|isteğe bağlı|taze|ince|kalın|iri|doğranmış|doğranmışı|rendelenmiş|haşlanmış|közlenmiş|kıyılmış|dilimlenmiş|soyulmuş|çekilmiş|ezilmiş|erimiş|oda sıcaklığında|ılık|sıcak|soğuk|kuru|yumuşak|süzülmüş|püre|için|üzeri|servis|süslemek|yağlamak|kızartmak|hafif|ve|veya|ile|az|çok|biraz|dolusu|kabaca|bütün"

def temizle(s):
    s = str(s).lower()
    s = re.sub(r"\(.*?\)", " ", s)           # parantez içi
    s = s.split(",")[0]                       # virgülden sonrası
    s = re.sub(r"[\d½¼¾⅓⅔/.\-–:]+", " ", s)  # sayılar
    s = re.sub(rf"\b({BIRIMLER})\b", " ", s)
    s = re.sub(rf"\b({SIFATLAR})\b", " ", s)
    s = re.sub(r"[^a-zçğıöşü ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s if 2 <= len(s) < 30 else None

recete_malzeme = []
for ing in df["ingredients"]:
    temiz = {temizle(x) for x in (ing if ing is not None else [])}
    temiz.discard(None)
    recete_malzeme.append(temiz)

# 3) EN SIK MALZEMELER = DÜĞÜMLER
sayac = collections.Counter(m for r in recete_malzeme for m in r)
top = {m for m, _ in sayac.most_common(TOP_N)}
recete_malzeme = [r & top for r in recete_malzeme]

# 4) İKİ PARÇALI AĞ İSTATİSTİĞİ (tarif <-> malzeme)
bip_kenar = sum(len(r) for r in recete_malzeme)
bip_tarif = sum(1 for r in recete_malzeme if r)

# 5) PROJEKSİYON: malzeme-malzeme (birlikte geçme sayısı = ağırlık)
cift = collections.Counter()
for r in recete_malzeme:
    for a, b in itertools.combinations(sorted(r), 2):
        cift[(a, b)] += 1

G = nx.Graph()
for m in top:
    G.add_node(m, tarif_sayisi=sayac[m])
for (a, b), w in cift.items():
    if w >= MIN_WEIGHT:
        G.add_edge(a, b, weight=w)
G.remove_nodes_from(list(nx.isolates(G)))

# 6) DOSYALARI KAYDET
pd.DataFrame([(a, b, d["weight"]) for a, b, d in G.edges(data=True)],
             columns=["source", "target", "weight"]).to_csv("edges.csv", index=False)
pd.DataFrame([(n, d["tarif_sayisi"]) for n, d in G.nodes(data=True)],
             columns=["malzeme", "tarif_sayisi"]).to_csv("nodes.csv", index=False)
df.head(500).to_csv("ornek_tarifler.csv", index=False)
nx.write_graphml(G, "malzeme_agi.graphml")

bilesenler = list(nx.connected_components(G))
ist = {
    "tarif_sayisi_ham": len(df),
    "ikiparcali_tarif_dugumu": bip_tarif,
    "ikiparcali_malzeme_dugumu": len(top),
    "ikiparcali_kenar": bip_kenar,
    "projeksiyon_dugum": G.number_of_nodes(),
    "projeksiyon_kenar": G.number_of_edges(),
    "yogunluk": round(nx.density(G), 4),
    "bilesen_sayisi": len(bilesenler),
    "en_buyuk_bilesen_dugum": len(max(bilesenler, key=len)),
    "min_agirlik_esigi": MIN_WEIGHT,
    "ilk_10_malzeme": sayac.most_common(10),
}
json.dump(ist, open("istatistikler.json", "w"), ensure_ascii=False, indent=2)
print(json.dumps(ist, ensure_ascii=False, indent=2))
