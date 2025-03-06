import os
from dotenv import load_dotenv
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

# Load environment variables from .env file
load_dotenv()

# SharePoint credentials and site information
site_url = os.getenv('SHAREPOINT_SITE_URL')
doc_lib = os.getenv('SHAREPOINT_DOC_LIB')
folder_name = os.getenv('SHAREPOINT_FOLDER')
client_id = os.getenv('SHAREPOINT_CLIENT_ID')
client_secret = os.getenv('SHAREPOINT_CLIENT_SECRET')

# Check if all required environment variables are set
if not all([site_url, doc_lib, folder_name, client_id, client_secret]):
    print("Please ensure all required environment variables are set in the .env file.")
else:
    try:
        # Authenticate with SharePoint
        ctx = ClientContext(site_url).with_credentials(ClientCredential(client_id, client_secret))

        # Get the folder containing the files
        folder = ctx.web.lists.get_by_title(doc_lib).root_folder.folders.get_by_url(folder_name)
        ctx.load(folder)
        ctx.execute_query()

        # Get the files in the folder
        files = folder.files
        ctx.load(files)
        ctx.execute_query()

        # Print the list of files
        if files:
            print(f"Files in '{folder_name}':")
            for file in files:
                print(file.name)
        else:
            print(f"No files found in '{folder_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")