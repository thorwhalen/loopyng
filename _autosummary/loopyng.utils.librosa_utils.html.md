# loopyng.utils.librosa_utils

A few utils (specshow, melspectrogram) vendored from librosa.

This code was copied from parts of librosa, and adapted, so as to be able to use
targeted functionality with less dependencies and manual installation
(namely for libsndfile) than librosa has.

Librosa can be found here: [https://librosa.org/](https://librosa.org/)

Librosa’s license follows.

ISC License
Copyright (c) 2013–2017, librosa development team.

Permission to use, copy, modify, and/or distribute this software for any purpose with or
without fee is hereby granted, provided that the above copyright notice and this
permission notice appear in all copies.

THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

### Functions

| `amplitude_to_db`(S[, ref, amin, top_db])                              |                                                                      |
|------------------------------------------------------------------------|----------------------------------------------------------------------|
| `cmap`(data[, robust, cmap_seq, cmap_bool, ...])                       |                                                                      |
| `cqt_frequencies`(n_bins, fmin[, ...])                                 |                                                                      |
| `db_to_amplitude`(S_db[, ref])                                         |                                                                      |
| `db_to_power`(S_db[, ref])                                             |                                                                      |
| `dtype_r2c`(d[, default])                                              |                                                                      |
| `fft_frequencies`([sr, n_fft])                                         |                                                                      |
| `fix_frames`(frames[, x_min, x_max, pad])                              |                                                                      |
| `fourier_tempo_frequencies`([sr, win_length, ...])                     |                                                                      |
| `frame`(x, frame_length, hop_length[, axis])                           |                                                                      |
| `frames_to_samples`(frames[, hop_length, n_fft])                       |                                                                      |
| `frames_to_time`(frames[, sr, hop_length, n_fft])                      |                                                                      |
| [`get_cmap`](#loopyng.utils.librosa_utils.get_cmap)(name[, lut]) | Look up a named colormap, optionally resampled down to `lut` colors. |
| `get_fftlib`()                                                         |                                                                      |
| `get_window`(window, Nx[, fftbins])                                    |                                                                      |
| `hz_to_mel`(frequencies[, htk])                                        |                                                                      |
| `index_to_slice`(idx[, idx_min, idx_max, ...])                         |                                                                      |
| `mel`(sr, n_fft[, n_mels, fmin, fmax, htk, ...])                       |                                                                      |
| `mel_frequencies`([n_mels, fmin, fmax, htk])                           |                                                                      |
| `mel_to_hz`(mels[, htk])                                               |                                                                      |
| `melspectrogram`([y, sr, S, n_fft, ...])                               |                                                                      |
| `midi_to_hz`(notes)                                                    |                                                                      |
| `normalize`(S[, norm, axis, threshold, fill])                          |                                                                      |
| `note_to_hz`(note, \*\*kwargs)                                         |                                                                      |
| `note_to_midi`(note[, round_midi])                                     |                                                                      |
| `onset_strength`([y, sr, S, lag, max_size, ...])                       |                                                                      |
| `onset_strength_multi`([y, sr, S, n_fft, ...])                         |                                                                      |
| `pad_center`(data, size[, axis])                                       |                                                                      |
| `power_to_db`(S[, ref, amin, top_db])                                  |                                                                      |
| `samples_to_time`(samples[, sr])                                       |                                                                      |
| `set_fftlib`([lib])                                                    |                                                                      |
| `specshow`(data[, x_coords, y_coords, x_axis, ...])                    |                                                                      |
| `spectral_centroid`([y, sr, S, n_fft, ...])                            |                                                                      |
| `spectral_contrast`([y, sr, S, n_fft, ...])                            |                                                                      |
| `stft`(y[, n_fft, hop_length, win_length, ...])                        |                                                                      |
| `sync`(data, idx[, aggregate, pad, axis])                              |                                                                      |
| `tempo_frequencies`(n_bins[, hop_length, sr])                          |                                                                      |
| `tiny`(x)                                                              |                                                                      |
| `valid_audio`(y[, mono])                                               |                                                                      |

### Classes

| `TimeFormatter`   |    |
|-------------------|----|

### loopyng.utils.librosa_utils.get_cmap(name, lut=None)

Look up a named colormap, optionally resampled down to `lut` colors.

Stands in for `matplotlib.cm.get_cmap`, which the vendored librosa code was
written against and which **no longer exists**: deprecated in matplotlib 3.7
and removed in 3.11. The supported spelling is the colormap registry
(`matplotlib.colormaps`, since 3.5) plus `Colormap.resampled` (since
3.6), which is why the viz extra floors matplotlib at 3.6.

Kept as a module-level function rather than an `optional_from` binding so
that a missing matplotlib is reported against `matplotlib` itself, which is
the package the user would actually install.

* **Parameters:**
  * **name** – A registered colormap name, e.g. `"magma"`
  * **lut** – If given, resample the colormap to this many colors
* **Returns:**
  A `matplotlib.colors.Colormap`
