"""Placement das articulacoes pelas expressoes e hierarquia gravadas no XML.
Nao executa Python do documento, nao abre nem salva o modelo.
"""
from pathlib import Path
import functools
import json
import math
import sys
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cinematica'))
from cinematica import Context


class XMLContext(Context):
    def prop(self, leaf, name):
        if (leaf,name) in self.overrides:return self.overrides[leaf,name]
        return super().prop(leaf,name)

    def attribute(self, owner, name):
        if (owner,name) in self.overrides:return self.overrides[owner,name]
        if owner in self.engine.data['sheets']:return self.cell(owner,name)
        if owner in self.engine.data['leaves']:return self.prop(owner,name)
        raise ValueError('Objeto fora do XML: '+owner+'.'+name)


class XMLPlacements:
    def __init__(self,cad):
        with zipfile.ZipFile(cad) as z:root=ET.fromstring(z.read('Document.xml'))
        self.data={'sheets':{},'controls':{},'leaves':{}};self.aliases={};self.parents={};self.placements={}
        for o in root.find('ObjectData'):
            name=o.get('name');p={x.get('name'):x for x in o.find('Properties')}
            ex=p.get('ExpressionEngine')
            expressions={} if ex is None else {x.get('path'):x.get('expression') for x in ex.iter('Expression')}
            props={}
            for n,v in p.items():
                for tag in ('Float','Integer'):
                    child=v.find(tag)
                    if child is not None:props[n]=float(child.get('value'))
            self.data['leaves'][name]={'props':props,'expressions':expressions}
            if 'Placement' in p:self.placements[name]={k:float(v) for k,v in p['Placement'][0].attrib.items()}
            if 'Group' in p:
                for child in p['Group'].iter('Link'):self.parents.setdefault(child.get('value'),[]).append(name)
            if 'cells' in p:
                cells={c.get('address'):{'content':c.get('content'),'alias':c.get('alias','')} for c in p['cells'].iter('Cell')}
                self.data['sheets'][name]=cells
                self.aliases[name]={v['alias']:a for a,v in cells.items() if v['alias']}

    def context(self,overrides):
        ctx=XMLContext(self,overrides)
        @functools.lru_cache(None)
        def local(name):
            if name not in self.placements:return np.eye(4)
            p=self.placements[name];ex=self.data['leaves'][name]['expressions']
            m=np.eye(4)
            for i,c in enumerate('xyz'):
                key='.Placement.Base.'+c
                m[i,3]=ctx.expression(ex[key],leaf=name) if key in ex else p['P'+c]
            angle='.Placement.Rotation.Angle'
            if angle in ex:
                theta=math.radians(ctx.expression(ex[angle],leaf=name));axis=np.array([p['Ox'],p['Oy'],p['Oz']])
                if np.linalg.norm(axis)<1e-12:raise ValueError('Eixo indeterminado: '+name)
                axis/=np.linalg.norm(axis);a,b,c=axis;K=np.array([[0,-c,b],[c,0,-a],[-b,a,0]])
                m[:3,:3]=np.eye(3)*math.cos(theta)+(1-math.cos(theta))*np.outer(axis,axis)+math.sin(theta)*K
            else:
                x,y,z,w=[p['Q'+str(i)] for i in range(4)]
                m[:3,:3]=[[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                           [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                           [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]]
            return m
        @functools.lru_cache(None)
        def world(name):
            parents=self.parents.get(name,[])
            if len(parents)>1:raise ValueError('Pais ambiguos: '+name+':'+','.join(parents))
            return (world(parents[0]) if parents else np.eye(4)) @ local(name)
        return world
