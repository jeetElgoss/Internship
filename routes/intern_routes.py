from flask import Blueprint, request, render_template,send_file
import pandas as pd
import base64
import os
import binascii

intern_bp = Blueprint('intern', __name__)

folder_path = "intern/profile/INT_2025"


@intern_bp.route('/image/<image_name>')
def serve_image(image_name):
    image_path = os.path.join(folder_path, image_name)
    print(f"Attempting to serve image: {image_path}")  # Debug print
    if not os.path.exists(image_path):
        print(f"File does not exist: {image_path}")  # Debug print
        return "Image not found", 404
    return send_file(image_path)


@intern_bp.route('/intern', methods=['GET'])
def get_intern():
    intern_id_encoded = request.args.get('intern_id')
    print(f"intern_id_encoded: {intern_id_encoded}")

    # Validate intern_id parameter
    if not intern_id_encoded:
        return render_template("error.html", error_message="Missing intern_id parameter")

    try:
        # Decode base64 intern_id
        try:
            intern_id_bytes = base64.b64decode(intern_id_encoded)
            intern_id = intern_id_bytes.decode('utf-8')
            print(f"intern_id: {intern_id}")
        except binascii.Error:
            return render_template("error.html", error_message="Invalid base64-encoded intern_id")
        except UnicodeDecodeError:
            return render_template("error.html", error_message="Failed to decode intern_id as UTF-8")

        # Validate intern_id format
        if '-' not in intern_id:
            return render_template("error.html", error_message="Invalid intern_id format. Expected format: prefix-year")

        year = intern_id.split('-')[1]
        print(f"year: {year}")

        # Construct and validate file path
        excel_file = os.path.join("intern", "excel", f"INT_{year}.xlsx")
        if not os.path.exists(excel_file):
            return render_template("error.html", error_message=f"Excel file not found: {excel_file}")

        # Read Excel file
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return render_template("error.html", error_message=f"Failed to read Excel file: {str(e)}")

        # Search for matching intern
        for index, row in df.iterrows():
            if str(row['Intern Id']).strip() == intern_id:
                profile_filename = os.path.basename(row['Profile'])  # Gets 'Aman Pandey.jpg'
                image_url = f"/image/{profile_filename}"
                data = {
                    'intern_id': row['Intern Id'],
                    'name': row['Name'],
                    'father_name': row['Father Name'],
                    'contact': row['Contact'],
                    'email': row['E-mail'],
                    'branch': row['Branch'],
                    'collage_name': row['Collage Name'],
                    'duration': row['Duration'],
                    'collage_name': row['Collage Name'],
                    'duration': row['Duration'],
                    'profile': image_url,
                    'sd': str(row['Start Date']).split(" ")[0],
                    'ed': str(row['End Date']).split(" ")[0],
                }
                return render_template("profile.html", data=data)

        return render_template("error.html", error_message=f"No intern found with ID: {intern_id}")

    except IndexError:
        return render_template("error.html", error_message="Invalid intern_id format. Year not found.")
    except Exception as e:
        return render_template("error.html", error_message=f"An unexpected error occurred: {str(e)}")