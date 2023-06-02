from flask import Flask, render_template, request, redirect, url_for
from forms import UploadForm
from analysis import process_uploaded_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        output_file_path = process_uploaded_file(file_path)
        return redirect(url_for('success', file=output_file_path))
    return render_template('upload.html', form=form)

@app.route('/success')
def success():
    file_path = request.args.get('file')
    return render_template('success.html', file=file_path)

if __name__ == '__main__':
    app.run(debug=True)
