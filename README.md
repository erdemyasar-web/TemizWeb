# TemizWeb DNS

TemizWeb'in ikinci katmanı: SafeSearch zorlamadan yetişkin alan adlarını ve isteğe bağlı aşma araçlarını DNS seviyesinde engelleyen açık kaynak listeler.

## Üretilen profiller

### Balanced — varsayılan

Yalnızca yetişkin alan adları. Kaynaklar:

- HaGeZi NSFW
- The Block List Project Porn
- TemizWeb Türkçe eki

### Adult + VPN

Balanced içeriğine ek olarak büyük VPN sağlayıcılarının, web proxy'lerin ve yaygın aşma araçlarının resmi/indirme alanları.

### Strict

Adult + VPN profiline ek olarak yaygın açık DNS-over-HTTPS / DNS-over-TLS hizmet alanları.

## SafeSearch

Hiçbir profil Google SafeSearch veya YouTube Restricted Mode DNS yönlendirmesi içermez.

## Çıktı biçimleri

Her profil için:

- `*-domains.txt`: yalnızca alan adları
- `*-hosts.txt`: hosts/Pi-hole biçimi
- `*-adguard.txt`: AdGuard/uBlock biçimi

## Derleme

```bash
python scripts/build_dns.py
python scripts/check_dns.py
```

Workflow listeleri günlük yeniler.

## Sınırlar

DNS yalnızca alan adını görür. Reddit, haber sitesi veya spor sitesindeki tek bir görseli sınıflandıramaz. Önceden yüklenmiş VPN uygulamalarını veya doğrudan IP ile çalışan tünelleri kesin olarak durduramaz.
