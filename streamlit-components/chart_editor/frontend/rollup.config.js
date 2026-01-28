import typescript from '@rollup/plugin-typescript';
import terser from '@rollup/plugin-terser';

export default {
  input: 'src/index.ts',
  output: {
    file: 'dist/chart-editor.js',
    format: 'iife',
    name: 'ChartEditor',
    sourcemap: true,
    banner: '/* Chart Editor Component - TypeScript Build */'
  },
  plugins: [
    typescript({
      tsconfig: './tsconfig.json',
      outDir: 'build',
      declaration: true,
      declarationMap: true
    }),
    terser({
      compress: {
        drop_console: false,
        drop_debugger: true
      },
      format: {
        comments: /^!/,
        preamble: '/* Chart Editor v2.0.0 - TypeScript Build */'
      }
    })
  ]
};
