from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        name = request.form['name']
        return render_template_string('''
            <h1>Hello, {{ name }}!</h1>
        ''', name=name)
    return render_template_string('''
        <form method="post">
            <label for="name">What is your name?</label>
            <input type="text" id="name" name="name">
            <button type="submit">Submit</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)