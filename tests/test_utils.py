# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import math
import random

import pytest
from lxml import etree
from qc_opendrive.base import models, utils


def test_get_root_without_default_namespace() -> None:
    # file containing namespace
    root = utils.get_root_without_default_namespace("tests/data/utils/namespace.xodr")
    assert type(root) == etree._ElementTree
    # file does not contain namespace
    root = utils.get_root_without_default_namespace(
        "tests/data/utils/Ex_Bidirectional_Junction.xodr"
    )
    assert type(root) == etree._ElementTree


def test_get_road_id_map() -> None:
    root = utils.get_root_without_default_namespace(
        "tests/data/utils/Ex_Bidirectional_Junction.xodr"
    )
    road_id_map = utils.get_road_id_map(root)
    assert len(road_id_map) == 6


def test_get_junction_id_map() -> None:
    root = utils.get_root_without_default_namespace(
        "tests/data/utils/Ex_Bidirectional_Junction.xodr"
    )
    junction_id_map = utils.get_junction_id_map(root)
    assert len(junction_id_map) == 1


@pytest.mark.parametrize(
    "junction,expected",
    [
        (None, False),
        ("-1", False),
        (" -1 ", False),
        ("-1.0", False),
        ("-01", False),
        ("", False),
        ("  ", False),
        ("1", True),
        ("7", True),
        ("0", True),
        ("j7", True),
    ],
)
def test_road_belongs_to_junction(junction, expected) -> None:
    road = etree.Element("road")
    if junction is not None:
        road.set("junction", junction)
    assert utils.road_belongs_to_junction(road) == expected


def test_get_point_xyz_from_road_invalid_s() -> None:
    root = utils.get_root_without_default_namespace("tests/data/utils/simple_line.xodr")

    road = utils.get_roads(root)[0]

    point = utils.get_point_xyz_from_road(road, -0.001, -10, -20)

    assert point is None

    point = utils.get_point_xyz_from_road(road, 100.001, -10, -20)

    assert point is None


@pytest.mark.parametrize(
    "file_name,s,t,h,x,y,z",
    [
        ("simple_line.xodr", 30, -10, -20, 30, -10, -20),
        ("simple_line_heading.xodr", 30, 10, 20, -10, 30, 20),
        (
            "Ex_Line-Spiral-Arc.xodr",
            0,
            0,
            0,
            -56.53979238754325,
            -34.39446366782007,
            0.0,
        ),
        (
            "Ex_Line-Spiral-Arc.xodr",
            230,
            0,
            0,
            111.21223886865663,
            94.90682833835331,
            0.0,
        ),
        (
            "Ex_Line-Spiral-Arc.xodr",
            230,
            10,
            0,
            101.26793707002476,
            95.96080259692272,
            0.0,
        ),
        (
            "Ex_Line-Spiral-Arc.xodr",
            230,
            -10,
            0,
            121.1565406672885,
            93.8528540797839,
            0.0,
        ),
        (
            "Ex_Line-Spiral-Arc.xodr",
            120,
            10,
            0,
            52.61995309748058,
            14.38548916295234,
            0.0,
        ),
        (
            "Ex_Line-Spiral-Arc.xodr",
            120,
            -10,
            0,
            60.789014235577646,
            -3.870097382596728,
            0.0,
        ),
        (
            "Ex_Line-Spiral-Arc.xodr",
            150,
            10,
            0,
            74.12961916583495,
            29.09285535716386,
            0.0,
        ),
        (
            "Ex_Line-Spiral-Arc.xodr",
            150,
            10,
            20,
            74.12961916583495,
            29.09285535716386,
            20.0,
        ),
        (
            "Ex_Line-Spiral-Arc.xodr",
            150,
            -10,
            0,
            88.45632996588242,
            15.137735950587523,
            0.0,
        ),
        ("simple_line_elevation.xodr", 0, 0, 0, 0, 0, 0),
        ("simple_line_elevation.xodr", 5, 0, 0, 5, 0, 5),
        ("simple_line_elevation.xodr", 5, 10, 0, 5, 10, 5),
        ("simple_line_elevation.xodr", 5, -10, 0, 5, -10, 5),
        ("simple_line_heading_and_elevation.xodr", 0, 5, 0, -5, 0, 0),
        ("simple_line_heading_and_elevation.xodr", 0, -5, 0, 5, 0, 0),
        ("simple_line_heading_and_elevation.xodr", 20, -5, 0, 5, 20, 20),
        ("simple_line_heading_and_elevation.xodr", 20, 5, 0, -5, 20, 20),
        (
            "Ex_Line-Spiral-Arc_elevation.xodr",
            150,
            10,
            0,
            74.12961916583495,
            29.09285535716386,
            150,
        ),
        (
            "Ex_Line-Spiral-Arc_elevation.xodr",
            150,
            -10,
            0,
            88.45632996588242,
            15.137735950587523,
            150,
        ),
        (
            "simple_line_elevation.xodr",
            0,
            0,
            10,
            0,
            0,
            10,
        ),
        (
            "simple_line_elevation.xodr",
            0,
            0,
            -10,
            0,
            0,
            -10,
        ),
        (
            "simple_line_superelevation.xodr",
            0,
            0,
            0,
            0,
            0,
            0,
        ),
        (
            "simple_line_superelevation.xodr",
            0,
            5,
            0,
            0,
            3.535534483629909,
            3.5355333282354717,
        ),
        (
            "simple_line_superelevation.xodr",
            0,
            -5,
            0,
            0,
            -3.535534483629909,
            -3.5355333282354717,
        ),
        (
            "simple_line_superelevation.xodr",
            50,
            5,
            0,
            50,
            3.535534483629909,
            3.5355333282354717,
        ),
        (
            "simple_line_superelevation.xodr",
            50,
            -5,
            0,
            50,
            -3.535534483629909,
            -3.5355333282354717,
        ),
        (
            "simple_line_superelevation.xodr",
            0,
            0,
            10,
            0.0,
            -7.0710666564709435,
            7.071068967259818,
        ),
        (
            "simple_line_heading_and_elevation_and_superelevation.xodr",
            50,
            5,
            0,
            -3.5355344833850797,
            50,
            53.5355333282354717,
        ),
        (
            "simple_line_heading_and_elevation_and_superelevation.xodr",
            50,
            -5,
            0,
            3.53553448388698,
            50,
            50 - 3.5355333282354717,
        ),
        (
            "Ex_Line-Spiral-Arc_elevation_and_superelevation.xodr",
            150,
            -5,
            0,
            83.82560356938673,
            19.64835535961951,
            150 - 3.5355333282354717,
        ),
        (
            "Ex_Line-Spiral-Arc_elevation_and_superelevation.xodr",
            150,
            5,
            0,
            78.76034556233064,
            24.58223594813187,
            153.5355333282354717,
        ),
        (
            "Ex_Line-Spiral-Arc_elevation_and_superelevation.xodr",
            150,
            5,
            10,
            83.82560191408653,
            19.648356971986246,
            160.6066022954953,
        ),
        (
            "Ex_Line-Spiral-Arc_superelevation.xodr",
            150,
            -5,
            0,
            83.82560356938673,
            19.64835535961951,
            -3.5355333282354717,
        ),
        (
            "Ex_Line-Spiral-Arc_superelevation.xodr",
            150,
            5,
            0,
            78.76034556233064,
            24.58223594813187,
            3.5355333282354717,
        ),
        (
            "Ex_Line-Spiral-Arc_superelevation.xodr",
            150,
            5,
            10,
            83.82560191408653,
            19.648356971986246,
            10.60660229549529,
        ),
    ],
)
def test_get_point_xyz_from_road(file_name, s, t, h, x, y, z) -> None:
    root = utils.get_root_without_default_namespace(f"tests/data/utils/{file_name}")

    road = utils.get_roads(root)[0]
    point = utils.get_point_xyz_from_road(road, s, t, h)

    assert point.x == pytest.approx(x, abs=1e-6)
    assert point.y == pytest.approx(y, abs=1e-6)
    assert point.z == pytest.approx(z, abs=1e-6)


# The parabola v = C * u^2 has a closed-form arc length, which gives expected
# positions independent of the numerical method under test.
PARABOLA_C = 0.01
PARABOLA_U_END = 40.0


def _parabola_arc_length(u: float) -> float:
    c = PARABOLA_C
    return (u / 2.0) * math.sqrt(1.0 + 4.0 * c * c * u * u) + math.asinh(
        2.0 * c * u
    ) / (4.0 * c)


def _parabola_u_at(s: float) -> float:
    """The u at arc length s, by bisection on the closed form."""
    low, high = 0.0, PARABOLA_U_END
    for _ in range(200):
        middle = (low + high) / 2.0
        if _parabola_arc_length(middle) < s:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


PARABOLA_LENGTH = _parabola_arc_length(PARABOLA_U_END)
PARABOLA_FRACTIONS = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]


def _parabola_param_poly3(p_range: models.ParamPoly3Range) -> models.ParamPoly3:
    # u(p) = k*p, v(p) = C*(k*p)^2 traces the same parabola for p in [0, p_end].
    p_end = 1.0 if p_range == models.ParamPoly3Range.NORMALIZED else PARABOLA_LENGTH
    k = PARABOLA_U_END / p_end
    return models.ParamPoly3(
        u=models.Poly3(a=0.0, b=k, c=0.0, d=0.0),
        v=models.Poly3(a=0.0, b=0.0, c=PARABOLA_C * k * k, d=0.0),
        range=p_range,
    )


@pytest.mark.parametrize("fraction", PARABOLA_FRACTIONS)
def test_poly3_is_evaluated_by_arc_length(fraction: float) -> None:
    s = fraction * PARABOLA_LENGTH
    u = _parabola_u_at(s)
    poly3 = models.Poly3(a=0.0, b=0.0, c=PARABOLA_C, d=0.0)

    point = utils.calculate_poly3_point(
        s=s, poly3=poly3, s0=0.0, x0=0.0, y0=0.0, heading=0.0, length=PARABOLA_LENGTH
    )
    heading = utils.calculate_poly3_heading(
        s=s, poly3=poly3, s0=0.0, heading=0.0, length=PARABOLA_LENGTH
    )

    assert point.x == pytest.approx(u, abs=1e-6)
    assert point.y == pytest.approx(PARABOLA_C * u * u, abs=1e-6)
    assert heading == pytest.approx(math.atan(2.0 * PARABOLA_C * u), abs=1e-9)


@pytest.mark.parametrize(
    "p_range", [models.ParamPoly3Range.NORMALIZED, models.ParamPoly3Range.ARC_LENGTH]
)
@pytest.mark.parametrize("fraction", PARABOLA_FRACTIONS)
def test_param_poly3_is_evaluated_by_arc_length(
    p_range: models.ParamPoly3Range, fraction: float
) -> None:
    s = fraction * PARABOLA_LENGTH
    u = _parabola_u_at(s)
    param_poly3 = _parabola_param_poly3(p_range)

    point = utils.calculate_param_poly3_point(
        s=s,
        param_poly3=param_poly3,
        s0=0.0,
        x0=0.0,
        y0=0.0,
        heading=0.0,
        length=PARABOLA_LENGTH,
    )
    heading = utils.calculate_param_poly3_heading(
        s=s, param_poly3=param_poly3, s0=0.0, heading=0.0, length=PARABOLA_LENGTH
    )

    assert point.x == pytest.approx(u, abs=1e-6)
    assert point.y == pytest.approx(PARABOLA_C * u * u, abs=1e-6)
    assert heading == pytest.approx(math.atan(2.0 * PARABOLA_C * u), abs=1e-9)


def test_param_poly3_keeps_its_ends_when_length_does_not_match() -> None:
    # @length 10 % shorter than the curve: road.geometry.parampoly3.length_match
    # reports that, but the geometry must still start and end where the
    # polynomial does, so s is mapped onto the curve proportionally.
    param_poly3 = _parabola_param_poly3(models.ParamPoly3Range.NORMALIZED)
    length = PARABOLA_LENGTH * 0.9

    start = utils.calculate_param_poly3_point(
        s=0.0,
        param_poly3=param_poly3,
        s0=0.0,
        x0=0.0,
        y0=0.0,
        heading=0.0,
        length=length,
    )
    end = utils.calculate_param_poly3_point(
        s=length,
        param_poly3=param_poly3,
        s0=0.0,
        x0=0.0,
        y0=0.0,
        heading=0.0,
        length=length,
    )

    assert (start.x, start.y) == (0.0, 0.0)
    assert end.x == pytest.approx(PARABOLA_U_END, abs=1e-9)
    assert end.y == pytest.approx(PARABOLA_C * PARABOLA_U_END**2, abs=1e-9)


def test_straight_poly3_is_a_line() -> None:
    poly3 = models.Poly3(a=0.0, b=0.0, c=0.0, d=0.0)
    for s in (0.0, 12.5, 50.0):
        point = utils.calculate_poly3_point(
            s=s, poly3=poly3, s0=0.0, x0=25.0, y0=0.0, heading=math.pi, length=50.0
        )
        line = utils.calculate_line_point(s=s, s0=0.0, x0=25.0, y0=0.0, heading=math.pi)
        assert point.x == pytest.approx(line.x, abs=1e-9)
        assert point.y == pytest.approx(line.y, abs=1e-9)


# The memoised tree exists because lxml's getpath() walks preceding siblings at
# every level, which makes reporting one issue per road quadratic in the size of
# the map. Its whole contract is to return what lxml would have returned, so the
# tests below compare it against the real getpath() rather than against expected
# strings.

TAGS = ["road", "lane", "width", "signal", "object"]
NAMESPACE = "http://example.com/vendor"


def _build_random_tree(random_generator, depth: int, parent: etree._Element) -> None:
    """Grow children under parent, with sibling counts straddling the threshold."""
    if depth == 0:
        return

    low, high = random_generator.choice(
        [
            (1, 1),  # a lone child, which libxml2 paths without an index
            (2, 5),  # comfortably under the threshold
            (30, 34),  # on both sides of it
            (40, 70),  # comfortably over
        ]
    )

    for _ in range(random_generator.randint(low, high)):
        kind = random_generator.random()
        if kind < 0.04:
            # Comments and processing instructions hold no children of their own.
            parent.append(etree.Comment("a comment"))
            continue
        if kind < 0.08:
            parent.append(etree.ProcessingInstruction("target", "value"))
            continue

        if kind < 0.12:
            child = etree.SubElement(parent, f"{{{NAMESPACE}}}extra")
        else:
            child = etree.SubElement(parent, random_generator.choice(TAGS))

        _build_random_tree(random_generator, depth - 1, child)


def _random_trees(count: int, seed: int = 20260920):
    random_generator = random.Random(seed)

    for _ in range(count):
        root = etree.Element("OpenDRIVE", nsmap={"vendor": NAMESPACE})
        _build_random_tree(random_generator, 3, root)
        yield random_generator, etree.ElementTree(root)


def test_memoised_path_tree_matches_lxml_getpath() -> None:
    total_nodes = 0

    for random_generator, tree in _random_trees(30):
        nodes = list(tree.getroot().iter())
        total_nodes += len(nodes)

        # Document order, then the same tree again to exercise the cache hits.
        memoised = utils.MemoisedPathTree(tree)
        for node in nodes + nodes:
            assert memoised.getpath(node) == tree.getpath(node)

        # A fresh wrapper visited out of order: which parents have been numbered
        # by the time an element is asked for must not change the answer.
        shuffled = list(nodes)
        random_generator.shuffle(shuffled)
        memoised = utils.MemoisedPathTree(tree)
        for node in shuffled:
            assert memoised.getpath(node) == tree.getpath(node)

    # Guard against the generator silently degenerating into empty trees.
    assert total_nodes > 10000


def test_memoised_path_tree_paths_the_root_and_namespaced_elements() -> None:
    root = etree.Element("OpenDRIVE", nsmap={"vendor": NAMESPACE})
    road = etree.SubElement(root, "road")
    etree.SubElement(road, f"{{{NAMESPACE}}}extra")
    etree.SubElement(road, f"{{{NAMESPACE}}}extra")
    road.append(etree.Comment("a comment"))
    tree = etree.ElementTree(root)

    memoised = utils.MemoisedPathTree(tree)

    for node in root.iter():
        assert memoised.getpath(node) == tree.getpath(node)

    # A namespaced element is pathed with the document's prefix, which the
    # {uri}local tag does not record, so those are left to lxml.
    assert memoised.getpath(road[0]) == "/OpenDRIVE/road/vendor:extra[1]"


def test_memoised_path_tree_caches_only_large_sibling_groups() -> None:
    root = etree.Element("OpenDRIVE")
    for _ in range(128):
        road = etree.SubElement(root, "road")
        plan_view = etree.SubElement(road, "planView")
        for _ in range(3):
            etree.SubElement(plan_view, "geometry")
    tree = etree.ElementTree(root)

    nodes = list(root.iter())
    assert len(nodes) == 641

    memoised = utils.MemoisedPathTree(tree)
    for node in nodes:
        memoised.getpath(node)

    # Only the roads earn an entry, plus the root's own path: the groups below a
    # road are small, and caching them would cost memory for nothing.
    assert memoised.cached_path_count() == 129


def test_memoised_path_tree_paths_a_subtree_from_its_own_root() -> None:
    root = etree.Element("OpenDRIVE")
    for _ in range(40):
        road = etree.SubElement(root, "road")
        etree.SubElement(road, "planView")
    subtree = etree.ElementTree(root[5])

    memoised = utils.MemoisedPathTree(subtree)

    for node in root[5].iter():
        assert memoised.getpath(node) == subtree.getpath(node)
    # lxml paths a subtree's descendants from its root as a bare /tag, while the
    # root itself keeps its path in the document.
    assert memoised.getpath(root[5]) == "/OpenDRIVE/road[6]"
    assert memoised.getpath(root[5][0]) == "/road/planView"

    compared = 0
    for random_generator, tree in _random_trees(10, seed=7):
        candidates = [
            node
            for node in tree.getroot().iter()
            if isinstance(node.tag, str) and not node.tag.startswith("{")
        ]
        for sub_root in random_generator.sample(candidates, min(15, len(candidates))):
            subtree = etree.ElementTree(sub_root)
            memoised = utils.MemoisedPathTree(subtree)
            for node in sub_root.iter():
                assert memoised.getpath(node) == subtree.getpath(node)
                compared += 1
    assert compared > 500


def test_memoised_path_tree_numbers_a_child_added_to_a_large_group() -> None:
    root = etree.Element("OpenDRIVE")
    for _ in range(40):
        etree.SubElement(root, "road")
    tree = etree.ElementTree(root)

    memoised = utils.MemoisedPathTree(tree)
    for road in root:
        memoised.getpath(road)

    appended = etree.SubElement(root, "road")
    assert memoised.getpath(appended) == tree.getpath(appended) == "/OpenDRIVE/road[41]"

    inserted = etree.Element("road")
    root.insert(0, inserted)
    assert memoised.getpath(inserted) == tree.getpath(inserted) == "/OpenDRIVE/road[1]"
    # Numbering the group again on that miss brought its other children up to date.
    assert memoised.getpath(appended) == tree.getpath(appended) == "/OpenDRIVE/road[42]"


def test_memoised_path_tree_delegates_the_rest_of_the_tree_api() -> None:
    tree = utils.get_root_without_default_namespace(
        "tests/data/utils/Ex_Bidirectional_Junction.xodr"
    )

    assert tree.getroot().tag == "OpenDRIVE"
    assert len(list(tree.iter("road"))) == 6
    assert len(tree.xpath("/OpenDRIVE/road")) == 6
    assert tree.find("header") is not None

    with pytest.raises(AttributeError):
        tree.no_such_attribute


def test_lxml_getpath_is_still_position_dependent() -> None:
    """Canary: the day this fails, MemoisedPathTree can probably be deleted.

    getpath() is costly only because it identifies an element by its position
    among its siblings, which it cannot know without walking them. If lxml ever
    returns a path that does not depend on position, there is nothing left to
    memoise.
    """
    root = etree.Element("OpenDRIVE")
    for index in range(100):
        etree.SubElement(root, "road", id=str(index))
    tree = etree.ElementTree(root)

    assert tree.getpath(root[99]) == "/OpenDRIVE/road[100]"


class _CountingTree:
    """A tree that records how often the real, costly getpath() is reached."""

    def __init__(self, tree: etree._ElementTree):
        self._tree = tree
        self.getpath_calls = 0

    def getroot(self) -> etree._Element:
        return self._tree.getroot()

    def getpath(self, element: etree._Element) -> str:
        self.getpath_calls += 1
        return self._tree.getpath(element)


def test_memoised_path_tree_never_delegates_a_small_sibling_group() -> None:
    """The threshold decides what is stored, never what is delegated.

    Handing small groups back to the real getpath() looks like a harmless
    simplification and keeps the entire quadratic: lxml has no way to ask for
    the tail of a path, so a call for a geometry deep in the document still
    walks every preceding road. Rebuilding the path level by level is the point.
    """
    root = etree.Element("OpenDRIVE")
    for _ in range(128):
        road = etree.SubElement(root, "road")
        plan_view = etree.SubElement(road, "planView")
        for _ in range(3):
            etree.SubElement(plan_view, "geometry")

    counting = _CountingTree(etree.ElementTree(root))
    memoised = utils.MemoisedPathTree(counting)

    for node in root.iter():
        memoised.getpath(node)

    # Once, for the root, whose own path has no siblings to walk.
    assert counting.getpath_calls == 1
