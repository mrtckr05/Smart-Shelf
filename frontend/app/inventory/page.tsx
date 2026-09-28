"use client";

import {
  ArrowLeft,
  Box,
  Package,
  RefreshCw,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

type InventoryItem = {
  id?: number;
  shelf_id?: number;
  product_id?: number;
  name: string;
  class_name: string;
  quantity: number;
};

const API_URL = "http://127.0.0.1:8000";

const productNames: Record<string, string> = {
  book: "Book",
  cup: "Cup",
  pen: "Pen",
  toy_car: "Toy Car",
};

export default function InventoryPage() {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchInventory = async () => {
    try {
      setError(null);

      const response = await fetch(
        `${API_URL}/api/v1/inventory?shelf_id=1`,
        {
          cache: "no-store",
        }
      );

      if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
          `Backend error ${response.status}: ${errorText}`
        );
      }

      const data = await response.json();

      setInventory(data);
    } catch (err) {
      console.error(err);

      setError(
        err instanceof Error
          ? err.message
          : "Could not load inventory."
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  const handleRefresh = () => {
    setRefreshing(true);
    fetchInventory();
  };

  const totalItems = inventory.reduce(
    (sum, item) => sum + item.quantity,
    0
  );

  return (
    <main className="inventory-page">
      <div className="background-shape background-shape-one" />
      <div className="background-shape background-shape-two" />
      <div className="background-shape background-shape-three" />

      <div className="inventory-container">
        <Link href="/" className="back-link">
          <ArrowLeft size={17} />
          Back to SmartShelf
        </Link>

        <header className="inventory-header">
          <div>
            <p className="eyebrow">SMART INVENTORY</p>

            <h1>
              Your shelf,
              <br />
              <span>at a glance.</span>
            </h1>

            <p>
              View the latest confirmed inventory state detected by
              SmartShelf.
            </p>
          </div>

          <button
            className="refresh-button"
            onClick={handleRefresh}
            disabled={refreshing}
          >
            <RefreshCw
              size={17}
              className={refreshing ? "spin" : ""}
            />
            Refresh
          </button>
        </header>

        <section className="inventory-summary">
          <div className="summary-card">
            <div className="summary-icon">
              <Package size={20} />
            </div>

            <div>
              <span>Total Products</span>
              <strong>{totalItems}</strong>
            </div>
          </div>

          <div className="summary-card">
            <div className="summary-icon">
              <Box size={20} />
            </div>

            <div>
              <span>Product Types</span>
              <strong>{inventory.length}</strong>
            </div>
          </div>
        </section>

        <section className="inventory-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">SHELF 01</p>
              <h2>Current Inventory</h2>
            </div>
          </div>

          {loading ? (
            <div className="inventory-state">
              <RefreshCw size={22} className="spin" />
              <span>Loading inventory...</span>
            </div>
          ) : error ? (
            <div className="inventory-error">
              <strong>Could not load inventory</strong>
              <span>{error}</span>
            </div>
          ) : inventory.length === 0 ? (
            <div className="inventory-state">
              <Box size={24} />
              <span>No inventory records found.</span>
            </div>
          ) : (
            <div className="inventory-grid">
              {inventory.map((item) => (
                <article
                  className="inventory-card"
                  key={item.id ?? item.product_id}
                >
                  <div className="inventory-card-top">
                    <div className="product-icon">
                      <Box size={20} />
                    </div>

                    <span className="product-class">
                      {item.class_name}
                    </span>
                  </div>

                  <div className="inventory-card-bottom">
                    <div>
                      <h3>
                        {item.name ||
                          productNames[item.class_name] ||
                          item.class_name}
                      </h3>

                      <span>Current quantity</span>
                    </div>

                    <strong>{item.quantity}</strong>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}