"""
Streamlit File‑Integrity Reporting Tool

This application allows users to generate and compare file integrity reports using
SHA‑256 checksums.  Users can either upload a set of files to create a baseline
checksum report, or upload both a baseline report and a new set of files to
identify additions, modifications and missing files.  All functionality is
contained in this single Streamlit script.

Usage:
    streamlit run streamlit_app.py

The app provides two modes of operation:

    • **Generate Baseline** – upload one or more files and compute SHA‑256
      checksums for each.  The resulting report can be downloaded as a CSV
      file for future comparisons.

    • **Compare With Baseline** – upload a previously generated baseline CSV
      and one or more new files.  The app will compute checksums for the
      uploaded files, compare them to the baseline, and highlight which
      files have changed, which are new, and which are missing.

The tool uses only standard Python libraries and the Streamlit API, so it
requires no additional packages beyond Streamlit itself.  Data downloads are
performed entirely within the browser to avoid exposing file contents.
"""

import io
import hashlib
import pandas as pd
import streamlit as st


def compute_checksums(files):
    """Return a DataFrame containing filenames and SHA‑256 checksums.

    Parameters
    ----------
    files : list of UploadedFile
        List of files uploaded via Streamlit.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ['filename', 'sha256'].
    """
    records = []
    for uploaded_file in files:
        # Read file content as bytes
        data = uploaded_file.read()
        # Compute SHA‑256 checksum
        checksum = hashlib.sha256(data).hexdigest()
        records.append({"filename": uploaded_file.name, "sha256": checksum})
    df = pd.DataFrame(records)
    return df


def compare_checksums(baseline_df, new_df):
    """Compare two checksum DataFrames and flag changes.

    Returns a DataFrame with columns:
        filename, baseline_sha256, new_sha256, status

    Status values:
        'unchanged' – checksum matches baseline
        'modified'  – checksum differs from baseline
        'new'       – file not present in baseline
        'missing'   – baseline file not uploaded in new files
    """
    # Merge on filename
    merged = pd.merge(
        baseline_df, new_df, on="filename", how="outer", suffixes=("_baseline", "_new")
    )
    statuses = []
    for _, row in merged.iterrows():
        baseline_hash = row.get("sha256_baseline")
        new_hash = row.get("sha256_new")
        if pd.isna(baseline_hash):
            status = "new"
        elif pd.isna(new_hash):
            status = "missing"
        elif baseline_hash == new_hash:
            status = "unchanged"
        else:
            status = "modified"
        statuses.append(status)
    merged["status"] = statuses
    return merged[["filename", "sha256_baseline", "sha256_new", "status"]]


def main():
    st.title("File‑Integrity Reporting Tool")
    st.write(
        "Use this app to generate SHA‑256 checksum reports for uploaded files and\n"
        "compare them against a baseline report to identify changes."
    )

    # Sidebar for mode selection
    mode = st.sidebar.radio(
        "Select mode", ["Generate Baseline", "Compare With Baseline"]
    )

    if mode == "Generate Baseline":
        st.header("Generate Baseline Checksums")
        files = st.file_uploader(
            "Upload one or more files to generate a baseline report",
            accept_multiple_files=True,
        )
        if files:
            df = compute_checksums(files)
            st.subheader("Checksum Report")
            st.dataframe(df)
            # Provide download button
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV Report",
                data=csv_bytes,
                file_name="baseline_checksums.csv",
                mime="text/csv",
            )
        else:
            st.info("Upload files to generate a baseline checksum report.")

    elif mode == "Compare With Baseline":
        st.header("Compare Current Files With Baseline")
        baseline_file = st.file_uploader(
            "Upload baseline CSV report", type="csv", key="baseline"
        )
        new_files = st.file_uploader(
            "Upload current files for comparison",
            accept_multiple_files=True,
            key="new_files",
        )
        if baseline_file and new_files:
            try:
                baseline_df = pd.read_csv(baseline_file)
            except Exception as e:
                st.error(f"Failed to read baseline CSV: {e}")
                return
            # Ensure the baseline DataFrame has expected columns
            if not {"filename", "sha256"}.issubset(baseline_df.columns):
                st.error(
                    "Baseline CSV must contain at least two columns: 'filename' and 'sha256'"
                )
                return
            # Rename columns to match our merge logic
            baseline_df = baseline_df[["filename", "sha256"]]
            # Compute new checksums
            new_df = compute_checksums(new_files)
            # Perform comparison
            comparison_df = compare_checksums(baseline_df, new_df)
            st.subheader("Comparison Results")
            st.dataframe(comparison_df)
            # Download comparison report
            csv_bytes = comparison_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Comparison Report",
                data=csv_bytes,
                file_name="comparison_report.csv",
                mime="text/csv",
            )
        else:
            st.info(
                "Upload a baseline checksum CSV and the current files you wish to compare."
            )


if __name__ == "__main__":
    main()