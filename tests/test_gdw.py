from typing import Any
from typing import Optional
from typing import Tuple

import pytest

import gdw.gdw as gdw


@pytest.mark.parametrize(
    "item",
    [
        # wrong value
        "hello",
        # wrong type
        {"a": 3},
        (1,),
        # not a single item
        ("a", 1),
        (-3, "a"),
    ],
)
def test_Wafer_invalid_x_offset_raises_typeerror(item: Any) -> None:
    wafer = gdw.Wafer((1, 1), (0, 0))
    with pytest.raises(TypeError):
        wafer.x_offset = item  # type: ignore[assignment]


@pytest.mark.parametrize(
    "item",
    [
        # wrong value
        "hello",
        # wrong type
        {"a": 3},
        (1,),
        # not a single item
        ("a", 1),
        (-3, "a"),
    ],
)
def test_Wafer_invalid_y_offset_raises_typeerror(item: Any) -> None:
    wafer = gdw.Wafer((1, 1), (0, 0))
    with pytest.raises(TypeError):
        wafer.y_offset = item  # type: ignore[assignment]


@pytest.mark.parametrize(
    "item",
    [
        # not lists or tuples
        "hello",
        123,
        # correct length, but mixed or invalid entries
        ("a", 1),
        (-3, "a"),
        # incorrect length
        ("even", "even", "even"),
        (1, 2, 3, 4),
        (1,),
    ],
)
def test_Wafer_invalid_center_offset_raises_typeerror(item: Any) -> None:
    wafer = gdw.Wafer((1, 1), (0, 0))
    with pytest.raises(TypeError):
        wafer.center_offset = item  # type: ignore[assignment]


def test_Die_cant_add_attribute() -> None:
    die = gdw.Die(1, 1, 1, 1, gdw.DieState.FLAT)
    with pytest.raises(AttributeError):
        die.new_attribute = 1  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "center_coord, box_size, want",
    [
        # fmt: off
        # center coord,  box size,       expected value
        ((0, 0),        (2, 2),          2),
        ((0, 0),        (6, 8),          25),
        ((0, 0),        (2, 36),         325),
        ((0, 0),        (0, 0),          0),
        ((0.5, 0.5),    (1, 1),          2),
        ((0, 0),        (3.14, 2.718),   4.311781),
        ((0, -10),      (3.14, 2.718),   131.491781),
        ((-10, 0),      (3.14, 2.718),   135.711781),
        ((-10, -10),    (3.14, 2.718),   262.891781),
        ((0, 10),       (3.14, 2.718),   131.491781),
        ((10, 0),       (3.14, 2.718),   135.711781),
        ((10, 10),      (3.14, 2.718),   262.891781),
        ((100000, 100000), (2, 2),       20000400002),
        ((1000, 0),     (100, 0.00001),  1102500),
        # fmt: on
    ],
)
def test_max_dist_squared_known_values(
    center_coord: Tuple[float, float], box_size: Tuple[float, float], want: float
) -> None:
    got = gdw.max_dist_sqrd(center_coord, box_size)
    assert got == pytest.approx(want)


@pytest.mark.parametrize(
    "diameter, want",
    [
        (50, -23.7056196),
        (75, -35.8164473),
        (100, -47.2857008),
        (125, -58.7765897),
        (150, -69.2707550),
        (35, -17.5),
        (120, -60),
        (237.68, -118.84),
    ],
)
def test_flat_location_known_values(diameter: float, want: float) -> None:
    got = gdw.flat_location(diameter)
    assert got == pytest.approx(want)


def test_flat_location_invalid_input_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        gdw.flat_location("hello")  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "test_name, die_xy, diameter, offset_xy, excl, scribe_excl, want",
    [
        # fmt: off
        # name,     die_xy,      dia, offset_xy,      excl, scribe_excl, expected
        ("ints",    (5, 5),       150, ('even', 'even'), 5,     5,       546),
        ("floats",  (5.0, 5.0),   150, ('even', 'even'), 5,     5,       546),
        ("t01",     (3.34, 3.16), 100, ('even', 'even'), 5,     5,       548),
        ("t02-1",   (2.43, 3.30), 150, ('even', 'odd'),  5,     4.5,     1814),
        ("t02-2",   (2.43, 3.30), 150, ('even', 'even'), 5,     4.5,     1794),
        ("t02-3",   (2.43, 3.30), 150, ('odd', 'odd'),   5,     4.5,     1800),
        ("t02-4",   (2.43, 3.30), 150, ('odd', 'even'),  5,     4.5,     1804),
        ("t03",     (4.34, 6.44), 150, ('even', 'even'), 5,     5,       484),
        ("t04",     (1, 1),       150, ('even', 'even'), 5,     5,       14902),
        ("t05",     (1, 1),       200, ('odd', 'even'),  5,     15,      27435),
        ("t06",     (2.9, 3.3),   150, (-1.65, 2.95),    4.5,   4.5,     1529),
        ("t07",     (2.69, 1.65), 150, (1.345, 2.1),     4.5,   4.5,     3346),
        ("t08",     (4.4, 5.02),  150, (0, -0.2),        4.5,   4.5,     648),
        # fmt: on
    ],
)
def test_gdw_known_values(
    test_name: str,
    die_xy: Tuple[float, float],
    diameter: float,
    offset_xy: Tuple[gdw.OFFSET_TYPE, gdw.OFFSET_TYPE],
    excl: float,
    scribe_excl: float,
    want: int,
) -> None:
    gdw_list = gdw.gdw(die_xy, diameter, offset_xy, excl, scribe_excl)
    # count only die that are probed
    got = sum(1 for x in gdw_list[0] if x[4] == gdw.DieState.PROBE)
    assert got == want


def test_max_gdw() -> None:
    die_size = (5, 4)
    diameter = 150
    excl = 3.5
    flat_excl = 5
    north_limit = None

    want_gross_die = 730
    want_grid_center = (30.5, 38.0)

    got_probe_list, got_grid_center = gdw.maxGDW(
        die_size, diameter, excl, flat_excl, north_limit
    )
    got_gross_die = sum(1 for x in got_probe_list if x.state == gdw.DieState.PROBE)
    assert got_gross_die == want_gross_die
    assert got_grid_center == want_grid_center


@pytest.mark.skip(reason="tested function not completed yet")
def test_die_to_radius_known_values() -> None:
    pass


@pytest.mark.parametrize(
    "wafer, diex, diey, northlim, want",
    [
        # note that the die X and die Y values are unadjusted for starting die!
        (
            gdw.Wafer((5, 5), (0, 0), 150, 4.5, 4.5, 70.2),
            21,
            17,
            None,
            gdw.DieState.WAFER,
        ),
        (
            gdw.Wafer((5, 5), (0, 0), 150, 4.5, 4.5, 70.2),
            30,
            30,
            None,
            gdw.DieState.PROBE,
        ),
        (
            gdw.Wafer((5, 5), (0, 0), 150, 4.5, 4.5, 70.2),
            28,
            43,
            None,
            gdw.DieState.FLAT_EXCLUSION,
        ),
        (
            gdw.Wafer((5, 5), (0, 0), 150, 4.5, 4.5, 70.2),
            31,
            44,
            None,
            gdw.DieState.FLAT,
        ),
        (
            gdw.Wafer((5, 5), (0, 0), 150, 4.5, 4.5, 70.2),
            40,
            21,
            None,
            gdw.DieState.EXCLUSION,
        ),
    ],
)
def test_calc_die_state_known_values(
    wafer: gdw.Wafer,
    diex: int,
    diey: int,
    northlim: Optional[float],
    want: gdw.DieState,
) -> None:
    got = gdw.calc_die_state(wafer, diex, diey, northlim)
    assert got[-1] == want


@pytest.mark.parametrize(
    "state, want",
    [
        (gdw.DieState.EXCLUSION, 3),
        (gdw.DieState.FLAT, 2),
        (gdw.DieState.SCRIBE, 1),
    ],
)
def test_count_by_state(state: gdw.DieState, want: int) -> None:
    data = [
        gdw.Die(1, 1, 1, 1, gdw.DieState.PROBE),
        gdw.Die(1, 1, 1, 1, gdw.DieState.EXCLUSION),
        gdw.Die(1, 1, 1, 1, gdw.DieState.EXCLUSION),
        gdw.Die(1, 1, 1, 1, gdw.DieState.EXCLUSION),
        gdw.Die(1, 1, 1, 1, gdw.DieState.FLAT),
        gdw.Die(1, 1, 1, 1, gdw.DieState.FLAT),
        gdw.Die(1, 1, 1, 1, gdw.DieState.SCRIBE),
        gdw.Die(1, 1, 1, 1, gdw.DieState.WAFER),
    ]
    got = gdw.count_by_state(data, state)
    assert got == want
