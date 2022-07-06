import pytest

from pygama import lgdo
from pygama.dsp.processing_chain import build_processing_chain


def test_waveform_slicing(geds_raw_tbl):
    dsp_config = {
        "outputs": ["wf_blsub"],
        "processors": {
            "wf_blsub": {
                "function": "bl_subtract",
                "module": "pygama.dsp.processors",
                "args": ["waveform[0:100]", "baseline", "wf_blsub"],
                "unit": "ADC"
            },
        }
    }
    proc_chain, _, tbl_out = build_processing_chain(geds_raw_tbl, dsp_config)
    proc_chain.execute(0, 1)

    assert list(tbl_out.keys()) == ["wf_blsub"]
    assert isinstance(tbl_out["wf_blsub"], lgdo.WaveformTable)
    assert tbl_out["wf_blsub"].wf_len == 100


def test_processor_none_arg(geds_raw_tbl):
    dsp_config = {
        "outputs": ["wf_cum"],
        "processors": {
            "wf_cum": {
                "function": "cumsum",
                "module": "numpy",
                "args": ["waveform", 1, None, "wf_cum"],
                "kwargs": {"signature": "(n),(),()->(n)", "types": ["fii->f"]},
                "unit": "ADC"
            }
        }
    }
    proc_chain, _, _ = build_processing_chain(geds_raw_tbl, dsp_config)
    proc_chain.execute(0, 1)

    dsp_config["processors"]["wf_cum"]["args"][2] = "None"
    proc_chain, _, _ = build_processing_chain(geds_raw_tbl, dsp_config)
    proc_chain.execute(0, 1)


def test_processor_kwarg_assignment(geds_raw_tbl):
    dsp_config = {
        "outputs": ["wf_cum"],
        "processors": {
            "wf_cum": {
                "function": "cumsum",
                "module": "numpy",
                "args": ["waveform", "axis=1", "out=wf_cum"],
                "kwargs": {"signature": "(n),()->(n)", "types": ["fi->f"]},
                "unit": "ADC"
            }
        }
    }
    proc_chain, _, _ = build_processing_chain(geds_raw_tbl, dsp_config)
    proc_chain.execute(0, 1)

    dsp_config["processors"]["wf_cum"]["args"][1] = "dtypo=None"
    proc_chain, _, _ = build_processing_chain(geds_raw_tbl, dsp_config)
    with pytest.raises(TypeError):
        proc_chain.execute(0, 1)


def test_processor_dtype_arg(geds_raw_tbl):
    dsp_config = {
        "outputs": ["wf_cum"],
        "processors": {
            "wf_cum": {
                "function": "cumsum",
                "module": "numpy",
                "args": ["waveform", "axis=0", "dtype='int32'", "out=wf_cum"],
                "kwargs": {"signature": "(n),(),()->(n)", "types": ["fiU->i"]},
                "unit": "ADC"
            }
        }
    }
    proc_chain, _, _ = build_processing_chain(geds_raw_tbl, dsp_config)
    proc_chain.execute(0, 1)


def test_scipy_gauss_filter(geds_raw_tbl):
    dsp_config = {
        "outputs": ["wf_gaus"],
        "processors": {
            "wf_gaus": {
                "function": "gaussian_filter1d",
                "module": "scipy.ndimage",
                "args": [
                    "waveform", "0.1*us", "mode='reflect'", "truncate=3",
                    "output=wf_gaus"
                ],
                "kwargs": {"signature": "(n),(),(),()->(n)", "types": ["ffUf->f"]},
                "unit": "ADC"
            }
        }
    }
    proc_chain, _, _ = build_processing_chain(geds_raw_tbl, dsp_config)
    proc_chain.execute(0, 1)
