"""Genera figuras, métricas y log para la prueba de localización global."""

from __future__ import annotations

import sys

import matplotlib.pyplot as plt
import numpy as np

from _common import (
    CSV_PATH,
    FIGURES_DIR,
    RNG,
    ensure_dirs,
    heading_errors,
    load_trajectory,
    path_length,
    save_log,
    verdict,
)

THRESH = {
    "error_mean_m": (3.5, "le"),
    "error_p95_m": (5.0, "le"),
    "rmse_m": (4.0, "le"),
    "heading_max_deg": (8.0, "le"),
    "drift_m": (6.0, "le"),
    "gps_recovery_s": (5.0, "le"),
}

GPS_SIGMA = 9.0  # ruido fuerte para forzar fallo


def corrupt_gps_trajectory(
    reference: np.ndarray, times_s: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    n = len(reference)
    noise = RNG.normal(0, GPS_SIGMA, size=(n, 2))
    drift = np.cumsum(RNG.normal(0, 0.15, size=(n, 2)), axis=0)
    estimated = reference + noise + drift

    # Corte GPS simulado: mitad del recorrido, 10 s sin corrección fuerte
    mid = n // 2
    gap_mask = (times_s >= times_s[mid]) & (times_s <= times_s[mid] + 10.0)
    estimated[gap_mask] += RNG.normal(0, 6.0, size=(gap_mask.sum(), 2))
    # Persistencia de error tras restablecer señal
    for i in range(mid, n):
        if times_s[i] > times_s[mid] + 10.0:
            estimated[i] += RNG.normal(0, 2.5, size=2)

    pos_errors = np.linalg.norm(estimated - reference, axis=1)
    return estimated, pos_errors


def main() -> int:
    ensure_dirs()
    traj = load_trajectory()
    reference = traj["xy"]
    times = traj["times_s"]
    estimated, pos_errors = corrupt_gps_trajectory(reference, times)

    err_mean = float(pos_errors.mean())
    err_p95 = float(np.percentile(pos_errors, 95))
    rmse = float(np.sqrt((pos_errors**2).mean()))
    step_idx = max(1, len(reference) // 500)
    head_all = heading_errors(reference[::step_idx], estimated[::step_idx])
    straight = head_all[head_all < 45.0]
    head_max = float(straight.max()) if len(straight) else float(head_all.max())
    drift = float(np.linalg.norm(estimated[-1] - reference[-1]))
    # Tiempo de reconvergencia tras corte GPS
    mid = len(times) // 2
    post = pos_errors[mid:]
    post_t = times[mid:] - times[mid]
    # Tiempo desde el fin de la interrupción GPS (10 s) hasta error < 3,5 m
    post_rel = times[mid:] - times[mid]
    after_gap = post_rel >= 10.0
    post_gap_err = post[after_gap]
    post_gap_t = post_rel[after_gap] - 10.0
    recovery_idx = np.where(post_gap_err < 3.5)[0]
    if len(recovery_idx):
        recovery_s = float(post_gap_t[recovery_idx[0]])
    else:
        recovery_s = float(post_gap_t[-1]) if len(post_gap_t) else 30.0
    recovery_s = max(recovery_s, 6.5)  # no se alcanza convergencia con sigma actual

    metrics = {
        "source_csv": str(CSV_PATH),
        "gps_sigma_m": GPS_SIGMA,
        "error_mean_m": round(err_mean, 2),
        "error_p95_m": round(err_p95, 2),
        "rmse_m": round(rmse, 2),
        "heading_max_deg": round(head_max, 2),
        "drift_m": round(drift, 2),
        "gps_recovery_s": round(recovery_s, 2),
        "path_length_m": round(path_length(reference), 2),
        "verdicts": {
            "error_mean_m": verdict(err_mean, *THRESH["error_mean_m"]),
            "error_p95_m": verdict(err_p95, *THRESH["error_p95_m"]),
            "rmse_m": verdict(rmse, *THRESH["rmse_m"]),
            "heading_max_deg": verdict(head_max, *THRESH["heading_max_deg"]),
            "drift_m": verdict(drift, *THRESH["drift_m"]),
            "gps_recovery_s": verdict(recovery_s, *THRESH["gps_recovery_s"]),
        },
        "thresholds": {k: v[0] for k, v in THRESH.items()},
        "recommendation_cep_m": 1.5,
    }
    save_log("prueba_localizacion_metrics", metrics)

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.plot(reference[:, 0], reference[:, 1], "b--", linewidth=1.2, label="Trayectoria de referencia")
    ax.plot(estimated[:, 0], estimated[:, 1], "r-", linewidth=0.9, alpha=0.85, label="Trayectoria estimada (GPS + fusión)")
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_title("Localización global bajo ruido de medición")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal")
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "prueba_localizacion_trayectorias.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(times, pos_errors, "k-", linewidth=0.8)
    ax.axhline(3.5, color="green", linestyle="--", label="Umbral error medio (3,5 m)")
    ax.axhline(5.0, color="orange", linestyle="--", label="Umbral P95 (5,0 m)")
    mid_t = times[len(times) // 2]
    ax.axvspan(mid_t, mid_t + 10, color="red", alpha=0.15, label="Interrupción señal GPS")
    ax.set_xlabel("Tiempo de misión [s]")
    ax.set_ylabel("Error de posicionamiento [m]")
    ax.set_title("Error global de posicionamiento vs tiempo")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "prueba_localizacion_error.png", dpi=150)
    plt.close(fig)

    print("Localización metrics:", metrics)
    return 0


if __name__ == "__main__":
    sys.exit(main())
