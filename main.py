import tkinter as tk
from tkinter import filedialog, messagebox
import docx
import PyPDF2
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# Download NLTK data (do once)
nltk.download('punkt')
nltk.download('stopwords')

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return '\n'.join([page.extract_text() for page in reader.pages if page.extract_text()])

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(words)

def calculate_similarity(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(similarity * 100, 2)


def select_resume():
    file = filedialog.askopenfilename(filetypes=[("Document files", "*.docx *.pdf")])
    resume_path.set(file)

def select_job_description():
    file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    job_path.set(file)

def match_resume():
    resume_file = resume_path.get()
    job_file = job_path.get()

    if not os.path.exists(resume_file) or not os.path.exists(job_file):
        messagebox.showerror("File Error", "Please select valid files.")
        return

    try:
        if resume_file.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_docx(resume_file)

        with open(job_file, 'r', encoding='utf-8') as f:
            job_text = f.read()

        resume_clean = preprocess_text(resume_text)
        job_clean = preprocess_text(job_text)

        score = calculate_similarity(resume_clean, job_clean)
        result_label.config(text=f"🔍 Match Score: {score}%", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process files: {e}")

# Tkinter GUI
root = tk.Tk()
root.title("Resume Matcher - GUI")
root.geometry("1200x700")
root.config(bg="#f0f0f0")

resume_path = tk.StringVar()
job_path = tk.StringVar()

tk.Label(root, text="Resume File:", bg="#f0f0f0").pack(pady=(20, 5))
tk.Entry(root, textvariable=resume_path, width=60).pack()
tk.Button(root, text="Browse Resume", command=select_resume).pack(pady=5)

tk.Label(root, text="Job Description File:", bg="#f0f0f0").pack(pady=5)
tk.Entry(root, textvariable=job_path, width=60).pack()
tk.Button(root, text="Browse Job Description", command=select_job_description).pack(pady=5)

tk.Button(root, text="Match Now", bg="#007acc", fg="white", command=match_resume).pack(pady=20)
result_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f0f0f0")
result_label.pack()

root.mainloop() 