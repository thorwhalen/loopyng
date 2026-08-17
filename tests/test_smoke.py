"""Numpy-only smoke tests for loopyng's core waveform generators.

These are the gate the CI leans on: they exercise the generators named in the
package's public API (``loopyng.gen.sine_mix``, ``loopyng.lite_sample_sounds``
and ``tag_wf_gen``) and assert the three properties a generated waveform must
always have -- **shape**, **dtype** and **all-finite** samples.

Deliberately numpy-only. No matplotlib, no IPython, no pandas, no scikit-learn,
no soundfile round-trip, no audio hardware. A signal-generation library must be
verifiable from a bare install, and a test suite that needs the visualisation
stack to prove a sine wave has the right length is testing the wrong thing.
"""

import numpy as np
import pytest

from loopyng.gen.sine_mix import mk_sine_wf, freq_based_stationary_wf
from loopyng.lite_sample_sounds import (
    AnnotatedWaveform,
    chk_from_pattern,
    pure_tone,
    random_samples,
    square_tone,
    tag_to_wf_gen_func,
    tag_wf_gen,
    triangular_tone,
)


def assert_is_finite_waveform(wf, *, n_samples, dtype_kind):
    """Assert ``wf`` is a length-``n_samples`` 1-D array of finite samples.

    ``dtype_kind`` is a numpy dtype *kind* character -- ``'f'`` for floating
    point, ``'i'`` for signed integer. Kind rather than an exact dtype keeps the
    assertion honest across platforms without letting an object-array through.
    """
    arr = np.asarray(wf)
    assert arr.ndim == 1, f"expected a 1-D waveform, got shape {arr.shape}"
    assert arr.shape == (n_samples,), f"expected {n_samples} samples, got {arr.shape}"
    assert arr.dtype.kind == dtype_kind, (
        f"expected dtype kind {dtype_kind!r}, got {arr.dtype!r}"
    )
    assert np.all(np.isfinite(arr)), "waveform contains NaN or inf samples"


# --------------------------------------------------------------------------
# loopyng.gen.sine_mix -- float waveforms
# --------------------------------------------------------------------------


def test_import_loopyng():
    """The package imports and re-exports its headline generators."""
    import loopyng

    for name in ("tag_wf_gen", "AnnotatedWaveform", "pure_tone", "mk_sine_wf"):
        assert hasattr(loopyng, name), f"loopyng.{name} is not exported"


@pytest.mark.parametrize("n_samples", [1, 3, 1024])
def test_mk_sine_wf_shape_dtype_finite(n_samples):
    wf = mk_sine_wf(freq=440, n_samples=n_samples, sr=44100)
    assert_is_finite_waveform(wf, n_samples=n_samples, dtype_kind="f")


def test_mk_sine_wf_is_bounded_by_gain():
    """A sine of gain g never leaves [-g, g] -- the amplitude contract."""
    gain = 3.0
    wf = mk_sine_wf(freq=440, n_samples=4096, sr=44100, gain=gain)
    assert np.max(np.abs(wf)) <= gain + 1e-12


def test_freq_based_stationary_wf_shape_dtype_finite():
    n_samples = 512
    wf = freq_based_stationary_wf(
        freqs=(200, 400, 600, 800), n_samples=n_samples, sr=44100
    )
    assert_is_finite_waveform(wf, n_samples=n_samples, dtype_kind="f")


def test_freq_based_stationary_wf_normalizes_weights():
    """Weights are normalized, so the mix stays inside the unit envelope."""
    wf = freq_based_stationary_wf(
        freqs=(200, 400), weights=[3, 7], n_samples=2048, sr=44100
    )
    assert np.max(np.abs(wf)) <= 1.0 + 1e-12


def test_freq_based_stationary_wf_rejects_mismatched_weights():
    with pytest.raises(AssertionError):
        freq_based_stationary_wf(freqs=(200, 400, 600), weights=[1, 2], n_samples=16)


# --------------------------------------------------------------------------
# loopyng.lite_sample_sounds -- int16 waveforms
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "gen_func", [random_samples, pure_tone, triangular_tone, square_tone]
)
@pytest.mark.parametrize("chk_size", [1, 5, 4096])
def test_lite_sample_sounds_shape_dtype_finite(gen_func, chk_size):
    wf = gen_func(chk_size)
    assert_is_finite_waveform(wf, n_samples=chk_size, dtype_kind="i")


def test_lite_sample_sounds_generators_are_int16():
    """int16 is the wire format these chunks are written/played as."""
    for gen_func in tag_to_wf_gen_func.values():
        assert np.asarray(gen_func(64)).dtype == np.int16


def test_chk_from_pattern_tiles_and_truncates():
    """A pattern is tiled to fill chk_size exactly, truncating the last repeat."""
    wf = chk_from_pattern(7, [1, 2, 3])
    assert_is_finite_waveform(wf, n_samples=7, dtype_kind="i")
    assert list(wf) == [1, 2, 3, 1, 2, 3, 1]


def test_random_samples_respects_max_amplitude():
    max_amplitude = 1000
    wf = random_samples(8192, max_amplitude=max_amplitude)
    assert np.max(np.abs(wf)) <= max_amplitude


# --------------------------------------------------------------------------
# loopyng.gen.signal_generators
# --------------------------------------------------------------------------


def test_bernoulli_returns_a_python_int():
    """Guards a numpy-2 incompatibility the 3.12 CI matrix surfaced.

    ``bernoulli`` drew with ``size=1`` and called ``int()`` on the resulting
    one-element array. That was a DeprecationWarning under numpy 1.25 and is a
    TypeError from numpy 2 onwards, so the doctest passed on a pinned older
    numpy and failed on a fresh install.
    """
    from loopyng.gen.signal_generators import bernoulli

    for p_out, expected in [(0, 0), (1, 1)]:
        value = bernoulli(p_out)
        assert value == expected
        assert type(value) is int, f"expected a Python int, got {type(value)}"

    assert {bernoulli(0.5) for _ in range(50)} <= {0, 1}


# --------------------------------------------------------------------------
# tag_wf_gen -- tagged waveform stream
# --------------------------------------------------------------------------


def test_tag_wf_gen_default_stream_is_indefinite_and_well_formed():
    gen = tag_wf_gen()
    for _ in range(4):
        tag, wf = next(gen)
        assert tag in tag_to_wf_gen_func
        assert_is_finite_waveform(wf, n_samples=21 * 2048, dtype_kind="i")


def test_tag_wf_gen_follows_an_explicit_tag_sequence():
    tags = ["random", "pure_tone", "triangular_tone", "square_tone"]
    pairs = list(tag_wf_gen(tag_sequence=tags))
    assert [tag for tag, _ in pairs] == tags
    for _, wf in pairs:
        assert_is_finite_waveform(wf, n_samples=21 * 2048, dtype_kind="i")


def test_tag_wf_gen_rejects_unknown_tags():
    with pytest.raises(ValueError, match="tag_wfgen_map"):
        list(tag_wf_gen(tag_sequence=["random", "no_such_tag"]))


def test_annotated_waveform_wf_and_annots_are_consistent():
    """The annotations must actually index the waveform they describe.

    Bounds-checking alone is too weak a claim: a cursor that never advances
    still yields in-bounds slices. So assert the stronger, real contract --
    the slices *partition* the waveform (contiguous, non-overlapping, complete)
    and each deterministic tag's slice holds exactly that tag's chunk.
    """
    chk_size = 8
    tags = ("random", "pure_tone", "triangular_tone", "square_tone")
    wf, annots = AnnotatedWaveform(chk_size=chk_size).get_wf_and_annots(chk_tags=tags)

    assert_is_finite_waveform(wf, n_samples=chk_size * len(tags), dtype_kind="i")
    assert set(annots) == set(tags)

    all_slices = sorted(sl for slices in annots.values() for sl in slices)
    assert len(all_slices) == len(tags)
    cursor = 0
    for bt, tt in all_slices:
        assert bt == cursor, f"slice ({bt}, {tt}) does not abut the previous one"
        assert tt == bt + chk_size, f"slice ({bt}, {tt}) is not one chunk long"
        cursor = tt
    assert cursor == len(wf), "the slices do not cover the whole waveform"

    # The deterministic tags must index the exact samples their generator makes.
    for tag in ("pure_tone", "triangular_tone", "square_tone"):
        ((bt, tt),) = annots[tag]
        expected = tag_to_wf_gen_func[tag](chk_size)
        assert list(wf[bt:tt]) == list(expected), f"{tag} slice holds the wrong chunk"
