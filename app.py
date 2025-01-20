import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
from flask import Flask, render_template, request
import matplotlib

# Set the matplotlib backend to Agg (non-GUI)
matplotlib.use('Agg')

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'zip'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_zip(filepath):
    """Extract ZIP files and return the path of the first valid dataset file."""
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(UPLOAD_FOLDER)
        for file in zip_ref.namelist():
            if allowed_file(file):
                return os.path.join(UPLOAD_FOLDER, file)
    return None

def generate_visualizations(data, file_identifier):
    """Generate visualizations and save them with a unique identifier."""
    output_images = []
    
    # Separate numeric and non-numeric columns
    numeric_data = data.select_dtypes(include=['number'])
    categorical_data = data.select_dtypes(include=['object', 'category'])
    
    # Create unique folder for each upload
    unique_folder = os.path.join(OUTPUT_FOLDER, file_identifier)
    os.makedirs(unique_folder, exist_ok=True)
    
    # 1. Line plot for numeric columns
    if numeric_data.shape[1] >= 2:
        plt.figure(figsize=(10, 6))
        numeric_data.plot()
        output_path = os.path.join(unique_folder, 'line_plot.png')
        plt.savefig(output_path)
        output_images.append(f'images/{file_identifier}/line_plot.png')
        plt.close()
    
    # 2. Correlation Heatmap for numeric columns
    if numeric_data.shape[1] > 1:
        plt.figure(figsize=(10, 6))
        sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm')
        output_path = os.path.join(unique_folder, 'heatmap.png')
        plt.savefig(output_path)
        output_images.append(f'images/{file_identifier}/heatmap.png')
        plt.close()
    
    # 3. Bar plot for first categorical column (if exists)
    if not categorical_data.empty:
        first_cat_col = categorical_data.columns[0]
        plt.figure(figsize=(10, 6))
        data[first_cat_col].value_counts().plot(kind='bar')
        output_path = os.path.join(unique_folder, 'bar_plot.png')
        plt.savefig(output_path)
        output_images.append(f'images/{file_identifier}/bar_plot.png')
        plt.close()
    
    # 4. Scatter plot for first two numeric columns
    if numeric_data.shape[1] >= 2:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=numeric_data.columns[0], y=numeric_data.columns[1], data=numeric_data)
        output_path = os.path.join(unique_folder, 'scatter_plot.png')
        plt.savefig(output_path)
        output_images.append(f'images/{file_identifier}/scatter_plot.png')
        plt.close()
    
    # 5. Pie chart for first categorical column
    if not categorical_data.empty:
        first_cat_col = categorical_data.columns[0]
        plt.figure(figsize=(10, 6))
        data[first_cat_col].value_counts().plot(kind='pie', autopct='%1.1f%%')
        output_path = os.path.join(unique_folder, 'pie_chart.png')
        plt.savefig(output_path)
        output_images.append(f'images/{file_identifier}/pie_chart.png')
        plt.close()
    
    return output_images

@app.route('/', methods=['GET', 'POST'])
def upload_and_visualize():
    images = []
    if request.method == 'POST':
        try:
            # Check if the file is in the request
            if 'file' not in request.files:
                return render_template('upload_and_results.html', images=[], error="No file part in the request.")
            
            file = request.files['file']

            # Check if a file is selected
            if file.filename == '':
                return render_template('upload_and_results.html', images=[], error="No file selected.")

            # Validate file extension
            if not allowed_file(file.filename):
                return render_template('upload_and_results.html', images=[], error="Invalid file type. Only CSV, Excel, or ZIP files are allowed.")

            # Save the uploaded file
            file_identifier = file.filename.rsplit('.', 1)[0]  # Unique identifier based on filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Handle ZIP files
            if file.filename.endswith('.zip'):
                extracted_file = extract_zip(filepath)
                if not extracted_file:
                    return render_template('upload_and_results.html', images=[], error="No valid dataset found in the ZIP file.")
                filepath = extracted_file

            # Load the dataset
            if filepath.endswith('.csv'):
                data = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx'):
                data = pd.read_excel(filepath)
            else:
                return render_template('upload_and_results.html', images=[], error="Unsupported file format.")

            # Generate visualizations
            images = generate_visualizations(data, file_identifier)

        except Exception as e:
            # Print the error message to the console for debugging
            print(f"Error: {str(e)}")
            return render_template('upload_and_results.html', images=[], error=f"An error occurred: {str(e)}")

    return render_template('upload_and_results.html', images=images, error=None)

if __name__ == '__main__':
    app.run(debug=True)
