# Sector: women's health, OB-GYN and doctor sites

Read this when the product is a doctor's or clinic's site. It covers
kadın doğum, jinekoloji, tüp bebek, gebelik takibi, perinatoloji and
menopause, and most of it also applies to other single-doctor sites
(dermatology, plastic surgery, dentistry).

The source is a benchmark of 53 live sites made in November 2026:
- 12 Turkish OB-GYN doctors' own sites
- 11 Turkish IVF and women's-health clinics
- 12 international women's-health brands and small practices: Tia, Maven,
  Oula, Pure OBGYN, Harley Street practices and Australian obstetricians
- 7 international fertility brands: Spring, CCRM, CREATE, Bourn Hall,
  Cofertility and others
- 11 premium sites from other specialties: Function, Parsley, Fountain
  Life, Harley Street and Turkish aesthetic surgeons

Fonts and colours were read from each site's code, not guessed.

This file is a **map of the neighbours**, used for step 1 of
`direction-finding.md` ("What the neighbours look like"). It does not supply
a look. Use it to stand apart from the category and to pick content scenes
that answer the patient's real questions. Never copy a palette or face
listed here.

## 1. The category's default look (what to stand apart from)

Almost every Turkish OB-GYN site is one of these four looks:

| Look | Signs | Seen on |
| --- | --- | --- |
| **Hospital blue** | royal/navy blue + white, Roboto/Open Sans, stock "doctor with stethoscope" | Jinepol, Gen. hastane microsites, London Women's Centre |
| **Fuşya + lacivert template** | magenta #e6007e-ish accent on navy, Nunito/Quicksand, rounded cards | Bahçeci, FertiJin, Aylin Totan |
| **Elementor/RevSlider doctor theme** | auto-rotating slider, 3–4 font families, counters, WOW.js reveals, floating WhatsApp | Serdinç Özdoğan, Aşkın Evren Güler, Murat Doruk |
| **Pastel baby** | baby-pink/baby-blue, stock newborn feet, script fonts | many small sites |

The global premium tier has its own sameness. Watch for it, because "make it
premium" drifts toward it:
- a cream/sand background (#f5f1e9–#fcf4e9)
- an editorial serif for headings with an italic emphasis word (Reckless,
  Domaine, Ivar, Playfair, Argent, Butler)
- a grotesk for body text
- one warm accent: terracotta, mustard, mauve or plum

Oula, Tia, Kindbody, Pure OBGYN, Nova Fertil and Ankara Tüp Bebek all look
like this. It reads as premium, but a doctor site built this way will look
like every other "boutique clinic" by 2027. Let it shape at most one
direction on a board, and only when the product's own material leads there.

## 2. What the best-scoring sites did differently

These are content and structure patterns. They hold for any visual
direction. Ranked by how much they changed the experience:

1. **Intent cards right after the hero.** 3–4 large doors in the
   patient's own words: "Gebeyim", "Gebelik planlıyorum", "Bir şikâyetim
   var", "Menopoz". Seen on Spring, CREATE, Anatolia, Bahçeci and Tia. The
   visitor finds her path in one tap instead of reading a list of 14
   treatments.
2. **"What happens at the first visit" as 3–4 numbered steps.** Seen on
   Tia (01–04), Zeki Yılmaz, CREATE, Fountain and Gennev. This is the
   strongest answer to the anxious first-time patient. It is a natural
   **process scene** for pinned steps (`motion-engine.md`).
3. **The pregnancy timeline as data.** Seen on Cihat Şen, İrfan Tarhan and
   Bülent Berker: exams by week (6–10, 11–13 ikili test, 18–22 detaylı
   ultrason, 24–28 şeker yükleme…). It is real, explorable data, so it is
   the domain's best candidate for the "explorable real data" scene in
   `high-end.md`. A due-date calculator should feed into it.
4. **Continuity of one doctor.** "From the first exam to the 6th week after
   birth, the same doctor." Seen on Kylie Goh, and on Dr. Cinik's "who is
   really doing your surgery?". This is the single-doctor site's core
   promise and should carry the hero copy. Big platforms cannot say it.
5. **A trust strip right under the hero.** 3–4 short facts with small icons:
   years, training institution, hospital, Google rating. Seen on Bourn
   Hall, Kemal Hükmen, Oula and De Silva. Only verifiable facts belong here
   (see §4).
6. **Symptom chips.** "Adet düzensizliği", "Kasık ağrısı", "Sıcak
   basması"… Seen on Tia, Gennev and Parsley. These are the patient's words,
   not medical terms, and each links to a treatment page.
7. **Life-stage navigation.** Puberty → reproductive years → pregnancy →
   postpartum → menopause. Seen on Pecoraro's "Women's Passage" (ages
   15→65), Maven and Motherfigure. A good organising idea for a treatments
   index and a candidate **metaphor** (a line through a lifetime).
8. **Real place, not stock.** Seen on Meltem Erhan's counted clinic
   gallery, Mira's office carousel and Aygın's 360° tour. "See the room
   before you come" lowers anxiety. Gen-Art opens on a full-screen video of
   its real lab.
9. **Responsible micro-copy beside every form.** "Bağlayıcı değildir, 24
   saat içinde dönüş", "Son değerlendirme muayenede hekim tarafından
   yapılır". Seen on Ankara Tüp Bebek and FertiJin. It costs nothing and
   builds trust.
10. **A medical-review byline on articles.** "Tıbben inceleyen / son
    güncelleme", seen on Gönül Çimen and Meltem Erhan. This is an E-E-A-T
    signal and is expected on health content.

Patterns that appear in under 15% of sites, and so are distinctive when
done well:
- a callback form with only two fields (name, phone)
- a downloadable guide such as "first-trimester rehberi"
- an embedded Instagram/reels feed
- a pause/play control on moving sections (Function Health). Use it
  wherever a marquee or auto-carousel exists, as an accessibility need.

## 3. Conversion and mobile

How common each feature was across the 53 sites:

| Feature | Share of sites |
| --- | --- |
| Online booking | 74% |
| Reviews or Google rating | 58% overall, 69% among sites scoring 7+ |
| Video | 55% |
| WhatsApp | 45% |
| Sticky mobile bar or floating button | 40% |
| Working calculators | 26% |

Rules taken from this:

- **The Turkish patient's first channel is WhatsApp.** Gönül Çimen's site
  is strong but has no WhatsApp, and that was its biggest gap. Put WhatsApp
  next to booking as a first-class CTA, not as a floating afterthought.
- **The mobile bar has 3–4 actions:** Ara, WhatsApp, Online randevu, and
  optionally Yol tarifi (Bülent Berker; Epione has Call/SMS/WhatsApp). Make
  booking the widest one.
- **Booking flow.** The best one is 3 steps: pick a day and time, verify
  the phone with an OTP, come to the clinic (Gönül Çimen). Offer a
  two-field "Sizi arayalım" form as the low-commitment fallback.
- **Calculators must work on the page.** Ankara Tüp Bebek and Gönül Çimen
  show the result in place. A link to a separate page loses most people.
- **Pair two-level CTAs:** "Randevu al" (primary) with "WhatsApp'tan yaz"
  or "Beni arayın" (secondary). CCRM does this, as do Kemal Hükmen and De
  Silva.

## 4. Turkish regulation and ethics constraints (always apply)

*Sağlık Hizmetlerinde Tanıtım ve Bilgilendirme Faaliyetleri Hakkında
Yönetmelik*, TTB ethics rules and KVKK limit what a Turkish doctor's site
may say. Design and copy must stay inside them. Global sites do several of
these things freely, so **don't import them**:

- No superlatives or guarantees: "en iyi", "tek", "%98 başarı". Success
  rates may only appear as sourced, non-promissory information. Gen-Art
  does this with "garanti değildir".
- No celebrity patients, no prices, no campaigns or discounts. Global
  sites (CREATE £175, Function's Black Friday) and Turkish aesthetic
  tourism sites do these; a Turkish OB-GYN site must not.
- Testimonials are a grey zone. Link out to Google/Doktortakvimi reviews or
  show the rating; don't fabricate or curate praise as advertising. Flag
  this to the user, and never invent review text (`copy.md`).
- Baby galleries ("Bebeklerimiz", Oula's "3,000+ babies") need explicit
  KVKK consent for every photo. Propose them only with that caveat.
- Keep sensitive procedures out of the home-page shop window: kürtaj,
  kızlık zarı, genital estetik. Putting them there lowered perceived
  quality on every site that did it (Aşkın Evren Güler, Burcu Timur).

Sector content that is correct and fully allowed:
- verifiable credentials
- the hospital the doctor works at
- years of practice
- memberships such as TJOD
- medical-review dates on articles
- "bilgilendirme amaçlıdır" notes

## 5. Repeated mistakes in the category (check before shipping)

- Unfinished template residue:
  - counters showing **0** (Murat Doruk)
  - "İçerik güncelleniyor"
  - a theme colour-switcher panel left visible on the live site
  - CTAs linking to `#` (Ozan Odabaş)
  - a placeholder WhatsApp link (FertiJin)

  The `verify.js` audit and `pitfalls.md` already catch some of these;
  check the CTA hrefs by hand too.
- 3–4+ font families on one site (Özdoğan, Rivela, Aşkın Evren Güler). Use
  one display face and one text face.
- An auto-rotating hero slider. It splits the message and dates the site
  instantly. One strong real image or a short real clip is better.
- Home pages with 17+ sections and a CTA repeated 6 times (Bahçeci, Shafer,
  Cinik, CREATE). The best sites stay at 8–10 scenes.
- An SEO link-dump on the home page (İrfan Tarhan, Bülent Berker). Long
  link lists belong on index pages.
- Stale proof: a COVID section, awards that stop in 2013, an expired
  accreditation shown proudly, or inconsistent numbers on the same site
  ("28 yıl" vs "30 yıl"). Every number shown needs one source (`config`)
  and must render the same everywhere.
- No CTA in the hero. London Gynaecology and Ali Gemici have only a phone
  number in the header.

## 6. Raw material for direction-finding (OB-GYN)

These nouns come from the domain, not from neighbours' looks. Use them in
`direction-finding.md` §1.

**Obvious:**
- ultrasound screen
- pregnancy weeks
- the due date
- the baby
- the hospital

**Less obvious:**
- the gel bottle and its warmer
- the grey-green glow of the ultrasound room with the lights off
- the paper roll on the exam table
- the printed ultrasound strip that patients keep in a wallet
- the "gebelik takip kartı"
- the 40-week ruler / gestation wheel the doctor spins
- the heartbeat sound on Doppler
- the waiting-room hush
- appointments counted in weeks, not dates
- the moment the doctor turns the screen toward the patient
- the hospital bag list
- the 6-week postpartum visit that closes the story

Each of these can carry a whole system: a weekly ruler as the brand shape,
a Doppler rhythm as motion, the turned screen as the hero's reveal. The
category's neighbours use none of them. Most of them use a stock
stethoscope or newborn feet.

## 7. Notes on motion stacks in the sample

- The top tier (Function, Fountain, Maven) runs GSAP + ScrollTrigger,
  sometimes with Lenis and Lottie. The motion is restrained: fade-ups,
  pinned explainers, marquee with pause.
- The Turkish tier is mostly Elementor + Swiper/Owl/Slick + WOW.js or AOS.
- Oula's buttons fill with a circle via `clip-path` on hover and use custom
  cubic-bezier easings. It is a small, brand-fit micro-interaction worth
  knowing as a technique (`motion-catalog.md`). Don't reuse it by default.

Motion in this sector should calm the visitor, not excite her. Good fits:
- slow reveals
- a timeline that fills as she scrolls
- numbers that settle into place

Avoid shakes, bounces and fast parallax on medical content.
`prefers-reduced-motion` is mandatory.
