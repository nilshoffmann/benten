import pathlib

import pytest

from benten.editing.cwldoc import CwlDoc


current_path = pathlib.Path(__file__).parent


def test_basics_salmon():

    wf_path = pathlib.Path(current_path, "cwl/sbg/salmon.cwl")
    c = CwlDoc(raw_cwl=wf_path.open("r").read(), path=wf_path, inline_path=None)
    cwl = c.cwl_dict

    assert c.process_type() == "Workflow"

    assert cwl["steps"]["Salmon_Quant___Reads"]["in"]["salmon_index_archive"].start_line == 2093
    assert cwl["steps"]["Salmon_Quant___Reads"]["in"]["salmon_index_archive"]["source"] == "Salmon_Index/salmon_index_archive"


def test_inline_salmon():

    wf_path = pathlib.Path(current_path, "cwl/sbg/salmon.cwl")
    c = CwlDoc(raw_cwl=wf_path.open("r").read(), path=wf_path, inline_path=None)

    c2 = c.get_nested_inline_step(["SBG_Create_Expression_Matrix___Transcripts"])
    cwl = c2.cwl_dict

    assert c2.process_type() == "CommandLineTool"

    assert cwl["class"] == "CommandLineTool"
    assert cwl["inputs"]["output_name"].start_line == 634 - 629

    c2 = c.get_nested_inline_step(["Salmon_Quant___Reads"])
    cwl = c2.cwl_dict

    assert cwl["class"] == "CommandLineTool"
    assert cwl["outputs"]["mapping_info"].start_line == 2955 - 2160


def test_nested_inline():

    wf_path = pathlib.Path(current_path, "cwl/002.nested.inline.sbg.eco/wf3.cwl")
    c = CwlDoc(raw_cwl=wf_path.open("r").read(), path=wf_path, inline_path=None)

    c2 = c.get_nested_inline_step(["wf2", "wf1", "wf0", "split"])
    cwl = c2.cwl_dict

    assert cwl["class"] == "CommandLineTool"
    assert cwl["inputs"]["input"].start_line == 1021 - 1013

    c2 = c.get_nested_inline_step(["wf2", "wf1", "wf0"])
    cwl = c2.cwl_dict

    assert cwl["steps"]["pass_through"]["in"]["input"].start_line == 1071 - 987

    with pytest.raises(RuntimeError):
        c3 = c2.get_nested_inline_step(("split",))


def test_nested_inline_both_list_and_dict():
    # Need to make sure we handle both lists and dicts

    wf_path = pathlib.Path(current_path, "cwl/001.basic/wf-nested-step-as-dict.cwl")
    c = CwlDoc(raw_cwl=wf_path.open("r").read(), path=wf_path, inline_path=None)

    c2 = c.get_nested_inline_step(("s1",))
    cwl = c2.cwl_dict

    assert cwl["class"] == "CommandLineTool"
    assert cwl["inputs"].start_line == 23 - 21

    wf_path = pathlib.Path(current_path, "cwl/001.basic/wf-nested-step-as-dict.cwl")
    c = CwlDoc(raw_cwl=wf_path.open("r").read(), path=wf_path, inline_path=None)

    c2 = c.get_nested_inline_step(("s1",))
    cwl = c2.cwl_dict

    assert cwl["class"] == "CommandLineTool"
    assert cwl["inputs"].start_line == 23 - 21
