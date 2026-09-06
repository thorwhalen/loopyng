"""Guard the vendored librosa DSP against numpy's removed scalar-type aliases.

``np.float`` was a deprecated alias for the builtin ``float``, and numpy 1.24
removed it. Two lines of the vendored librosa code still asked for it, and both
sat on live paths that no test ever walked:

* ``tempo_frequencies`` -- reached from ``specshow(..., y_axis='tempo')``
* ``normalize`` -- reached from ``mel`` (and so ``melspectrogram``) whenever
  ``norm`` is anything but the default ``'slaney'``, and from
  ``spectral_centroid`` unconditionally

Under any numpy new enough to have dropped the alias, calling those functions
raised ``AttributeError: module 'numpy' has no attribute 'float'``. The suite
stayed green because the only mel path it exercised was the default
``norm='slaney'``, which happens to skip the broken line.

Each test below therefore asserts on an observable that the repaired line
actually decides -- a Nyquist bound, a filter bank that sums to one, a column
that only survives at full float precision -- rather than on a shape or a dtype
that would look identical with the line broken or narrowed. Shapes and
"it returned something" are what let the original breakage hide.
"""

import numpy as np
import pytest

from loopyng.utils.librosa_utils import (
    mel,
    melspectrogram,
    normalize,
    spectral_centroid,
    tempo_frequencies,
)

SR = 22050
N_FFT = 2048
HOP_LENGTH = 512
N_MELS = 128
NYQUIST = SR / 2
# ``_spectrogram`` centre-pads, so a one-second signal yields this many frames.
N_FRAMES = 1 + SR // HOP_LENGTH


@pytest.fixture
def noise():
    """One second of reproducible white noise at ``SR``."""
    return np.random.default_rng(0).standard_normal(SR).astype(np.float32)


def test_normalize_max_norms_each_column():
    """``normalize`` divides every column by its own maximum magnitude."""
    normalized = normalize(np.array([[1.0, 2.0], [3.0, 4.0]]))

    assert np.allclose(normalized, [[1 / 3, 0.5], [1.0, 1.0]])


def test_normalize_takes_magnitudes_at_full_float_precision():
    """The repaired ``np.abs(S).astype(float)`` must not narrow to float32.

    No assertion on an ordinary input can see this: ``normalize`` builds its
    result with ``np.empty_like(S)``, so the *output* dtype comes from the input
    and says nothing about the magnitudes computed on the way. A column whose
    magnitudes overflow float32 does see it -- narrowing makes the column
    maximum ``inf``, and dividing by that zeroes the whole column.
    """
    beyond_float32 = np.array([[1e300, 1.0], [1e-300, 2.0]])

    assert np.allclose(normalize(beyond_float32), [[1.0, 0.5], [0.0, 1.0]])


@pytest.mark.parametrize("dtype", [np.float32, np.float64])
def test_normalize_preserves_a_floating_input_dtype(dtype):
    """``np.empty_like(S)`` means the input picks the output dtype, not the fix.

    Worth pinning because it is easy to read the ``.astype(float)`` on the
    magnitudes as a promise that the result is float64. It is not: the mel
    filter bank, ``normalize``'s main caller here, is float32 and stays float32.
    """
    normalized = normalize(np.array([[1.0, 2.0], [3.0, 4.0]], dtype=dtype))

    assert normalized.dtype == dtype
    assert np.allclose(normalized, [[1 / 3, 0.5], [1.0, 1.0]])


def test_normalize_truncates_integer_input_as_upstream_librosa_does():
    """Integer input comes back truncated -- matched on purpose, not overlooked.

    ``np.empty_like(S)`` keeps an integer input's dtype, so the float division is
    truncated on assignment into it. That is exactly what upstream
    ``librosa.util.normalize`` does; this module is a vendored copy, so the
    behaviour is matched rather than quietly corrected. Before the numpy-alias
    fix every dtype raised ``AttributeError``, which is what kept the trap out of
    sight -- pinning it here keeps it visible. Callers wanting ratios pass floats.
    """
    integers = np.array([[1, 2], [3, 4]])

    assert np.array_equal(normalize(integers), [[0, 0], [1, 1]])
    assert np.allclose(normalize(integers.astype(float)), [[1 / 3, 0.5], [1.0, 1.0]])


def test_tempo_frequencies_allocates_float_bins():
    """Bin 0 holds ``inf``, which only a float array can.

    Here the dtype assertion *is* the guard: ``np.zeros(n_bins, dtype=float)`` is
    the repaired line, and the finite bins would survive a narrower dtype well
    within ``allclose``'s tolerance.
    """
    n_bins = 4
    bin_frequencies = tempo_frequencies(n_bins, hop_length=HOP_LENGTH, sr=SR)

    assert bin_frequencies.dtype == np.float64
    assert bin_frequencies[0] == np.inf
    assert np.allclose(
        bin_frequencies[1:], 60.0 * SR / (HOP_LENGTH * np.arange(1.0, n_bins))
    )


def test_mel_filter_bank_with_non_slaney_norm(noise):
    """``norm=1`` routes the filter bank through ``normalize``, so rows sum to 1.

    The melspectrogram's shape cannot show this -- it is the same for every
    ``norm``, including the default ``'slaney'`` that skips the repaired line
    (and whose rows sum to roughly 0.09).
    """
    assert np.allclose(mel(SR, N_FFT, norm=1).sum(axis=1), 1.0)
    assert melspectrogram(y=noise, sr=SR, n_fft=N_FFT, norm=1).shape == (
        N_MELS,
        N_FRAMES,
    )


def test_spectral_centroid_stays_below_nyquist(noise):
    """``spectral_centroid`` normalizes its spectrogram, so it needs the fix too.

    The Nyquist bound is what makes this a test of the ``normalize`` call rather
    than of the shape: drop the normalization and the "centroid" becomes a raw
    weighted energy sum, four orders of magnitude above the highest frequency the
    signal can even represent.
    """
    centroid = spectral_centroid(y=noise, sr=SR, n_fft=N_FFT, hop_length=HOP_LENGTH)

    assert centroid.shape == (1, N_FRAMES)
    assert np.all((centroid > 0) & (centroid < NYQUIST))
