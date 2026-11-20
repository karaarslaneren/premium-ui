# Değişiklik günlüğü

## Yayınlanmadı

- **Kendini tekrar etme sorunu:** SKILL.md her landing için sabit bir bölüm
  sırası veriyordu (hero → entegrasyonlar → akış → sabitlenen adımlar →
  bento → hesaplayıcı → fiyat → SSS carousel → CTA → footer'da dev yazı);
  brief şablonu ve animasyon kataloğu da aynı listeyi öneriyordu. Bu yüzden
  her sayfa aynı iskelette ve aynı footer'la çıkıyordu. Sabit sıra kaldırıldı;
  yerine ürünün hikâyesinden çıkan bir sahne planı geldi. Footer'daki dev
  yazı artık varsayılan değil, yalnızca marka adı yönün fikriyse
  kullanılıyor.
- **Sayfa hareketleri hafızada:** `learn.py build` kullanılan sahne planını
  ve hareketleri (footer-wordmark, pinned-steps, carousel…) kaydediyor;
  `recall` son projelerde 2+ kez kullanılanları "varsayılan olarak kapalı"
  diye listeliyor.
- **Üst düzey tasarım rehberi:** yeni `references/high-end.md`, ajans
  seviyesindeki bir siteyi (teknokent tanıtım sitesi) inceleyerek yazıldı:
  sahneler (5–8, yan yana iki sahne aynı düzende değil, uzun hikâyeler
  sabitlenen dizilerle), marka şeklinin grafik sistem olması, gerçek
  fotoğraf ve ürüne özel görseller, gerçek verinin keşfedilebilir
  görselleştirmesi (kat planı, harita), arayüz detayları, tipografik
  kontrast, scroll'a bağlı koreografi. 8 maddelik seviye kontrolü (16
  üzerinden 12 altı gösterilmiyor). Öneri panosuna "Sayfa kurgusu" eklendi.
- **Bileşen kapsamı:** "sadece inputlar", "butonlar", "tablolar" gibi
  istekler artık skill'in içinde. Yeni `references/component-craft.md`
  (kapsam kuralları, durum matrisi, türce farklı varyantlar, input / select
  / checkbox / buton / tablo tarifleri, Türkçe formatlar) ve
  `assets/component-board.html`. Bu kapsamda bölüm, footer ya da sayfa
  düzeni değişmiyor; bileşen merkezden (ortak bileşen ya da tema) değişiyor.
- **Eval:** (1) "Sadece inputları premium yap": skill projeye dokunmadan 9
  alanı buldu, mevcut slate renkleriyle türce farklı üç varyant (çerçeve +
  halka, dolgulu + parıltı, etiket solda grup kartı) ve tüm durumları açık
  ve koyu gösterdi; uygulama planı ortak bileşen ve tema üzerinden, sayfa
  düzeni değişmeden. Gerçek bir hata da yakaladı: `--input` ve `--ring`
  tanımsız olduğu için inputlar varsayılan griye düşüyordu. (2) Hafızasında
  footer yazısı 6, sabitlenen adımlar 4 kez geçen bir kullanıcıyla "ajans
  işi landing": 7 sahnelik kurgu, yan yana aynı düzen yok, footer sade
  (menü, iletişim, yasal), sık kullanılan hareketlerin hiçbiri yok. Seviye
  kontrolü 14/16; en zayıf madde görseller (projede fotoğraf yok).
- **Tasarım araştırması sonrası eklemeler** (ödül alan siteler üzerine
  yazılar, jüri rehberleri ve web platformu güncellemeleri):
  - `references/motion-engine.md`: GSAP + ScrollTrigger (artık ücretsiz),
    Lenis, CSS scroll-driven animations ve View Transitions için hangi
    durumda hangisi; koreografi token'ları (süre, gecikme, üç easing,
    kişilik), sahne başına tek ana zaman çizelgesi, kaydırma hızına uyum,
    sayfa ve durum geçişleri, hareket bütçesi.
  - **İmza anı:** sayfa tek bir unutulmaz an etrafında kuruluyor; kodlamadan
    önce üç karelik senaryo, her kare tek başına güçlü olmalı. Öneri
    panosuna eklendi.
  - `references/art-direction.md`: görsel envanteri, tüm fotoğraflara tek
    işlem, fotoğraf yoksa kullanıcıya çekim listesi (stok ya da üretilmiş
    insan yok), gerçek veriden SVG görseller, kinetik ve değişken fontlu
    tipografi.
  - `references/copy.md`: başlık kalıpları, yasak klişeler ("geleceği…",
    "yenilikçi çözümler"), sahne metni düzeni.
  - `scripts/study.js`: referans siteyi tarayıcıda ölçüyor (sahneler,
    sabitlenen bölümler, ölçek sıçraması, palet, GSAP/Lenis/CSS scroll
    timeline, hover sayısı). Nehir Teknokent sitesinde denendi: 8 sahne,
    3'ü sabitlenmiş, 72/14,5 px (5×), Lenis + ScrollTrigger, 155 hover
    kuralı.
  - `references/webgl.md`: isteğe bağlı 3D katmanı; yalnızca fiziksel ürün
    ya da yer için, cihaz kademeleri, düz HTML yedeği.
  - Arayüz detayları (imleç, menü, dokunmatik karşılık, sahne geçişi)
    `high-end.md`'ye eklendi.
  - `verify.js` performans bloğu: LCP, CLS, sayfa ağırlığı, JS boyutu,
    yükleme sonrası uzun kareler, DOM boyutu (laboratuvar ölçümü, yalnızca
    uyarı).
  - Görsel kontrole üç eleştirmen (sanat yönetmeni, hareket tasarımcısı,
    erişilebilirlik) ve "yapay zekâ yapmış gibi mi" testi.
- **`verify.js`:** odak stili kontrolü artık sarmalayıcıdaki `:focus-within`
  kuralını da sayıyor (stillenmiş alan içindeki input yanlış uyarı
  veriyordu).

## 1.2.0

- **Tekdüzeliğe karşı yön bulma yöntemi:** eval'de skill her projede aynı üç
  yönü (sıcak kâğıt + italik serif, koyu "kontrol kulesi", sarı-siyah afiş)
  ve aynı landing görünümünü üretiyordu. Yeni `references/direction-finding.md`
  yönleri ürünün dünyasından, kitlesinden ve mevcut marka varlıklarından
  türetiyor. Yönler en az üç eksende farklı olmak zorunda. Sık kullanılan
  kalıplar yalnızca ürüne özgü bir gerekçeyle seçilebiliyor. Her yön "takas"
  ve "kısma" testlerinden geçiyor.
- **Kalıp oluşturan örnekler kaldırıldı:** SKILL.md'deki örnek yönler,
  proposal-board.md'deki sabit "editoryal / koyu / cesur" dağılımı, brief
  şablonundaki görünüm örneği ve panel/auth tariflerindeki "kâğıt" ile
  "serif vurgu" varsayımları çıkarıldı.
- **Nötr şablon:** `assets/proposal-board.html` artık gri tonlar ve sistem
  fontuyla gelen bir iskelet. Hazır font, renk ve isim içermiyor. Vurgu,
  `--em-*` token'larıyla yönün kendi vurgu aracına (ağırlık, renk, büyük harf,
  ikinci font, vurgulama) bağlanıyor.
- **Çeşitlilik eval'i sonrası:** üç farklı üründe (kargo, fatura, QR menü)
  1.1.0'ın 9 yönünün 6'sı "kâğıt + italik serif" ya da "kontrol kulesi"
  kalıbındaydı; 1.2.0'da 12 yönden yalnızca 1'i. Yerine yeni bir çekim
  noktası çıktı (koyu lacivert + Barlow Condensed büyük harf, kraft bej,
  IBM Plex). Bunlar da sık kullanılan kalıplar listesine eklendi. Panoda
  sık kullanılan fontlardan en fazla biri olabiliyor. "Her panoda bir koyu
  yön" alışkanlığı kaldırıldı. Yeniden öneri istendiğinde önceki panonun
  metaforları ve fontları tekrar kullanılamıyor.
- **Çeşitlilik eval'i, ikinci tur:** Barlow, IBM Plex, kraft bej ve koyu
  lacivert + dar büyük harf tamamen kayboldu. 4 panoda 13 farklı font ailesi
  (önceki tur 9). Yeni tekrarlar (Rubik, "her şey mono + büyük harf + 2px
  çerçeve") listeye eklendi. Aynı panoda bir font yalnızca bir yönde
  kullanılabiliyor. Renkli zeminde görünmeyen ghost buton hatası pitfalls'a
  eklendi.
- **Tipografi kütüphanesi:** yeni `references/type-library.md` yaklaşık 125
  Google Fonts yazı tipini 12 türe ayırıyor (geometrik, grotesk, humanist,
  yuvarlak, dar, geniş, iki tür serif, slab, mono, el yazısı, display) ve
  her birine karakter ve uygun olduğu dünya notu ekliyor. Listeler
  alfabetik; skill fontu ilk sıradan değil, yönün metaforuna uyan nottan
  seçiyor. Yeni `scripts/check-fonts.py` font dosyasının glif tablosunu
  okuyup Türkçe karakterleri kontrol ediyor. 11 popüler fontta (Fredoka,
  Arvo, Prata, Lilita One…) ğ, ş ya da İ eksik çıktı; Atkinson Hyperlegible
  ve Titan One latin-ext sunduğu halde İ içermiyor.
- **Çeşitlilik eval'i, üçüncü tur (kütüphaneyle):** 4 panoda 17 farklı font
  ailesi (önceki tur 13). Sık kullanılan fontlar listesinden hiçbiri ve
  "her şey mono + büyük harf" yönü hiç çıkmadı. Hiçbir font 3 panoda
  tekrar etmedi. Dört panonun hepsi `verify.js` kontrollerini geçti (önceki
  turda iki panoda kontrast hatası vardı). Kalan tekrar: aynı ürünün
  bağımsız iki çalıştırması aynı üç metafora (otoyol tabelası, SMS,
  15 dakikalık tur) ve dolayısıyla aynı fontlara dönüyor.
- **Az belirgin metafor kuralı:** `direction-finding.md` artık ürünün
  nesnelerini "belirgin" ve "az belirgin" diye ayırıyor; panodaki yönlerden
  en az biri az belirgin yarıdan (bir ritüel, ses, zanaat aleti, günün bir
  saati) gelmek zorunda. Dördüncü turda etkisi sınırlı kaldı: 12 yönden
  yalnızca 2'si yeniydi (Sevk İrsaliyesi, Masa Kartı). Aynı ürün bağımsız
  çalıştırmalarda büyük ölçüde aynı metaforlara, aynı metafor da
  kütüphanedeki aynı fonta gidiyor (Defterim iki turda da Antonio, Onest,
  Kumbh Sans). Bir kullanıcı tek pano gördüğü ve "başka seçenek"
  istendiğinde önceki pano tekrar edilmediği için bu kabul edildi.
- **Görsel eleştiri adımı:** yeni `references/visual-critique.md`. Pano
  doldurulduktan sonra ve her bölüm yapıldıktan sonra ekran görüntüsü
  alınıyor ve altı soru yanıtlanıyor: okunuyor mu, bitmiş mi, kırık mı,
  kısma, takas, mobil. Bulunanlar düzeltilip görüntü yeniden alınıyor,
  en fazla iki tur.
- **`scripts/snapshot.py`:** tarayıcı aracı olmayan ortamlar için. Makinedeki
  Chrome/Chromium/Edge'i headless çalıştırıp yerel bir HTML dosyasının
  masaüstü ve mobil ekran görüntüsünü alıyor, `verify.js` raporunu aynı
  sayfada üretiyor. Headless Chrome 500px'ten dar pencere açmadığı için
  mobil görünüm tam genişlikte bir iframe içinde çiziliyor.
- **Görsel kontrol eval'i:** 4 panoda modeller kendi ekran görüntülerinde
  10 sorun bulup düzeltti: ilk karede boş telefon/bant animasyonları, iki
  satıra bölünen etiketler, taşan kaşe, kesilen yazı. Bağımsız ölçümde
  dört panonun hepsi masaüstü ve mobilde `verify.js` kontrollerinin
  hepsini geçti. Önceki üç turda her turda bir ya da iki panoda ghost buton
  kontrast hatası vardı. 4 panoda 19 farklı font ailesi kullanıldı.
- README görseli son turun Masada panosuyla değiştirildi.
- **Kendini geliştirme (hafıza):** yeni `scripts/learn.py` ve
  `references/learning.md`. Skill her oturumun başında `recall` ile önceki
  panolarda kullanılan fontları ve metaforları, bu projede daha önce
  gösterilenleri, kullanıcının seçimlerini ve sözlerini, tekrar eden hataları
  ve dersleri okuyor. Oturum sırasında panoyu, seçimi, geri bildirimi ve
  bulunan hataları kaydediyor; sonda en fazla üç ders çıkarıyor. 3 kez
  tekrarlayan hata için `pitfalls.md` satırı öneriyor. Hafıza
  `~/.claude/premium-ui/` altında, plugin güncellemesinden etkilenmiyor;
  `PREMIUM_UI_MEMORY=off` ile kapanıyor. Hafıza yalnızca tekrarı önlemek
  için kullanılıyor; beğenilen görünümü yeniden üretmek için değil.
- **Hafıza eval'i:** önceki üç turun panoları hafızaya yüklenip iki ajan
  çalıştırıldı. Kargonet, altı turdur dönüp durduğu metaforlardan (otoyol
  tabelası, çeyrek saat, aktarma bandı) ilk kez çıktı: Seksen Bir İl, El
  Terminali, Kapı Numarası; 7 fontun hiçbiri önceki panolarda yoktu.
  Masada, kayıtlı "kırtasiye hissi istemiyorum, akşam servisi gibi canlı
  olsun" geri bildirimine uydu (Kordon Masası, Ocak Başı, Kuş Bakışı Sofra).
  İki pano da masaüstü ve mobilde `verify.js` kontrollerini geçti. Ajanlar
  hafızaya kendi dersini ekledi; biri mevcut dersi kopyalamak yerine
  genişletti. Ghost buton hatası ders varken yine çıktı ama görsel kontrolde
  yakalandı; `pitfalls.md` satırına `:not(.ghost)` ayrıntısı eklendi.
- **Öğrenilenleri paylaşma:** `learn.py share`, son paylaşımdan bu yana
  birikenlerden anonim bir rapor hazırlıyor: dersler, hata türü sayıları,
  kullanılan fontlar, seçilen yönlerin açık/koyu ve köşe dağılımı. Proje
  adları, yollar, URL'ler ve e-postalar maskeleniyor; kullanıcının sözleri,
  metafor adları ve kod rapora girmiyor. Skill raporu kullanıcıya gösterip
  yalnızca açık onayla gönderiyor (`gh` ile issue ya da önceden doldurulmuş
  bağlantı). Yeterince şey öğrendiğinde oturum sonunda bir kez soruyor;
  "bir daha sorma" kalıcı. Bakımcı için `tools/collect-lessons.py` açık
  `[öğrenilenler]` issue'larını toplayıp birden fazla kullanıcıdan gelen dersleri,
  `pitfalls.md`'de olmayan hata türlerini ve † işaretsiz ama sık kullanılan
  fontları listeliyor. `.github/ISSUE_TEMPLATE/ogrenilenler.md` eklendi.
- README baştan yazıldı: neden, nasıl çalışır, gereksinimler, kurulum
  (plugin, güncelleme, elle), kullanım örnekleri, hafıza.

## 1.1.0

- **Stack'e özel dosyalar:** Laravel/Livewire/Flux tarifleri ve hataları
  `references/stacks/laravel-livewire.md` dosyasına taşındı. `react-next.md`
  (React, Next.js, shadcn/ui) ve `vue-nuxt.md` (Vue, Nuxt, Inertia + Vue)
  eklendi. Skill önce stack'i tespit ediyor ve yalnızca ona uyan dosyayı okuyor.
- **`scripts/verify.js`:** tarayıcıda çalışan sayfa denetimi. Yatay taşma,
  tıklama alanı, WCAG AA kontrast, odak stili, reduced-motion, layout
  animasyonu, görsel alt/boyut, lazy hero görseli, font-display ve sayfa
  temellerini kontrol edip JSON rapor veriyor. Gerçek bir sitede denenip
  yanlış pozitiflere karşı ayarlandı: kardeş elemandan gelen arka planlar,
  gradyan/blend yazılar, üst üste binen katmanlar, etrafı boş küçük hedefler
  (WCAG 2.5.8) ve okunamayan cross-origin CSS (`unverified` durumu).
- **`assets/proposal-board.html`:** üç yönlü, çalışan öneri panosu şablonu.
- **`references/craft-baseline.md`:** tip ve boşluk ölçekleri, erişilebilirlik,
  performans bütçesi, metin (copy) kuralları, yükleniyor/boş/hata/limit durumları.
- **Tetiklenme:** description alanına skill'in hangi durumlarda
  kullanılmayacağı eklendi.
- **Pitfalls:** oturumda yeni bir hata düzeltildiğinde `pitfalls.md`'ye
  satır önerme kuralı eklendi.
- **Eval seti:** `skills/premium-ui/evals/` altında üç test senaryosu
  (`claude plugin eval` formatında, örnek bir Next.js projesiyle) ve repo
  kökündeki `evals/trigger-queries.json` içinde 20 tetiklenme sorgusu.
- **README:** örnek öneri panosu görseli (`docs/proposal-board.png`).
- **Eval'den çıkan düzeltmeler:** scroll-pinned tarifi artık
  `grid-template-rows`/`width` animasyonu önermiyor; JS ile gizlenen her durum
  `.armed` altında; butonlarda uydurma teklif ("Ücretsiz başla") yasak;
  opacity ile gizlenen durumlara `aria-hidden`; sayaç ekrandaki değerden
  devam ediyor.

## 1.0.0

- İlk sürüm: öneri panosu akışı, motion kataloğu, panel kalıpları, pitfalls,
  brief şablonu.
