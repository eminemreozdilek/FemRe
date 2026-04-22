from math import isclose
from pathlib import Path
from typing import Dict, List, Tuple, Union


# === Small helpers =============================================================

def __calculate_compact_float_string(value: float) -> str:
    """Compact float formatting with special-cases for 0 and 1."""
    if isclose(value, 0.0, abs_tol=1e-12):
        return "0"
    if isclose(value, 1.0, abs_tol=1e-12):
        return "1"
    return f"{value:.10g}"


def __calculate_phase_scaled_string(value: float) -> str:
    """
    Map normalized [0,1] node coordinate into [0, 2*pi].
    Used ONLY for positions, not directions.
    """
    if isclose(value, 0.0, abs_tol=1e-12):
        return "0"
    if isclose(value, 1.0, abs_tol=1e-12):
        return "2*pi"
    return f"({__calculate_compact_float_string(value)}*2*pi)"


def __calculate_phase_midpoint_string(a: float, b: float) -> str:
    """Midpoint in normalized space, scaled into [0, 2*pi]."""
    midpoint = 0.5 * (a + b)
    if isclose(midpoint, 0.0, abs_tol=1e-12):
        return "0"
    if isclose(midpoint, 1.0, abs_tol=1e-12):
        return "2*pi"
    return f"({__calculate_compact_float_string(midpoint)}*2*pi)"


def __calculate_clamped_unit_interval_string(scalar_string: str) -> str:
    """Clamp a scalar expression into [0,1]."""
    return f"Min(1, Max(0, {scalar_string}))"


def __calculate_dot_product_string(ax: str, ay: str, az: str,
                                   bx: str, by: str, bz: str) -> str:
    return f"(({ax})*({bx}) + ({ay})*({by}) + ({az})*({bz}))"


def __calculate_vector_addition_strings(ax: str, ay: str, az: str,
                                        bx: str, by: str, bz: str) -> Tuple[str, str, str]:
    return (
        f"(({ax})+({bx}))",
        f"(({ay})+({by}))",
        f"(({az})+({bz}))",
    )


def __calculate_vector_subtraction_strings(ax: str, ay: str, az: str,
                                           bx: str, by: str, bz: str) -> Tuple[str, str, str]:
    return (
        f"(({ax})-({bx}))",
        f"(({ay})-({by}))",
        f"(({az})-({bz}))",
    )


def __calculate_vector_scalar_multiplication_strings(scalar_string: str,
                                                     vx: str, vy: str, vz: str) -> Tuple[str, str, str]:
    return (
        f"(({scalar_string})*({vx}))",
        f"(({scalar_string})*({vy}))",
        f"(({scalar_string})*({vz}))",
    )


def __calculate_vector_squared_norm_string(vx: str, vy: str, vz: str) -> str:
    return f"(({vx})*({vx}) + ({vy})*({vy}) + ({vz})*({vz}))"


def __calculate_cross_product_strings(ax: str, ay: str, az: str,
                                      bx: str, by: str, bz: str) -> Tuple[str, str, str]:
    return (
        f"(({ay})*({bz}) - ({az})*({by}))",
        f"(({az})*({bx}) - ({ax})*({bz}))",
        f"(({ax})*({by}) - ({ay})*({bx}))",
    )


def __calculate_normalized_vector_strings(vx: str, vy: str, vz: str) -> Tuple[str, str, str]:
    """Return (vx,vy,vz)/||v|| as strings."""
    norm_sq = __calculate_vector_squared_norm_string(vx, vy, vz)
    inv_norm = f"(1/sqrt({norm_sq}))"
    return (
        f"(({vx})*{inv_norm})",
        f"(({vy})*{inv_norm})",
        f"(({vz})*{inv_norm})",
    )


def __periodic_shift_strings(px: str, py: str, pz: str,
                             x: str = "x", y: str = "y", z: str = "z") -> Tuple[str, str, str]:
    """
    Given a reference point (px,py,pz) in phase-space (0..2*pi),
    return shifts that move it to the nearest periodic image around (x,y,z).
    """
    sx = f"(2*pi*floor(({x}-({px}))/(2*pi) + 1/2))"
    sy = f"(2*pi*floor(({y}-({py}))/(2*pi) + 1/2))"
    sz = f"(2*pi*floor(({z}-({pz}))/(2*pi) + 1/2))"
    return sx, sy, sz


def __reduce_minimum_strings(terms: List[str], group_size: int = 12) -> str:
    """Build a balanced Min-tree to avoid huge flat Min(...) arguments."""
    working_terms = terms[:]
    if not working_terms:
        raise ValueError("No terms to reduce")

    while len(working_terms) > 1:
        next_terms: List[str] = []
        for start in range(0, len(working_terms), group_size):
            chunk = working_terms[start:start + group_size]
            if len(chunk) == 1:
                next_terms.append(chunk[0])
            else:
                next_terms.append("Min(" + ",".join(chunk) + ")")
        working_terms = next_terms

    return working_terms[0]


# === Legacy reader (NODE/STRUT only) ===========================================

def read_lif(lif_path: Union[str, bytes, Path]) -> Tuple[
    List[Tuple[float, float, float]],
    List[Tuple[int, int, float]],
]:
    """
    Backwards-compatible helper for old code:
    parses NODE/STRUT and ignores WALL/SPHERE/CYLINDER.
    """
    nodes: List[Tuple[float, float, float]] = []
    struts: List[Tuple[int, int, float]] = []

    with open(lif_path, "r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith("//"):
                continue
            parts = line.split()
            tag = parts[0].upper()
            if tag == "NODE" and len(parts) >= 5:
                _, nid, xs, ys, zs = parts[:5]
                nodes.append((float(xs), float(ys), float(zs)))
            elif tag == "STRUT" and len(parts) >= 6:
                _, sid, sid_a, sid_b, mat, rad = parts[:6]
                struts.append((int(sid_a), int(sid_b), float(rad)))

    return nodes, struts


def calculate_implicit_formula_string_from_lif(
        lif_path: Union[str, bytes, Path],
        unit_cell_size: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> str:
    """
    Build a 2*pi-periodic implicit function f(x,y,z) from a .lif file.

    - NODE coordinates in [0,1] (unit cell in normalized space).
    - All RADIUS / INNER_RADIUS / OUTER_RADIUS are relative.
    - Distances are computed in a metric scaled by unit_cell_size so that
      physical thickness is invariant under non-cubic cell aspect ratios.
    - f(x,y,z) = sqrt( Min_i term_i ), with term_i <= 1 inside each primitive.
    """
    ux, uy, uz = unit_cell_size
    ux_s = __calculate_compact_float_string(float(ux))
    uy_s = __calculate_compact_float_string(float(uy))
    uz_s = __calculate_compact_float_string(float(uz))

    def _scale_coords(px: str, py: str, pz: str) -> Tuple[str, str, str]:
        """
        Map phase-space coordinates (0..2*pi, per-axis) into a scaled
        coordinate system where each axis is multiplied by the corresponding
        unit cell size. For a cubic cell (1,1,1) this is the identity.
        """
        return (
            f"(({ux_s})*({px}))",
            f"(({uy_s})*({py}))",
            f"(({uz_s})*({pz}))",
        )

    node_pos: Dict[int, Tuple[float, float, float]] = {}

    # STRUT: (start_id, end_id, radius)
    struts: List[Tuple[int, int, float]] = []

    # WALL: (start_id, end_id, dir_x, dir_y, dir_z, radius)
    walls: List[Tuple[int, int, float, float, float, float]] = []

    # SPHERE: (node_id, inner_radius, outer_radius)
    spheres: List[Tuple[int, float, float]] = []

    # CYLINDER: (node_id, dir_x, dir_y, dir_z, inner_radius, outer_radius)
    cylinders: List[Tuple[int, float, float, float, float, float]] = []

    # --- parse ---------------------------------------------------------------
    with open(lif_path, "r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith("//"):
                continue

            parts = line.split()
            if not parts:
                continue

            tag = parts[0].upper()

            if tag == "NODE" and len(parts) >= 5:
                _, nid, xs, ys, zs = parts[:5]
                node_pos[int(nid)] = (float(xs), float(ys), float(zs))

            elif tag == "STRUT" and len(parts) >= 6:
                # STRUT ID START_NODE END_NODE MATERIAL RADIUS
                _, sid, a, b, mat, rad = parts[:6]
                struts.append((int(a), int(b), float(rad)))

            elif tag == "WALL" and len(parts) >= 9:
                # WALL ID START_NODE END_NODE DIR_X DIR_Y DIR_Z MATERIAL RADIUS
                (
                    _,
                    wid,
                    a,
                    b,
                    dx,
                    dy,
                    dz,
                    mat,
                    rad,
                ) = parts[:9]
                walls.append((int(a), int(b), float(dx), float(dy), float(dz), float(rad)))

            elif tag == "SPHERE" and len(parts) >= 7:
                # SPHERE ID NODE MATERIAL INNER_RADIUS OUTER_RADIUS
                (
                    _,
                    sid,
                    nid,
                    mat,
                    r_in,
                    r_out,
                ) = parts[:7]
                inner = float(r_in)
                outer = float(r_out)
                if outer <= 0:
                    continue
                if inner < 0:
                    inner = 0.0
                if inner > outer:
                    inner, outer = outer, inner
                spheres.append((int(nid), inner, outer))

            elif tag == "CYLINDER" and len(parts) >= 9:
                # CYLINDER ID NODE DIR_X DIR_Y DIR_Z MATERIAL INNER_RADIUS OUTER_RADIUS
                (
                    _,
                    cid,
                    nid,
                    dx,
                    dy,
                    dz,
                    mat,
                    r_in,
                    r_out,
                ) = parts[:9]
                inner = float(r_in)
                outer = float(r_out)
                if outer <= 0:
                    continue
                if inner < 0:
                    inner = 0.0
                if inner > outer:
                    inner, outer = outer, inner
                cylinders.append(
                    (int(nid), float(dx), float(dy), float(dz), inner, outer)
                )

    if not node_pos:
        raise ValueError("Empty or invalid .lif file: no NODE records found")

    if not (struts or walls or spheres or cylinders):
        raise ValueError(
            "Empty or invalid .lif file: no STRUT, WALL, SPHERE, or CYLINDER records found"
        )

    terms: List[str] = []

    # === STRUTS: capsule between two nodes, periodic ==========================
    for a_id, b_id, rad in struts:
        if a_id not in node_pos or b_id not in node_pos:
            continue

        ax, ay, az = node_pos[a_id]
        bx, by, bz = node_pos[b_id]

        # nodes in phase-space [0, 2*pi]
        ax_s = __calculate_phase_scaled_string(ax)
        ay_s = __calculate_phase_scaled_string(ay)
        az_s = __calculate_phase_scaled_string(az)

        bx_s = __calculate_phase_scaled_string(bx)
        by_s = __calculate_phase_scaled_string(by)
        bz_s = __calculate_phase_scaled_string(bz)

        # midpoint in phase for periodic wrapping
        midx_s = __calculate_phase_midpoint_string(ax, bx)
        midy_s = __calculate_phase_midpoint_string(ay, by)
        midz_s = __calculate_phase_midpoint_string(az, bz)

        shift_x, shift_y, shift_z = __periodic_shift_strings(midx_s, midy_s, midz_s)

        sa_x, sa_y, sa_z = __calculate_vector_addition_strings(
            ax_s, ay_s, az_s, shift_x, shift_y, shift_z
        )
        sb_x, sb_y, sb_z = __calculate_vector_addition_strings(
            bx_s, by_s, bz_s, shift_x, shift_y, shift_z
        )

        # scale into physical-like coordinates
        SA_x, SA_y, SA_z = _scale_coords(sa_x, sa_y, sa_z)
        SB_x, SB_y, SB_z = _scale_coords(sb_x, sb_y, sb_z)
        RX, RY, RZ = _scale_coords("x", "y", "z")

        # direction and projection in scaled metric
        d_x, d_y, d_z = __calculate_vector_subtraction_strings(
            SB_x, SB_y, SB_z, SA_x, SA_y, SA_z
        )
        d_norm_sq = __calculate_vector_squared_norm_string(d_x, d_y, d_z)

        rxm_x, rxm_y, rxm_z = __calculate_vector_subtraction_strings(
            RX, RY, RZ, SA_x, SA_y, SA_z
        )
        num = __calculate_dot_product_string(rxm_x, rxm_y, rxm_z, d_x, d_y, d_z)
        t = __calculate_clamped_unit_interval_string(f"(({num})/({d_norm_sq}))")

        tdx, tdy, tdz = __calculate_vector_scalar_multiplication_strings(
            t, d_x, d_y, d_z
        )
        c_x, c_y, c_z = __calculate_vector_addition_strings(
            SA_x, SA_y, SA_z, tdx, tdy, tdz
        )

        dx, dy, dz = __calculate_vector_subtraction_strings(
            RX, RY, RZ, c_x, c_y, c_z
        )
        dist2 = __calculate_vector_squared_norm_string(dx, dy, dz)

        terms.append(
            f"(({dist2})/({__calculate_compact_float_string(rad)}**2))"
        )

    # === WALLS: 2D capsule between nodes, extruded along DIR =================
    for a_id, b_id, dx, dy, dz, rad in walls:
        if a_id not in node_pos or b_id not in node_pos:
            continue

        ax, ay, az = node_pos[a_id]
        bx, by, bz = node_pos[b_id]

        # node positions in phase
        ax_s = __calculate_phase_scaled_string(ax)
        ay_s = __calculate_phase_scaled_string(ay)
        az_s = __calculate_phase_scaled_string(az)

        bx_s = __calculate_phase_scaled_string(bx)
        by_s = __calculate_phase_scaled_string(by)
        bz_s = __calculate_phase_scaled_string(bz)

        # periodic shift by edge midpoint (phase)
        midx_s = __calculate_phase_midpoint_string(ax, bx)
        midy_s = __calculate_phase_midpoint_string(ay, by)
        midz_s = __calculate_phase_midpoint_string(az, bz)
        shift_x, shift_y, shift_z = __periodic_shift_strings(midx_s, midy_s, midz_s)

        sa_x, sa_y, sa_z = __calculate_vector_addition_strings(
            ax_s, ay_s, az_s, shift_x, shift_y, shift_z
        )
        sb_x, sb_y, sb_z = __calculate_vector_addition_strings(
            bx_s, by_s, bz_s, shift_x, shift_y, shift_z
        )

        # scale node positions
        SA_x, SA_y, SA_z = _scale_coords(sa_x, sa_y, sa_z)
        SB_x, SB_y, SB_z = _scale_coords(sb_x, sb_y, sb_z)
        RX, RY, RZ = _scale_coords("x", "y", "z")

        # axis direction in scaled metric (dir components scaled by unit cell)
        dx_s = __calculate_compact_float_string(dx)
        dy_s = __calculate_compact_float_string(dy)
        dz_s = __calculate_compact_float_string(dz)
        dir_x, dir_y, dir_z = _scale_coords(dx_s, dy_s, dz_s)
        u_x, u_y, u_z = __calculate_normalized_vector_strings(dir_x, dir_y, dir_z)

        # helper: orthogonal projection to plane ⟂ u in scaled coords
        def proj_to_plane(px: str, py: str, pz: str) -> Tuple[str, str, str]:
            dot = __calculate_dot_product_string(px, py, pz, u_x, u_y, u_z)
            par_x, par_y, par_z = __calculate_vector_scalar_multiplication_strings(
                dot, u_x, u_y, u_z
            )
            return __calculate_vector_subtraction_strings(px, py, pz,
                                                          par_x, par_y, par_z)

        # project start, end, and query point
        pa_x, pa_y, pa_z = proj_to_plane(SA_x, SA_y, SA_z)
        pb_x, pb_y, pb_z = proj_to_plane(SB_x, SB_y, SB_z)
        pp_x, pp_y, pp_z = proj_to_plane(RX, RY, RZ)

        # STRUT-like capsule distance in this plane
        e_x, e_y, e_z = __calculate_vector_subtraction_strings(
            pb_x, pb_y, pb_z, pa_x, pa_y, pa_z
        )
        e_norm_sq = __calculate_vector_squared_norm_string(e_x, e_y, e_z)

        r_x, r_y, r_z = __calculate_vector_subtraction_strings(
            pp_x, pp_y, pp_z, pa_x, pa_y, pa_z
        )

        num = __calculate_dot_product_string(r_x, r_y, r_z, e_x, e_y, e_z)
        t = __calculate_clamped_unit_interval_string(f"(({num})/({e_norm_sq}))")

        t_ex, t_ey, t_ez = __calculate_vector_scalar_multiplication_strings(
            t, e_x, e_y, e_z
        )
        c_x, c_y, c_z = __calculate_vector_addition_strings(
            pa_x, pa_y, pa_z, t_ex, t_ey, t_ez
        )

        d_x, d_y, d_z = __calculate_vector_subtraction_strings(
            pp_x, pp_y, pp_z, c_x, c_y, c_z
        )
        dist2 = __calculate_vector_squared_norm_string(d_x, d_y, d_z)

        terms.append(
            f"(({dist2})/({__calculate_compact_float_string(rad)}**2))"
        )

    # === SPHERES: periodic, solid or hollow shells ===========================
    for nid, inner, outer in spheres:
        if nid not in node_pos:
            continue

        cx, cy, cz = node_pos[nid]

        cx_s = __calculate_phase_scaled_string(cx)
        cy_s = __calculate_phase_scaled_string(cy)
        cz_s = __calculate_phase_scaled_string(cz)

        shift_x, shift_y, shift_z = __periodic_shift_strings(cx_s, cy_s, cz_s)
        scx, scy, scz = __calculate_vector_addition_strings(
            cx_s, cy_s, cz_s, shift_x, shift_y, shift_z
        )

        SCX, SCY, SCZ = _scale_coords(scx, scy, scz)
        RX, RY, RZ = _scale_coords("x", "y", "z")

        dx, dy, dz = __calculate_vector_subtraction_strings(
            RX, RY, RZ, SCX, SCY, SCZ
        )
        r2 = __calculate_vector_squared_norm_string(dx, dy, dz)
        r = f"sqrt({r2})"

        if inner <= 0.0:
            outer_s = __calculate_compact_float_string(outer)
            term = f"(({r2})/({outer_s}**2))"
        else:
            if isclose(inner, outer, abs_tol=1e-12):
                mid_s = __calculate_compact_float_string(outer)
                term = f"(({r2})/({mid_s}**2))"
            else:
                mid = 0.5 * (inner + outer)
                halfw = 0.5 * (outer - inner)
                mid_s = __calculate_compact_float_string(mid)
                halfw_s = __calculate_compact_float_string(halfw)
                term = f"((({r} - {mid_s})**2)/({halfw_s}**2))"

        terms.append(term)

    # === CYLINDERS: periodic, solid or hollow around DIR =====================
    for nid, dx, dy, dz, inner, outer in cylinders:
        if nid not in node_pos:
            continue

        cx, cy, cz = node_pos[nid]

        cx_s = __calculate_phase_scaled_string(cx)
        cy_s = __calculate_phase_scaled_string(cy)
        cz_s = __calculate_phase_scaled_string(cz)

        shift_x, shift_y, shift_z = __periodic_shift_strings(cx_s, cy_s, cz_s)
        scx, scy, scz = __calculate_vector_addition_strings(
            cx_s, cy_s, cz_s, shift_x, shift_y, shift_z
        )

        SCX, SCY, SCZ = _scale_coords(scx, scy, scz)
        RX, RY, RZ = _scale_coords("x", "y", "z")

        # axis direction from raw components, but scaled by unit cell size
        dx_s = __calculate_compact_float_string(dx)
        dy_s = __calculate_compact_float_string(dy)
        dz_s = __calculate_compact_float_string(dz)
        dir_x, dir_y, dir_z = _scale_coords(dx_s, dy_s, dz_s)
        ax_x, ax_y, ax_z = __calculate_normalized_vector_strings(dir_x, dir_y, dir_z)

        # vector from axis point to query (scaled coords)
        rx, ry, rz = __calculate_vector_subtraction_strings(
            RX, RY, RZ, SCX, SCY, SCZ
        )

        # projection onto axis
        t = __calculate_dot_product_string(rx, ry, rz, ax_x, ax_y, ax_z)

        # closest point on axis
        t_ax_x, t_ax_y, t_ax_z = __calculate_vector_scalar_multiplication_strings(
            t, ax_x, ax_y, ax_z
        )

        # radial vector
        rpx, rpy, rpz = __calculate_vector_subtraction_strings(
            rx, ry, rz, t_ax_x, t_ax_y, t_ax_z
        )
        rp2 = __calculate_vector_squared_norm_string(rpx, rpy, rpz)
        rp = f"sqrt({rp2})"

        if inner <= 0.0:
            outer_s = __calculate_compact_float_string(outer)
            term = f"(({rp2})/({outer_s}**2))"
        else:
            if isclose(inner, outer, abs_tol=1e-12):
                mid_s = __calculate_compact_float_string(outer)
                term = f"(({rp2})/({mid_s}**2))"
            else:
                mid = 0.5 * (inner + outer)
                halfw = 0.5 * (outer - inner)
                mid_s = __calculate_compact_float_string(mid)
                halfw_s = __calculate_compact_float_string(halfw)
                term = f"((({rp} - {mid_s})**2)/({halfw_s}**2))"

        terms.append(term)

    if not terms:
        raise ValueError("No valid geometry found in .lif file")

    min_term = __reduce_minimum_strings(terms, group_size=12)
    return f"sqrt({min_term})"
