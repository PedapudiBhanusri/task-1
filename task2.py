import pdfplumber

def extract_tables_from_page(pdf_path, page_number):
    """
    Extract tables from a specific page in a PDF file.
    """
    with pdfplumber.open(pdf_path) as pdf:
        if page_number < 0 or page_number >= len(pdf.pages):
            return None
        page = pdf.pages[page_number]
        tables = page.extract_tables()
        return tables

def format_table_output(tables):
    """
    Format the extracted tables into a readable string format.
    """
    output = ""
    if tables:
        for i, table in enumerate(tables):
            output += f"\nTable {i + 1}:\n"
            for row in table:
                output += " | ".join(str(cell) if cell else "" for cell in row) + "\n"
    else:
        output += "No tables found on this page."
    return output

def handle_query(user_query, pdf_path):
    """
    Handle user query to extract tables from a specified PDF page.
    """
    try:
        # Extract the page number from the user's query.
        page_number = int(user_query.split("page")[1].strip()) - 1
    except (IndexError, ValueError):
        return "Invalid query format. Please specify a valid page number (e.g., 'page 2')."

    # Extract tables from the specified page.
    tables = extract_tables_from_page(pdf_path, page_number)
    if tables is None:
        return f"The specified page {page_number + 1} does not exist in the PDF."

    # Format and return the response.
    response = f"Tables found on page {page_number + 1}:\n"
    response += format_table_output(tables)
    return response

if __name__ == "__main__":
    # Path to the PDF file
    pdf_path = r"C:\Users\Bhanu Sri\tables.pdf"  # Update this path with your file's location
    # Take user input for the query
    user_query = input("Enter your query (e.g., 'page 2'): ")
    # Process the query and print the result
    response = handle_query(user_query, pdf_path)
    print(response)
