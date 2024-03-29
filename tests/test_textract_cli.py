import boto3
from click.testing import CliRunner
from textract_cli.cli import cli
from moto import mock_aws
from moto.textract.models import TextractBackend
import pytest


TextractBackend.BLOCKS = [{"BlockType": "LINE", "Text": "This is a test image"}]


@mock_aws
@pytest.mark.parametrize("use_output_file", (False, True))
def test_start_document_text_detection(tmp_path, use_output_file):
    image_path = tmp_path / "test_image.jpeg"
    image_path.write_text("This is a test image")

    args = [str(image_path)]

    if use_output_file:
        output_path = tmp_path / "output.txt"
        args.extend(["-o", str(output_path)])

    runner = CliRunner()
    result = runner.invoke(cli, args)
    assert result.exit_code == 0

    expected = "This is a test image"
    if use_output_file:
        assert expected in output_path.read_text("utf-8")
    else:
        assert expected in result.stdout
