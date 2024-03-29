import boto3
import click


@click.command()
@click.version_option()
@click.argument("image_path", type=click.Path(exists=True))
@click.option(
    "-o", "--output", type=click.File("w"), help="Output file to write the results to"
)
def cli(image_path, output):
    """CLI tool to extract text from an image using AWS Textract."""
    # Create a Textract client
    client = boto3.client("textract")

    # Read the image as bytes
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    # Call the detect_document_text API
    response = client.detect_document_text(Document={"Bytes": image_bytes})
    # Collect the detected text
    detected_text = "\n".join(
        item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"
    )

    # Output the results
    if output:
        output.write(detected_text)
    else:
        click.echo(detected_text)
