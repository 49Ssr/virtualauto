# SPDX-License-Identifier: GPL-3.0-or-later
"""Check solid-cell scalar exclusion on the GPU and at real cache submission."""

import inspect
from contextlib import contextmanager


def run(work, context, queue):
    import numpy as np
    import pyopencl as cl

    directory = work / "candidate/Solver/Kernel/OpenCL"
    program = cl.Program(context, (directory / "scalar_update.cl").read_text()).build(
        options=["-DTILE_SIZE=4", "-I", str(directory)]
    )
    kernel = program.clear_solid_scalars
    flags = cl.mem_flags
    tile_map = np.array([0, -1], dtype=np.int32)
    map_buffer = cl.Buffer(
        context, flags.READ_ONLY | flags.COPY_HOST_PTR, hostbuf=tile_map
    )
    reports = {}
    for name, active_solids in (
        ("wall", [0, 17, 63]),
        ("moved_wall", [5, 32]),
        ("empty", []),
    ):
        mask = np.zeros(128, dtype=np.uint8)
        mask[active_solids] = 1
        mask[64:] = 1  # Unmapped pool capacity must remain untouched.
        mask_buffer = cl.Buffer(
            context, flags.READ_ONLY | flags.COPY_HOST_PTR, hostbuf=mask
        )
        original = [np.arange(128, dtype=np.float32) + i + 0.25 for i in range(4)]
        buffers = [
            cl.Buffer(context, flags.READ_WRITE | flags.COPY_HOST_PTR, hostbuf=a)
            for a in original
        ]
        kernel(
            queue,
            (8, 4, 4),
            (4, 4, 4),
            *buffers,
            mask_buffer,
            map_buffer,
            np.int32(2),
            np.int32(1),
            np.int32(1),
        )
        for source, buffer in zip(original, buffers, strict=True):
            result = np.empty_like(source)
            cl.enqueue_copy(queue, result, buffer).wait()
            expected = source.copy()
            expected[active_solids] = 0
            np.testing.assert_array_equal(result, expected)
        reports[name] = {
            "cleared_solid_cells": len(active_solids),
            "fluid_and_unmapped_unchanged": True,
        }
    return reports


@contextmanager
def observe_outputs(output_module):
    """Check the actual buffers passed to VDB export, after the full solver step."""
    import numpy as np
    import pyopencl as cl

    original = output_module.submit_output
    reports = []

    def submit(*args, **kwargs):
        state = inspect.currentframe().f_back.f_locals
        mask = np.empty(state["obstacle_mask"].size, dtype=np.uint8)
        queue = kwargs["queue"]
        cl.enqueue_copy(queue, mask, state["obstacle_mask"]).wait()
        solid = mask.astype(bool)
        report = {"frame": kwargs["frame"], "solid_cells": int(solid.sum())}
        for name in ("smoke", "fuel", "flame"):
            values = np.empty(mask.size, dtype=np.float32)
            cl.enqueue_copy(queue, values, kwargs[name]).wait()
            count = int(np.count_nonzero(values[solid]))
            report[name + "_inside_solids"] = count
            assert count == 0, report
        reports.append(report)
        return original(*args, **kwargs)

    output_module.submit_output = submit
    try:
        yield reports
    finally:
        output_module.submit_output = original
