# SPDX-License-Identifier: MPL-2.0
# Copyright 2024, ASAM e.V.
# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from typing import List, Optional, Tuple

from lxml import etree
from qc_baselib import IssueSeverity

from qc_opendrive import basic_preconditions
from qc_opendrive import constants
from qc_opendrive.base import models, utils

CHECKER_ID = "check_asam_xodr_road_geometry_contact_point"
CHECKER_DESCRIPTION = "If two roads are connected without a junction, the road reference line of a new road shall always begin at the <contactPoint> element of its successor or predecessor road. The road reference lines may be directed in opposite directions."
CHECKER_PRECONDITIONS = basic_preconditions.CHECKER_PRECONDITIONS
RULE_UID = "asam.net:xodr:1.7.0:road.geometry.contact_point"


FLOAT_COMPARISON_THRESHOLD = 1e-6


def _raise_issue(
    checker_data: models.CheckerData,
    road: etree._ElementTree,
    contact_point: models.Point3D,
):
    issue_id = checker_data.result.register_issue(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        description="The road reference line does not begin at the contact point of its predecessor or successor.",
        level=IssueSeverity.ERROR,
        rule_uid=RULE_UID,
    )
    checker_data.result.add_xml_location(
        checker_bundle_name=constants.BUNDLE_NAME,
        checker_id=CHECKER_ID,
        issue_id=issue_id,
        xpath=checker_data.input_file_xml_root.getpath(road),
        description="The road reference line does not begin at the contact point of its predecessor or successor.",
    )

    if contact_point is not None:
        checker_data.result.add_inertial_location(
            checker_bundle_name=constants.BUNDLE_NAME,
            checker_id=CHECKER_ID,
            issue_id=issue_id,
            x=contact_point.x,
            y=contact_point.y,
            z=contact_point.z,
            description="The road reference line does not begin at the contact point of its predecessor or successor.",
        )


# Road ids listed in the checker summary for connections left unchecked. The
# count is always reported in full; only the list is cut short.
UNCHECKED_ROAD_IDS_SHOWN = 10


def _get_xcessor_road_and_contact_point(
    xcessor: etree._Element,
    road_id_map: dict,
) -> Optional[Tuple[etree._Element, str]]:
    """The linked road and the contact point on it, or None when the link is
    not a road-to-road connection this rule can check."""
    if xcessor.get("elementType") == "junction":
        return None

    xcessor_road = road_id_map.get(utils.to_int(xcessor.get("elementId")))
    if xcessor_road is None:
        return None

    contact_point = xcessor.get("contactPoint")
    if contact_point not in (models.ContactPoint.START, models.ContactPoint.END):
        return None

    return xcessor_road, contact_point


def _points_differ(a: models.Point3D, b: models.Point3D) -> bool:
    # allow error in the order of 1e-6 for floating point comparison of coordinates
    return any(
        abs(getattr(a, attr) - getattr(b, attr)) >= FLOAT_COMPARISON_THRESHOLD
        for attr in ("x", "y", "z")
    )


def _report_unchecked_connections(
    checker_data: models.CheckerData,
    unchecked_road_ids: List[str],
) -> None:
    if not unchecked_road_ids:
        return

    shown = ", ".join(unchecked_road_ids[:UNCHECKED_ROAD_IDS_SHOWN])
    if len(unchecked_road_ids) > UNCHECKED_ROAD_IDS_SHOWN:
        shown += ", ..."

    message = (
        f"{len(unchecked_road_ids)} road connection(s) were not checked because "
        "a road reference line could not be evaluated (e.g. unsupported "
        f"<poly3> geometry). Road id(s): {shown}."
    )
    logging.warning(message)
    checker_data.result.add_checker_summary(
        constants.BUNDLE_NAME,
        CHECKER_ID,
        message,
    )


def _check_road_geometry_contact_point(
    checker_data: models.CheckerData,
) -> None:
    roads = utils.get_roads(checker_data.input_file_xml_root)
    road_id_map = utils.get_road_id_map(checker_data.input_file_xml_root)
    unchecked_road_ids = []

    for road in roads:
        # the rule does not apply to roads that belong to a junction
        if utils.road_belongs_to_junction(road):
            continue

        road_link = road.find("link")
        # <link> is optional (minOccurs="0"); an isolated road may omit it.
        if road_link is None:
            continue

        road_start = (
            road_link.find("predecessor"),
            utils.get_start_point_xyz_from_road_reference_line,
        )
        road_end = (
            road_link.find("successor"),
            utils.get_end_point_xyz_from_road_reference_line,
        )

        for xcessor, get_road_contact_point_xyz in (road_start, road_end):
            # <predecessor> and <successor> are optional as well.
            if xcessor is None:
                continue

            xcessor_road_and_contact_point = _get_xcessor_road_and_contact_point(
                xcessor, road_id_map
            )
            if xcessor_road_and_contact_point is None:
                continue
            xcessor_road, contact_point = xcessor_road_and_contact_point

            # Reference lines are evaluated only once there is a road to compare
            # against: spiral and paramPoly3 integrate numerically, and a link to
            # a junction needs neither point.
            road_contact_point_xyz = get_road_contact_point_xyz(road)
            xcessor_contact_point_xyz = (
                utils.get_point_xyz_from_contact_point(xcessor_road, contact_point)
                if road_contact_point_xyz is not None
                else None
            )

            # A reference line that cannot be evaluated leaves the connection
            # unchecked. Record it so that it does not pass as a clean result.
            if road_contact_point_xyz is None or xcessor_contact_point_xyz is None:
                unchecked_road_ids.append(str(road.get("id")))
                continue

            if _points_differ(road_contact_point_xyz, xcessor_contact_point_xyz):
                _raise_issue(checker_data, road, xcessor_contact_point_xyz)

    _report_unchecked_connections(checker_data, unchecked_road_ids)


def check_rule(checker_data: models.CheckerData) -> None:
    """
    Rule ID: asam.net:xodr:1.7.0:road.geometry.contact_point

    Description: If two roads are connected without a junction, the road reference line of a new road shall always begin
    at the <contactPoint> element of its successor or predecessor road. The road reference lines may be directed in opposite directions.

    Severity: ERROR

    Version range: [1.7.0, )

    Remark:
        This check currently relies on the accuracy of the scipy.integrate.quad method.
        The estimated absolute error of the numerical integration is included in
        the issue description message.
    """
    logging.info("Executing road.geometry.contact_point check")
    _check_road_geometry_contact_point(checker_data)
