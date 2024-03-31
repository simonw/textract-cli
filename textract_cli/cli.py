import boto3
import click
import textract_cli.tables as text_tables

@click.command()
@click.version_option()
@click.argument("image_path", type=click.Path(exists=True))
@click.option(
    "-o", "--output", type=click.File("w"), help="Output file to write the results to"
)
@click.option(
    "-t", "--table", is_flag=True, show_default=True, default=False, help="Write table(s) to output in csv format."
)
def cli(image_path, output, table):
    """CLI tool to extract text from an image using AWS Textract."""
    # Create a Textract client
    client = boto3.client("textract")

    # Read the image as bytes
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    if table:
        # Call the analyze_document API and collect the tables
        detected_text = text_tables.get_table_csv_results(client,image_bytes)
    else:
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
