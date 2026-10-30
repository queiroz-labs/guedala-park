// esbuild já é dependência do site. Preserva nomes usados entre scripts globais.
const fs=require('node:fs'),esbuild=require('esbuild');
let html=fs.readFileSync(0,'utf8');
html=html.replace(/<script>([\s\S]*?)<\/script>/g,(_,code)=>'<script>'+esbuild.transformSync(code,{loader:'js',minifyWhitespace:true,minifyIdentifiers:false,legalComments:'none'}).code+'</script>');
process.stdout.write(html);
