from flask import Blueprint, request, jsonify, render_template
from utils.read_excel import ReadExcel
from utils.date_utils import DateHelper
import pandas as pd
import qrcode
import os
import base64
from werkzeug.exceptions import BadRequest, NotFound

qr_bp = Blueprint('qr', __name__)

@qr_bp.route("/")
def index():
    return render_template("index.html")

@qr_bp.route("/generate_qr_codes")
def generate_qr_codes():
    # Read Excel file
    year = request.args.get('year')
    excel_file = os.path.join("intern/excel", f"INT_{year}.xlsx")
    df = ReadExcel.read_excel(excel_file)

    # Create output directory for QR codes
    year = DateHelper.get_year()
    year_folder = f'intern/qr_code/{year}'
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)

    # Process each student
    for index, column in df.iterrows():
        intern_id = column['Intern Id']
        intern_id_encoded = base64.urlsafe_b64encode(str(intern_id).encode()).decode()
        # qr_url = f"http://127.0.0.1:5000/intern?intern_id={intern_id_encoded}"
        # Create QR code URL for production
        qr_url = f"https://internship.elgoss.com/intern?intern_id={intern_id_encoded}"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)

        # Save QR code as image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(f"intern/qr_code/{year}/QR_{intern_id}.png")
    return "QR-code generated"

@qr_bp.route("/get_intern_dropdown", methods=["POST"])
def get_intern_dropdown():
    try:
        data = request.get_json()
        if not data or 'year' not in data:
            raise BadRequest("Year is required in the request body")

        year = data.get('year')
        if not str(year).isdigit() or len(str(year)) != 4:
            raise BadRequest("Invalid year format. Please provide a 4-digit year")

        file_path = os.path.join("intern/excel", f"INT_{year}.xlsx")
        if not os.path.exists(file_path):
            raise NotFound(f"No data available for year {year}")

        dataframe = pd.read_excel(file_path)
        if dataframe.empty:
            return jsonify({
                "interns": [],
                "message": f"No intern data found for year {year}"
            }), 200

        intern_list = [
            {
                'intern_id': base64.urlsafe_b64encode(str(row['Intern Id']).encode()).decode(),
                'name': row['Name']
            }
            for _, row in dataframe.iterrows()
        ]

        return jsonify({
            "interns": intern_list,
            "message": "Intern data retrieved successfully"
        }), 200

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500