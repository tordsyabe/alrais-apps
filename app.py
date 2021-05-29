from flask import Flask, render_template, request, send_file, request, jsonify

from datetime import datetime

from flask_cors import cross_origin

from barcode import create_barcodes
from name_tag import create_name_tag
from amazon_scrape import scrape_data

from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'alrais.meeting.rooms@gmail.com'
app.config['MAIL_PASSWORD'] = 'alraisgroup@2021'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create-name-tags', methods=['GET'])
def create_name_tags():
    return render_template('name-tag.html')


@app.route('/amazon-price-list', methods=['GET'])
def amazon_price_list():
    return render_template('amazon-price-list.html')


@app.route('/create', methods=['POST'])
def generate():
    if request.method == 'POST':
        barcode = request.form['barcode']
        if barcode == '':
            return render_template('index.html', message='Please enter required fields')

        stripped_barcode = barcode.strip()

        create_barcodes(stripped_barcode)
        return send_file(stripped_barcode + '.pdf', as_attachment=True)


@app.route('/name-tag', methods=['POST'])
def name_tag():
    if request.method == 'POST':
        content = request.json
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")
        create_name_tag(content['names'], timestampStr)
        print(timestampStr + '.pdf')
        return {"filename": timestampStr + '.pdf'}


@app.route('/amazon-scrape', methods=['POST'])
def amazon_scrape():
    if request.method == 'POST':
        asin = request.form['asin']
        if asin == '':
            return render_template('amazon-price-list.html', message='Please enter required fields')
        asins = asin.split(',')
        print(asins)
        vendors = scrape_data(asins)
        if isinstance(vendors, str):
            merged_list = vendors
        else:
            merged_list = [(vendors[0][i], vendors[1][i], vendors[2][i], vendors[3][i]) for i in
                           range(0, len(vendors[0]))]
        print(merged_list)
        return render_template('amazon-price-list.html', table_data=merged_list)


@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        filename = request.form['filename']
        return send_file(filename, as_attachment=True)


@app.route('/download-amazon-price-list', methods=['POST'])
def download_amazon_price_list():
    if request.method == 'POST':
        filename = request.form['filename']
        return send_file('amazon-prices.xlsx', as_attachment=True)

@app.route('/send-verification-email', methods=['POST'])
@cross_origin()
def send_verification_email():
    if request.method == 'POST':
        content = request.json
        # meeting_id = content['data'].get('id')
        recipient = content['data'].get('organizer')
        msg = Message('Verify your booked meeting', sender='alrais.meeting-rooms@gmail.com', recipients=[recipient])
        # msg.body = f"Please click the link to verify your booked meeting http://192.168.10.70:3000/verify?email={recipient}&meeting_id={meeting_id}"
        msg.html = render_template("email.html", details=content['data'])
        mail.send(msg)
        return {"result": "Verification email sent, please verify your booking."}

@app.route('/send-approved-email', methods=['POST'])
@cross_origin()
def send_approved_email():
    if request.method == 'POST':
        content = request.json
        # meeting_id = content['data'].get('id')
        recipient = content['data'].get('organizer')
        msg = Message('Your meeting is approved', sender='alrais.meeting-rooms@gmail.com', recipients=[recipient])
        # msg.body = f"Please click the link to verify your booked meeting http://192.168.10.70:3000/verify?email={recipient}&meeting_id={meeting_id}"
        msg.html = render_template("approved-mail.html", details=content['data'])
        mail.send(msg)
        return {"result": "Your meeting had been approved."}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.debug(True)
