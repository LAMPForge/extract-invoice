import React, { useState } from 'react';
import axios from 'axios';

function UploadInvoice() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [responseData, setResponseData] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    // Handle file selection
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
        setResponseData(null);
        setError(null);

        // Create a preview URL for the selected image
        if (file) {
            setPreviewUrl(URL.createObjectURL(file));
        } else {
            setPreviewUrl(null);
        }
    };

    // Handle form submission
    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!selectedFile) {
            setError("Please select a file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        setLoading(true);
        try {
            const response = await axios.post('https://e2b7-35-240-132-242.ngrok-free.app/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            setResponseData(response.data);
            setError(null);
        } catch (err) {
            setError("Failed to upload the file. Please try again.");
            console.error(err);
        }
        setLoading(false);
    };

    return (
        <div className="container mt-5">
            <div className="card shadow-sm">
                <div className="card-header">
                    <h2>Upload Invoice</h2>
                </div>
                <div className="card-body">
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label className="form-label">Select Invoice File</label>
                            <input type="file" className="form-control" onChange={handleFileChange} />
                        </div>
                        {previewUrl && (
                            <div>
                                <img src={previewUrl} alt="Preview" className="image-preview" />
                            </div>
                        )}
                        <button type="submit" className="btn btn-primary mt-3" disabled={loading}>
                            {loading ? "Uploading..." : "Upload"}
                        </button>
                    </form>

                    {error && <div className="alert alert-danger mt-3">{error}</div>}

                    {responseData && (
                        <div className="mt-4">
                            <h3>Extracted Invoice Data</h3>
                            <div className="card">
                                <div className="card-body">
                                    <h5 className="card-title">Invoice Details</h5>
                                    <p className="card-text"><strong>Invoice Date:</strong> {responseData.invoice_date || 'N/A'}</p>
                                    <p className="card-text"><strong>Invoice Symbol:</strong> {responseData.invoice_symbol || 'N/A'}</p>
                                    <p className="card-text"><strong>Invoice Number:</strong> {responseData.invoice_number || 'N/A'}</p>
                                    <p className="card-text"><strong>Total Amount:</strong> {responseData.total_amount || 'N/A'}</p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default UploadInvoice;
