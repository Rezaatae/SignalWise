import { Link } from "react-router";
import { TrendingUp, TrendingDown, Activity, ArrowRight, PlayCircle } from "lucide-react";

const mockBacktests = [
  {
    id: "1",
    name: "MA Crossover - SPY",
    date: "2026-05-20",
    return: 12.4,
    sharpe: 1.8,
    status: "success",
  }
];

export function Dashboard() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="mb-2">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome back.
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6 mb-8">
        <div className="p-6 rounded-lg border border-border bg-card">
          <h3 className="mb-4">Quick Start Strategy</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm mb-2 text-muted-foreground">Strategy Type</label>
              <select className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring">
                <option>Moving Average Crossover</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm mb-2 text-muted-foreground">Fast MA</label>
                <input
                  type="number"
                  defaultValue={10}
                  className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div>
                <label className="block text-sm mb-2 text-muted-foreground">Slow MA</label>
                <input
                  type="number"
                  defaultValue={50}
                  className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm mb-2 text-muted-foreground">Asset</label>
              <select className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring">
                <option>AAPL</option>
              </select>
            </div>

            <div>
              <label className="block text-sm mb-2 text-muted-foreground">Timeframe</label>
              <select className="w-full px-3 py-2 rounded-lg bg-input border border-border focus:outline-none focus:ring-2 focus:ring-ring">
                <option>Daily</option>
              </select>
            </div>

            <Link
              to="/app/strategy-builder"
              className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg bg-primary text-primary-foreground hover:opacity-90 transition-opacity"
            >
              <PlayCircle className="w-5 h-5" />
              Run Backtest
            </Link>
          </div>
        </div>

        <div className="space-y-6">
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 rounded-lg border border-border bg-card">
              <div className="flex items-center gap-2 text-muted-foreground text-sm mb-2">
                <TrendingUp className="w-4 h-4" />
                <span>Total Return</span>
              </div>
              <div className="text-2xl font-medium text-green-500">+24.8%</div>
            </div>

          </div>

          <div className="p-6 rounded-lg border border-border bg-card h-64">
            <h4 className="mb-4 text-sm text-muted-foreground">Portfolio Equity Curve</h4>
            <div className="h-full flex items-end gap-1 pb-8">
              {Array.from({ length: 30 }).map((_, i) => {
                const height = 40 + Math.random() * 60;
                return (
                  <div
                    key={i}
                    className="flex-1 bg-chart-1 rounded-sm opacity-70"
                    style={{ height: `${height}%` }}
                  />
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
