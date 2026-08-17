"""Guard the contract that moving deps to extras created.

matplotlib, IPython, pandas and scikit-learn moved out of the hard install
requirements into extras. That is only a safe change if two things hold, and
neither is checked by any other test:

1. ``import loopyng`` still works, and the core generators still run, on an
   install that has none of those four packages.
2. Reaching for a feature that does need one raises an **ImportError naming the
   extra to install** -- not an AttributeError, a NameError, or silence.

Rather than require a second CI environment, these tests simulate the bare
install in-process: a meta-path hook makes the four packages unimportable, the
loopyng modules are re-imported under that condition, and the assertions run
against those freshly-imported modules.
"""

import importlib
import sys

import pytest

OPTIONAL_ROOTS = ("matplotlib", "IPython", "pandas", "sklearn")


class BlockedImportFinder:
    """A meta-path finder that makes the named top-level packages unimportable."""

    def __init__(self, blocked_roots):
        self.blocked_roots = set(blocked_roots)

    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in self.blocked_roots:
            raise ImportError(f"simulated bare install: {fullname} is not installed")
        return None


def _purge(predicate):
    for name in [n for n in sys.modules if predicate(n)]:
        del sys.modules[name]


@pytest.fixture
def bare_install():
    """Yield a ``import_fresh`` callable that imports under a bare install."""
    finder = BlockedImportFinder(OPTIONAL_ROOTS)
    saved = dict(sys.modules)

    def is_optional(name):
        return name.split(".")[0] in OPTIONAL_ROOTS

    def is_loopyng(name):
        return name == "loopyng" or name.startswith("loopyng.")

    _purge(lambda n: is_optional(n) or is_loopyng(n))
    sys.meta_path.insert(0, finder)
    try:
        yield importlib.import_module
    finally:
        sys.meta_path.remove(finder)
        # Restore a normal loopyng for the rest of the session.
        _purge(lambda n: is_optional(n) or is_loopyng(n))
        sys.modules.update(saved)


def test_optional_packages_really_are_blocked(bare_install):
    """Sanity-check the simulation itself before trusting what it proves."""
    for root in OPTIONAL_ROOTS:
        with pytest.raises(ImportError):
            bare_install(root)


def test_import_loopyng_without_optional_deps(bare_install):
    """The headline claim: a bare install can import the package."""
    loopyng = bare_install("loopyng")
    assert hasattr(loopyng, "tag_wf_gen")
    assert hasattr(loopyng, "mk_sine_wf")


def test_core_generators_work_without_optional_deps(bare_install):
    """And can actually generate signals, which is the point of the package."""
    import numpy as np

    loopyng = bare_install("loopyng")

    wf = loopyng.mk_sine_wf(freq=440, n_samples=256, sr=44100)
    assert wf.shape == (256,) and np.all(np.isfinite(wf))

    tag, chunk = next(loopyng.tag_wf_gen())
    assert isinstance(tag, str) and len(chunk) == 21 * 2048

    assert loopyng.pure_tone(64).dtype == np.int16


@pytest.mark.parametrize(
    "module_name",
    [
        "loopyng.utils.plotting",
        "loopyng.utils.librosa_utils",
        "loopyng.sound.audio",
        "loopyng.gen.signal_generators",
        "loopyng.examples.annotated_sounds",
    ],
)
def test_modules_with_optional_deps_still_import(bare_install, module_name):
    """Every guarded module imports; the error is deferred to point of use.

    This is what lets the docs build (which imports every module to read its
    docstrings) work against a bare install.
    """
    assert bare_install(module_name) is not None


def test_plot_wf_names_the_viz_extra(bare_install):
    plotting = bare_install("loopyng.utils.plotting")
    with pytest.raises(ImportError) as excinfo:
        plotting.plot_wf([0, 1, 0, -1])
    message = str(excinfo.value)
    assert "matplotlib" in message
    assert 'pip install "loopyng[viz]"' in message


def test_disp_wf_names_the_viz_extra(bare_install):
    plotting = bare_install("loopyng.utils.plotting")
    with pytest.raises(ImportError) as excinfo:
        plotting.disp_wf([0, 1, 0, -1])
    assert 'pip install "loopyng[viz]"' in str(excinfo.value)


def test_audio_widget_names_the_notebook_extra(bare_install):
    """With plotting skipped, disp_wf's next need is IPython -- a different extra."""
    plotting = bare_install("loopyng.utils.plotting")
    with pytest.raises(ImportError) as excinfo:
        plotting.disp_wf([0, 1, 0, -1], wf_plot_func=None)
    message = str(excinfo.value)
    assert "IPython" in message
    assert 'pip install "loopyng[notebook]"' in message


def test_session_to_df_names_the_data_extra(bare_install):
    signal_generators = bare_install("loopyng.gen.signal_generators")
    with pytest.raises(ImportError) as excinfo:
        signal_generators.pd.DataFrame()
    assert 'pip install "loopyng[data]"' in str(excinfo.value)


def test_annotated_sounds_scaler_names_the_data_extra(bare_install):
    annotated_sounds = bare_install("loopyng.examples.annotated_sounds")
    with pytest.raises(ImportError) as excinfo:
        annotated_sounds.session_phase_rpm_temparature()
    message = str(excinfo.value)
    assert "sklearn" in message
    assert 'pip install "loopyng[data]"' in message


def test_librosa_utils_formatter_subclass_survives_the_missing_base(bare_install):
    """The vendored TimeFormatter subclasses matplotlib's Formatter.

    Defining that class must not fail at import time -- only instantiating it.
    """
    librosa_utils = bare_install("loopyng.utils.librosa_utils")
    with pytest.raises(ImportError) as excinfo:
        librosa_utils.TimeFormatter()
    assert 'pip install "loopyng[viz]"' in str(excinfo.value)


def test_placeholder_distinguishes_informational_from_protocol_dunders():
    """``lib.__version__`` must explain itself; ``lib.__copy__`` must not.

    The vendored librosa code branches on ``matplotlib.__version__``. Reading it
    off a missing dependency has to give the actionable ImportError, while the
    protocol dunders that copy/pickle/inspect probe must keep raising
    AttributeError -- otherwise ordinary introspection blows up with the wrong
    error type.
    """
    from loopyng._optional import optional_import

    missing = optional_import("no_such_module_at_all", extra="viz")

    with pytest.raises(ImportError) as excinfo:
        missing.__version__
    assert 'pip install "loopyng[viz]"' in str(excinfo.value)

    for protocol_dunder in ("__copy__", "__deepcopy__", "__wrapped__", "__iter__"):
        with pytest.raises(AttributeError):
            getattr(missing, protocol_dunder)


def test_missing_attribute_of_a_present_module_is_not_reported_as_missing():
    """An "installed but renamed" dep must not be reported as "not installed".

    ``optional_from`` used to catch AttributeError alongside ImportError, so a
    dependency that was installed but had dropped an attribute -- exactly what
    matplotlib 3.11 did to ``matplotlib.cm.get_cmap`` -- was reported as not
    installed. That message sends the user to pip, pip reports success, and they
    are left where they started. The two failures have opposite remedies and must
    read differently.
    """
    from loopyng._optional import optional_from

    renamed = optional_from(
        "numpy", "no_such_numpy_attribute", extra="viz", used_by="a test"
    )

    with pytest.raises(ImportError) as excinfo:
        renamed()
    message = str(excinfo.value)

    assert "not installed" not in message
    assert "pip install" not in message
    assert "no_such_numpy_attribute" in message
    assert "numpy" in message


def test_a_genuinely_missing_module_still_names_the_extra():
    """The other half of the same branch: absent module keeps the pip message."""
    from loopyng._optional import optional_from

    absent = optional_from(
        "no_such_module_at_all", "anything", extra="viz", used_by="a test"
    )

    with pytest.raises(ImportError) as excinfo:
        absent()
    message = str(excinfo.value)

    assert "is not installed" in message
    assert 'pip install "loopyng[viz]"' in message


def test_dsp_half_of_librosa_utils_works_without_matplotlib(bare_install):
    """melspectrogram/amplitude_to_db are numpy+scipy -- viz must not gate them."""
    import numpy as np

    librosa_utils = bare_install("loopyng.utils.librosa_utils")
    wf = np.sin(np.linspace(0, 100, 4096))
    spectrogram = librosa_utils.melspectrogram(y=wf, sr=22050)
    assert spectrogram.ndim == 2
    assert np.all(np.isfinite(librosa_utils.amplitude_to_db(spectrogram)))
