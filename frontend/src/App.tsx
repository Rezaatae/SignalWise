import { RouterProvider } from 'react-router';
import { router } from './routes';
import { ThemeProvider } from './theme/ThemeProvider';

export default function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="signalwise-theme">
      <RouterProvider router={router} />
    </ThemeProvider>
  );
}