

# 📂 File‑Integrity Reporting Tool

Have you ever worried that a file on your computer might have been changed without you noticing?  This little app helps you check!  It creates a kind of *digital fingerprint* for each file, so you can tell if anything has been added, removed or modified.  It’s perfect for researchers who need to protect their data, but it’s easy enough for anyone to use.

## 🔍 What does it do?

Every file – whether it’s a document, a photo or a program – can be represented by a unique code called a **checksum**.  If even a single character in the file changes, its checksum changes too.  Our tool computes these codes for your files and saves them as a **baseline**.  Later on, you can run the app again with a fresh set of files and it will tell you which ones are new, missing or modified.

Think of it like taking fingerprints for a bunch of homework assignments on Day 1.  On Day 2, you check the fingerprints again – if a fingerprint has changed, you know someone has tampered with that assignment!

## ✨ Features

* **Generate baseline**: Upload one or more files and create a CSV report with their checksums.  You can download this report and keep it safe.
* **Compare with baseline**: Upload a saved baseline report and a new set of files.  The app will show you which files are:

  * ✅ Unchanged – exactly the same as before.
  * 📝 Modified – the file name matches but the contents are different.
  * ➕ New – not present in the baseline at all.
  * ❌ Missing – listed in the baseline but not in the new upload.
* **CSV downloads**: Download your baseline or comparison results as a CSV file for record‑keeping.

## 🚀 How to use it 

1. **Open the app** (for example on [Streamlit Cloud](https://share.streamlit.io/) or by running it locally).  You’ll see a sidebar with two options.
2. **Generate baseline**: Choose this if it’s your first time.  Click the file uploader and select the files you want to track.  When the table appears, click “Download CSV Report” and save the file (this is your baseline).
3. **Compare with baseline**: Next time you want to check your files, come back, choose this option and upload the baseline CSV from step 2.  Then upload the current versions of your files.  The app will highlight what’s changed and let you download a report.

That’s it!  You don’t need to write any code or install anything beyond the app itself.

## 🎓 Example for a high school student

Let’s say you have two homework essays saved as `essay1.txt` and `essay2.txt`.

1. On Monday you upload both essays in “Generate baseline” mode and download the baseline CSV.  The app remembers their fingerprints.
2. On Wednesday you realise you accidentally edited `essay2.txt` without saving a backup.  You’re not sure what changed.  Go to “Compare with baseline”, upload Monday’s CSV, then upload `essay1.txt` and `essay2.txt` again.
3. The app shows:

   * `essay1.txt` ✅ unchanged
   * `essay2.txt` 📝 modified

Now you know exactly which essay was altered and which wasn’t.  This same idea helps researchers ensure their scientific data hasn’t been tampered with or corrupted.

## 🛠️ Running the app locally

If you want to run this on your own machine:

```bash
pip install streamlit pandas
streamlit run streamlit_app.py
```

Then open the URL `http://localhost:8501` in your web browser to use the app.

## 🌐 Deploying to Streamlit Cloud

1. Create a GitHub repository containing `streamlit_app.py` and a simple `requirements.txt` with the line `streamlit>=1.28.0`.
2. Sign in to [Streamlit Cloud](https://share.streamlit.io/) with your GitHub account.
3. Click **New app**, select your repository and the `streamlit_app.py` file, and press **Deploy**.

Your file‑integrity tool will be live on the web and ready to use!
