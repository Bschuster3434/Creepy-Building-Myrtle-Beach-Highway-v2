import {defineConfig} from 'vite';
export default defineConfig({
  optimizeDeps:{esbuildOptions:{absWorkingDir:import.meta.dirname}},
  build:{rollupOptions:{output:{manualChunks:{three:['three','three/addons/loaders/GLTFLoader.js'],react:['react','react-dom/client']}}}},
});
