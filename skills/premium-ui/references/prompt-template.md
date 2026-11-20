# Brief template

Ask the user only for what you cannot find in the project. Fill the rest from
the code and say what you assumed.

```text
[Proje] için [landing page | panel / dashboard | ekran] tasarla.
Ürün: [ne yaptığı, kime sattığı].

Tasarım yönü:
- Referans: [link]. Animasyon kalitesini referans al ama kopyalama; bu ürüne özgü olsun.
- Görünüm: [varsa: marka renkleri, logo, beğenilen/beğenilmeyen siteler; yoksa "ürünün dünyasından türet"].

Animasyonlar ürünün kendisini anlatsın, süs olmasın:
- Kapsam: [tüm sayfa | panel | tek bölüm | tek bileşen ailesi, ör. "sadece inputlar"].
- Mutlaka anlatılsın: [ürünün göstermek istediğiniz 2–3 gerçeği, ör. "sipariş pazaryerinden mağazaya nasıl gidiyor"].
- Elimizde olan görseller: [fotoğraflar, logo, ürün ekran görüntüleri; yoksa "yok"].
- İstemediklerim: [ör. "footer'a dev yazı", "kart ızgarası", "koyu tema"].
- Panel: [varsa: landing ile aynı tasarım dili, gerçek verili genel bakış].
- Genel: [istenen hareket karakteri, ör. sakin / mekanik / oyuncu].

Kısıtlar:
- Stack: [ör. Laravel Blade + Tailwind v4 + Livewire + vanilla JS]. Yeni bağımlılık: [izin yok | GSAP/Lenis olabilir | 3D olabilir].
- Sadece transform/opacity animasyonu; prefers-reduced-motion'a uy; mobilde yatay taşma olmasın.
- Rakamlar ve iddialar gerçek veriden/config'den gelsin, uydurma olmasın.

Bitince tarayıcıda masaüstü ve mobilde kontrol et, ekran görüntüsüyle göster.
```

Working style that produced the best results: one section at a time, user
reacts with a screenshot + one sentence, redo only that section.
