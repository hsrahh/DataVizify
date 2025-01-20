# **DataVizify**  
An interactive web application to upload datasets and generate insightful visualizations, such as charts, graphs, and heatmaps, all in one place.  

## **Features**  
- Upload CSV, Excel, or ZIP files containing datasets.  
- Automatic visualization of data through:  
  - Line plots  
  - Bar charts  
  - Correlation heatmaps  
  - Scatter plots  
  - Pie charts  
- Handles both numeric and non-numeric data seamlessly.  
- Displays visualizations on the same page for an intuitive user experience.  
- Error handling for unsupported file types and invalid datasets.  

---

## **Tech Stack**  
- **Backend**: Python, Flask  
- **Frontend**: HTML, CSS, Jinja2  
- **Visualization**: Matplotlib, Seaborn, Pandas  

---

## **Getting Started**  
  

### **Installation**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/hsrahh/DataVizify.git
   cd DataVizify
   ```  
2. Create and activate a virtual environment:  
   ```bash
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```  

---

## **Usage**  
1. Start the Flask application:  
   ```bash
   python app.py
   ```  
2. Open your browser and navigate to:  
   ```
   http://127.0.0.1:5000/
   ```  
3. Upload a dataset file (CSV, Excel, or ZIP).  
4. View the generated visualizations directly on the page.  

---

## **Project Structure**  
```
DataVizify/
│
├── app.py                     # Main Flask application
├── static/                    # Static files
│   ├── images/                # Generated visualization images
│   └── styles/                # CSS styles (if any)
├── templates/                 # HTML templates
│   └── upload_and_results.html
├── uploads/                   # Uploaded datasets
└── README.md                  # Project documentation
```  

---

## **Contributing**  
Contributions are welcome!  
1. Fork the repository.  
2. Create a new branch:  
   ```bash
   git checkout -b feature-name
   ```  
3. Make your changes and commit:  
   ```bash
   git commit -m "Add feature-name"
   ```  
4. Push to your branch:  
   ```bash
   git push origin feature-name
   ```  
5. Submit a pull request.  

---

## **License**  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  

---

## **Contact**  
For any questions or feedback, feel free to reach out:  
- **Email**: harshjoil02@gmail.com  
- **GitHub**: [yourusername](https://github.com/hsrahh)  

--- 

Let me know if you'd like to customize any section further! 😊
