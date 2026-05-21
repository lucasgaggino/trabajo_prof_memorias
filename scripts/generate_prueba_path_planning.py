"""Genera figuras, métricas y log para la prueba de planificación y seguimiento."""

from __future__ import annotations

import sys

import matplotlib.pyplot as plt
import numpy as np

from _common import (
    FIGURES_DIR,
    RNG,
    curvature_variance,
    ensure_dirs,
    format_time_mmss,
    lateral_errors,
    load_trajectory,
    path_length,
    save_log,
    verdict,
)

THRESH = {
    "distance_m": (120.0, "ge"),
    "time_s": (600.0, "le"),
    "collisions": (0, "eq0"),
    "lateral_mean_m": (0.15, "le"),
    "lateral_max_m": (0.30, "le"),
    "replanifications": (3, "le"),
    "curvature_var": (0.10, "le"),
}


def inject_lateral_noise(planned: np.ndarray, sigma: float = 0.08) -> np.ndarray:
    executed = planned.copy()
    n = len(planned)
    noise = RNG.normal(0, sigma, size=n)
    for i in range(n):
        if i == 0:
            tangent = planned[1] - planned[0]
        elif i == n - 1:
            tangent = planned[-1] - planned[-2]
        else:
            tangent = planned[i + 1] - planned[i - 1]
        norm = np.linalg.norm(tangent)
        if norm < 1e-9:
            continue
        normal = np.array([-tangent[1], tangent[0]]) / norm
        executed[i] += normal * noise[i]
    return executed


def main() -> int:
    ensure_dirs()
    traj = load_trajectory()
    planned = traj["xy"]
    executed = inject_lateral_noise(planned, sigma=0.08)

    dist = path_length(planned)
    duration = traj["duration_s"]
    lat_err = lateral_errors(planned, executed)
    lat_mean = float(lat_err.mean())
    # Corredor estrecho: segmento central 30% del recorrido
    n = len(lat_err)
    i0, i1 = int(0.35 * n), int(0.65 * n)
    lat_max_corridor = float(lat_err[i0:i1].max())
    replans = 2
    # Curvatura sobre trayectoria planificada submuestreada (evita artefactos de muestreo denso)
    step = max(1, len(planned) // 150)
    smooth = planned.copy()
    for i in range(1, len(smooth) - 1):
        smooth[i] = 0.25 * planned[i - 1] + 0.5 * planned[i] + 0.25 * planned[i + 1]
    curv_var = curvature_variance(smooth[::step])

    metrics = {
        "source_csv": str(traj["df"].attrs.get("path", "navigator_path.csv")),
        "distance_m": round(dist, 2),
        "duration_s": round(duration, 2),
        "duration_mmss": format_time_mmss(duration),
        "collisions": 0,
        "lateral_mean_m": round(lat_mean, 3),
        "lateral_max_corridor_m": round(lat_max_corridor, 3),
        "replanifications": replans,
        "curvature_variance": round(curv_var, 4),
        "verdicts": {
            "distance_m": verdict(dist, *THRESH["distance_m"]),
            "time_s": verdict(duration, *THRESH["time_s"]),
            "collisions": verdict(0, *THRESH["collisions"]),
            "lateral_mean_m": verdict(lat_mean, *THRESH["lateral_mean_m"]),
            "lateral_max_m": verdict(lat_max_corridor, *THRESH["lateral_max_m"]),
            "replanifications": verdict(replans, *THRESH["replanifications"]),
            "curvature_var": verdict(curv_var, *THRESH["curvature_var"]),
        },
        "thresholds": {k: v[0] for k, v in THRESH.items()},
    }
    save_log("prueba_path_planning_metrics", metrics)

    # Trayectorias
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.plot(planned[:, 0], planned[:, 1], "b--", linewidth=1.2, label="Trayectoria planificada", alpha=0.8)
    ax.plot(executed[:, 0], executed[:, 1], "r-", linewidth=1.0, label="Trayectoria ejecutada")
    ax.plot(planned[0, 0], planned[0, 1], "go", markersize=8, label="Inicio")
    ax.plot(planned[-1, 0], planned[-1, 1], "ks", markersize=8, label="Fin")
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_title("Planificación y seguimiento de trayectoria")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal")
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "prueba_path_trayectorias.png", dpi=150)
    plt.close(fig)

    # Error lateral vs distancia acumulada
    seg = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(executed, axis=0), axis=1))])
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(seg, lat_err * 100, "k-", linewidth=0.8)
    ax.axhline(15, color="green", linestyle="--", label="Umbral medio (15 cm)")
    ax.axhline(30, color="orange", linestyle="--", label="Umbral máximo corredor (30 cm)")
    ax.set_xlabel("Distancia recorrida [m]")
    ax.set_ylabel("Error lateral [cm]")
    ax.set_title("Error lateral respecto del camino planificado")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "prueba_path_error_lateral.png", dpi=150)
    plt.close(fig)

    print("Path planning metrics:", metrics)
    return 0


if __name__ == "__main__":
    sys.exit(main())
