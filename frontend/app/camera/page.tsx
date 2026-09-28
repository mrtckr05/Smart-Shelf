"use client";

import {
  ArrowLeft,
  Camera,
  Circle,
  Loader2,
  Wifi,
  WifiOff,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

type DetectionCounts = Record<string, number>;

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const productNames: Record<string, string> = {
  book: "Book",
  cup: "Cup",
  pen: "Pen",
  toy_car: "Toy Car",
};

export default function CameraPage() {
  const [counts, setCounts] = useState<DetectionCounts>({});
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const ws = new WebSocket(
      "ws://127.0.0.1:8000/api/v1/camera/ws"
    );

    ws.onopen = () => {
      setConnected(true);
      setError(null);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.counts) {
          setCounts(data.counts);
        }
      } catch (err) {
        console.error("Invalid WebSocket message:", err);
      }
    };

    ws.onerror = () => {
      setConnected(false);
      setError("Could not connect to the camera service.");
    };

    ws.onclose = () => {
      setConnected(false);
    };

    return () => {
      ws.close();
    };
  }, []);

  const totalObjects = Object.values(counts).reduce(
    (sum, quantity) => sum + quantity,
    0
  );

  return (
    <main className="camera-page">
      <div className="background-shape background-shape-one" />
      <div className="background-shape background-shape-two" />
      <div className="background-shape background-shape-three" />

      <div className="camera-container">
        <Link href="/" className="back-link">
          <ArrowLeft size={17} />
          Back to SmartShelf
        </Link>

        <header className="camera-header">
          <div>
            <p className="eyebrow">LIVE COMPUTER VISION</p>

            <h1>
              Your shelf,
              <br />
              <span>in real time.</span>
            </h1>

            <p>
              SmartShelf is watching the camera and detecting products
              automatically.
            </p>
          </div>

          <div
            className={`connection-status ${
              connected ? "connected" : "disconnected"
            }`}
          >
            {connected ? (
              <>
                <Wifi size={16} />
                Connected
              </>
            ) : (
              <>
                <WifiOff size={16} />
                Disconnected
              </>
            )}
          </div>
        </header>

        <section className="camera-layout">
          <div className="camera-view">
            <div className="camera-view-header">
              <div className="camera-title">
                <Camera size={18} />
                Camera Feed
              </div>

              {connected && (
                <div className="live-indicator">
                  <Circle size={8} fill="currentColor" />
                  LIVE
                </div>
              )}
            </div>

            <div className="video-wrapper">
              <img
                src={`${API_URL}/api/v1/camera/stream`}
                alt="SmartShelf camera feed"
                className="camera-stream"
              />

              {!connected && (
                <div className="camera-overlay">
                  <Loader2 size={28} className="spin" />

                  <span>
                    Waiting for camera connection...
                  </span>
                </div>
              )}
            </div>
          </div>

          <aside className="detection-panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">DETECTION</p>
                <h2>Products found</h2>
              </div>

              <span className="object-count">
                {totalObjects}
              </span>
            </div>

            {Object.keys(counts).length === 0 ? (
              <div className="empty-detection">
                <Camera size={22} />
                <span>No products detected yet.</span>
              </div>
            ) : (
              <div className="live-results">
                {Object.entries(counts).map(
                  ([className, quantity]) => (
                    <div
                      className="live-result"
                      key={className}
                    >
                      <span>
                        {productNames[className] ?? className}
                      </span>

                      <strong>{quantity}</strong>
                    </div>
                  )
                )}
              </div>
            )}

            {error && (
              <p className="camera-error">
                {error}
              </p>
            )}
          </aside>
        </section>
      </div>
    </main>
  );
}