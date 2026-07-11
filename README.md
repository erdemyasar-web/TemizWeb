# TemizWeb Ultimate

Türkçe odaklı, açık kaynak, mahremiyet dostu uBlock Origin paketi.

## Tek bağlantı

```text
https://raw.githubusercontent.com/erdemyasar-web/TemizWeb/main/filters/dist/temizweb-main.txt
```

Bu tek çıktı iki katmanı birleştirir:

1. TemizWeb'in YouTube/Reddit/Instagram arayüz ve Türkçe içerik kuralları.
2. HaGeZi NSFW yetişkin alan adı listesi.

Kullanıcıların HaGeZi'yi ayrıca eklemesi gerekmez. GitHub Actions listeyi her gün günceller.

## İlk kurulum

1. Bu arşivin **içindekileri** `erdemyasar-web/TemizWeb` adlı herkese açık GitHub deposunun köküne yükleyin.
2. Depoda **Actions** sekmesini açın ve `Build TemizWeb Ultimate` iş akışını çalıştırın.
3. **Settings → Pages** bölümünde `main` dalı ve `/docs` klasörünü seçin.
4. Kurulum sayfası: `https://erdemyasar-web.github.io/TemizWeb/`

## Tasarım ilkeleri

- SafeSearch veya YouTube Kısıtlı Mod zorlanmaz.
- Reddit/Instagram/YouTube tümden engellenmez.
- Banka, e-Devlet, sağlık, haber ve genel arama sitelerinde evrensel kelime gizleme yapılmaz.
- Bikini/mayo gibi bağlama bağlı görseller uBlock kelimeleriyle körlemesine engellenmez; görsel sınıflandırma aşamasına bırakılır.
- Tarama verisi toplanmaz veya bir sunucuya gönderilmez.

## Kaynak ve lisans

TemizWeb ve birleşik çıktı GPL-3.0-or-later lisanslıdır. Yetişkin alan adı katmanı HaGeZi DNS Blocklists projesinin GPL-3.0 lisanslı NSFW listesinden otomatik alınır. Kaynak bilgisi üretilen filtre içinde korunur.
