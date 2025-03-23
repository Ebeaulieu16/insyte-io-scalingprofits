import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

try {
  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
} catch (error) {
  console.error("Erreur lors du rendu de l'application:", error);
  
  // Afficher un message d'erreur dans le DOM
  const rootElement = document.getElementById('root');
  if (rootElement) {
    rootElement.innerHTML = `
      <div style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: 0 auto; text-align: center;">
        <h1 style="color: #e53e3e;">Erreur de chargement</h1>
        <p>Une erreur s'est produite lors du chargement de l'application.</p>
        <p>Veuillez vérifier la console pour plus de détails.</p>
        <div style="margin: 20px; padding: 10px; background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 4px; text-align: left;">
          <pre style="overflow: auto;">${error?.toString()}</pre>
        </div>
      </div>
    `;
  }
}
