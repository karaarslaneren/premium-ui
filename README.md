# premium-ui

Claude Code için bir skill: **premium, ürüne özgü arayüzler** ve ürünü anlatan
animasyonlar. Hem tanıtım sayfaları hem de uygulama panelleri, dashboard'lar ve
yönetim ekranları için.

Bir projede çalıştırınca hemen kod yazmaz:

1. **Projeyi inceler.** Ürünün ne yaptığına, mevcut ekranlara, bileşen
   kütüphanesine, gerçek rakamlara (fiyat, limit, zamanlama) ve zayıf noktalara bakar.
2. **Öneri panosu hazırlar.** 2–3 farklı tasarım yönünü canlı mini tasarımlar
   olarak tek sayfada gösterir: renk paleti, fontlar, örnek giriş bölümü ve
   örnek panel kartı, üzerinde çalışan imza animasyonu.
3. **Projeye özel iyileştirmeler listeler.** "Dashboard yer tutucu kutulardan
   oluşuyor → gerçek verili genel bakış" gibi somut öneriler.
4. **Seçtiğiniz yönü uygular** ve her bölümü tarayıcıda masaüstü ve mobilde kontrol eder.

## Kurulum

Claude Code'da:

```text
/plugin marketplace add karaarslaneren/premium-ui
/plugin install premium-ui@premium-ui
```

Ya da terminalde:

```bash
claude plugin marketplace add karaarslaneren/premium-ui
```

```bash
claude plugin install premium-ui@premium-ui
```

Güncelleme:

```bash
claude plugin update premium-ui@premium-ui
```

## Kullanım

Doğrudan çağırın:

```text
/premium-ui Bu projenin tanıtım sayfasını ve panelini yeniden tasarla.
```

Ya da sadece isteğinizi yazın. "Premium", "profesyonel", "animasyonlu",
"bu tarzda yap" gibi ifadeler veya bir referans site linki skill'i kendiliğinden
devreye sokar.

İsterseniz ayrıntılı bir brief verin:
[`skills/premium-ui/references/prompt-template.md`](skills/premium-ui/references/prompt-template.md).

## İçerik

| Dosya | Ne anlatır |
| --- | --- |
| [`SKILL.md`](skills/premium-ui/SKILL.md) | Çalışma yöntemi: önce öneri, ürün gerçekleri, token'lar, bölüm bölüm ilerleme, tarayıcıda doğrulama |
| [`proposal-board.md`](skills/premium-ui/references/proposal-board.md) | Tasarım yönlerini canlı mini tasarımlarla önerme |
| [`motion-catalog.md`](skills/premium-ui/references/motion-catalog.md) | Animasyon teknikleri ve hazır kodları: scroll reveal, line mask, count-up, SVG akış, sabitlenen bölüm (scroll-pinned), magnetic buton, glow kart, plan önerici, carousel, footer yazısı |
| [`panel-patterns.md`](skills/premium-ui/references/panel-patterns.md) | Panel çerçevesi, bileşen kütüphanesini merkezden temalama, gerçek verili dashboard, giriş ekranları, dil ayarları |
| [`pitfalls.md`](skills/premium-ui/references/pitfalls.md) | Gerçekte yaşanmış hatalar ve çözümleri |
| [`prompt-template.md`](skills/premium-ui/references/prompt-template.md) | Doldurulacak istek şablonu |

## İlkeler

- Animasyonlar süs değil, ürünün ne yaptığını anlatır.
- Referans site kopyalanmaz; sadece kalitesi örnek alınır.
- Rakamlar ve iddialar gerçek veriden gelir, uydurulmaz.
- Yalnızca transform/opacity animasyonu, `prefers-reduced-motion` desteği, mobilde yatay taşma yok.
- Her değişiklik tarayıcıda gerçek etkileşimle kontrol edilir.
