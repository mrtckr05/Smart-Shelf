"use client";

import { ArrowLeft, ImagePlus, Loader2, Upload } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

type DetectionResult = {
  counts: Record<string, number>;
};

const API_URL = "http://127.0.0.1:8000";

const productNames: Record<string, string> = {
  book: "Book",
  cup: "Cup",
  pen: "Pen",
  toy_car: "Toy Car",
};

export default function SamplePage() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<DetectionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (selectedFile: File | undefined) => {
    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setResult(null);
    setError(null);
  };

  const handleDetect = async () => {
    if (!file) {
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `${API_URL}/api/v1/detection/image`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Detection request failed.");
      }

      const data: DetectionResult = await response.json();

      setResult(data);
    } catch (err) {
      console.error(err);
      setError(
        "Could not connect to SmartShelf. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="sample-page">
      <div className="background-shape background-shape-one" />
      <div className="background-shape background-shape-two" />
      <div className="background-shape background-shape-three" />

      <div className="sample-container">
        <Link href="/" className="back-link">
          <ArrowLeft size={17} />
          Back to SmartShelf
        </Link>

        <div className="sample-header">
          <p className="eyebrow">COMPUTER VISION</p>

          <h1>
            Test with an <span>image.</span>
          </h1>

          <p>
            Upload an image of your shelf and SmartShelf will detect the
            products it can recognize.
          </p>
        </div>

        <div className="upload-area">
          {preview ? (
            <div className="preview-wrapper">
              <img
                src={preview}
                alt="Selected shelf"
                className="image-preview"
              />

              <button
                className="change-image"
                onClick={() => {
                  setFile(null);
                  setPreview(null);
                  setResult(null);
                }}
              >
                Choose another image
              </button>
            </div>
          ) : (
            <label className="upload-placeholder">
              <div className="upload-icon">
                <Upload size={24} />
              </div>

              <span className="upload-title">
                Choose an image
              </span>

              <span className="upload-description">
                JPG, PNG or WEBP
              </span>

              <input
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={(event) =>
                  handleFileChange(event.target.files?.[0])
                }
                hidden
              />
            </label>
          )}
        </div>

        {file && (
          <button
            className="detect-button"
            onClick={handleDetect}
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="spin" size={19} />
                Detecting...
              </>
            ) : (
              <>
                <ImagePlus size={19} />
                Detect Products
              </>
            )}
          </button>
        )}

        {error && <p className="error-message">{error}</p>}

        {result && (
          <section className="result-section">
            <div className="result-heading">
              <p className="eyebrow">DETECTION RESULT</p>
              <h2>What SmartShelf found</h2>
            </div>

            <div className="result-grid">
              {Object.entries(result.counts).map(
                ([className, quantity]) => (
                  <div className="result-card" key={className}>
                    <span className="result-name">
                      {productNames[className] ?? className}
                    </span>

                    <strong>{quantity}</strong>
                  </div>
                )
              )}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}