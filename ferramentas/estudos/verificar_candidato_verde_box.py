"""Confere candidato externo com o inspetor vigente, sem trocar release/base/modelo."""
import argparse,ast,importlib.util,json,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidato',type=Path,required=True)
    args=parser.parse_args();candidate=args.candidato.resolve()
    if ROOT in candidate.parents:raise ValueError('O candidato deve ficar fora do repositório')
    spec=importlib.util.spec_from_file_location('verificador_modelo',ROOT/'ferramentas/verificar_modelo/verificar_modelo.py')
    v=importlib.util.module_from_spec(spec)
    # O arquivo oficial termina com main() incondicional; carrega só definições,
    # sem executar a CLI que selecionaria o vigente. Funções/regras ficam intactas.
    tree=ast.parse(Path(spec.origin).read_text(encoding='utf-8'))
    assert isinstance(tree.body[-1],ast.Expr) and isinstance(tree.body[-1].value,ast.Call) and tree.body[-1].value.func.id=='main'
    tree.body.pop();exec(compile(tree,spec.origin,'exec'),v.__dict__)
    source=ROOT/'02_Modelo_3D/Guedala_Park_R54_Berlin.FCStd'
    original={p:v.sha(p) for p in (source,v.BASE,v.RELEASE)}
    inv=json.loads(v.INVARIANTES.read_text(encoding='utf-8'))
    cases=json.loads(v.MOVIMENTOS.read_text(encoding='utf-8'))
    retrato=v.inspecionar(candidate,props=v.propriedades_pedidas(inv),movimentos=cases)
    if not retrato:raise RuntimeError(v.erros)
    retrato.update(sha256=v.sha(candidate),revisao='R55 candidata',aparencia=v.ap.ler_aparencia(candidate),schema=v.SCHEMA)
    external=candidate.parent
    (external/'Retrato_completo.json').write_text(json.dumps(retrato,ensure_ascii=False),encoding='utf-8')
    invariant_errors=v.avaliar_invariantes(retrato,inv);v.erros.extend(invariant_errors)
    dif=v.comparar(v.ler_base(),retrato,inv);collisions=v.refinar_colisoes(candidate,dif)
    assert all(v.sha(p)==sha for p,sha in original.items())
    gui='GuiDocument.xml' in zipfile.ZipFile(candidate).namelist()
    report=dict(aprovacao='PENDENTE',candidato_sha256=v.sha(candidate),gui_document_preservado=gui,
                objetos=retrato['total_objetos'],expressoes=retrato['total_expressoes'],
                cenarios=len(retrato.get('movimentos') or {}),invariantes=invariant_errors,
                invalidos=retrato['invalidos'],colisoes_novas=collisions,erros=v.erros,avisos=v.avisos,diferencas=dif)
    area=ROOT/'02_Modelo_3D'
    (area/'Verificacao_verde_box.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Candidato: verde na janela do box','', '**Aprovação: PENDENTE.** Pedido de alteração: Elias, 30/10/2026, “quero que esteja na parede da janela tbm”.',
           '', 'R54 e base permanecem vigentes e intactas. Candidato externo em `../outputs/R55_candidato/`; salvo na GUI oculta por `aplicar_verde_janela_box.FCMacro`, fechada ao fim. Nenhum FCStd/base entra no git.',
           '', 'A nova camada copia os 20 mm e o topo desenhado de 2250 mm da Peca160; não presume o teto nem a hipótese orçamentária. Recorta a abertura da Peca071 e os encontros com piso, enchimento e revestimento do fundo. Cor/material copiados; esquadria e vidro preservados.',
           '', '[Assinaturas por objeto](Preservacao_verde_box.json): volume, área, faces, vértices, caixa, centro de massa e posição global antes/depois, com hashes individuais. Dados completos ficam junto ao candidato, hash registrado. [Verificação](Verificacao_verde_box.json).',
           '', f"Inspetor completo: {report['objetos']} objetos, {report['expressoes']} expressões, {report['cenarios']} cenários. GuiDocument.xml presente: {gui}. Invariantes com erro: {len(invariant_errors)}. Colisões novas: {len(collisions)}. Erros: {len(v.erros)}.",
           '', 'A CLI oficial seleciona somente o vigente. Este estudo chama as mesmas funções `inspecionar`, `avaliar_invariantes`, `comparar` e `refinar_colisoes`, passando o candidato explicitamente. Não modifica regras nem base. Diferenças esperadas em agregados e no novo objeto ficam no JSON.',
           '', 'Reproduzir: definir LOCALAPPDATA para a instalação local e TEMP externo; executar `python -B ferramentas/estudos/verificar_candidato_verde_box.py --candidato <FCStd externo>`.',
           '', 'Integração: candidato não promovido; aprovação continua PENDENTE. Este pedido não autoriza trocar vigente ou base.']
    if v.erros:lines+=['','Pendências:']+['- '+e for e in v.erros]
    (area/'Verde_box_candidato.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:report[k] for k in ('objetos','expressoes','cenarios','invariantes','colisoes_novas','erros')},ensure_ascii=False))


if __name__=='__main__':main()
