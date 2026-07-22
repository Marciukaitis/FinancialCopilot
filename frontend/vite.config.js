import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/health": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/status": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/upload": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/reindex": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/query": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/retrieve": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/documents": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/docs": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/openapi.json": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
