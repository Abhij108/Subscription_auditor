import { useState } from "react";
import { analyzeCSV } from "../services/api";
import "./UploadBox.css";

function UploadBox({ onResult }) {
    const [loading, setLoading] = useState(false);

    const handleUpload = async (event) => {
        const file = event.target.files[0];

        if (!file) return;

        setLoading(true);

        try {
            const data = await analyzeCSV(file);
            onResult(data);
        } catch (error) {
            console.error(error);
            alert("Unable to analyze CSV");
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="upload-section">

            <div className="upload-container">

                {/* Header */}
                <div className="upload-header">

                    <div className="header-content">

                        <div className="brand-badge">
                            SUBSCRIPTION AUDITOR
                        </div>

                        <h1>
                            Know where your
                            <span> money goes.</span>
                        </h1>

                        <p>
                            Analyze your bank statement and discover
                            recurring payments, subscriptions and
                            hidden expenses.
                        </p>

                    </div>

                    <div className="header-icon">
                        ₹
                    </div>

                </div>


                {/* Upload Card */}
                <div className="upload-card">

                    <div className="upload-icon">
                        ↑
                    </div>

                    <h2>
                        Upload Bank Statement
                    </h2>

                    <p className="upload-description">
                        Upload your CSV bank statement to analyze
                        your spending automatically.
                    </p>


                    {/* File Input */}
                    <label className="file-input">

                        <input
                            type="file"
                            accept=".csv"
                            onChange={handleUpload}
                        />

                        <span className="file-button">
                            Choose CSV File
                        </span>

                    </label>


                    {/* Loading */}
                    {loading && (
                        <div className="loading-box">

                            <span className="spinner"></span>

                            <span>
                                Analyzing your statement...
                            </span>

                        </div>
                    )}


                    {/* Information */}
                    <div className="upload-info">

                        <span>✓ CSV supported</span>

                        <span>✓ Automatic analysis</span>

                        <span>✓ Secure processing</span>

                    </div>

                </div>

            </div>

        </section>
    );
}

export default UploadBox;