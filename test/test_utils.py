from src.utils.create_ref import create_ref
import pytest


class TestCreateRef():
    @pytest.mark.it("creates a reference dict for a single item")
    def test_matches_single_item(self):
        input_data = [[1,  "name_1"]]
        expected_output = {"name_1": 1}
        assert create_ref(input_data, 1, 0) == expected_output

    @pytest.mark.it("creates a reference dict for multiple items")
    def test_matches_multiple_items(self):
        input_data = [[1, True,  "name_1"], [7, True, "name_4"]]
        expected_output = {"name_1": 1, "name_4": 7}
        assert create_ref(input_data, 2, 0) == expected_output
