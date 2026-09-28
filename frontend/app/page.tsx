import { ArrowRight, Camera, Image as ImageIcon } from "lucide-react";
import Link from "next/link";

import ThemeToggle from "./components/ThemeToggle";

const detectedProducts = ["Book", "Cup", "Pen", "Toy Car"];

export default function Home() {
  return (
    <main className="home">
      <div className="background-shape background-shape-one" />
      <div className="background-shape background-shape-two" />
      <div className="background-shape background-shape-three" />

      <section className="hero">
        <div className="top-bar">
          <div className="brand">
            <div className="brand-mark">S</div>
            <span>SmartShelf</span>
          </div>

          <ThemeToggle />
        </div>

        <div className="hero-content">
          <p className="eyebrow">
            COMPUTER VISION · SMART INVENTORY
          </p>

          <h1>
            Your shelf,
            <br />
            <span>understood.</span>
          </h1>

          <p className="description">
            SmartShelf uses computer vision to recognize products on your
            shelf and keep track of your inventory automatically.
          </p>

          <div className="detected">
            <span className="detected-label">
              Currently detects
            </span>

            <div className="products">
              {detectedProducts.map((product) => (
                <span key={product} className="product">
                  {product}
                </span>
              ))}
            </div>
          </div>

          <div className="actions">
            <Link href="/sample" className="action-card">
              <div className="icon-wrapper">
                <ImageIcon size={22} strokeWidth={1.8} />
              </div>

              <div className="action-text">
                <span className="action-title">
                  Test with a Sample Image
                </span>

                <span className="action-description">
                  Upload an image and detect products
                </span>
              </div>

              <ArrowRight className="arrow" size={20} />
            </Link>

            <Link href="/camera" className="action-card">
              <div className="icon-wrapper">
                <Camera size={22} strokeWidth={1.8} />
              </div>

              <div className="action-text">
                <span className="action-title">
                  Test with Your Camera
                </span>

                <span className="action-description">
                  See detections in real time
                </span>
              </div>

              <ArrowRight className="arrow" size={20} />
            </Link>
          </div>
        </div>

        <p className="footer-note">
          Computer Vision <span>·</span> AI <span>·</span> Smart Inventory
        </p>
      </section>
    </main>
  );
}