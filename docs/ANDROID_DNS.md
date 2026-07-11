# TemizWeb DNS — Android kurulumu

## Şimdilik önerilen kurulum: Rethink DNS + Firewall

Rethink açık kaynaklıdır ve Android'in VPN yuvasını kullanarak cihaz genelindeki DNS isteklerini seçtiğiniz çözücüye yönlendirir.

### Dengeli profil

Bu profil yalnızca yetişkin alan adlarını engeller. SafeSearch veya YouTube Restricted Mode zorlamaz.

1. Rethink DNS + Firewall uygulamasını F-Droid veya Google Play üzerinden kurun.
2. Uygulamayı açın ve DNS modunu etkinleştirin.
3. Rethink'in yapılandırma sayfasında yalnızca **Adult** listesini seçin.
4. Gambling, Dating ve Social Media kategorilerini seçmeyin.
5. Android VPN iznini kabul edin.
6. İsterseniz Android ayarlarında Always-on VPN'i etkinleştirin.

### TemizWeb özel listeleri

`dns/dist/` çıktıları Pi-hole, AdGuard Home, NextDNS benzeri özel liste kabul eden sistemlerde kullanılabilir.

Rethink'in mevcut genel Android sürümünde uzaktaki özel GitHub listesini tek dokunuşla topluca içe aktarmak için güvenilir bir akış bulunmadığından, VPN/proxy ve DNS-bypass profilleri şimdilik altyapı çıktısı olarak yayımlanır.

## Profiller

- `temizweb-balanced`: yalnızca yetişkin alan adları.
- `temizweb-adult-vpn`: yetişkin alan adları + VPN/proxy resmi ve indirme siteleri.
- `temizweb-strict`: bunlara ek olarak yaygın alternatif DoH/DoT hizmet alanları.

Strict profil normal gizlilik araçlarını da engelleyebilir. Varsayılan yapılmamalıdır.
