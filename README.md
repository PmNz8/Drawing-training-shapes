# 🖊️ Drawing Training Shapes

A simple Python script collection for generating practice sheets to improve your accuracy and confidence with a thin-liner or pencil.

---

## 📄 `elipses.py`

Generates a **10-page A4 PDF** filled with randomly sized and shaped ellipses made of dots.

🎯 Ideal for practicing **freehand ellipse drawing**. Helps you assess:
- How accurate your ellipses are
- How confident and steady your lines feel

📷 Example:
![Ellipses Example](https://github.com/user-attachments/assets/1c9eeef8-fe2b-4465-ac9e-4ce101537c3e)

---

## 📄 `points.py`

Generates a **10-page A4 PDF**, each page containing up to **25 pseudo-randomly placed dots**.

🎯 Great for practicing **line drawing from point A to point B**. Helps you check:
- How close your line ends at the target point
- How confident and straight your stroke is

📷 Example:
![Points Example](https://github.com/user-attachments/assets/0a015cee-bef2-475a-b234-c9b96c798f7b)

---

## 🪟 Windows Users

If you're on **Windows**, you can download precompiled `.exe` files from the [Releases](../../releases) tab.

✅ Just click and run — no installation needed.

> **Note**:  
> - **Ellipses** generation may take some time  
> - **Points** generation is instant  
> - Output PDF will be saved in the same folder as the `.exe` file

---

## 💻 Python Usage

To run via Python:
```bash
python elipses.py
# or
python points.py


Requires reportlab:
pip install reportlab
