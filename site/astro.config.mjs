import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

export default defineConfig({
  site: 'https://dongyang26.github.io',
  base: '/awesome-radio-map-estimation',
  integrations: [react()],
});
