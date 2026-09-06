"""Guard the vendored librosa DSP against numpy's removed scalar-type aliases.

``np.float`` was a deprecated alias for the builtin ``float``, and numpy 1.24
removed it. Two lines of the vendored librosa code still asked for it, and both
sat on live paths that no test ever walked:

* ``tempo_frequencies`` -- reached from ``specshow(..., y_axis='tempo')``
* ``normalize`` -- reached from ``melspectrogram`` whenever ``norm`` is anything
  but the default ``'slaney'``, and from ``spectral_centroid`` unconditionally

Under any numpy new enough to have dropped the alias, calling those functions
raised ``AttributeError: module 'numpy' has no attribute 'float'``. The suite
stayed green because the only mel path it exercised was the default
``norm='slaney'``, which happens to skip the broken line.

So these tests call the functions and check their *values*, not just that they
return. They are the reason a scalar-alias removal in numpy now turns the suite
red instead of turning three functions into a lie.
"""

import numpy as np
import pytest

from loopyng.utils.librosa_utils import (
    melspectrogram,
    normalize,
    spectral_centroid,
    tempo_frequencies,
)

SR = 22050


@pytest.fixture
def noise():
    """One second of reproducible white noise at ``SR``."""
    return np.random.default_rng(0).standard_normal(SR).astype(np.float32)


def test_normalize_runs():
    """``normalize`` max-norms each column and yields float64."""
    normalized = normalize(np.array([[1.0, 2.0], [3.0, 4.0]]))

    assert normalized.dtype == np.float64
    assert np.allclose(normalized, [[1 / 3, 0.5], [1.0, 1.0]])


def test_tempo_frequencies_runs():
    """``tempo_frequencies`` yields float64 bins, the first of them infinite."""
    bin_frequencies = tempo_frequencies(4)

    assert bin_frequencies.dtype == np.float64
    assert bin_frequencies[0] == np.inf
    assert np.allclose(bin_frequencies[1:], 60.0 * SR / (512 * np.arange(1.0, 4)))


def test_melspectrogram_with_non_slaney_norm(noise):
    """A ``norm`` other than the default routes through ``normalize``."""
    assert melspectrogram(y=noise, sr=SR, norm=1).shape == (128, 44)


def test_spectral_centroid_runs(noise):
    """``spectral_centroid`` normalizes its spectrogram, so it needs the fix too."""
    centroid = spectral_centroid(y=noise, sr=SR)

    assert centroid.shape == (1, 44)
    assert np.all(centroid > 0)
