from flask import Flask, render_template, request, send_file
from gen_ai import generate_csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    category = request.form.get('category')
    
    if not category:
        return "Category not selected.", 400  # Handle case where no category is selected
    
    category = category.capitalize()  # Ensure correct casing
    
    if category not in ['Collaboration', 'Quality Assurance', 'Marketing', 'Development']:
        return "Invalid category selected.", 400

    output_file = "leads.csv"
    try:
        # Generate CSV file using the AI script
        generate_csv(category, output_file)
        # Return the generated CSV file to the user
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return f"Error generating CSV: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
