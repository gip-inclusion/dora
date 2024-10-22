from dora.core.test_utils import make_structure, make_user

from ..models import Structure, StructurePutativeMember


def test_orphan_structures():
    assert make_structure() in Structure.objects.orphans()
    assert make_structure(user=make_user()) not in Structure.objects.orphans()

    structure = make_structure()
    structure.members.add(make_user())

    assert structure not in Structure.objects.orphans()

    structure = make_structure()
    # il n'y a pas (encore?) de lien direct pour les membres invités, comme 'members'
    StructurePutativeMember(user=make_user(), structure=structure).save()

    assert structure not in Structure.objects.orphans()
