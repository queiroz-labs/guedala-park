// Extract the existing scene without changing the website or running its UI.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const here = __dirname;
const src = path.join(here, '..', '..', 'Estudo_interativo', 'src');
const data = fs.readFileSync(path.join(src, 'data.js'), 'utf8');
const app = fs.readFileSync(path.join(src, 'app.js'), 'utf8').split('// Mesh generation:')[0];
const ctx = vm.createContext({matchMedia: () => ({matches: true})});
vm.runInContext(data + '\n' + app + '\nstate.walls=true; state.inside=false; globalThis.exported={project:PROJECT,items:ITEMS,nodes:buildScene()};', ctx);
const out = JSON.parse(JSON.stringify(ctx.exported));
out.exportDate = '2026-10-13';
out.note = 'Base gráfica R09. Decisões posteriores são aplicadas por gerar_modelo.py. Coordenadas fonte em cm: x e z em planta, y vertical.';
fs.writeFileSync(path.join(here, 'Base_interativa.json'), JSON.stringify(out, null, 2));
console.log(JSON.stringify({nodes: out.nodes.length, items: out.items.length}));
