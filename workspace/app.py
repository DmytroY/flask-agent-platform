from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        name = request.form.get('name', 'World')
        return render_template_string('Hello, {{ name }}!', name=name)
    return render_template_string('''
        <form method="post">
            <label for="name">What is your name?</label>
            <input type="text" id="name" name="name">
            <button type="submit">Send</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)