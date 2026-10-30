# Değişiklik günlüğü

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
