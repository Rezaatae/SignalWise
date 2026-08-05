import { Link } from "react-router";
import { TrendingUp, Moon, Sun } from "lucide-react";
import { useTheme } from "../theme/ThemeProvider";

export function LandingPage() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="min-h-screen bg-background text-foreground">
      <nav className="border-b border-border">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-6 h-6" />
            <span className="font-medium text-lg">SignalWise</span>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              className="p-2 rounded-lg hover:bg-accent transition-colors"
            >
              {theme === "dark" ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            <Link
              to="/app"
              className="px-4 py-2 rounded-lg bg-primary text-primary-foreground hover:opacity-90 transition-opacity"
            >
              Start Backtesting
            </Link>
          </div>
        </div>
      </nav>

      <footer className="border-t border-border mt-24">
        <div className="max-w-6xl mx-auto px-6 py-12 text-center text-muted-foreground">
          <p>© 2026 SignalWise.</p>
        </div>
      </footer>
    </div>
  );
}
