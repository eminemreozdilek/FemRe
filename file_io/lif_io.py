from math import isclose
from pathlib import Path
from typing import Dict, List, Tuple, Union


def __calculate_compact_float_string(value: float) -> str:
    if isclose(value, 0.0, abs_tol=1e-12):
        return "0"
    if isclose(value, 1.0, abs_tol=1e-12):
        return "1"
    return f"{value:.10g}"


def __calculate_phase_scaled_string(value: float) -> str:
    if isclose(value, 0.0, abs_tol=1e-12):
        return "0"
    if isclose(value, 1.0, abs_tol=1e-12):
        return "2*pi"
    return f"({__calculate_compact_float_string(value)}*2*pi)"


def __calculate_phase_midpoint_string(a: float, b: float) -> str:
    midpoint: float = 0.5 * (a + b)
    if isclose(midpoint, 0.0, abs_tol=1e-12):
        return "0"
    if isclose(midpoint, 1.0, abs_tol=1e-12):
        return "2*pi"
    return f"({__calculate_compact_float_string(midpoint)}*2*pi)"


def __calculate_clamped_unit_interval_string(scalar_string: str) -> str:
    return f"Min(1, Max(0, {scalar_string}))"


def __calculate_dot_product_string(ax: str, ay: str, az: str, bx: str, by: str, bz: str) -> str:
    return f"(({ax})*({bx}) + ({ay})*({by}) + ({az})*({bz}))"


def __calculate_vector_addition_strings(ax: str, ay: str, az: str, bx: str, by: str, bz: str) -> Tuple[str, str, str]:
    return f"(({ax})+({bx}))", f"(({ay})+({by}))", f"(({az})+({bz}))"


def __calculate_vector_subtraction_strings(ax: str, ay: str, az: str, bx: str, by: str, bz: str) -> Tuple[str, str, str]:
    return f"(({ax})-({bx}))", f"(({ay})-({by}))", f"(({az})-({bz}))"


def __calculate_vector_scalar_multiplication_strings(scalar_string: str, vx: str, vy: str, vz: str) -> Tuple[
    str, str, str]:
    return f"(({scalar_string})*({vx}))", f"(({scalar_string})*({vy}))", f"(({scalar_string})*({vz}))"


def __calculate_vector_squared_norm_string(vx: str, vy: str, vz: str) -> str:
    return f"(({vx})*({vx}) + ({vy})*({vy}) + ({vz})*({vz}))"


def __reduce_minimum_strings(terms: List[str], group_size: int = 12) -> str:
    working_terms: List[str] = terms[:]
    if not working_terms:
        raise ValueError("No terms to reduce")
    while len(working_terms) > 1:
        next_terms: List[str] = []
        for start_index in range(0, len(working_terms), group_size):
            chunk: List[str] = working_terms[start_index:start_index + group_size]
            if len(chunk) == 1:
                next_terms.append(chunk[0])
            else:
                next_terms.append("Min(" + ",".join(chunk) + ")")
        working_terms = next_terms
    return working_terms[0]


def calculate_implicit_formula_string_from_lif(lif_path: Union[str, bytes, Path]) -> str:
    node_positions_by_id: Dict[int, Tuple[float, float, float]] = {}
    edges_with_radius: List[Tuple[int, int, float]] = []
    with open(lif_path, "r", encoding="utf-8") as file_handle:
        for raw_line in file_handle:
            line: str = raw_line.strip()
            if not line or line.startswith("//"):
                continue
            parts: List[str] = line.split()
            tag: str = parts[0].upper()
            if tag == "NODE" and len(parts) >= 5:
                _, node_id_str, x_str, y_str, z_str = parts[:5]
                node_positions_by_id[int(node_id_str)] = (float(x_str), float(y_str), float(z_str))
            elif tag == "STRUT" and len(parts) >= 6:
                _, strut_id_str, start_id_str, end_id_str, material_str, radius_str = parts[:6]
                edges_with_radius.append((int(start_id_str), int(end_id_str), float(radius_str)))
    if not node_positions_by_id or not edges_with_radius:
        raise ValueError("Empty or invalid .lif file")
    quadratics_over_radius_squared: List[str] = []
    for start_id, end_id, radius_value in edges_with_radius:
        start_x, start_y, start_z = node_positions_by_id[start_id]
        end_x, end_y, end_z = node_positions_by_id[end_id]
        start_x_string: str = __calculate_phase_scaled_string(start_x)
        start_y_string: str = __calculate_phase_scaled_string(start_y)
        start_z_string: str = __calculate_phase_scaled_string(start_z)
        end_x_string: str = __calculate_phase_scaled_string(end_x)
        end_y_string: str = __calculate_phase_scaled_string(end_y)
        end_z_string: str = __calculate_phase_scaled_string(end_z)
        midpoint_x_string: str = __calculate_phase_midpoint_string(start_x, end_x)
        midpoint_y_string: str = __calculate_phase_midpoint_string(start_y, end_y)
        midpoint_z_string: str = __calculate_phase_midpoint_string(start_z, end_z)
        shift_x_string: str = f"(2*pi*floor((x-({midpoint_x_string}))/(2*pi) + 1/2))"
        shift_y_string: str = f"(2*pi*floor((y-({midpoint_y_string}))/(2*pi) + 1/2))"
        shift_z_string: str = f"(2*pi*floor((z-({midpoint_z_string}))/(2*pi) + 1/2))"
        shifted_start_x, shifted_start_y, shifted_start_z = __calculate_vector_addition_strings(start_x_string,
                                                                                                start_y_string,
                                                                                                start_z_string,
                                                                                                shift_x_string,
                                                                                                shift_y_string,
                                                                                                shift_z_string)
        shifted_end_x, shifted_end_y, shifted_end_z = __calculate_vector_addition_strings(end_x_string, end_y_string,
                                                                                          end_z_string, shift_x_string,
                                                                                          shift_y_string, shift_z_string)
        direction_x, direction_y, direction_z = __calculate_vector_subtraction_strings(shifted_end_x, shifted_end_y,
                                                                                       shifted_end_z, shifted_start_x,
                                                                                       shifted_start_y, shifted_start_z)
        direction_norm_squared_string: str = __calculate_vector_squared_norm_string(direction_x, direction_y, direction_z)
        rx, ry, rz = "x", "y", "z"
        rx_minus_start_x, ry_minus_start_y, rz_minus_start_z = __calculate_vector_subtraction_strings(rx, ry, rz,
                                                                                                      shifted_start_x,
                                                                                                      shifted_start_y,
                                                                                                      shifted_start_z)
        numerator_string: str = __calculate_dot_product_string(rx_minus_start_x, ry_minus_start_y, rz_minus_start_z,
                                                               direction_x, direction_y, direction_z)
        parameter_t_string: str = __calculate_clamped_unit_interval_string(
            f"(({numerator_string})/({direction_norm_squared_string}))")
        t_scaled_x, t_scaled_y, t_scaled_z = __calculate_vector_scalar_multiplication_strings(parameter_t_string,
                                                                                              direction_x, direction_y,
                                                                                              direction_z)
        closest_point_x, closest_point_y, closest_point_z = __calculate_vector_addition_strings(shifted_start_x,
                                                                                                shifted_start_y,
                                                                                                shifted_start_z,
                                                                                                t_scaled_x, t_scaled_y,
                                                                                                t_scaled_z)
        dx, dy, dz = __calculate_vector_subtraction_strings(rx, ry, rz, closest_point_x, closest_point_y, closest_point_z)
        squared_distance_string: str = __calculate_vector_squared_norm_string(dx, dy, dz)
        quadratics_over_radius_squared.append(
            f"(({squared_distance_string})/({__calculate_compact_float_string(radius_value)}**2))")
    minimum_quadratic_string: str = __reduce_minimum_strings(quadratics_over_radius_squared, group_size=12)
    return f"sqrt({minimum_quadratic_string})"
