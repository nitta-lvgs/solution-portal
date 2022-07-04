import { defineConfig } from 'vite'
import laravel from 'vite-plugin-laravel'
import reactRefresh from '@vitejs/plugin-react-refresh';

export default defineConfig({
    plugins: [
        laravel(),
        reactRefresh()
    ],
})
