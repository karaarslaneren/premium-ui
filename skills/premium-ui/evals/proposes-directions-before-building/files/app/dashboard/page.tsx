import { Button } from '@/components/ui/button'

export default function Dashboard() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="h-32 rounded border bg-muted" />
        <div className="h-32 rounded border bg-muted" />
        <div className="h-32 rounded border bg-muted" />
      </div>
      <Button className="mt-6">Kaydet</Button>
    </div>
  )
}
