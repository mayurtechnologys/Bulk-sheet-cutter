# Image Cropping and Processing Tool

This project is a **Python-based GUI tool** for cropping specific regions from multiple images. You can mark and save **photo areas** and **signature areas** from scanned sheets, with the output saved in organized folders. It allows processing multiple sheets sequentially and ensures each cropped image is saved with unique filenames.

## 🛠 Features

- **Interactive Cropping:** Draw rectangles using the mouse to select areas.
- **Multiple Image Support:** Automatically processes all images from the `sheet` folder.
- **Save Photo and Signature Areas:** Separate cropped outputs for photos and signatures.
- **Automatic Folder Creation:** Creates `photos` and `sign` folders for saving output images.
- **Image Compression:** Cropped images are saved under 20 KB without compromising quality.
  
---

## 🚀 How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/image-cropping-tool.git
cd image-cropping-tool
```

### 2. Install Dependencies
This project requires **OpenCV**. You can install it with:
```bash
pip install opencv-python-headless numpy
```

### 3. Prepare the `sheet` Folder
- Place all your input images (sheets) inside a folder named **`sheet`**.
- Supported image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`.

### 4. Run the Program
```bash
python your_script_name.py
```

---

## 🖱 Runtime Controls

| **Action**                     | **Key / Mouse**            |
|---------------------------------|----------------------------|
| Draw a rectangle                | Click + Drag (Left Mouse)  |
| Add the selection as a **photo**| Press `p`                  |
| Add the selection as a **signature** | Press `s`            |
| Clear all selections            | Press `c`                  |
| Save and move to the next image | Press `q`                  |

---

## 📂 Output

- **Photos Folder:** Contains all cropped photo areas (`photo_<image_index>_<box_index>.jpg`).
- **Signatures Folder:** Contains all cropped signature areas (`sign_<image_index>_<box_index>.jpg`).

Each image is saved with a unique filename to avoid overwriting.

---

## 🔧 Image Compression Logic

Cropped images are saved with **compressed JPEG quality** under **20 KB**. If the initial size exceeds 20 KB, the compression level is gradually reduced until the target size is reached.

---

## Troubleshooting

- **No images loaded:** Make sure the `sheet` folder exists and contains valid image files.
- **Key commands not working:** Ensure the image window is active (click on it before using the keyboard).
- **Overwritten output files:** Use the latest version of the code with unique filename logic.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🤝 Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!

---

## 🧑‍💻 Author

**[Mayur Chavan / NikolaIndustry]**  
Developed with ❤️ for interactive image processing needs.
