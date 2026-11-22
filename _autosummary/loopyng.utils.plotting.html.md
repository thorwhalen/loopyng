# loopyng.utils.plotting

Plot utilities for visualizing audio waveforms and spectrograms.

Provides functions for displaying waveforms with proper time axes and playback options.

### Functions

| [`disp_wf`](#loopyng.utils.plotting.disp_wf)(wf[, sr, autoplay, wf_plot_func])   | Plot a waveform and return an IPython Audio widget for it.   |
|----------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| [`getmodulename`](#loopyng.utils.plotting.getmodulename)(obj[, default])               | Get name of module of object                                 |
| `plot_wf`(wf[, sr, figsize, offset_s, ax])                                                   |                                                              |

### loopyng.utils.plotting.disp_wf(wf, sr=44100, autoplay=False, wf_plot_func='specgram')

Plot a waveform and return an IPython Audio widget for it.

* **Parameters:**
  * **wf** – The waveform to display
  * **sr** – Sample rate
  * **autoplay** – Whether the returned Audio widget should play immediately
  * **wf_plot_func** – Plotting function, or the name of a `matplotlib.pylab`
    one (default: `"specgram"`). Pass `None` to skip plotting.

Needs the `viz` extra to plot and the `notebook` extra for the widget.

### loopyng.utils.plotting.getmodulename(obj, default='')

Get name of module of object
