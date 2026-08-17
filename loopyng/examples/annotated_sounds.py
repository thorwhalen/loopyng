"""Make annotated sounds"""

import random
import itertools
from itertools import starmap
from functools import partial

import numpy as np

from i2 import Pipe
from slink import dict_generator, GetFromIter, Repeater

from loopyng._optional import optional_import, require
from loopyng.gen.sine_mix import dflt_wf_params_to_wf

# Optional: this example needs the tabular/scaling stack. Bound lazily so the
# module still imports (and documents) without the `data` extra installed.
pd = optional_import(
    "pandas", extra="data", used_by="loopyng.examples.annotated_sounds"
)

# Sentinel for the default scaler. It cannot default to MinMaxScaler().fit_transform
# directly: that would instantiate a scikit-learn object at import time, which is
# exactly what the optional-dependency handling exists to avoid.
DFLT_ANNOTS_DF_TO_WF_PARAMS = "MinMaxScaler"


def _resolve_scaler(scaler_name):
    """Turn a ``sklearn.preprocessing`` class name into its ``fit_transform``."""
    preprocessing = require(
        "sklearn.preprocessing",
        extra="data",
        used_by="loopyng.examples.annotated_sounds",
    )
    return getattr(preprocessing, scaler_name)().fit_transform


def session_phase_rpm_temparature(
    n_sessions=2,
    n_phases_per_session=3,
    n_blocks_per_phase=2,
    average_block_duration=21 * 2048,
    wf_params_cols=(
        "session",
        "phase",
        "rpm",
        "temperature",
    ),  # TODO: perhaps an exclusion list is more general
    annots_df_to_wf_params=DFLT_ANNOTS_DF_TO_WF_PARAMS,
    params_and_duration_to_wf=lambda p, duration: dflt_wf_params_to_wf(
        p, n_samples=duration
    ),
):
    if isinstance(annots_df_to_wf_params, str):
        # Resolved here, not at import time, so this module imports without the
        # `data` extra and only errors (clearly) if the example is actually run.
        annots_df_to_wf_params = _resolve_scaler(annots_df_to_wf_params)
    wf_params_cols = list(wf_params_cols)
    f = dict_generator(
        # make n_sessions copies of the dict so far... i.e. empty dict
        Repeater(n_sessions),
        # --> {}, {}
        #
        # for each, call function and assign to session key
        dict(session=GetFromIter(itertools.count())),
        # --> {'session': 0}, {'session': 1}
        #
        # make n_phases_per_session copies of each
        Repeater(n_phases_per_session),
        # --> {'session': 0}, {'session': 0}, {'session': 0}, ...
        # ... {'session': 1}, {'session': 1}, {'session': 1}
        #
        # for each, make a phase using given (indep) function
        dict(phase=GetFromIter(itertools.cycle(range(n_phases_per_session)))),
        #
        # etc.
        Repeater(n_blocks_per_phase),
        dict(
            rpm=Pipe(partial(random.uniform, 200, 800), int),  # make a randome rpm
            temperature=lambda rpm: int(
                rpm * random.uniform(0.5, 2) / 50
            ),  # use the rpm to compute temperature
            duration=lambda: int(average_block_duration * random.random()),
        ),
    )
    annots_df = pd.DataFrame(f())
    annots_df["timestamp"] = list(itertools.accumulate(annots_df["duration"]))
    wf_params = annots_df_to_wf_params(annots_df[wf_params_cols])

    wf = np.hstack(
        list(starmap(params_and_duration_to_wf, zip(wf_params, annots_df["duration"])))
    )

    return annots_df.to_dict(orient="records"), wf
