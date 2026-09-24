import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    // Needed so Monocart can map V8 coverage when using production preview builds
    sourcemap: true,
  },
  server: {
    port: 5173,
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
  preview: {
    port: 5173,
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
});
