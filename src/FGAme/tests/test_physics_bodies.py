from FGAme.physics.bodies import Circle, AABB, Poly, Rectangle, RegularPoly, Body
from FGAme.physics import get_collision

CLASSES = [Circle, AABB, Poly, Rectangle, RegularPoly, Body]

def test_subclasses_have_has_triggers():
    for cls in CLASSES:
        methods = dir(cls)
        assert 'trigger_pre_collision' in methods
        assert 'trigger_frame_enter' in methods
        assert 'trigger_out_of_bounds' in methods

def test_body_subclass_names():
    assert Body.__name__ == 'Body'
    assert Circle.__name__ == 'Circle'

#
# Collision tests
#
def test_circle_collision():
    c1 = Circle(10, (0, 0))
    c2 = Circle(10, (10, 10))
    c3 = Circle(10, (20, 20))
    assert get_collision(c1, c2) is not None
    assert get_collision(c2, c3) is not None
    assert get_collision(c1, c3) is None

def test_aabb_collision():
    a = AABB(0, 10, 0, 10)
    b = AABB(5, 15, 5, 15)
    c = AABB(10, 15, 11, 16)
    assert get_collision(a, b) is not None
    assert get_collision(b, c) is not None
    assert get_collision(a, c) is None

def test_poly_collision():
    a = Poly(AABB(0, 10, 0, 10).vertices)
    b = Poly(AABB(5, 15, 5, 15).vertices)
    c = Poly(AABB(10, 15, 11, 16).vertices)
    assert get_collision(a, b) is not None
    assert get_collision(b, c) is not None
    assert get_collision(a, c) is None

def test_poly_aabb_collision():
    a = AABB(0, 10, 0, 10)
    b = AABB(5, 15, 5, 15)
    c = AABB(10, 15, 11, 16)
    pa, pb, pc = [Poly(x.vertices) for x in (a, b, c)]
    assert get_collision(a, pa) is not None
    assert get_collision(a, pb) is not None
    assert get_collision(pa, b) is not None
    
    assert get_collision(b, pb) is not None
    assert get_collision(b, pc) is not None
    assert get_collision(pb, c) is not None
    
    assert get_collision(a, pa) is not None
    assert get_collision(a, pc) is None
    assert get_collision(pa, c) is None


def test_cbb_radius_is_not_null():
    assert AABB(0, 10, 0, 10).cbb_radius > 5
    assert RegularPoly(3, 10).cbb_radius > 5
    assert Rectangle(shape=(10, 20)).cbb_radius > 5
    assert Poly(AABB(0, 10, 0, 10).vertices).cbb_radius > 5
    assert Circle(10, (0, 0)).cbb_radius >= 10

if __name__ == '__main__':
    from pytest import main 
    main('test_physics_bodies.py -q')

