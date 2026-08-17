"""Exercise the viz surface against a matplotlib that is actually installed.

``test_optional_deps.py`` proves the viz surface degrades *gracefully* when
matplotlib is absent. Nothing proved it *works* when matplotlib is present --
and that gap is exactly how a live breakage hid in a green suite:

``matplotlib.cm.get_cmap`` was deprecated in matplotlib 3.7 and **removed** in
3.11, which is the version ``loopyng[viz]`` and ``loopyng[dev]`` resolve to. The
optional-dependency machinery caught the resulting failure and replaced the name
with a placeholder, so ``specshow`` -- the headline of the README's viz row --
raised *"matplotlib is not installed, install loopyng[viz]"* on a machine with
matplotlib **and** the viz extra installed. CI installed matplotlib 3.11 through
the ``dev`` extra and stayed green throughout, because no test ever drew
anything.

So these tests draw. They are the reason an API removal in an optional
dependency now turns the suite red instead of turning a function into a lie.
"""

import numpy as np
import pytest

matplotlib = pytest.importorskip("matplotlib", reason="the viz extra is not installed")


@pytest.fixture(autouse=True)
def headless_backend():
    """Draw to an in-memory canvas: no display, no window, no interactivity."""
    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    yield
    plt.close("all")


@pytest.fixture
def waveform():
    """A short, deterministic, non-trivial signal to draw."""
    sr = 22050
    t = np.linspace(0, 0.25, int(sr * 0.25), endpoint=False)
    return np.sin(2 * np.pi * 440 * t).astype(np.float32), sr


# --------------------------------------------------------------------------
# get_cmap: the specific API that broke
# --------------------------------------------------------------------------


def test_get_cmap_returns_a_real_colormap():
    """Not a placeholder, not a stub -- a colormap you can call on values."""
    from loopyng.utils.librosa_utils import get_cmap

    colormap = get_cmap("magma")
    assert colormap.name == "magma"
    rgba = colormap(0.5)
    assert len(rgba) == 4 and all(0.0 <= channel <= 1.0 for channel in rgba)


def test_get_cmap_honours_lut():
    """``lut`` resamples the colormap; the bool branch of ``cmap`` relies on it."""
    from loopyng.utils.librosa_utils import get_cmap

    assert get_cmap("gray_r", lut=2).N == 2
    assert get_cmap("gray_r").N == 256


@pytest.mark.parametrize(
    "data, expected_name",
    [
        (np.array([True, False, True]), "gray_r"),
        (np.array([0.0, 1.0, 2.0]), "magma"),
        (np.array([-1.0, 0.0, 1.0]), "coolwarm"),
    ],
)
def test_cmap_dispatches_on_the_data(data, expected_name):
    """Boolean -> two-tone, one-signed -> sequential, two-signed -> divergent."""
    from loopyng.utils.librosa_utils import cmap

    assert cmap(data).name == expected_name


# --------------------------------------------------------------------------
# specshow: the headline the README advertises
# --------------------------------------------------------------------------


def test_specshow_draws_a_mel_spectrogram(waveform):
    """The end-to-end path the README's viz row promises."""
    import matplotlib.pyplot as plt
    from matplotlib.collections import QuadMesh

    from loopyng.utils.librosa_utils import (
        amplitude_to_db,
        melspectrogram,
        specshow,
    )

    wf, sr = waveform
    spectrogram = amplitude_to_db(melspectrogram(y=wf, sr=sr))

    figure, axes = plt.subplots()
    mesh = specshow(spectrogram, sr=sr, y_axis="mel", x_axis="time", ax=axes)

    assert isinstance(mesh, QuadMesh)
    # A drawn mesh, not an empty axes: the frequency axis is labelled and the
    # colours came from a colormap that resolved.
    assert mesh.get_cmap() is not None
    assert axes.get_ylabel()
    figure.canvas.draw()  # rasterize: catches anything deferred until render


def test_specshow_without_an_axes_uses_the_current_figure(waveform):
    """``ax=None`` goes through ``__check_axes``/``__set_current_image``."""
    import matplotlib.pyplot as plt

    from loopyng.utils.librosa_utils import (
        amplitude_to_db,
        melspectrogram,
        specshow,
    )

    wf, sr = waveform
    plt.figure()
    mesh = specshow(amplitude_to_db(melspectrogram(y=wf, sr=sr)), sr=sr, x_axis="time")
    assert mesh in plt.gca().collections


# --------------------------------------------------------------------------
# plotting: the other half of the viz extra
# --------------------------------------------------------------------------


def test_plot_wf_draws_a_line(waveform):
    """``plot_wf`` with a sample rate exercises the date-tick relabelling too."""
    import matplotlib.pyplot as plt

    from loopyng.utils.plotting import plot_wf

    wf, sr = waveform
    plot_wf(wf, sr=sr, figsize=(4, 2))
    lines = plt.gca().get_lines()
    assert len(lines) == 1
    assert len(lines[0].get_xdata()) == len(wf)
    plt.gcf().canvas.draw()


def test_disp_wf_plots_and_returns_an_audio_widget(waveform):
    """The notebook path: a specgram plus an ``IPython.display.Audio``."""
    IPython_display = pytest.importorskip(
        "IPython.display", reason="the notebook extra is not installed"
    )
    import matplotlib.pyplot as plt

    from loopyng.utils.plotting import disp_wf

    wf, sr = waveform
    widget = disp_wf(wf, sr=sr)
    assert isinstance(widget, IPython_display.Audio)
    assert plt.gcf().axes  # something was actually drawn
