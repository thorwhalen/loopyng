"""
Plot utilities for visualizing audio waveforms and spectrograms.

Provides functions for displaying waveforms with proper time axes and playback options.
"""

from inspect import getmodule
from numpy import linspace
from loopyng._optional import optional_import, optional_from
from loopyng.utils.date_ticks import str_ticks

# Optional: plotting needs matplotlib, notebook playback needs IPython. Both are
# bound lazily so `import loopyng` works on a bare install; using a function that
# actually needs one raises an ImportError naming the extra to install.
plt = optional_import("matplotlib.pylab", extra="viz", used_by="loopyng.utils.plotting")
Audio = optional_from(
    "IPython.display", "Audio", extra="notebook", used_by="loopyng.utils.plotting"
)

DFLT_FIGSIZE_FOR_WF_PLOTS = (22, 5)
DFLT_SR = 44100

# Sentinel for disp_wf's default plotting function. It cannot default directly to
# plt.specgram: that would touch matplotlib at import time, which is exactly what
# the optional-dependency handling exists to avoid.
DFLT_WF_PLOT_FUNC = "specgram"


def getmodulename(obj, default=""):
    """Get name of module of object"""
    return getattr(getmodule(obj), "__name__", default)


# def plot_wf(wf, sr=None, figsize=(20, 6), **kwargs):
#     if figsize is not None:
#         plt.figure(figsize=figsize)
#     if sr is not None:
#         plt.plot(linspace(start=0, stop=len(wf) / float(sr), num=len(wf)), wf, **kwargs)
#     else:
#         plt.plot(wf, **kwargs)


def plot_wf(
    wf, sr=None, figsize=DFLT_FIGSIZE_FOR_WF_PLOTS, offset_s=0, ax=None, **kwargs
):
    if figsize is not None:
        plt.figure(figsize=figsize)
    _ax = ax or plt
    if sr is not None:
        _ax.plot(
            offset_s + linspace(start=0, stop=len(wf) / float(sr), num=len(wf)),
            wf,
            **kwargs,
        )
        plt.margins(x=0)
    else:
        _ax.plot(wf, **kwargs)
        plt.margins(x=0)
        return
    if _ax == plt:
        _xticks, _ = plt.xticks()
        plt.xticks(_xticks, str_ticks(ticks=_xticks, ticks_unit=1))
        plt.margins(x=0)
    else:
        _xticks = _ax.get_xticks()
        _ax.set_xticks(_xticks)
        _ax.set_xticklabels(str_ticks(ticks=_xticks, ticks_unit=1))
        plt.margins(x=0)


def disp_wf(wf, sr=DFLT_SR, autoplay=False, wf_plot_func=DFLT_WF_PLOT_FUNC):
    """Plot a waveform and return an IPython Audio widget for it.

    :param wf: The waveform to display
    :param sr: Sample rate
    :param autoplay: Whether the returned Audio widget should play immediately
    :param wf_plot_func: Plotting function, or the name of a ``matplotlib.pylab``
        one (default: ``"specgram"``). Pass ``None`` to skip plotting.

    Needs the ``viz`` extra to plot and the ``notebook`` extra for the widget.
    """
    if isinstance(wf_plot_func, str):
        # Resolved here, not at import time, so a bare install can still import
        # this module -- and gets a clear error naming the extra if it plots.
        wf_plot_func = getattr(plt, wf_plot_func)
    if wf_plot_func is not None:
        if getmodulename(wf_plot_func, "").startswith("matplotlib"):
            plt.figure(figsize=DFLT_FIGSIZE_FOR_WF_PLOTS)
        wf_plot_func(wf, sr)
    return Audio(data=wf, rate=sr, autoplay=autoplay)
