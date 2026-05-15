import { CircuitGrid } from '../features/circuit/components/CircuitGrid'
import { GatePalette } from '../features/circuit/components/GatePalette'
import { SimulationPanel } from '../features/circuit/components/SimulationPanel'

export function ComposerPage() {
  return (
    <main className="composer-page">
      <GatePalette />
      <CircuitGrid />
      <SimulationPanel />
    </main>
  )
}
