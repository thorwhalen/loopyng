# loopyng.sound.audio

Audio processing and playback utilities.

Provides classes and functions for working with audio data, including
playback, visualization, and basic audio transformations.

### Functions

| `ensure_channels_in_columns`(wf)                                               |    |
|--------------------------------------------------------------------------------|----|
| `ensure_mono`(wf)                                                              |    |
| `is_wav_file`(filepath)                                                        |    |
| `plot_melspectrogram`(spect_mat[, sr, ...])                                    |    |
| `stereo_to_mono_by_taking_first_channel`(wf)                                   |    |
| `subtype_of_wf`(wf)                                                            |    |
| [`wf_and_sr`](#loopyng.sound.audio.wf_and_sr)(\*args, \*\*kwargs) |    |

### Classes

| `Sound`([wf, sr, wf_type])   |    |
|------------------------------|----|

### loopyng.sound.audio.wf_and_sr(\*args, \*\*kwargs)

* **Parameters:**
  * **args** – Either the file path to a sound or a tuple of (wf, sr)
  * **kwargs** – wf = wf, sr = sr
* **Returns:**
  wf, sr
