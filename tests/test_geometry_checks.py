# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import pytest

from typing import List, Optional

from lxml import etree
from qc_baselib import IssueSeverity
from qc_opendrive.checks import geometry

from test_setup import *


@pytest.mark.parametrize(
    "target_file,issue_count,issue_xpath",
    [
        (
            "valid",
            0,
            [],
        ),
        (
            "invalid",
            1,
            [
                "/OpenDRIVE/road/planView/geometry[2]",
            ],
        ),
        (
            "invalid_multiple_cases",
            3,
            [
                "/OpenDRIVE/road/planView/geometry[2]",
                "/OpenDRIVE/road/planView/geometry[3]",
                "/OpenDRIVE/road/planView/geometry[4]",
            ],
        ),
    ],
)
def test_road_geometry_param_poly3_length_match(
    target_file: str,
    issue_count: int,
    issue_xpath: List[str],
    monkeypatch,
) -> None:
    base_path = "tests/data/road_geometry_param_poly3_length_match/"
    target_file_name = f"road_geometry_param_poly3_length_match_{target_file}.xodr"
    rule_uid = "asam.net:xodr:1.7.0:road.geometry.parampoly3.length_match"
    issue_severity = IssueSeverity.WARNING

    target_file_path = os.path.join(base_path, target_file_name)
    create_test_config(target_file_path)
    launch_main(monkeypatch)
    check_issues(
        rule_uid,
        issue_count,
        issue_xpath,
        issue_severity,
        geometry.road_geometry_parampoly3_length_match.CHECKER_ID,
    )
    cleanup_files()


@pytest.mark.parametrize(
    "target_file,issue_count,issue_xpath",
    [
        (
            "valid",
            0,
            [],
        ),
        (
            "valid_1",
            0,
            [],
        ),
        (
            "invalid",
            2,
            [
                "/OpenDRIVE/road/lanes/laneSection/left/lane[1]",
                "/OpenDRIVE/road/lanes/laneSection/left/lane[2]",
                "/OpenDRIVE/road/lanes/laneSection/right/lane[1]",
                "/OpenDRIVE/road/lanes/laneSection/right/lane[2]",
            ],
        ),
        (
            "invalid_1",
            1,
            [
                "/OpenDRIVE/road/lanes/laneSection/left/lane[1]",
                "/OpenDRIVE/road/lanes/laneSection/left/lane[2]",
            ],
        ),
    ],
)
def test_road_lane_border_overlap_with_inner_lanes(
    target_file: str,
    issue_count: int,
    issue_xpath: List[str],
    monkeypatch,
) -> None:
    base_path = "tests/data/road_lane_border_overlap_with_inner_lanes/"
    target_file_name = f"road_lane_border_overlap_with_inner_lanes_{target_file}.xodr"
    rule_uid = "asam.net:xodr:1.4.0:road.lane.border.overlap_with_inner_lanes"
    issue_severity = IssueSeverity.ERROR

    target_file_path = os.path.join(base_path, target_file_name)
    create_test_config(target_file_path)
    launch_main(monkeypatch)
    check_issues(
        rule_uid,
        issue_count,
        issue_xpath,
        issue_severity,
        geometry.road_lane_border_overlap_with_inner_lanes.CHECKER_ID,
    )
    cleanup_files()


@pytest.mark.parametrize(
    "target_file,issue_count,issue_xpath",
    [
        (
            "valid",
            0,
            [],
        ),
        (
            "invalid",
            3,
            [
                "/OpenDRIVE/road/planView/geometry[3]",
                "/OpenDRIVE/road/planView/geometry[4]",
                "/OpenDRIVE/road/planView/geometry[6]",
            ],
        ),
    ],
)
def test_road_geometry_parampoly3_arclength_range(
    target_file: str,
    issue_count: int,
    issue_xpath: List[str],
    monkeypatch,
) -> None:
    base_path = "tests/data/road_geometry_parampoly3_arclength_range/"
    target_file_name = f"road_geometry_parampoly3_arclength_range_{target_file}.xodr"
    rule_uid = "asam.net:xodr:1.7.0:road.geometry.parampoly3.arclength_range"
    issue_severity = IssueSeverity.ERROR

    target_file_path = os.path.join(base_path, target_file_name)
    create_test_config(target_file_path)
    launch_main(monkeypatch)
    check_issues(
        rule_uid,
        issue_count,
        issue_xpath,
        issue_severity,
        geometry.road_geometry_parampoly3_arclength_range.CHECKER_ID,
    )
    cleanup_files()


@pytest.mark.parametrize(
    "target_file,issue_count,issue_xpath",
    [
        (
            "valid",
            0,
            [],
        ),
        (
            "invalid",
            1,
            [
                "/OpenDRIVE/road/planView/geometry[2]",
            ],
        ),
    ],
)
def test_road_geometry_param_poly3_normalized_range(
    target_file: str,
    issue_count: int,
    issue_xpath: List[str],
    monkeypatch,
) -> None:
    base_path = "tests/data/road_geometry_param_poly3_length_match/"
    target_file_name = f"road_geometry_param_poly3_length_match_{target_file}.xodr"
    rule_uid = "asam.net:xodr:1.7.0:road.geometry.parampoly3.normalized_range"
    issue_severity = IssueSeverity.ERROR

    target_file_path = os.path.join(base_path, target_file_name)
    create_test_config(target_file_path)
    launch_main(monkeypatch)
    check_issues(
        rule_uid,
        issue_count,
        issue_xpath,
        issue_severity,
        geometry.road_geometry_parampoly3_normalized_range.CHECKER_ID,
    )
    cleanup_files()


@pytest.mark.parametrize(
    "target_file,issue_count,issue_xpath",
    [
        # Examples from https://publications.pages.asam.net/standards/ASAM_OpenDRIVE/ASAM_OpenDRIVE_Specification/latest/specification/10_roads/10_03_road_linkage.html#top-86fc414c-6211-4777-b40e-466d4551d23e
        (
            "valid_1",
            0,
            [],
        ),
        (
            "valid_2",
            0,
            [],
        ),
        (
            "valid_3",
            0,
            [],
        ),
        (
            "valid_missing_link",
            0,
            [],
        ),
        (
            "valid_unevaluable_geometry",
            0,
            [],
        ),
        (
            "invalid",
            2,
            [
                "/OpenDRIVE/road[2]",
                "/OpenDRIVE/road[1]",
            ],
        ),
        (
            "invalid_2",
            1,
            [
                "/OpenDRIVE/road[1]",
            ],
        ),
    ],
)
def test_road_geometry_contact_point(
    target_file: str,
    issue_count: int,
    issue_xpath: List[str],
    monkeypatch,
) -> None:
    base_path = "tests/data/road_geometry_contact_point/"
    target_file_name = f"{target_file}.xodr"
    rule_uid = "asam.net:xodr:1.7.0:road.geometry.contact_point"
    issue_severity = IssueSeverity.ERROR

    target_file_path = os.path.join(base_path, target_file_name)
    create_test_config(target_file_path)
    launch_main(monkeypatch)
    check_issues(
        rule_uid,
        issue_count,
        issue_xpath,
        issue_severity,
        geometry.road_geometry_contact_point.CHECKER_ID,
    )
    cleanup_files()


JUNCTION_EXAMPLE = "tests/data/junctions_connection_one_link_to_incoming/Ex_Bidirectional_Junction_valid.xodr"


def _junction_example_variant(
    tmp_path, junction_id: str, extra_roads_file: Optional[str] = None
) -> str:
    """The bidirectional junction example with its junction id replaced, and
    optionally extra roads inserted before the junction, written to tmp_path."""
    tree = etree.parse(JUNCTION_EXAMPLE)
    root = tree.getroot()
    junction = root.find("junction")
    original_id = junction.get("id")

    junction.set("id", junction_id)
    for road in root.iter("road"):
        if road.get("junction") == original_id:
            road.set("junction", junction_id)
        for link in road.iter("predecessor", "successor"):
            if (
                link.get("elementType") == "junction"
                and link.get("elementId") == original_id
            ):
                link.set("elementId", junction_id)

    if extra_roads_file is not None:
        for road in etree.parse(extra_roads_file).getroot().iter("road"):
            junction.addprevious(road)

    # Every reference to the original id must have been replaced, or the variant
    # silently tests the original junction.
    assert not root.xpath(
        "//road[@junction=$id] | //*[@elementType='junction'][@elementId=$id]",
        id=original_id,
    )

    path = tmp_path / f"junction_{junction_id}.xodr"
    tree.write(str(path), xml_declaration=True, encoding="utf-8")
    return str(path)


@pytest.mark.parametrize(
    "junction_id,extra_roads_file,issue_count,issue_xpath",
    [
        # The reference line of a connecting road is laterally offset from the
        # incoming road, so the rule must not be applied to roads that belong to a
        # junction, whatever its id.
        ("7", None, 0, []),
        # A non-numeric junction id, which road@junction allows since it is an
        # xs:string.
        ("j7", None, 0, []),
        # The same junction plus a pair of directly connected roads whose
        # successor contact point is wrong: the junction roads stay skipped while
        # the road that does not belong to a junction is still reported.
        (
            "7",
            "tests/data/road_geometry_contact_point/directly_connected_roads_wrong_contact_point.xml",
            1,
            ["/OpenDRIVE/road[7]"],
        ),
    ],
)
def test_road_geometry_contact_point_junction_variants(
    junction_id: str,
    extra_roads_file: Optional[str],
    issue_count: int,
    issue_xpath: List[str],
    tmp_path,
    monkeypatch,
) -> None:
    target_file_path = _junction_example_variant(
        tmp_path, junction_id, extra_roads_file
    )
    create_test_config(target_file_path)
    launch_main(monkeypatch)
    check_issues(
        "asam.net:xodr:1.7.0:road.geometry.contact_point",
        issue_count,
        issue_xpath,
        IssueSeverity.ERROR,
        geometry.road_geometry_contact_point.CHECKER_ID,
    )
    cleanup_files()


@pytest.mark.parametrize(
    "target_file,unchecked",
    [
        ("valid_1", False),
        ("valid_missing_link", False),
        ("valid_unevaluable_geometry", True),
    ],
)
def test_road_geometry_contact_point_reports_unchecked_connections(
    target_file: str,
    unchecked: bool,
    monkeypatch,
) -> None:
    # A road whose reference line cannot be evaluated is skipped without an
    # issue, which must not read as a clean result: the summary says so.
    base_path = "tests/data/road_geometry_contact_point/"
    target_file_path = os.path.join(base_path, f"{target_file}.xodr")
    create_test_config(target_file_path)
    launch_main(monkeypatch)

    result = Result()
    result.load_from_file(REPORT_FILE_PATH)
    summary = result.get_checker_result(
        constants.BUNDLE_NAME, geometry.road_geometry_contact_point.CHECKER_ID
    ).summary
    assert ("were not checked" in summary) == unchecked
    assert (
        result.get_checker_status(geometry.road_geometry_contact_point.CHECKER_ID)
        == StatusType.COMPLETED
    )

    cleanup_files()


@pytest.mark.parametrize(
    "target_file,issue_count,issue_xpath",
    [
        (
            "valid",
            0,
            [],
        ),
        (
            "invalid",
            1,
            [
                "/OpenDRIVE/road/planView/geometry[3]",
            ],
        ),
    ],
)
def test_road_geometry_elem_asc_order(
    target_file: str,
    issue_count: int,
    issue_xpath: List[str],
    monkeypatch,
) -> None:
    base_path = "tests/data/road_geometry_elem_asc_order/"
    target_file_name = f"{target_file}.xodr"
    rule_uid = "asam.net:xodr:1.4.0:road.geometry.elem_asc_order"
    issue_severity = IssueSeverity.ERROR

    target_file_path = os.path.join(base_path, target_file_name)
    create_test_config(target_file_path)
    launch_main(monkeypatch)
    check_issues(
        rule_uid,
        issue_count,
        issue_xpath,
        issue_severity,
        geometry.road_geometry_elem_asc_order.CHECKER_ID,
    )
    cleanup_files()


@pytest.mark.parametrize(
    "target_file,issue_count,issue_xpath",
    [
        (
            "valid",
            0,
            [],
        ),
        (
            "aU_invalid",
            1,
            [
                "/OpenDRIVE/road/planView/geometry[1]/paramPoly3",
            ],
        ),
        (
            "aV_invalid",
            1,
            [
                "/OpenDRIVE/road/planView/geometry[1]/paramPoly3",
            ],
        ),
        (
            "bU_invalid",
            1,
            [
                "/OpenDRIVE/road/planView/geometry[2]/paramPoly3",
            ],
        ),
        (
            "bV_invalid",
            1,
            [
                "/OpenDRIVE/road/planView/geometry[2]/paramPoly3",
            ],
        ),
    ],
)
def test_road_geometry_parampoly3_valid_parameters(
    target_file: str,
    issue_count: int,
    issue_xpath: List[str],
    monkeypatch,
) -> None:
    base_path = "tests/data/road_geometry_parampoly3_valid_parameters/"
    target_file_name = f"{target_file}.xodr"
    rule_uid = "asam.net:xodr:1.7.0:road.geometry.paramPoly3.valid_parameters"
    issue_severity = IssueSeverity.ERROR

    target_file_path = os.path.join(base_path, target_file_name)
    create_test_config(target_file_path)
    launch_main(monkeypatch)
    check_issues(
        rule_uid,
        issue_count,
        issue_xpath,
        issue_severity,
        geometry.road_geometry_parampoly3_valid_parameters.CHECKER_ID,
    )
    cleanup_files()
