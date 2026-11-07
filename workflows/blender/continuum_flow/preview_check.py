# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise preview buffer growth/shrinkage on a real OpenCL device."""

import importlib.util
import math

import numpy as np
import pyopencl as cl


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(work, context, queue):
    report = {}
    for name in ("baseline", "candidate"):
        module = load("va_cf_buffers_" + name, work / name / "Solver/Kernel/preview.py")
        replacements = 0
        counter_replacements = 0
        counts = [64, 63, 62, 61, 60, 27, 64, 65, 64, 65]
        previous = None
        previous_counter = None
        for index, count in enumerate(counts):
            module.ensure_capacity(context, count, 4)
            if previous is not None:
                replacements += module.fields_buffer is not previous
                counter_replacements += module.counter_buffer is not previous_counter
            length = math.prod(module.atlas_shape(count)) * 4**3 * 2
            assert module.fields_buffer.size >= length * 4
            value = np.float32(index + 0.25)
            cl.enqueue_fill_buffer(queue, module.fields_buffer, value, 0, length * 4)
            actual = np.empty(length, dtype=np.float32)
            cl.enqueue_copy(queue, actual, module.fields_buffer).wait()
            assert np.all(actual == value)
            previous = module.fields_buffer
            previous_counter = module.counter_buffer
        report[name] = {
            "field_replacements": replacements,
            "counter_replacements": counter_replacements,
        }
        module.close()
        assert module.fields_buffer is None and module.counter_buffer is None
    assert report["baseline"]["field_replacements"] == 9
    assert report["candidate"]["field_replacements"] == 1
    assert report["candidate"]["counter_replacements"] == 0
    report["readback_matches"] = True
    return report
