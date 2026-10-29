import io,unittest,zipfile
import numpy as np
from articulacoes_cinematica import XMLPlacements


class Hierarchy(unittest.TestCase):
    def model(self, expression='Controle.Abertura'):
        xml=f'''<Document><ObjectData>
        <Object name="Controle"><Properties><Property name="Abertura"><Float value="0"/></Property></Properties></Object>
        <Object name="Pai"><Properties>
        <Property name="Group"><LinkList><Link value="Filho"/></LinkList></Property>
        <Property name="Placement"><PropertyPlacement Px="10" Py="20" Pz="0" Q0="0" Q1="0" Q2="0" Q3="1" A="0" Ox="0" Oy="0" Oz="-1"/></Property>
        <Property name="ExpressionEngine"><ExpressionEngine><Expression path=".Placement.Rotation.Angle" expression="{expression}"/></ExpressionEngine></Property>
        </Properties></Object>
        <Object name="Filho"><Properties><Property name="Placement"><PropertyPlacement Px="2" Py="0" Pz="0" Q0="0" Q1="0" Q2="0" Q3="1" A="0" Ox="0" Oy="0" Oz="1"/></Property></Properties></Object>
        </ObjectData></Document>'''
        archive=io.BytesIO()
        with zipfile.ZipFile(archive,'w') as z:z.writestr('Document.xml',xml)
        archive.seek(0)
        return XMLPlacements(archive)

    def test_parent_rotation_moves_child_about_parent(self):
        m=self.model()
        np.testing.assert_allclose(m.context({})('Filho')[:3,3],[12,20,0])
        np.testing.assert_allclose(m.context({('Controle','Abertura'):90})('Filho')[:3,3],[10,18,0])

    def test_unknown_ternary_is_rejected_not_silently_frozen(self):
        with self.assertRaises(SyntaxError):self.model('Controle.Abertura == 0 ? 0 : 90').context({})('Filho')

    def test_ambiguous_parent_is_rejected(self):
        m=self.model();m.parents['Filho'].append('Controle')
        with self.assertRaises(ValueError):m.context({})('Filho')

    def test_local_property_override_drives_motion(self):
        m=self.model('Abertura')
        m.data['leaves']['Pai']['props']['Abertura']=0
        np.testing.assert_allclose(m.context({('Pai','Abertura'):90})('Filho')[:3,3],[10,18,0])


if __name__=='__main__':unittest.main()
