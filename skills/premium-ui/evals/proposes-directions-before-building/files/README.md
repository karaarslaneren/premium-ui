# Kargonet

Küçük e-ticaret satıcıları için kargo takibi. Satıcı Trendyol / Hepsiburada
mağazasını bağlar; Kargonet siparişlerin kargo kodlarını kargo firmalarından
(Yurtiçi, Aras, MNG) 15 dakikada bir çeker, gecikenleri işaretler ve müşteriye
SMS ile "kargonuz yolda" bildirimi gönderir.

- Next.js 14 (App Router), Tailwind v3, shadcn/ui
- Planlar ve limitler: `config/plans.ts`
- Senkron aralığı: `config/sync.ts`
