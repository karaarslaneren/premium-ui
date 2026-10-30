# Brief template

Ask the user only for what you cannot find in the project. Fill the rest from
the code and say what you assumed.

```text
[Proje] için [landing page | panel / dashboard | ekran] tasarla.
Ürün: [ne yaptığı, kime sattığı].

Tasarım yönü:
- Referans: [link]. Animasyon kalitesini referans al ama kopyalama; bu ürüne özgü olsun.
- Görünüm: [ör. açık editoryal, kırık beyaz zemin, italik serif vurgu kelimeleri, yuvarlak hap butonlar].

Animasyonlar ürünün kendisini anlatsın, süs olmasın:
- Hero: [ör. bir ürün pazaryerlerine dağılsın, fiyatlar count-up ile hesaplansın].
- Akış: [ör. sipariş X'ten merkeze, oradan mağazaya SVG path üzerinde paket olarak gitsin].
- Nasıl çalışır: scroll-pinned scrollytelling; bölüm sabit kalsın, adımlar yerinde kaysın.
- Fiyatlar: plan önerici (kaydırıcı → sliding highlight), yıllıkta tasarruf count-up.
- SSS: yatay scroll-snap carousel. Footer: giant wordmark reveal.
- Panel: sayfa yükseltilmiş kâğıt gibi, gerçek verili genel bakış, kurulum listesi.
- Genel: line mask reveal başlıklar, magnetic butonlar, cursor-follow glow kartlar, spring easing.

Kısıtlar:
- Stack: [ör. Laravel Blade + Tailwind v4 + Livewire + vanilla JS]. Yeni bağımlılık ekleme.
- Sadece transform/opacity animasyonu; prefers-reduced-motion'a uy; mobilde yatay taşma olmasın.
- Rakamlar ve iddialar gerçek veriden/config'den gelsin, uydurma olmasın.

Bitince tarayıcıda masaüstü ve mobilde kontrol et, ekran görüntüsüyle göster.
```

Working style that produced the best results: one section at a time, user
reacts with a screenshot + one sentence, redo only that section.
