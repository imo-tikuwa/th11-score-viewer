from flask import Flask, render_template, request
import io

app = Flask(__name__, static_folder = 'assets')
# 10MBまでアップロード可
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


@app.route("/", methods=['GET'])
def index():
    # トップ画面表示
    return render_template("index.html")


@app.route("/", methods=['POST'])
def disp_chart():
    # グラフ表示

    # CSVファイル1は必須
#     if 'csv_file1' not in request.files:
#         return render_template("index.html")
#
#     csv_file1 = request.files.get('csv_file1')
#     if csv_file1.mimetype != 'text/csv':
#         return render_template("index.html")
#
#     text_stream = io.TextIOWrapper(csv_file1.stream, encoding = 'cp932')
#     for row in csv.reader(text_stream):
#         print(row)






    return render_template("charts.html")


if __name__ == "__main__":
    app.run(debug=True)
#     app.run()