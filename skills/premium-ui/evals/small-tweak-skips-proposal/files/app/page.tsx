import { Button } from '@/components/ui/button'
import { plans } from '@/config/plans'

export default function Home() {
  return (
    <main className="mx-auto max-w-4xl p-8">
      <h1 className="text-3xl font-bold">Kargonet</h1>
      <p className="mt-2 text-muted-foreground">Kargo takibi.</p>
      <Button className="mt-4">Get started</Button>
      <section className="mt-12 grid grid-cols-3 gap-4">
        {plans.map((p) => (
          <div key={p.id} className="rounded border p-4">
            <h2 className="font-semibold">{p.name}</h2>
            <p>{p.monthlyPrice} TL / ay</p>
          </div>
        ))}
      </section>
    </main>
  )
}
