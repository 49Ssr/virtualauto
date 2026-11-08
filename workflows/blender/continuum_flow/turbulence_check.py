# SPDX-License-Identifier: GPL-3.0-or-later
"""GPU checks for vector turbulence, including its analytic noise derivatives."""

from pathlib import Path

SAMPLE_KERNEL = r"""
__kernel void sample_force(__global const float4 *points,
                           __global const float *config,
                           __global float4 *result) {
    const int i = get_global_id(0);
    const float4 p = points[i];
    float x, y, z;
    apply_turbulence_forces(config, 1, 0, 0, 0, 1.0f,
                            p.x, p.y, p.z, &x, &y, &z);
    result[i] = (float4)(x, y, z, 0.0f);
}
"""

GRADIENT_KERNEL = r"""
__kernel void sample_gradient(__global const float4 *points,
                              __global float4 *result) {
    const int i = get_global_id(0);
    const float3 p = points[i].xyz;
    const float3 g = gradient_noise_gradient(p, 7, 0.65f);
    const float value = gradient_noise_3d(p.x, p.y, p.z, 7, 0.65f);
    result[i] = (float4)(g.x, g.y, g.z, value);
}
"""


def run(work: Path, context, queue):
    import numpy as np
    import pyopencl as cl

    flags = cl.mem_flags
    points = np.zeros((512, 4), dtype=np.float32)
    points[:, :3] = np.random.default_rng(73).uniform(-1.3, 1.3, (512, 3))
    epsilon = 0.001

    def evaluate(kernel, positions, amplitude=2.5, phase=1.0, seed=7):
        positions = np.ascontiguousarray(positions)
        inputs = cl.Buffer(
            context, flags.READ_ONLY | flags.COPY_HOST_PTR, hostbuf=positions
        )
        config = np.array([amplitude, 0.65, seed, phase], dtype=np.float32)
        config_buffer = cl.Buffer(
            context, flags.READ_ONLY | flags.COPY_HOST_PTR, hostbuf=config
        )
        values = np.empty_like(positions)
        output = cl.Buffer(context, flags.WRITE_ONLY, values.nbytes)
        kernel(queue, (len(positions),), None, inputs, config_buffer, output)
        cl.enqueue_copy(queue, values, output).wait()
        return values[:, :3]

    reports = {}
    for variant in ("baseline", "candidate"):
        directory = work / variant / "Solver/Kernel/OpenCL"
        source = (directory / "forces.cl").read_text() + SAMPLE_KERNEL
        if variant == "candidate":
            source += GRADIENT_KERNEL
        program = cl.Program(context, source).build(
            options=["-DTILE_SIZE=4", "-I", str(directory)]
        )
        kernel = program.sample_force
        values = evaluate(kernel, points)
        zero_time = evaluate(kernel, points, phase=0)
        divergence = np.zeros(len(points))
        for axis in range(3):
            plus, minus = points.copy(), points.copy()
            plus[:, axis] += epsilon
            minus[:, axis] -= epsilon
            divergence += (
                evaluate(kernel, plus)[:, axis] - evaluate(kernel, minus)[:, axis]
            ) / (2 * epsilon)
        reports[variant] = {
            "axis_correlation": np.corrcoef(values.T).tolist(),
            "divergence_rms": float(np.sqrt(np.mean(divergence**2))),
            "zero_time_rms": float(np.sqrt(np.mean(zero_time**2))),
        }
        if variant == "baseline":
            assert np.array_equal(values[:, 0], values[:, 1])
            assert np.array_equal(values[:, 1], values[:, 2])
            assert not zero_time.any()
            continue
        assert not evaluate(kernel, points, amplitude=0).any()
        np.testing.assert_allclose(
            evaluate(kernel, points, amplitude=5), values * 2, rtol=1e-6, atol=1e-6
        )
        assert not np.allclose(evaluate(kernel, points, seed=8), values)
        assert not np.allclose(evaluate(kernel, points, phase=2), values)
        assert reports[variant]["zero_time_rms"] > 0.1
        assert (
            max(abs(np.corrcoef(values.T)[i, j]) for i in range(3) for j in range(i))
            < 0.5
        )

        gradient_kernel = program.sample_gradient

        def noise_gradient(positions, gradient_kernel=gradient_kernel):
            positions = np.ascontiguousarray(positions)
            inputs = cl.Buffer(
                context, flags.READ_ONLY | flags.COPY_HOST_PTR, hostbuf=positions
            )
            output = cl.Buffer(context, flags.WRITE_ONLY, positions.nbytes)
            result = np.empty_like(positions)
            gradient_kernel(queue, (len(positions),), None, inputs, output)
            cl.enqueue_copy(queue, result, output).wait()
            return result

        analytic = noise_gradient(points)[:, :3]
        finite = np.empty_like(analytic)
        for axis in range(3):
            plus, minus = points.copy(), points.copy()
            plus[:, axis] += epsilon
            minus[:, axis] -= epsilon
            finite[:, axis] = (
                noise_gradient(plus)[:, 3] - noise_gradient(minus)[:, 3]
            ) / (2 * epsilon)
        error = float(np.max(abs(analytic - finite)))
        assert error < 0.003, error
        reports[variant]["analytic_gradient_max_error"] = error
    assert (
        reports["candidate"]["divergence_rms"]
        < reports["baseline"]["divergence_rms"] * 0.01
    )
    return reports
